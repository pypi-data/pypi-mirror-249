

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class StartDriver:
    # Object "StartDriver" class for software "Project"
    
    properties = ['actualStartDrivers', 'application', 'calendarDrivers', 'childTaskDrivers', 'effectiveDateAdd', 'effectiveDateDifference', 'effectiveDateSubtract', 'overAllocatedAssignments', 'parent', 'predecessorDrivers', 'suggestions', 'warnings']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def actualStartDrivers(self) -> "Any":
        return (self.native_obj.ActualStartDrivers)
        
    @actualStartDrivers.setter     
    def _set_actualStartDrivers(self, value):
        self.native_obj.ActualStartDrivers = value
            
    # -> Any            
    @property         
    def application(self) -> "Any":
        return (self.native_obj.Application)
        
    @application.setter     
    def _set_application(self, value):
        self.native_obj.Application = value
            
    # -> Any            
    @property         
    def calendarDrivers(self) -> "Any":
        return (self.native_obj.CalendarDrivers)
        
    @calendarDrivers.setter     
    def _set_calendarDrivers(self, value):
        self.native_obj.CalendarDrivers = value
            
    # -> Any            
    @property         
    def childTaskDrivers(self) -> "Any":
        return (self.native_obj.ChildTaskDrivers)
        
    @childTaskDrivers.setter     
    def _set_childTaskDrivers(self, value):
        self.native_obj.ChildTaskDrivers = value
            
    # -> Any            
    @property         
    def effectiveDateAdd(self) -> "Any":
        return (self.native_obj.EffectiveDateAdd)
        
    @effectiveDateAdd.setter     
    def _set_effectiveDateAdd(self, value):
        self.native_obj.EffectiveDateAdd = value
            
    # -> Any            
    @property         
    def effectiveDateDifference(self) -> "Any":
        return (self.native_obj.EffectiveDateDifference)
        
    @effectiveDateDifference.setter     
    def _set_effectiveDateDifference(self, value):
        self.native_obj.EffectiveDateDifference = value
            
    # -> Any            
    @property         
    def effectiveDateSubtract(self) -> "Any":
        return (self.native_obj.EffectiveDateSubtract)
        
    @effectiveDateSubtract.setter     
    def _set_effectiveDateSubtract(self, value):
        self.native_obj.EffectiveDateSubtract = value
            
    # -> Any            
    @property         
    def overAllocatedAssignments(self) -> "Any":
        return (self.native_obj.OverAllocatedAssignments)
        
    @overAllocatedAssignments.setter     
    def _set_overAllocatedAssignments(self, value):
        self.native_obj.OverAllocatedAssignments = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def predecessorDrivers(self) -> "Any":
        return (self.native_obj.PredecessorDrivers)
        
    @predecessorDrivers.setter     
    def _set_predecessorDrivers(self, value):
        self.native_obj.PredecessorDrivers = value
            
    # -> Any            
    @property         
    def suggestions(self) -> "Any":
        return (self.native_obj.Suggestions)
        
    @suggestions.setter     
    def _set_suggestions(self, value):
        self.native_obj.Suggestions = value
            
    # -> Any            
    @property         
    def warnings(self) -> "Any":
        return (self.native_obj.Warnings)
        
    @warnings.setter     
    def _set_warnings(self, value):
        self.native_obj.Warnings = value
            
# end "StartDriver"       
        