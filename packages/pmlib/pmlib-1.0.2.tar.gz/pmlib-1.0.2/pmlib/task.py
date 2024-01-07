from collections.abc import Sequence
from typing import List

from email_validator import validate_email, EmailNotValidError
from loguru import logger
import attrs
import texttable

from tasklib.lazy import LazyUUIDTaskSet
from tasklib.task import TaskQuerySet
from tasklib import Task, TaskWarrior


@attrs.define(repr=False)
class OwnedTask(Task):
    """
    A tasklib.task.Task() subclass which is owned by an email address and has a UUID.

    :param tw: A ``tasklib.TaskWarrior()`` instance
    :type tw: TaskWarrior
    :param description: The description of the task
    :type description: str
    :param due: The date due in form of 'YYYY-MM-DD'
    :type due: str
    :param priority: Character representing the priority: H, M, or L
    :type priority: str
    :param owner: The email address of the person who owns the task; this is stored as a Task() tag.
    :type owner: str
    :return: An OwnedTask(), which is an instance of ``tasklib.task.Task()`` with a string ``owner``
    :rtype: OwnedTask
    """
    tw: TaskWarrior = None
    due: str = None
    priority: str = None
    owner: str = None
    project: str = None
    description: str = None

    @logger.catch(reraise=True)
    def __init__(self,
                 tw: TaskWarrior = None,
                 due: str = None,
                 priority: str = 'M',
                 owner: str = None,
                 project: str = None,
                 description: str = None):

        super(OwnedTask, self).__init__(
            tw,
            description=description,
            project=project,
            due=due,
            priority=priority)

        # Ensure that the task has a project defined...
        if not isinstance(project, str):
            error = f"Cannot create task -->{description}<-- due {due} without a valid project string"
            logger.critical(error)
            raise NotImplementedError(error)

        # The original tasklib.Task() instances do not have a self.tw attribute
        self.tw = tw
        self['due'] = due
        self['priority'] = priority

        self['description'] = description
        self.owner = self.set_owner(owner)

    def __repr__(self):
        return f"""<OwnedTask '{self['description']}' due: {self['due']} owner: {self.owner}>"""

    def __str__(self):
        return self.__repr__()

    @logger.catch(reraise=True)
    def __hash__(self):
        total = 0
        for value in self.__dict__.values():
            if isinstance(value, dict):
                for other in value.values():
                    if isinstance(other, set):
                        for item in other:
                            total += hash(item)
                    else:
                        total += hash(other)
            else:
                total += hash(value)
        return total

    @logger.catch(reraise=True)
    def get_depends(self):
        return self['depends']

    @logger.catch(reraise=True)
    def set_depends(self, value: List[Task]) -> LazyUUIDTaskSet:
        """
        Set the dependencies for this task
        """
        if isinstance(value, Sequence):
            for task in value:
                if not isinstance(task, Task):
                    error = f"{task} {type(task)} must be an instance of tasklib.Task()"
                    logger.critical(error)
                    raise ValueError(error)
            self['depends'] = LazyUUIDTaskSet(self.tw, [ii['uuid'] for ii in value])
            return self['depends']
        else:
            error = f"OwnedTaskWarrior().set_depends() requires a list of task instances, but got {type(value)}"
            logger.critical(error)
            raise NotImplementedError(error)

    @logger.catch(reraise=True)
    def get_owner(self) -> str:
        """
        :return: The value of the owner email from tags
        :rtype: str
        """
        for tag in self['tags']:
            if tag[0:7] == "owner=":
                return tag.split("=", 1)[1]

        # We could not find the owner tag...
        error = "OwnedTask['uuid'] {self['uuid']} does not have an owner tag"
        logger.critical(error)
        raise NotImplementedError(error)

    @logger.catch(reraise=True)
    def set_owner(self, email_value: str) -> str:
        """
        Validate the owner's email address in ``email_value``, set an owner tag

        :return: The string owner email address
        :rtype: str
        """
        if isinstance(email_value, str):
            try:
                validate_email(email_value)
            except EmailNotValidError:
                error = f"{email_value} is not a valid email address"
                logger.critical(error)
                raise EmailNotValidError(error)
            except BaseException:
                error = f"{email_value} has some unexpected problem"
                logger.critical(error)
                raise NotImplementedError(error)
        else:
            error = "Email addresses must be a string"
            logger.critical(error)
            raise NotImplementedError(error)

        correct_owner_tag = f"owner={email_value}"
        for tag in self['tags']:
            if tag[0:7] == 'owner=':
                if tag == correct_owner_tag:
                    return correct_owner_tag
                else:
                    self['tags'].remove(tag)

        self['tags'].add(correct_owner_tag)
        return correct_owner_tag.split("=", 1)[1]


@attrs.define(repr=False)
class OwnedTaskWarrior(TaskWarrior):
    """
    A TaskWarrior() subclass that implements owned tasks.
    """

    @logger.catch(reraise=True)
    def __init__(self, data_location=None, create=True,
                 taskrc_location=None, task_command='task',
                 version_override=None):
        TaskWarrior.__init__(self,
                             data_location=data_location,
                             create=create,
                             taskrc_location=taskrc_location,
                             task_command=task_command,
                             version_override=version_override)

        if not isinstance(self.tasks, TaskQuerySet):
            error = f"{self.tasks} {type(self.tasks)} must be a tasklib TaskQuerySet() instance"
            logger.critical(error)
            raise NotImplementedError(error)

    @logger.catch(reraise=True)
    def __hash__(self) -> int:
        """
        :return: An hash value that uniquely represents this ``OwnedTaskWarrior()`` collection
        :rtype: int
        """
        total = 0
        if self.tasks:
            for task in self.tasks:
                total += hash(task)
        return total

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.tasks is not None:
            return f"""<OwnedTaskWarrior with {len(self.tasks)} OwnedTask() instances>"""
        else:
            return """<OwnedTaskWarrior with 0 OwnedTask() instances>"""

    def reload_tasks(self) -> None:
        """Reload tasks from disk"""
        self.tasks = TaskQuerySet(self)

    def delete_project(self, task: Task, project: str) -> None:
        """
        Delete all ``task`` instances associated with ``project`` (case-insensitive) from TaskWarrior().

        This method is an addition to the original ``tasklib`` API.
        """
        if self.tasks:
            for task in self.tasks:
                if task['project'].lower() == project.lower():
                    self.execute_command([task['uuid'], 'delete'])

    def purge_project(self, project: str) -> None:
        """
        Permanently remove all ``task`` instances associated with ``project`` (case-insensitive) from TaskWarrior().  This causes data loss.

        This method is an addition to the original ``tasklib`` API.
        """
        if self.tasks:
            for task in self.tasks:
                if task['project'] == project:
                    self.execute_command([task['uuid'], 'delete'])
                    self.execute_command([task['uuid'], 'purge'])

    def purge_task(self, task):
        """
        Permanently remove the task from TaskWarrior().  This causes data loss.

        The task will not be completely purged until OwnedTaskWarrior() is re-loaded from disk.

        This method is an addition to the original ``tasklib`` API; it was submitted
        as ``tasklib`` github PR number 130.
        """
        self.execute_command([task['uuid'], 'delete'])
        self.execute_command([task['uuid'], 'purge'])

    @logger.catch(reraise=True)
    def get_task(self, uuid_value: str) -> OwnedTask:
        """
        :return: Walk the task database and return an OwnedTask() instance representing the UUID in ``uuid_value``, default to None
        :rtype: OwnedTask
        """

        for task in self.tasks:
            if task['uuid'] == uuid_value:

                # Ensure that the task has a project defined...
                if not isinstance(task['project'], str):
                    error = f"Cannot manage task {task['uuid']} without a valid project string"
                    logger.critical(error)
                    raise NotImplementedError(error)

                # Find the owner in the Task() tags and copy into
                # the new OwnedTask() instance
                for tag in task['tags']:
                    if tag[0:6] == "owner=":
                        owner = tag.split("=", 1)[1]
                        break

                owned_task = OwnedTask(tw=None,
                                       description=task['description'],
                                       project=task['project'],
                                       due=task['due'],
                                       owner=owner)
                # Take all the attributes of the Task instance and copy
                # into the new OwnedTask() instance.
                owned_task.__dict__ = task.__dict__
                return owned_task
        return None

    @logger.catch(reraise=True)
    def get_table(self, max_width=80) -> str:
        """
        :param max_width: The maximum table width without wrapping cells
        :type max_width: int
        :return: A string task table rendering
        :rtype: str
        """
        # Reload tasks from disk
        self.reload_tasks()

        all_tasks = list()
        table = texttable.Texttable(max_width=max_width)
        table.set_deco(texttable.Texttable.HEADER)
        table.set_cols_dtype(["t", "t", "i", "t", "t", "t"])
        table.set_cols_align(["l", "l", "l", "l", "l", "l"])

        # Append a list of titles
        all_tasks.append(["uuid", "due", "depends", "owner", "project", "description"])
        if self.tasks:
            for task in self.tasks:
                owner = None
                for tag in task['tags']:
                    if tag[0:6] == "owner=":
                        owner = tag.split("=", 1)[1]
                all_tasks.append([task['uuid'], task['due'], len(task['depends']), owner, task['project'], task['description']])
        table.add_rows(all_tasks)
        return table.draw()
