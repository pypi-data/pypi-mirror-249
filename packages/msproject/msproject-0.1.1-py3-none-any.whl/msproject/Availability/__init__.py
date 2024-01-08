

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Availability:
    # Object "Availability" class for software "Project"
    
    properties = ['application', 'availableFrom', 'availableTo', 'availableUnit', 'index', 'parent']
    
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
    def availableFrom(self) -> "Any":
        return (self.native_obj.AvailableFrom)
        
    @availableFrom.setter     
    def _set_availableFrom(self, value):
        self.native_obj.AvailableFrom = value
            
    # -> Any            
    @property         
    def availableTo(self) -> "Any":
        return (self.native_obj.AvailableTo)
        
    @availableTo.setter     
    def _set_availableTo(self, value):
        self.native_obj.AvailableTo = value
            
    # -> Any            
    @property         
    def availableUnit(self) -> "Any":
        return (self.native_obj.AvailableUnit)
        
    @availableUnit.setter     
    def _set_availableUnit(self, value):
        self.native_obj.AvailableUnit = value
            
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
            
# end "Availability"       
        