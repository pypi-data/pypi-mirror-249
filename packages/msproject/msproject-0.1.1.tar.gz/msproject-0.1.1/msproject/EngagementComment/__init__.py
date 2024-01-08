

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class EngagementComment:
    # Object "EngagementComment" class for software "Project"
    
    properties = ['application', 'authorResEmail', 'authorResGuid', 'authorResName', 'createdDate', 'guid', 'message', 'parent']
    
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
    def authorResEmail(self) -> "Any":
        return (self.native_obj.AuthorResEmail)
        
    @authorResEmail.setter     
    def _set_authorResEmail(self, value):
        self.native_obj.AuthorResEmail = value
            
    # -> Any            
    @property         
    def authorResGuid(self) -> "Any":
        return (self.native_obj.AuthorResGuid)
        
    @authorResGuid.setter     
    def _set_authorResGuid(self, value):
        self.native_obj.AuthorResGuid = value
            
    # -> Any            
    @property         
    def authorResName(self) -> "Any":
        return (self.native_obj.AuthorResName)
        
    @authorResName.setter     
    def _set_authorResName(self, value):
        self.native_obj.AuthorResName = value
            
    # -> Any            
    @property         
    def createdDate(self) -> "Any":
        return (self.native_obj.CreatedDate)
        
    @createdDate.setter     
    def _set_createdDate(self, value):
        self.native_obj.CreatedDate = value
            
    # -> Any            
    @property         
    def guid(self) -> "Any":
        return (self.native_obj.Guid)
        
    @guid.setter     
    def _set_guid(self, value):
        self.native_obj.Guid = value
            
    # -> Any            
    @property         
    def message(self) -> "Any":
        return (self.native_obj.Message)
        
    @message.setter     
    def _set_message(self, value):
        self.native_obj.Message = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
# end "EngagementComment"       
        