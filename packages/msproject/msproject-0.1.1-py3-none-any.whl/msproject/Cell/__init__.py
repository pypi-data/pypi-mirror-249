

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Cell:
    # Object "Cell" class for software "Project"
    
    properties = ['application', 'assignment', 'cellColor', 'cellColorEx', 'engagement', 'fieldID', 'fieldName', 'fontColor', 'fontColorEx', 'parent', 'pattern', 'resource', 'task', 'text']
    
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
    def assignment(self) -> "Any":
        return (self.native_obj.Assignment)
        
    @assignment.setter     
    def _set_assignment(self, value):
        self.native_obj.Assignment = value
            
    # -> Any            
    @property         
    def cellColor(self) -> "Any":
        return (self.native_obj.CellColor)
        
    @cellColor.setter     
    def _set_cellColor(self, value):
        self.native_obj.CellColor = value
            
    # -> Any            
    @property         
    def cellColorEx(self) -> "Any":
        return (self.native_obj.CellColorEx)
        
    @cellColorEx.setter     
    def _set_cellColorEx(self, value):
        self.native_obj.CellColorEx = value
            
    # -> Any            
    @property         
    def engagement(self) -> "Any":
        return (self.native_obj.Engagement)
        
    @engagement.setter     
    def _set_engagement(self, value):
        self.native_obj.Engagement = value
            
    # -> Any            
    @property         
    def fieldID(self) -> "Any":
        return (self.native_obj.FieldID)
        
    @fieldID.setter     
    def _set_fieldID(self, value):
        self.native_obj.FieldID = value
            
    # -> Any            
    @property         
    def fieldName(self) -> "Any":
        return (self.native_obj.FieldName)
        
    @fieldName.setter     
    def _set_fieldName(self, value):
        self.native_obj.FieldName = value
            
    # -> Any            
    @property         
    def fontColor(self) -> "Any":
        return (self.native_obj.FontColor)
        
    @fontColor.setter     
    def _set_fontColor(self, value):
        self.native_obj.FontColor = value
            
    # -> Any            
    @property         
    def fontColorEx(self) -> "Any":
        return (self.native_obj.FontColorEx)
        
    @fontColorEx.setter     
    def _set_fontColorEx(self, value):
        self.native_obj.FontColorEx = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def pattern(self) -> "Any":
        return (self.native_obj.Pattern)
        
    @pattern.setter     
    def _set_pattern(self, value):
        self.native_obj.Pattern = value
            
    # -> Any            
    @property         
    def resource(self) -> "Any":
        return (self.native_obj.Resource)
        
    @resource.setter     
    def _set_resource(self, value):
        self.native_obj.Resource = value
            
    # -> Any            
    @property         
    def task(self) -> "Any":
        return (self.native_obj.Task)
        
    @task.setter     
    def _set_task(self, value):
        self.native_obj.Task = value
            
    # -> Any            
    @property         
    def text(self) -> "Any":
        return (self.native_obj.Text)
        
    @text.setter     
    def _set_text(self, value):
        self.native_obj.Text = value
            
# end "Cell"       
        