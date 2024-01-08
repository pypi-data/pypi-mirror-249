

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class EventInfo:
    # Object "EventInfo" class for software "Project"
    
    properties = ['cancel']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def cancel(self) -> "Any":
        return (self.native_obj.Cancel)
        
    @cancel.setter     
    def _set_cancel(self, value):
        self.native_obj.Cancel = value
            
# end "EventInfo"       
        