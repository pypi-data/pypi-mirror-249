# Summary

[`pmlib`][1] is a library to leverage [`TaskWarrior`][2] to track and manage projects.

[`pmlib`][1] requires adds per-task project owners, which are a basic requirement of any project tracking system.  The original [`TaskWarrior`][2] concept assumes all tasks are owned by the user running TaskWarrior.

# Installation

`pip install pmlib`

# Usage

Assume you want to create three tasks, two of which depend on the first:

```python
from pmlib.task import OwnedTask
from pmlib.task import OwnedTaskWarrior

otw = OwnedTaskWarrior(data_location="~/.pm", create=True)
newtask01 = OwnedTask(otw,
                      description="Task 01",
                      due="2023-12-26",
                      project="ciscoconfparse",
                      owner="mike@gmail.com")
newtask02 = OwnedTask(otw,
                      description="Do this for Task 01",
                      due="2023-12-26",
                      project="ciscoconfparse",
                      owner="jeff@gmail.com")
newtask03 = OwnedTask(otw,
                      description="Do that for Task 01",
                      due="2023-12-26",
                      project="ciscoconfparse",
                      owner="joe@gmail.com")
newtask02.save()
newtask03.save()
newtask01.set_depends([newtask02, newtask03])
newtask01.save()
# This should be True, newtask02 is in the list of dependencies
print(newtask02 in newtask01['depends'])
# Print a task table wrapped to 100 characters wide...
print(otw.get_table(100))
```

That will print (task UUIDs will be different):

```none
True
      uuid                 due          depends       owner           project         description
====================================================================================================
b5aa69dd-476c-      2023-12-26          0         jeff@gmail.com   ciscoconfparse   Do this for Task
4902-a77f-          00:00:00-06:00                                                  01
1c8eb1fcb409
b65d2904-551b-      2023-12-26          0         joe@gmail.com    ciscoconfparse   Do that for Task
470f-85c5-          00:00:00-06:00                                                  01
85946de4a512
2756ae85-bf6b-      2023-12-26          2         mike@gmail.com   ciscoconfparse   Task 01
47ce-81b6-          00:00:00-06:00
197ecb5a4601
```

 [1]: https://github.com/mpenning/pmlib
 [2]: https://github.com/GothenburgBitFactory/taskwarrior

