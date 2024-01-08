

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class TimeScaleValue:
    # Object "TimeScaleValue" class for software "Project"
    
    properties = ['application', 'endDate', 'index', 'parent', 'startDate', 'value']
    
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
    def endDate(self) -> "Any":
        return (self.native_obj.EndDate)
        
    @endDate.setter     
    def _set_endDate(self, value):
        self.native_obj.EndDate = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def startDate(self) -> "Any":
        return (self.native_obj.StartDate)
        
    @startDate.setter     
    def _set_startDate(self, value):
        self.native_obj.StartDate = value
            
    # -> Any            
    @property         
    def value(self) -> "Any":
        return (self.native_obj.Value)
        
    @value.setter     
    def _set_value(self, value):
        self.native_obj.Value = value
            
# end "TimeScaleValue"       
        