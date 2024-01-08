

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Series:
    # Object "Series" class for software "Project"
    
    properties = ['application', 'name', 'parent', 'values', 'xValues']
    
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
    def values(self) -> "Any":
        return (self.native_obj.Values)
        
    @values.setter     
    def _set_values(self, value):
        self.native_obj.Values = value
            
    # -> Any            
    @property         
    def xValues(self) -> "Any":
        return (self.native_obj.XValues)
        
    @xValues.setter     
    def _set_xValues(self, value):
        self.native_obj.XValues = value
            
# end "Series"       
        