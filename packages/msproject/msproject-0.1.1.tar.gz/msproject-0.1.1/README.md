# Project 

A Basic Win32 Python Controller for Microsoft Project. It requires an installed Microsoft Project license. Not affiliated with Microsoft.

Example:

```
from msproject import Project, Task

project = Project(r"C:\Users\mrebu\Desktop\trackprj.mpp")

print(project.name)
task: Task
for t in project.tasks:
    print(t.name)
```