

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class ReportTable:
    # Object "ReportTable" class for software "Project"
    
    properties = ['columnsCount', 'rowsCount']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def columnsCount(self) -> "Any":
        return (self.native_obj.ColumnsCount)
        
    @columnsCount.setter     
    def _set_columnsCount(self, value):
        self.native_obj.ColumnsCount = value
            
    # -> Any            
    @property         
    def rowsCount(self) -> "Any":
        return (self.native_obj.RowsCount)
        
    @rowsCount.setter     
    def _set_rowsCount(self, value):
        self.native_obj.RowsCount = value
            
# end "ReportTable"       
        