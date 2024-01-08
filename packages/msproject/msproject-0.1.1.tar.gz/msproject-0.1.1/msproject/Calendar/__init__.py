

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Calendar:
    # Object "Calendar" class for software "Project"
    
    properties = ['application', 'baseCalendar', 'enterprise', 'exceptions', 'guid', 'index', 'name', 'parent', 'resourceGuid', 'weekDays', 'workWeeks', 'years']
    
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
    def baseCalendar(self) -> "Any":
        return (self.native_obj.BaseCalendar)
        
    @baseCalendar.setter     
    def _set_baseCalendar(self, value):
        self.native_obj.BaseCalendar = value
            
    # -> Any            
    @property         
    def enterprise(self) -> "Any":
        return (self.native_obj.Enterprise)
        
    @enterprise.setter     
    def _set_enterprise(self, value):
        self.native_obj.Enterprise = value
            
    # -> Any            
    @property         
    def exceptions(self) -> "Any":
        return (self.native_obj.Exceptions)
        
    @exceptions.setter     
    def _set_exceptions(self, value):
        self.native_obj.Exceptions = value
            
    # -> Any            
    @property         
    def guid(self) -> "Any":
        return (self.native_obj.Guid)
        
    @guid.setter     
    def _set_guid(self, value):
        self.native_obj.Guid = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def name(self) -> "Any":
        return (self.native_obj.Name)
        
    @name.setter     
    def _set_name(self, value):
        self.native_obj.Name = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def resourceGuid(self) -> "Any":
        return (self.native_obj.ResourceGuid)
        
    @resourceGuid.setter     
    def _set_resourceGuid(self, value):
        self.native_obj.ResourceGuid = value
            
    # -> Any            
    @property         
    def weekDays(self) -> "Any":
        return (self.native_obj.WeekDays)
        
    @weekDays.setter     
    def _set_weekDays(self, value):
        self.native_obj.WeekDays = value
            
    # -> Any            
    @property         
    def workWeeks(self) -> "Any":
        return (self.native_obj.WorkWeeks)
        
    @workWeeks.setter     
    def _set_workWeeks(self, value):
        self.native_obj.WorkWeeks = value
            
    # -> Any            
    @property         
    def years(self) -> "Any":
        return (self.native_obj.Years)
        
    @years.setter     
    def _set_years(self, value):
        self.native_obj.Years = value
            
# end "Calendar"       
        