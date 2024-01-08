

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class SplitPart:
    # Object "SplitPart" class for software "Project"
    
    properties = ['application', 'finish', 'index', 'parent', 'start']
    
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
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def start(self) -> "Any":
        return (self.native_obj.Start)
        
    @start.setter     
    def _set_start(self, value):
        self.native_obj.Start = value
            
# end "SplitPart"       
        