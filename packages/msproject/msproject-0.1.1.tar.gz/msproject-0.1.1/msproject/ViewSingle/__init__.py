

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class ViewSingle:
    # Object "ViewSingle" class for software "Project"
    
    properties = ['application', 'filter', 'group', 'highlightFilter', 'index', 'name', 'parent', 'screen', 'showInMenu', 'single', 'table', 'type']
    
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
    def filter(self) -> "Any":
        return (self.native_obj.Filter)
        
    @filter.setter     
    def _set_filter(self, value):
        self.native_obj.Filter = value
            
    # -> Any            
    @property         
    def group(self) -> "Any":
        return (self.native_obj.Group)
        
    @group.setter     
    def _set_group(self, value):
        self.native_obj.Group = value
            
    # -> Any            
    @property         
    def highlightFilter(self) -> "Any":
        return (self.native_obj.HighlightFilter)
        
    @highlightFilter.setter     
    def _set_highlightFilter(self, value):
        self.native_obj.HighlightFilter = value
            
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
    def screen(self) -> "Any":
        return (self.native_obj.Screen)
        
    @screen.setter     
    def _set_screen(self, value):
        self.native_obj.Screen = value
            
    # -> Any            
    @property         
    def showInMenu(self) -> "Any":
        return (self.native_obj.ShowInMenu)
        
    @showInMenu.setter     
    def _set_showInMenu(self, value):
        self.native_obj.ShowInMenu = value
            
    # -> Any            
    @property         
    def single(self) -> "Any":
        return (self.native_obj.Single)
        
    @single.setter     
    def _set_single(self, value):
        self.native_obj.Single = value
            
    # -> Any            
    @property         
    def table(self) -> "Any":
        return (self.native_obj.Table)
        
    @table.setter     
    def _set_table(self, value):
        self.native_obj.Table = value
            
    # -> Any            
    @property         
    def type(self) -> "Any":
        return (self.native_obj.Type)
        
    @type.setter     
    def _set_type(self, value):
        self.native_obj.Type = value
            
# end "ViewSingle"       
        