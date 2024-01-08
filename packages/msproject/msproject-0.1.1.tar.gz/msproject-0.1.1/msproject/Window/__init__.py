

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Window:
    # Object "Window" class for software "Project"
    
    properties = ['activePane', 'application', 'bottomPane', 'caption', 'height', 'index', 'left', 'parent', 'top', 'topPane', 'visible', 'width', 'windowState']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def activePane(self) -> "Any":
        return (self.native_obj.ActivePane)
        
    @activePane.setter     
    def _set_activePane(self, value):
        self.native_obj.ActivePane = value
            
    # -> Any            
    @property         
    def application(self) -> "Any":
        return (self.native_obj.Application)
        
    @application.setter     
    def _set_application(self, value):
        self.native_obj.Application = value
            
    # -> Any            
    @property         
    def bottomPane(self) -> "Any":
        return (self.native_obj.BottomPane)
        
    @bottomPane.setter     
    def _set_bottomPane(self, value):
        self.native_obj.BottomPane = value
            
    # -> Any            
    @property         
    def caption(self) -> "Any":
        return (self.native_obj.Caption)
        
    @caption.setter     
    def _set_caption(self, value):
        self.native_obj.Caption = value
            
    # -> Any            
    @property         
    def height(self) -> "Any":
        return (self.native_obj.Height)
        
    @height.setter     
    def _set_height(self, value):
        self.native_obj.Height = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def left(self) -> "Any":
        return (self.native_obj.Left)
        
    @left.setter     
    def _set_left(self, value):
        self.native_obj.Left = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def top(self) -> "Any":
        return (self.native_obj.Top)
        
    @top.setter     
    def _set_top(self, value):
        self.native_obj.Top = value
            
    # -> Any            
    @property         
    def topPane(self) -> "Any":
        return (self.native_obj.TopPane)
        
    @topPane.setter     
    def _set_topPane(self, value):
        self.native_obj.TopPane = value
            
    # -> Any            
    @property         
    def visible(self) -> "Any":
        return (self.native_obj.Visible)
        
    @visible.setter     
    def _set_visible(self, value):
        self.native_obj.Visible = value
            
    # -> Any            
    @property         
    def width(self) -> "Any":
        return (self.native_obj.Width)
        
    @width.setter     
    def _set_width(self, value):
        self.native_obj.Width = value
            
    # -> Any            
    @property         
    def windowState(self) -> "Any":
        return (self.native_obj.WindowState)
        
    @windowState.setter     
    def _set_windowState(self, value):
        self.native_obj.WindowState = value
            
# end "Window"       
        