

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Profile:
    # Object "Profile" class for software "Project"
    
    properties = ['connectionState', 'loginType', 'name', 'server', 'siteId', 'type', 'userName']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def connectionState(self) -> "Any":
        return (self.native_obj.ConnectionState)
        
    @connectionState.setter     
    def _set_connectionState(self, value):
        self.native_obj.ConnectionState = value
            
    # -> Any            
    @property         
    def loginType(self) -> "Any":
        return (self.native_obj.LoginType)
        
    @loginType.setter     
    def _set_loginType(self, value):
        self.native_obj.LoginType = value
            
    # -> Any            
    @property         
    def name(self) -> "Any":
        return (self.native_obj.Name)
        
    @name.setter     
    def _set_name(self, value):
        self.native_obj.Name = value
            
    # -> Any            
    @property         
    def server(self) -> "Any":
        return (self.native_obj.Server)
        
    @server.setter     
    def _set_server(self, value):
        self.native_obj.Server = value
            
    # -> Any            
    @property         
    def siteId(self) -> "Any":
        return (self.native_obj.SiteId)
        
    @siteId.setter     
    def _set_siteId(self, value):
        self.native_obj.SiteId = value
            
    # -> Any            
    @property         
    def type(self) -> "Any":
        return (self.native_obj.Type)
        
    @type.setter     
    def _set_type(self, value):
        self.native_obj.Type = value
            
    # -> Any            
    @property         
    def userName(self) -> "Any":
        return (self.native_obj.UserName)
        
    @userName.setter     
    def _set_userName(self, value):
        self.native_obj.UserName = value
            
# end "Profile"       
        