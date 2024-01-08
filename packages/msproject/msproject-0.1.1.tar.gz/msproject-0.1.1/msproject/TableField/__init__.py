

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class TableField:
    # Object "TableField" class for software "Project"
    
    properties = ['alignData', 'alignTitle', 'application', 'autoWrap', 'field', 'index', 'parent', 'title', 'width']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def alignData(self) -> "Any":
        return (self.native_obj.AlignData)
        
    @alignData.setter     
    def _set_alignData(self, value):
        self.native_obj.AlignData = value
            
    # -> Any            
    @property         
    def alignTitle(self) -> "Any":
        return (self.native_obj.AlignTitle)
        
    @alignTitle.setter     
    def _set_alignTitle(self, value):
        self.native_obj.AlignTitle = value
            
    # -> Any            
    @property         
    def application(self) -> "Any":
        return (self.native_obj.Application)
        
    @application.setter     
    def _set_application(self, value):
        self.native_obj.Application = value
            
    # -> Any            
    @property         
    def autoWrap(self) -> "Any":
        return (self.native_obj.AutoWrap)
        
    @autoWrap.setter     
    def _set_autoWrap(self, value):
        self.native_obj.AutoWrap = value
            
    # -> Any            
    @property         
    def field(self) -> "Any":
        return (self.native_obj.Field)
        
    @field.setter     
    def _set_field(self, value):
        self.native_obj.Field = value
            
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
    def title(self) -> "Any":
        return (self.native_obj.Title)
        
    @title.setter     
    def _set_title(self, value):
        self.native_obj.Title = value
            
    # -> Any            
    @property         
    def width(self) -> "Any":
        return (self.native_obj.Width)
        
    @width.setter     
    def _set_width(self, value):
        self.native_obj.Width = value
            
# end "TableField"       
        