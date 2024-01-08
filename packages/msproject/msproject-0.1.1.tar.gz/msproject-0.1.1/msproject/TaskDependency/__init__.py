

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class TaskDependency:
    # Object "TaskDependency" class for software "Project"
    
    properties = ['application', 'from_', 'index', 'lag', 'lagType', 'parent', 'path', 'to', 'type']
    
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
    def from_(self) -> "Any":
        return (self.native_obj.From)
        
    @from_.setter     
    def _set_from_(self, value):
        self.native_obj.From = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def lag(self) -> "Any":
        return (self.native_obj.Lag)
        
    @lag.setter     
    def _set_lag(self, value):
        self.native_obj.Lag = value
            
    # -> Any            
    @property         
    def lagType(self) -> "Any":
        return (self.native_obj.LagType)
        
    @lagType.setter     
    def _set_lagType(self, value):
        self.native_obj.LagType = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def path(self) -> "Any":
        return (self.native_obj.Path)
        
    @path.setter     
    def _set_path(self, value):
        self.native_obj.Path = value
            
    # -> Any            
    @property         
    def to(self) -> "Any":
        return (self.native_obj.To)
        
    @to.setter     
    def _set_to(self, value):
        self.native_obj.To = value
            
    # -> Any            
    @property         
    def type(self) -> "Any":
        return (self.native_obj.Type)
        
    @type.setter     
    def _set_type(self, value):
        self.native_obj.Type = value
            
# end "TaskDependency"       
        