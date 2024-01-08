

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class OutlineCode:
    # Object "OutlineCode" class for software "Project"
    
    properties = ['application', 'codeMask', 'defaultValue', 'fieldID', 'index', 'linkedFieldID', 'lookupTable', 'matchGeneric', 'name', 'onlyCompleteCodes', 'onlyLeaves', 'onlyLookUpTableCodes', 'parent', 'requiredCode', 'sortOrder']
    
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
    def codeMask(self) -> "Any":
        return (self.native_obj.CodeMask)
        
    @codeMask.setter     
    def _set_codeMask(self, value):
        self.native_obj.CodeMask = value
            
    # -> Any            
    @property         
    def defaultValue(self) -> "Any":
        return (self.native_obj.DefaultValue)
        
    @defaultValue.setter     
    def _set_defaultValue(self, value):
        self.native_obj.DefaultValue = value
            
    # -> Any            
    @property         
    def fieldID(self) -> "Any":
        return (self.native_obj.FieldID)
        
    @fieldID.setter     
    def _set_fieldID(self, value):
        self.native_obj.FieldID = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def linkedFieldID(self) -> "Any":
        return (self.native_obj.LinkedFieldID)
        
    @linkedFieldID.setter     
    def _set_linkedFieldID(self, value):
        self.native_obj.LinkedFieldID = value
            
    # -> Any            
    @property         
    def lookupTable(self) -> "Any":
        return (self.native_obj.LookupTable)
        
    @lookupTable.setter     
    def _set_lookupTable(self, value):
        self.native_obj.LookupTable = value
            
    # -> Any            
    @property         
    def matchGeneric(self) -> "Any":
        return (self.native_obj.MatchGeneric)
        
    @matchGeneric.setter     
    def _set_matchGeneric(self, value):
        self.native_obj.MatchGeneric = value
            
    # -> Any            
    @property         
    def name(self) -> "Any":
        return (self.native_obj.Name)
        
    @name.setter     
    def _set_name(self, value):
        self.native_obj.Name = value
            
    # -> Any            
    @property         
    def onlyCompleteCodes(self) -> "Any":
        return (self.native_obj.OnlyCompleteCodes)
        
    @onlyCompleteCodes.setter     
    def _set_onlyCompleteCodes(self, value):
        self.native_obj.OnlyCompleteCodes = value
            
    # -> Any            
    @property         
    def onlyLeaves(self) -> "Any":
        return (self.native_obj.OnlyLeaves)
        
    @onlyLeaves.setter     
    def _set_onlyLeaves(self, value):
        self.native_obj.OnlyLeaves = value
            
    # -> Any            
    @property         
    def onlyLookUpTableCodes(self) -> "Any":
        return (self.native_obj.OnlyLookUpTableCodes)
        
    @onlyLookUpTableCodes.setter     
    def _set_onlyLookUpTableCodes(self, value):
        self.native_obj.OnlyLookUpTableCodes = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def requiredCode(self) -> "Any":
        return (self.native_obj.RequiredCode)
        
    @requiredCode.setter     
    def _set_requiredCode(self, value):
        self.native_obj.RequiredCode = value
            
    # -> Any            
    @property         
    def sortOrder(self) -> "Any":
        return (self.native_obj.SortOrder)
        
    @sortOrder.setter     
    def _set_sortOrder(self, value):
        self.native_obj.SortOrder = value
            
# end "OutlineCode"       
        