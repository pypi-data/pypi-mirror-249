

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Selection:
    # Object "Selection" class for software "Project"
    
    properties = ['application', 'fieldIDList', 'fieldNameList', 'parent', 'resources', 'tasks']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def application(self) -> "Any":
        return (self.native_obj.Application)
        
    @application.setter     
    def _set_application(self, value):
        self.native_obj.Application = value
            
    # -> Any            
    @property         
    def fieldIDList(self) -> "Any":
        return (self.native_obj.FieldIDList)
        
    @fieldIDList.setter     
    def _set_fieldIDList(self, value):
        self.native_obj.FieldIDList = value
            
    # -> Any            
    @property         
    def fieldNameList(self) -> "Any":
        return (self.native_obj.FieldNameList)
        
    @fieldNameList.setter     
    def _set_fieldNameList(self, value):
        self.native_obj.FieldNameList = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def resources(self) -> "Any":
        return (self.native_obj.Resources)
        
    @resources.setter     
    def _set_resources(self, value):
        self.native_obj.Resources = value
            
    # -> Any            
    @property         
    def tasks(self) -> "Any":
        return (self.native_obj.Tasks)
        
    @tasks.setter     
    def _set_tasks(self, value):
        self.native_obj.Tasks = value
            
# end "Selection"       
        