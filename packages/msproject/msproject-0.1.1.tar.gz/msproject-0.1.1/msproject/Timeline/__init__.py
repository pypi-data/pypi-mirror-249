

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Timeline:
    # Object "Timeline" class for software "Project"
    
    properties = ['application', 'barCount', 'finishDate', 'label', 'startDate']
    
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
    def barCount(self) -> "Any":
        return (self.native_obj.BarCount)
        
    @barCount.setter     
    def _set_barCount(self, value):
        self.native_obj.BarCount = value
            
    # -> Any            
    @property         
    def finishDate(self) -> "Any":
        return (self.native_obj.FinishDate)
        
    @finishDate.setter     
    def _set_finishDate(self, value):
        self.native_obj.FinishDate = value
            
    # -> Any            
    @property         
    def label(self) -> "Any":
        return (self.native_obj.Label)
        
    @label.setter     
    def _set_label(self, value):
        self.native_obj.Label = value
            
    # -> Any            
    @property         
    def startDate(self) -> "Any":
        return (self.native_obj.StartDate)
        
    @startDate.setter     
    def _set_startDate(self, value):
        self.native_obj.StartDate = value
            
# end "Timeline"       
        