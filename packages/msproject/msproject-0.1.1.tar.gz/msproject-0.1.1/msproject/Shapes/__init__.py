

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Shapes:
    # Object "Shapes" class for software "Project"
    
    properties = ['background', 'count', 'default', 'parent', 'value']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def background(self) -> "Any":
        return (self.native_obj.Background)
        
    @background.setter     
    def _set_background(self, value):
        self.native_obj.Background = value
            
    # -> Any            
    @property         
    def count(self) -> "Any":
        return (self.native_obj.Count)
        
    @count.setter     
    def _set_count(self, value):
        self.native_obj.Count = value
            
    # -> Any            
    @property         
    def default(self) -> "Any":
        return (self.native_obj.Default)
        
    @default.setter     
    def _set_default(self, value):
        self.native_obj.Default = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def value(self) -> "Any":
        return (self.native_obj.Value)
        
    @value.setter     
    def _set_value(self, value):
        self.native_obj.Value = value
            
# end "Shapes"       
        