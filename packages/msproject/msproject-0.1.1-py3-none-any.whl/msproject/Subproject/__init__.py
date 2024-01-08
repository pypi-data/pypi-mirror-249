

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Subproject:
    # Object "Subproject" class for software "Project"
    
    properties = ['application', 'index', 'insertedProjectSummary', 'isLoaded', 'linkToSource', 'parent', 'path', 'readOnly', 'sourceProject']
    
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
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def insertedProjectSummary(self) -> "Any":
        return (self.native_obj.InsertedProjectSummary)
        
    @insertedProjectSummary.setter     
    def _set_insertedProjectSummary(self, value):
        self.native_obj.InsertedProjectSummary = value
            
    # -> Any            
    @property         
    def isLoaded(self) -> "Any":
        return (self.native_obj.IsLoaded)
        
    @isLoaded.setter     
    def _set_isLoaded(self, value):
        self.native_obj.IsLoaded = value
            
    # -> Any            
    @property         
    def linkToSource(self) -> "Any":
        return (self.native_obj.LinkToSource)
        
    @linkToSource.setter     
    def _set_linkToSource(self, value):
        self.native_obj.LinkToSource = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def path(self) -> "Any":
        return (self.native_obj.Path)
        
    @path.setter     
    def _set_path(self, value):
        self.native_obj.Path = value
            
    # -> Any            
    @property         
    def readOnly(self) -> "Any":
        return (self.native_obj.ReadOnly)
        
    @readOnly.setter     
    def _set_readOnly(self, value):
        self.native_obj.ReadOnly = value
            
    # -> Any            
    @property         
    def sourceProject(self) -> "Any":
        return (self.native_obj.SourceProject)
        
    @sourceProject.setter     
    def _set_sourceProject(self, value):
        self.native_obj.SourceProject = value
            
# end "Subproject"       
        