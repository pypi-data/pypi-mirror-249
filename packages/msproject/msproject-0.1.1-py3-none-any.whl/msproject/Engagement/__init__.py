

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Engagement:
    # Object "Engagement" class for software "Project"
    
    properties = ['application', 'comments', 'committedFinish', 'committedMaxUnits', 'committedStart', 'committedWork', 'createdDate', 'draftFinish', 'draftMaxUnits', 'draftStart', 'draftWork', 'guid', 'index', 'modifiedByGuid', 'modifiedByName', 'modifiedDate', 'name', 'parent', 'projectGuid', 'projectName', 'proposedFinish', 'proposedMaxUnits', 'proposedStart', 'proposedWork', 'resourceGuid', 'resourceID', 'resourceName', 'reviewedByGuid', 'reviewedByName', 'reviewedDate', 'status', 'submittedByGuid', 'submittedByName', 'submittedDate']
    
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
    def comments(self) -> "Any":
        return (self.native_obj.Comments)
        
    @comments.setter     
    def _set_comments(self, value):
        self.native_obj.Comments = value
            
    # -> Any            
    @property         
    def committedFinish(self) -> "Any":
        return (self.native_obj.CommittedFinish)
        
    @committedFinish.setter     
    def _set_committedFinish(self, value):
        self.native_obj.CommittedFinish = value
            
    # -> Any            
    @property         
    def committedMaxUnits(self) -> "Any":
        return (self.native_obj.CommittedMaxUnits)
        
    @committedMaxUnits.setter     
    def _set_committedMaxUnits(self, value):
        self.native_obj.CommittedMaxUnits = value
            
    # -> Any            
    @property         
    def committedStart(self) -> "Any":
        return (self.native_obj.CommittedStart)
        
    @committedStart.setter     
    def _set_committedStart(self, value):
        self.native_obj.CommittedStart = value
            
    # -> Any            
    @property         
    def committedWork(self) -> "Any":
        return (self.native_obj.CommittedWork)
        
    @committedWork.setter     
    def _set_committedWork(self, value):
        self.native_obj.CommittedWork = value
            
    # -> Any            
    @property         
    def createdDate(self) -> "Any":
        return (self.native_obj.CreatedDate)
        
    @createdDate.setter     
    def _set_createdDate(self, value):
        self.native_obj.CreatedDate = value
            
    # -> Any            
    @property         
    def draftFinish(self) -> "Any":
        return (self.native_obj.DraftFinish)
        
    @draftFinish.setter     
    def _set_draftFinish(self, value):
        self.native_obj.DraftFinish = value
            
    # -> Any            
    @property         
    def draftMaxUnits(self) -> "Any":
        return (self.native_obj.DraftMaxUnits)
        
    @draftMaxUnits.setter     
    def _set_draftMaxUnits(self, value):
        self.native_obj.DraftMaxUnits = value
            
    # -> Any            
    @property         
    def draftStart(self) -> "Any":
        return (self.native_obj.DraftStart)
        
    @draftStart.setter     
    def _set_draftStart(self, value):
        self.native_obj.DraftStart = value
            
    # -> Any            
    @property         
    def draftWork(self) -> "Any":
        return (self.native_obj.DraftWork)
        
    @draftWork.setter     
    def _set_draftWork(self, value):
        self.native_obj.DraftWork = value
            
    # -> Any            
    @property         
    def guid(self) -> "Any":
        return (self.native_obj.Guid)
        
    @guid.setter     
    def _set_guid(self, value):
        self.native_obj.Guid = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def modifiedByGuid(self) -> "Any":
        return (self.native_obj.ModifiedByGuid)
        
    @modifiedByGuid.setter     
    def _set_modifiedByGuid(self, value):
        self.native_obj.ModifiedByGuid = value
            
    # -> Any            
    @property         
    def modifiedByName(self) -> "Any":
        return (self.native_obj.ModifiedByName)
        
    @modifiedByName.setter     
    def _set_modifiedByName(self, value):
        self.native_obj.ModifiedByName = value
            
    # -> Any            
    @property         
    def modifiedDate(self) -> "Any":
        return (self.native_obj.ModifiedDate)
        
    @modifiedDate.setter     
    def _set_modifiedDate(self, value):
        self.native_obj.ModifiedDate = value
            
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
    def projectGuid(self) -> "Any":
        return (self.native_obj.ProjectGuid)
        
    @projectGuid.setter     
    def _set_projectGuid(self, value):
        self.native_obj.ProjectGuid = value
            
    # -> Any            
    @property         
    def projectName(self) -> "Any":
        return (self.native_obj.ProjectName)
        
    @projectName.setter     
    def _set_projectName(self, value):
        self.native_obj.ProjectName = value
            
    # -> Any            
    @property         
    def proposedFinish(self) -> "Any":
        return (self.native_obj.ProposedFinish)
        
    @proposedFinish.setter     
    def _set_proposedFinish(self, value):
        self.native_obj.ProposedFinish = value
            
    # -> Any            
    @property         
    def proposedMaxUnits(self) -> "Any":
        return (self.native_obj.ProposedMaxUnits)
        
    @proposedMaxUnits.setter     
    def _set_proposedMaxUnits(self, value):
        self.native_obj.ProposedMaxUnits = value
            
    # -> Any            
    @property         
    def proposedStart(self) -> "Any":
        return (self.native_obj.ProposedStart)
        
    @proposedStart.setter     
    def _set_proposedStart(self, value):
        self.native_obj.ProposedStart = value
            
    # -> Any            
    @property         
    def proposedWork(self) -> "Any":
        return (self.native_obj.ProposedWork)
        
    @proposedWork.setter     
    def _set_proposedWork(self, value):
        self.native_obj.ProposedWork = value
            
    # -> Any            
    @property         
    def resourceGuid(self) -> "Any":
        return (self.native_obj.ResourceGuid)
        
    @resourceGuid.setter     
    def _set_resourceGuid(self, value):
        self.native_obj.ResourceGuid = value
            
    # -> Any            
    @property         
    def resourceID(self) -> "Any":
        return (self.native_obj.ResourceID)
        
    @resourceID.setter     
    def _set_resourceID(self, value):
        self.native_obj.ResourceID = value
            
    # -> Any            
    @property         
    def resourceName(self) -> "Any":
        return (self.native_obj.ResourceName)
        
    @resourceName.setter     
    def _set_resourceName(self, value):
        self.native_obj.ResourceName = value
            
    # -> Any            
    @property         
    def reviewedByGuid(self) -> "Any":
        return (self.native_obj.ReviewedByGuid)
        
    @reviewedByGuid.setter     
    def _set_reviewedByGuid(self, value):
        self.native_obj.ReviewedByGuid = value
            
    # -> Any            
    @property         
    def reviewedByName(self) -> "Any":
        return (self.native_obj.ReviewedByName)
        
    @reviewedByName.setter     
    def _set_reviewedByName(self, value):
        self.native_obj.ReviewedByName = value
            
    # -> Any            
    @property         
    def reviewedDate(self) -> "Any":
        return (self.native_obj.ReviewedDate)
        
    @reviewedDate.setter     
    def _set_reviewedDate(self, value):
        self.native_obj.ReviewedDate = value
            
    # -> Any            
    @property         
    def status(self) -> "Any":
        return (self.native_obj.Status)
        
    @status.setter     
    def _set_status(self, value):
        self.native_obj.Status = value
            
    # -> Any            
    @property         
    def submittedByGuid(self) -> "Any":
        return (self.native_obj.SubmittedByGuid)
        
    @submittedByGuid.setter     
    def _set_submittedByGuid(self, value):
        self.native_obj.SubmittedByGuid = value
            
    # -> Any            
    @property         
    def submittedByName(self) -> "Any":
        return (self.native_obj.SubmittedByName)
        
    @submittedByName.setter     
    def _set_submittedByName(self, value):
        self.native_obj.SubmittedByName = value
            
    # -> Any            
    @property         
    def submittedDate(self) -> "Any":
        return (self.native_obj.SubmittedDate)
        
    @submittedDate.setter     
    def _set_submittedDate(self, value):
        self.native_obj.SubmittedDate = value
            
# end "Engagement"       
        