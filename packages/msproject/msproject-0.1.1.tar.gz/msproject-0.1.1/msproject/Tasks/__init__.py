

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Tasks:
    # Object "Tasks" class for software "Project"
    # Kind of list: Task
    
    def __init__(self, native_obj):
        self.native_obj = native_obj
        
    def __getitem__(self, index) -> "Task":
        if index >= self.native_obj.Count:
            raise IndexError("Index out of range")
        return Task(self.native_obj.Item(index + 1))
        
    def first(self) -> "Task":
        return Task(self.native_obj.Item(1))
        
    def __len__(self):
        return self.native_obj.Count
        
# end "Tasks"       
        