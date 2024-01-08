

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class WorkWeekDay:
    # Object "WorkWeekDay" class for software "Project"
    
    properties = ['application', 'calendar', 'count', 'index', 'name', 'parent', 'shift1', 'shift2', 'shift3', 'shift4', 'shift5', 'working']
    
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
    def calendar(self) -> "Any":
        return (self.native_obj.Calendar)
        
    @calendar.setter     
    def _set_calendar(self, value):
        self.native_obj.Calendar = value
            
    # -> Any            
    @property         
    def count(self) -> "Any":
        return (self.native_obj.Count)
        
    @count.setter     
    def _set_count(self, value):
        self.native_obj.Count = value
            
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
    def shift1(self) -> "Any":
        return (self.native_obj.Shift1)
        
    @shift1.setter     
    def _set_shift1(self, value):
        self.native_obj.Shift1 = value
            
    # -> Any            
    @property         
    def shift2(self) -> "Any":
        return (self.native_obj.Shift2)
        
    @shift2.setter     
    def _set_shift2(self, value):
        self.native_obj.Shift2 = value
            
    # -> Any            
    @property         
    def shift3(self) -> "Any":
        return (self.native_obj.Shift3)
        
    @shift3.setter     
    def _set_shift3(self, value):
        self.native_obj.Shift3 = value
            
    # -> Any            
    @property         
    def shift4(self) -> "Any":
        return (self.native_obj.Shift4)
        
    @shift4.setter     
    def _set_shift4(self, value):
        self.native_obj.Shift4 = value
            
    # -> Any            
    @property         
    def shift5(self) -> "Any":
        return (self.native_obj.Shift5)
        
    @shift5.setter     
    def _set_shift5(self, value):
        self.native_obj.Shift5 = value
            
    # -> Any            
    @property         
    def working(self) -> "Any":
        return (self.native_obj.Working)
        
    @working.setter     
    def _set_working(self, value):
        self.native_obj.Working = value
            
# end "WorkWeekDay"       
        