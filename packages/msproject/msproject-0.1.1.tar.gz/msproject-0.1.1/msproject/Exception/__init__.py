

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Exception:
    # Object "Exception" class for software "Project"
    
    properties = ['application', 'daysOfWeek', 'finish', 'index', 'month', 'monthDay', 'monthItem', 'monthPosition', 'name', 'occurrences', 'parent', 'period', 'shift1', 'shift2', 'shift3', 'shift4', 'shift5', 'start', 'type']
    
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
    def daysOfWeek(self) -> "Any":
        return (self.native_obj.DaysOfWeek)
        
    @daysOfWeek.setter     
    def _set_daysOfWeek(self, value):
        self.native_obj.DaysOfWeek = value
            
    # -> Any            
    @property         
    def finish(self) -> "Any":
        return (self.native_obj.Finish)
        
    @finish.setter     
    def _set_finish(self, value):
        self.native_obj.Finish = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def month(self) -> "Any":
        return (self.native_obj.Month)
        
    @month.setter     
    def _set_month(self, value):
        self.native_obj.Month = value
            
    # -> Any            
    @property         
    def monthDay(self) -> "Any":
        return (self.native_obj.MonthDay)
        
    @monthDay.setter     
    def _set_monthDay(self, value):
        self.native_obj.MonthDay = value
            
    # -> Any            
    @property         
    def monthItem(self) -> "Any":
        return (self.native_obj.MonthItem)
        
    @monthItem.setter     
    def _set_monthItem(self, value):
        self.native_obj.MonthItem = value
            
    # -> Any            
    @property         
    def monthPosition(self) -> "Any":
        return (self.native_obj.MonthPosition)
        
    @monthPosition.setter     
    def _set_monthPosition(self, value):
        self.native_obj.MonthPosition = value
            
    # -> Any            
    @property         
    def name(self) -> "Any":
        return (self.native_obj.Name)
        
    @name.setter     
    def _set_name(self, value):
        self.native_obj.Name = value
            
    # -> Any            
    @property         
    def occurrences(self) -> "Any":
        return (self.native_obj.Occurrences)
        
    @occurrences.setter     
    def _set_occurrences(self, value):
        self.native_obj.Occurrences = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def period(self) -> "Any":
        return (self.native_obj.Period)
        
    @period.setter     
    def _set_period(self, value):
        self.native_obj.Period = value
            
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
    def start(self) -> "Any":
        return (self.native_obj.Start)
        
    @start.setter     
    def _set_start(self, value):
        self.native_obj.Start = value
            
    # -> Any            
    @property         
    def type(self) -> "Any":
        return (self.native_obj.Type)
        
    @type.setter     
    def _set_type(self, value):
        self.native_obj.Type = value
            
# end "Exception"       
        