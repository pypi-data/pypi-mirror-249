import tempfile
import sys

sys.path.insert(0, "..")

from loguru import logger
import pytest
from pmlib.task import OwnedTaskWarrior, OwnedTask
import tasklib
import email_validator


def test_ownedtaskwarrior_01():
    """Test that the OwnedTaskWarrior is correctly created and that the default number of tasks is zero"""
    with tempfile.TemporaryDirectory() as tmp:
        tw = OwnedTaskWarrior(data_location=tmp, create=True)
        assert len(tw.tasks) == 0


def test_ownedtaskwarrior_02():
    """Test that the OwnedTaskWarrior is correctly created and that the default number of tasks is one"""
    with tempfile.TemporaryDirectory() as tmp:
        tw = OwnedTaskWarrior(data_location=tmp, create=True)
        twtask01 = OwnedTask(tw,
                             description="My new python task 01",
                             due="2023-12-26",
                             project="project01",
                             owner="foo01@bar.com")
        twtask01.save()

        assert len(tw.tasks) == 1

def test_ownedtaskwarrior_03():
    """Test that the OwnedTaskWarrior is correctly created and that you can get a task by uuid"""
    with tempfile.TemporaryDirectory() as tmp:
        tw = OwnedTaskWarrior(data_location=tmp, create=True)
        twtask01 = OwnedTask(tw,
                             description="My new python task 01",
                             due="2023-12-26",
                             project="project01",
                             owner="foo01@bar.com")
        twtask01.save()
        assert len(tw.tasks) == 1

        _uuid = None
        for task in tw.tasks:
            _uuid = task['uuid']

        uut = tw.get_task(_uuid)
        assert isinstance(uut, OwnedTask)


def test_ownedtaskwarrior_04():
    """Test that the OwnedTaskWarrior is correctly created and that you can load saved tasks from disk"""
    with tempfile.TemporaryDirectory() as tmp:
        tw = OwnedTaskWarrior(data_location=tmp, create=True)
        twtask01 = OwnedTask(tw,
                             description="My new python task 01",
                             due="2023-12-26",
                             project="project01",
                             owner="foo01@bar.com")
        twtask01.save()
        assert len(tw.tasks) == 1

        tw.reload_tasks()
        # Ensure the task is loaded from disk...
        assert len(tw.tasks) == 1


def test_ownedtaskwarrior_05():
    """Test that the OwnedTaskWarrior is correctly created and that you can purge a task by instance"""
    with tempfile.TemporaryDirectory() as tmp:
        tw = OwnedTaskWarrior(data_location=tmp, create=True)
        twtask01 = OwnedTask(tw,
                             description="My new python task 01",
                             due="2023-12-26",
                             project="project01",
                             owner="foo01@bar.com")
        twtask01.save()
        assert len(tw.tasks) == 1

        # Purge the task instance
        tw.purge_task(twtask01)
        

        # Re-load the task DB... to ensure we get the
        # most up-to-date-info
        tw = OwnedTaskWarrior(data_location=tmp, create=True)
        # Ensure the task is purged...
        assert len(tw.tasks) == 0


def test_ownedtaskwarrior_06():
    """Test that the OwnedTaskWarrior is correctly created and that you can purge a project by name"""
    with tempfile.TemporaryDirectory() as tmp:
        tw = OwnedTaskWarrior(data_location=tmp, create=True)
        twtask01 = OwnedTask(tw,
                             description="My new python task 01",
                             due="2023-12-26",
                             project="project01",
                             owner="foo01@bar.com")
        twtask01.save()
        assert len(tw.tasks) == 1

        # Purge the task instance
        tw.purge_project("project01")
        

        # Re-load the task DB... to ensure we get the
        # most up-to-date-info
        tw.reload_tasks()
        # Ensure the task is purged...
        assert len(tw.tasks) == 0


def test_ownedtaskwarrior_07():
    """Test that the OwnedTaskWarrior is correctly created and that you can get a string table of tasks"""
    with tempfile.TemporaryDirectory() as tmp:
        tw = OwnedTaskWarrior(data_location=tmp, create=True)
        twtask01 = OwnedTask(tw,
                             description="My new python task 01",
                             due="2023-12-26",
                             project="project01",
                             owner="foo01@bar.com")
        twtask01.save()
        assert len(tw.tasks) == 1

        task_table = tw.get_table(200)
        assert isinstance(task_table, str)
        # There should be a title line, seperator line, and task line...
        assert len(task_table.splitlines()) == 3

def test_ownedtask_01():
    """Test that the OwnedTask() fails with an empty owner"""
    with pytest.raises(NotImplementedError):
        with tempfile.TemporaryDirectory() as tmp:
            tw = OwnedTaskWarrior(data_location=tmp, create=True)
            twtask01 = OwnedTask(tw,
                                 description="My new python task 01",
                                 due="2023-12-26",
                                 project="project01",
                                 owner=None)
            twtask01.save()


def test_ownedtask_02():
    """Test that the OwnedTask() fails with an owner that isn't an email address"""
    with pytest.raises(email_validator.exceptions_types.EmailNotValidError):
        with tempfile.TemporaryDirectory() as tmp:
            tw = OwnedTaskWarrior(data_location=tmp, create=True)
            twtask01 = OwnedTask(tw,
                                 description="My new python task 01",
                                 due="2023-12-26",
                                 project="project01",
                                 owner="123 Sesame Street")
            twtask01.save()


def test_ownedtask_03():
    """Test that the OwnedTask().get_owner() returns the right owner"""
    with pytest.raises(NotImplementedError):
        with tempfile.TemporaryDirectory() as tmp:
            tw = OwnedTaskWarrior(data_location=tmp, create=True)
            twtask01 = OwnedTask(tw,
                                 description="My new python task 01",
                                 due="2023-12-26",
                                 project="project01",
                                 owner="foo01@bar.com")
            twtask01.save()
            assert twtask01.get_owner() == "foo01@bar.com"


def test_ownedtask_04():
    """Test that the OwnedTask() fails with an empty project"""
    with pytest.raises(NotImplementedError):
        with tempfile.TemporaryDirectory() as tmp:
            tw = OwnedTaskWarrior(data_location=tmp, create=True)
            twtask01 = OwnedTask(tw,
                                 description="My new python task 01",
                                 due="2023-12-26",
                                 project=None,
                                 owner="foo01@bar.com")
            twtask01.save()


def test_ownedtask_05():
    """Test that the OwnedTask() fails with an empty description"""
    with pytest.raises(tasklib.backends.TaskWarriorException):
        with tempfile.TemporaryDirectory() as tmp:
            tw = OwnedTaskWarrior(data_location=tmp, create=True)
            twtask01 = OwnedTask(tw,
                                 description=None,
                                 due="2023-12-26",
                                 project="project01",
                                 owner="foo01@bar.com")
            twtask01.save()


def test_ownedtask_06():
    """Test that the OwnedTask() is allowed with an empty due"""
    with tempfile.TemporaryDirectory() as tmp:
        tw = OwnedTaskWarrior(data_location=tmp, create=True)
        twtask01 = OwnedTask(tw,
                             description="Description 01",
                             due=None,
                             project="project01",
                             owner="foo01@bar.com")
        twtask01.save()
        assert len(tw.tasks) == 1


def test_ownedtask_07():
    """Test that the OwnedTask().set_depends() can set task dependencies"""
    with tempfile.TemporaryDirectory() as tmp:
        tw = OwnedTaskWarrior(data_location=tmp, create=True)
        twtask01 = OwnedTask(tw,
                             description="Description 01",
                             due=None,
                             project="project01",
                             owner="foo01@bar.com")
        twtask02 = OwnedTask(tw,
                             description="Description 02",
                             due=None,
                             project="project01",
                             owner="foo01@bar.com")
        twtask03 = OwnedTask(tw,
                             description="Description 03",
                             due=None,
                             project="project01",
                             owner="foo01@bar.com")
        twtask02.save()
        twtask03.save()
        twtask01.set_depends([twtask02, twtask03])
        twtask01.save()
        assert len(tw.tasks) == 3
        assert len(twtask01['depends']) == 2


def test_ownedtask_08():
    """Test that the OwnedTask().set_depends() rejects a direct task dependency (must be a list of dependencies)"""
    with pytest.raises(NotImplementedError):
        with tempfile.TemporaryDirectory() as tmp:
            tw = OwnedTaskWarrior(data_location=tmp, create=True)
            twtask01 = OwnedTask(tw,
                                 description="Description 01",
                                 due=None,
                                 project="project01",
                                 owner="foo01@bar.com")
            twtask02 = OwnedTask(tw,
                                 description="Description 02",
                                 due=None,
                                 project="project01",
                                 owner="foo01@bar.com")
            twtask02.save()
            twtask01.set_depends(twtask02)
            twtask01.save()


def test_ownedtask_09():
    """Test that the OwnedTask().set_depends() rejects a list of non-task dependencies (must be a list of OwnedTask() instances)"""
    with pytest.raises(ValueError):
        with tempfile.TemporaryDirectory() as tmp:
            tw = OwnedTaskWarrior(data_location=tmp, create=True)
            twtask01 = OwnedTask(tw,
                                 description="Description 01",
                                 due=None,
                                 project="project01",
                                 owner="foo01@bar.com")
            twtask02 = OwnedTask(tw,
                                 description="Description 02",
                                 due=None,
                                 project="project01",
                                 owner="foo01@bar.com")
            twtask02.save()
            twtask01.set_depends([1, 2])
            twtask01.save()


def test_ownedtask_10():
    """Test that the OwnedTask().__hash__() returns the correct number"""
    with tempfile.TemporaryDirectory() as tmp:
        tw = OwnedTaskWarrior(data_location=tmp, create=True)
        twtask01 = OwnedTask(tw,
                             description="Description 01",
                             due=None,
                             project="project01",
                             owner="foo01@bar.com")
        twtask01.save()
        assert isinstance(twtask01.__hash__(), int)

