

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class CodeMaskLevel:
    # Object "CodeMaskLevel" class for software "Project"
    
    properties = ['application', 'index', 'length', 'level', 'parent', 'separator', 'sequence']
    
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
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def length(self) -> "Any":
        return (self.native_obj.Length)
        
    @length.setter     
    def _set_length(self, value):
        self.native_obj.Length = value
            
    # -> Any            
    @property         
    def level(self) -> "Any":
        return (self.native_obj.Level)
        
    @level.setter     
    def _set_level(self, value):
        self.native_obj.Level = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def separator(self) -> "Any":
        return (self.native_obj.Separator)
        
    @separator.setter     
    def _set_separator(self, value):
        self.native_obj.Separator = value
            
    # -> Any            
    @property         
    def sequence(self) -> "Any":
        return (self.native_obj.Sequence)
        
    @sequence.setter     
    def _set_sequence(self, value):
        self.native_obj.Sequence = value
            
# end "CodeMaskLevel"       
        