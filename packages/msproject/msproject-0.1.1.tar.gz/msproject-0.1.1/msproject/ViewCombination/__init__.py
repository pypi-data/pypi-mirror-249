

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class ViewCombination:
    # Object "ViewCombination" class for software "Project"
    
    properties = ['application', 'bottomView', 'index', 'name', 'parent', 'screen', 'showInMenu', 'single', 'topView', 'type']
    
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
    def bottomView(self) -> "Any":
        return (self.native_obj.BottomView)
        
    @bottomView.setter     
    def _set_bottomView(self, value):
        self.native_obj.BottomView = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def name(self) -> "Any":
        return (self.native_obj.Name)
        
    @name.setter     
    def _set_name(self, value):
        self.native_obj.Name = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def screen(self) -> "Any":
        return (self.native_obj.Screen)
        
    @screen.setter     
    def _set_screen(self, value):
        self.native_obj.Screen = value
            
    # -> Any            
    @property         
    def showInMenu(self) -> "Any":
        return (self.native_obj.ShowInMenu)
        
    @showInMenu.setter     
    def _set_showInMenu(self, value):
        self.native_obj.ShowInMenu = value
            
    # -> Any            
    @property         
    def single(self) -> "Any":
        return (self.native_obj.Single)
        
    @single.setter     
    def _set_single(self, value):
        self.native_obj.Single = value
            
    # -> Any            
    @property         
    def topView(self) -> "Any":
        return (self.native_obj.TopView)
        
    @topView.setter     
    def _set_topView(self, value):
        self.native_obj.TopView = value
            
    # -> Any            
    @property         
    def type(self) -> "Any":
        return (self.native_obj.Type)
        
    @type.setter     
    def _set_type(self, value):
        self.native_obj.Type = value
            
# end "ViewCombination"       
        