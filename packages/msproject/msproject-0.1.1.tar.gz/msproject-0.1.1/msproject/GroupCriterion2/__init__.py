

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class GroupCriterion2:
    # Object "GroupCriterion2" class for software "Project"
    
    properties = ['application', 'ascending', 'assignment', 'cellColor', 'cellColorEx', 'fieldName', 'fontBold', 'fontColor', 'fontColorEx', 'fontItalic', 'fontName', 'fontSize', 'fontUnderLine', 'groupInterval', 'groupOn', 'index', 'parent', 'pattern', 'startAt']
    
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
    def ascending(self) -> "Any":
        return (self.native_obj.Ascending)
        
    @ascending.setter     
    def _set_ascending(self, value):
        self.native_obj.Ascending = value
            
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
    def fieldName(self) -> "Any":
        return (self.native_obj.FieldName)
        
    @fieldName.setter     
    def _set_fieldName(self, value):
        self.native_obj.FieldName = value
            
    # -> Any            
    @property         
    def fontBold(self) -> "Any":
        return (self.native_obj.FontBold)
        
    @fontBold.setter     
    def _set_fontBold(self, value):
        self.native_obj.FontBold = value
            
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
    def fontItalic(self) -> "Any":
        return (self.native_obj.FontItalic)
        
    @fontItalic.setter     
    def _set_fontItalic(self, value):
        self.native_obj.FontItalic = value
            
    # -> Any            
    @property         
    def fontName(self) -> "Any":
        return (self.native_obj.FontName)
        
    @fontName.setter     
    def _set_fontName(self, value):
        self.native_obj.FontName = value
            
    # -> Any            
    @property         
    def fontSize(self) -> "Any":
        return (self.native_obj.FontSize)
        
    @fontSize.setter     
    def _set_fontSize(self, value):
        self.native_obj.FontSize = value
            
    # -> Any            
    @property         
    def fontUnderLine(self) -> "Any":
        return (self.native_obj.FontUnderLine)
        
    @fontUnderLine.setter     
    def _set_fontUnderLine(self, value):
        self.native_obj.FontUnderLine = value
            
    # -> Any            
    @property         
    def groupInterval(self) -> "Any":
        return (self.native_obj.GroupInterval)
        
    @groupInterval.setter     
    def _set_groupInterval(self, value):
        self.native_obj.GroupInterval = value
            
    # -> Any            
    @property         
    def groupOn(self) -> "Any":
        return (self.native_obj.GroupOn)
        
    @groupOn.setter     
    def _set_groupOn(self, value):
        self.native_obj.GroupOn = value
            
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
    def pattern(self) -> "Any":
        return (self.native_obj.Pattern)
        
    @pattern.setter     
    def _set_pattern(self, value):
        self.native_obj.Pattern = value
            
    # -> Any            
    @property         
    def startAt(self) -> "Any":
        return (self.native_obj.StartAt)
        
    @startAt.setter     
    def _set_startAt(self, value):
        self.native_obj.StartAt = value
            
# end "GroupCriterion2"       
        