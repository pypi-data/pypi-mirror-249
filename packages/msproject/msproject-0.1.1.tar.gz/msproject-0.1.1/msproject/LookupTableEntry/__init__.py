

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class LookupTableEntry:
    # Object "LookupTableEntry" class for software "Project"
    
    properties = ['application', 'cookie', 'description', 'fullName', 'index', 'isValid', 'level', 'localizedCookie', 'name', 'parent', 'parentEntry', 'uniqueID']
    
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
    def cookie(self) -> "Any":
        return (self.native_obj.Cookie)
        
    @cookie.setter     
    def _set_cookie(self, value):
        self.native_obj.Cookie = value
            
    # -> Any            
    @property         
    def description(self) -> "Any":
        return (self.native_obj.Description)
        
    @description.setter     
    def _set_description(self, value):
        self.native_obj.Description = value
            
    # -> Any            
    @property         
    def fullName(self) -> "Any":
        return (self.native_obj.FullName)
        
    @fullName.setter     
    def _set_fullName(self, value):
        self.native_obj.FullName = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def isValid(self) -> "Any":
        return (self.native_obj.IsValid)
        
    @isValid.setter     
    def _set_isValid(self, value):
        self.native_obj.IsValid = value
            
    # -> Any            
    @property         
    def level(self) -> "Any":
        return (self.native_obj.Level)
        
    @level.setter     
    def _set_level(self, value):
        self.native_obj.Level = value
            
    # -> Any            
    @property         
    def localizedCookie(self) -> "Any":
        return (self.native_obj.LocalizedCookie)
        
    @localizedCookie.setter     
    def _set_localizedCookie(self, value):
        self.native_obj.LocalizedCookie = value
            
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
    def parentEntry(self) -> "Any":
        return (self.native_obj.ParentEntry)
        
    @parentEntry.setter     
    def _set_parentEntry(self, value):
        self.native_obj.ParentEntry = value
            
    # -> Any            
    @property         
    def uniqueID(self) -> "Any":
        return (self.native_obj.UniqueID)
        
    @uniqueID.setter     
    def _set_uniqueID(self, value):
        self.native_obj.UniqueID = value
            
# end "LookupTableEntry"       
        