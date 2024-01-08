

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class SeriesCollection:
    # Object "SeriesCollection" class for software "Project"
    
    properties = ['application', 'count', 'creator', 'parent']
    
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
    def count(self) -> "Any":
        return (self.native_obj.Count)
        
    @count.setter     
    def _set_count(self, value):
        self.native_obj.Count = value
            
    # -> Any            
    @property         
    def creator(self) -> "Any":
        return (self.native_obj.Creator)
        
    @creator.setter     
    def _set_creator(self, value):
        self.native_obj.Creator = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
# end "SeriesCollection"       
        