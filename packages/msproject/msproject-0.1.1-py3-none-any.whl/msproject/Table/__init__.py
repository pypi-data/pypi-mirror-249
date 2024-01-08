

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Table:
    # Object "Table" class for software "Project"
    
    properties = ['adjustHeaderRowHeight', 'application', 'dateFormat', 'index', 'lockFirstColumn', 'name', 'parent', 'rowHeight', 'showInMenu', 'tableFields', 'tableType']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def adjustHeaderRowHeight(self) -> "Any":
        return (self.native_obj.AdjustHeaderRowHeight)
        
    @adjustHeaderRowHeight.setter     
    def _set_adjustHeaderRowHeight(self, value):
        self.native_obj.AdjustHeaderRowHeight = value
            
    # -> Any            
    @property         
    def application(self) -> "Any":
        return (self.native_obj.Application)
        
    @application.setter     
    def _set_application(self, value):
        self.native_obj.Application = value
            
    # -> Any            
    @property         
    def dateFormat(self) -> "Any":
        return (self.native_obj.DateFormat)
        
    @dateFormat.setter     
    def _set_dateFormat(self, value):
        self.native_obj.DateFormat = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def lockFirstColumn(self) -> "Any":
        return (self.native_obj.LockFirstColumn)
        
    @lockFirstColumn.setter     
    def _set_lockFirstColumn(self, value):
        self.native_obj.LockFirstColumn = value
            
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
    def rowHeight(self) -> "Any":
        return (self.native_obj.RowHeight)
        
    @rowHeight.setter     
    def _set_rowHeight(self, value):
        self.native_obj.RowHeight = value
            
    # -> Any            
    @property         
    def showInMenu(self) -> "Any":
        return (self.native_obj.ShowInMenu)
        
    @showInMenu.setter     
    def _set_showInMenu(self, value):
        self.native_obj.ShowInMenu = value
            
    # -> Any            
    @property         
    def tableFields(self) -> "Any":
        return (self.native_obj.TableFields)
        
    @tableFields.setter     
    def _set_tableFields(self, value):
        self.native_obj.TableFields = value
            
    # -> Any            
    @property         
    def tableType(self) -> "Any":
        return (self.native_obj.TableType)
        
    @tableType.setter     
    def _set_tableType(self, value):
        self.native_obj.TableType = value
            
# end "Table"       
        