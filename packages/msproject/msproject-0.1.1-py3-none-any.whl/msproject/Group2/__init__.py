

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Group2:
    # Object "Group2" class for software "Project"
    
    properties = ['application', 'groupAssignments', 'groupCriteria', 'index', 'maintainHierarchy', 'name', 'parent', 'showSummary']
    
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
    def groupAssignments(self) -> "Any":
        return (self.native_obj.GroupAssignments)
        
    @groupAssignments.setter     
    def _set_groupAssignments(self, value):
        self.native_obj.GroupAssignments = value
            
    # -> Any            
    @property         
    def groupCriteria(self) -> "Any":
        return (self.native_obj.GroupCriteria)
        
    @groupCriteria.setter     
    def _set_groupCriteria(self, value):
        self.native_obj.GroupCriteria = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def maintainHierarchy(self) -> "Any":
        return (self.native_obj.MaintainHierarchy)
        
    @maintainHierarchy.setter     
    def _set_maintainHierarchy(self, value):
        self.native_obj.MaintainHierarchy = value
            
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
    def showSummary(self) -> "Any":
        return (self.native_obj.ShowSummary)
        
    @showSummary.setter     
    def _set_showSummary(self, value):
        self.native_obj.ShowSummary = value
            
# end "Group2"       
        