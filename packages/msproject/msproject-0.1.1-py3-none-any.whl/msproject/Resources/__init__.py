

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Resources:
    # Object "Resources" class for software "Project"
    # Kind of list: Resource
    
    def __init__(self, native_obj):
        self.native_obj = native_obj
        
    def __getitem__(self, index) -> "Resource":
        if index >= self.native_obj.Count:
            raise IndexError("Index out of range")
        return Resource(self.native_obj.Item(index + 1))
        
    def first(self) -> "Resource":
        return Resource(self.native_obj.Item(1))
        
    def __len__(self):
        return self.native_obj.Count
        
# end "Resources"       
        