

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class PayRate:
    # Object "PayRate" class for software "Project"
    
    properties = ['application', 'costPerUse', 'effectiveDate', 'index', 'overtimeRate', 'parent', 'standardRate']
    
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
    def costPerUse(self) -> "Any":
        return (self.native_obj.CostPerUse)
        
    @costPerUse.setter     
    def _set_costPerUse(self, value):
        self.native_obj.CostPerUse = value
            
    # -> Any            
    @property         
    def effectiveDate(self) -> "Any":
        return (self.native_obj.EffectiveDate)
        
    @effectiveDate.setter     
    def _set_effectiveDate(self, value):
        self.native_obj.EffectiveDate = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def overtimeRate(self) -> "Any":
        return (self.native_obj.OvertimeRate)
        
    @overtimeRate.setter     
    def _set_overtimeRate(self, value):
        self.native_obj.OvertimeRate = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def standardRate(self) -> "Any":
        return (self.native_obj.StandardRate)
        
    @standardRate.setter     
    def _set_standardRate(self, value):
        self.native_obj.StandardRate = value
            
# end "PayRate"       
        