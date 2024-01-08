

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class ReportTemplate:
    # Object "ReportTemplate" class for software "Project"
    
    properties = ['cubeType', 'templatePath', 'templateType']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def cubeType(self) -> "Any":
        return (self.native_obj.CubeType)
        
    @cubeType.setter     
    def _set_cubeType(self, value):
        self.native_obj.CubeType = value
            
    # -> Any            
    @property         
    def templatePath(self) -> "Any":
        return (self.native_obj.TemplatePath)
        
    @templatePath.setter     
    def _set_templatePath(self, value):
        self.native_obj.TemplatePath = value
            
    # -> Any            
    @property         
    def templateType(self) -> "Any":
        return (self.native_obj.TemplateType)
        
    @templateType.setter     
    def _set_templateType(self, value):
        self.native_obj.TemplateType = value
            
# end "ReportTemplate"       
        