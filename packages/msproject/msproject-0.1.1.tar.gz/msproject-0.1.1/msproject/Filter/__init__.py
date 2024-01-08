

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Filter:
    # Object "Filter" class for software "Project"
    
    properties = ['application', 'filterType', 'index', 'name', 'parent', 'showInMenu', 'showRelatedSummaryRows']
    
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
    def filterType(self) -> "Any":
        return (self.native_obj.FilterType)
        
    @filterType.setter     
    def _set_filterType(self, value):
        self.native_obj.FilterType = value
            
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
    def showInMenu(self) -> "Any":
        return (self.native_obj.ShowInMenu)
        
    @showInMenu.setter     
    def _set_showInMenu(self, value):
        self.native_obj.ShowInMenu = value
            
    # -> Any            
    @property         
    def showRelatedSummaryRows(self) -> "Any":
        return (self.native_obj.ShowRelatedSummaryRows)
        
    @showRelatedSummaryRows.setter     
    def _set_showRelatedSummaryRows(self, value):
        self.native_obj.ShowRelatedSummaryRows = value
            
# end "Filter"       
        