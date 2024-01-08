

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Resource:
    # Object "Resource" class for software "Project"
    
    properties = ['accrueAt', 'actualCost', 'actualOvertimeCost', 'actualOvertimeWork', 'actualWork', 'aCWP', 'application', 'assignments', 'availabilities', 'availableFrom', 'availableTo', 'baseCalendar', 'baseline10BudgetCost', 'baseline10BudgetWork', 'baseline10Cost', 'baseline10Work', 'baseline1BudgetCost', 'baseline1BudgetWork', 'baseline1Cost', 'baseline1Work', 'baseline2BudgetCost', 'baseline2BudgetWork', 'baseline2Cost', 'baseline2Work', 'baseline3BudgetCost', 'baseline3BudgetWork', 'baseline3Cost', 'baseline3Work', 'baseline4BudgetCost', 'baseline4BudgetWork', 'baseline4Cost', 'baseline4Work', 'baseline5BudgetCost', 'baseline5BudgetWork', 'baseline5Cost', 'baseline5Work', 'baseline6BudgetCost', 'baseline6BudgetWork', 'baseline6Cost', 'baseline6Work', 'baseline7BudgetCost', 'baseline7BudgetWork', 'baseline7Cost', 'baseline7Work', 'baseline8BudgetCost', 'baseline8BudgetWork', 'baseline8Cost', 'baseline8Work', 'baseline9BudgetCost', 'baseline9BudgetWork', 'baseline9Cost', 'baseline9Work', 'baselineBudgetCost', 'baselineBudgetWork', 'baselineCost', 'baselineWork', 'bCWP', 'bCWS', 'bookingType', 'budget', 'budgetCost', 'budgetWork', 'calendar', 'calendarGuid', 'canLevel', 'code', 'compliant', 'confirmed', 'cost', 'cost1', 'cost10', 'cost2', 'cost3', 'cost4', 'cost5', 'cost6', 'cost7', 'cost8', 'cost9', 'costCenter', 'costPerUse', 'costRateTables', 'costVariance', 'created', 'cV', 'date1', 'date10', 'date2', 'date3', 'date4', 'date5', 'date6', 'date7', 'date8', 'date9', 'defaultAssignmentOwner', 'duration1', 'duration10', 'duration2', 'duration3', 'duration4', 'duration5', 'duration6', 'duration7', 'duration8', 'duration9', 'eMailAddress', 'engagementCommittedFinish', 'engagementCommittedMaxUnits', 'engagementCommittedStart', 'engagementCommittedWork', 'engagementDraftFinish', 'engagementDraftMaxUnits', 'engagementDraftStart', 'engagementDraftWork', 'engagementProposedFinish', 'engagementProposedMaxUnits', 'engagementProposedStart', 'engagementProposedWork', 'enterprise', 'enterpriseBaseCalendar', 'enterpriseCheckedOutBy', 'enterpriseGeneric', 'enterpriseInactive', 'enterpriseIsCheckedOut', 'enterpriseLastModifiedDate', 'enterpriseNameUsed', 'enterpriseRequiredValues', 'enterpriseUniqueID', 'errorMessage', 'finish1', 'finish10', 'finish2', 'finish3', 'finish4', 'finish5', 'finish6', 'finish7', 'finish8', 'finish9', 'flag1', 'flag10', 'flag11', 'flag12', 'flag13', 'flag14', 'flag15', 'flag16', 'flag17', 'flag18', 'flag19', 'flag2', 'flag20', 'flag3', 'flag4', 'flag5', 'flag6', 'flag7', 'flag8', 'flag9', 'group', 'groupBySummary', 'guid', 'hyperlink', 'hyperlinkAddress', 'hyperlinkHREF', 'hyperlinkScreenTip', 'hyperlinkSubAddress', 'iD', 'import_', 'index', 'initials', 'isLocked', 'isTeam', 'linkedFields', 'materialLabel', 'maxUnits', 'name', 'notes', 'number1', 'number10', 'number11', 'number12', 'number13', 'number14', 'number15', 'number16', 'number17', 'number18', 'number19', 'number2', 'number20', 'number3', 'number4', 'number5', 'number6', 'number7', 'number8', 'number9', 'objects', 'outlineCode1', 'outlineCode10', 'outlineCode2', 'outlineCode3', 'outlineCode4', 'outlineCode5', 'outlineCode6', 'outlineCode7', 'outlineCode8', 'outlineCode9', 'overallocated', 'overtimeCost', 'overtimeRate', 'overtimeWork', 'parent', 'payRates', 'peakUnits', 'percentWorkComplete', 'phonetics', 'project', 'regularWork', 'remainingCost', 'remainingOvertimeCost', 'remainingOvertimeWork', 'remainingWork', 'responsePending', 'standardRate', 'start1', 'start10', 'start2', 'start3', 'start4', 'start5', 'start6', 'start7', 'start8', 'start9', 'sV', 'teamStatusPending', 'text1', 'text10', 'text11', 'text12', 'text13', 'text14', 'text15', 'text16', 'text17', 'text18', 'text19', 'text2', 'text20', 'text21', 'text22', 'text23', 'text24', 'text25', 'text26', 'text27', 'text28', 'text29', 'text3', 'text30', 'text4', 'text5', 'text6', 'text7', 'text8', 'text9', 'type', 'uniqueID', 'updateNeeded', 'vAC', 'windowsUserAccount', 'work', 'workVariance']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> int            
    @property         
    def accrueAt(self) -> "int":
        return (self.native_obj.AccrueAt)
        
    @accrueAt.setter     
    def _set_accrueAt(self, value):
        self.native_obj.AccrueAt = value
            
    # -> float            
    @property         
    def actualCost(self) -> "float":
        return (self.native_obj.ActualCost)
        
    @actualCost.setter     
    def _set_actualCost(self, value):
        self.native_obj.ActualCost = value
            
    # -> float            
    @property         
    def actualOvertimeCost(self) -> "float":
        return (self.native_obj.ActualOvertimeCost)
        
    @actualOvertimeCost.setter     
    def _set_actualOvertimeCost(self, value):
        self.native_obj.ActualOvertimeCost = value
            
    # -> float            
    @property         
    def actualOvertimeWork(self) -> "float":
        return (self.native_obj.ActualOvertimeWork)
        
    @actualOvertimeWork.setter     
    def _set_actualOvertimeWork(self, value):
        self.native_obj.ActualOvertimeWork = value
            
    # -> float            
    @property         
    def actualWork(self) -> "float":
        return (self.native_obj.ActualWork)
        
    @actualWork.setter     
    def _set_actualWork(self, value):
        self.native_obj.ActualWork = value
            
    # -> float            
    @property         
    def aCWP(self) -> "float":
        return (self.native_obj.ACWP)
        
    @aCWP.setter     
    def _set_aCWP(self, value):
        self.native_obj.ACWP = value
            
    # -> Application            
    @property         
    def application(self) -> "Application":
        return Application(self.native_obj.Application)
        
    @application.setter     
    def _set_application(self, value):
        self.native_obj.Application = value
            
    # -> Assignments            
    @property         
    def assignments(self) -> "Assignments":
        return Assignments(self.native_obj.Assignments)
        
    @assignments.setter     
    def _set_assignments(self, value):
        self.native_obj.Assignments = value
            
    # -> Availabilities            
    @property         
    def availabilities(self) -> "Availabilities":
        return Availabilities(self.native_obj.Availabilities)
        
    @availabilities.setter     
    def _set_availabilities(self, value):
        self.native_obj.Availabilities = value
            
    # -> str            
    @property         
    def availableFrom(self) -> "str":
        return (self.native_obj.AvailableFrom)
        
    @availableFrom.setter     
    def _set_availableFrom(self, value):
        self.native_obj.AvailableFrom = value
            
    # -> str            
    @property         
    def availableTo(self) -> "str":
        return (self.native_obj.AvailableTo)
        
    @availableTo.setter     
    def _set_availableTo(self, value):
        self.native_obj.AvailableTo = value
            
    # -> str            
    @property         
    def baseCalendar(self) -> "str":
        return (self.native_obj.BaseCalendar)
        
    @baseCalendar.setter     
    def _set_baseCalendar(self, value):
        self.native_obj.BaseCalendar = value
            
    # -> str            
    @property         
    def baseline10BudgetCost(self) -> "str":
        return (self.native_obj.Baseline10BudgetCost)
        
    @baseline10BudgetCost.setter     
    def _set_baseline10BudgetCost(self, value):
        self.native_obj.Baseline10BudgetCost = value
            
    # -> str            
    @property         
    def baseline10BudgetWork(self) -> "str":
        return (self.native_obj.Baseline10BudgetWork)
        
    @baseline10BudgetWork.setter     
    def _set_baseline10BudgetWork(self, value):
        self.native_obj.Baseline10BudgetWork = value
            
    # -> float            
    @property         
    def baseline10Cost(self) -> "float":
        return (self.native_obj.Baseline10Cost)
        
    @baseline10Cost.setter     
    def _set_baseline10Cost(self, value):
        self.native_obj.Baseline10Cost = value
            
    # -> float            
    @property         
    def baseline10Work(self) -> "float":
        return (self.native_obj.Baseline10Work)
        
    @baseline10Work.setter     
    def _set_baseline10Work(self, value):
        self.native_obj.Baseline10Work = value
            
    # -> str            
    @property         
    def baseline1BudgetCost(self) -> "str":
        return (self.native_obj.Baseline1BudgetCost)
        
    @baseline1BudgetCost.setter     
    def _set_baseline1BudgetCost(self, value):
        self.native_obj.Baseline1BudgetCost = value
            
    # -> str            
    @property         
    def baseline1BudgetWork(self) -> "str":
        return (self.native_obj.Baseline1BudgetWork)
        
    @baseline1BudgetWork.setter     
    def _set_baseline1BudgetWork(self, value):
        self.native_obj.Baseline1BudgetWork = value
            
    # -> float            
    @property         
    def baseline1Cost(self) -> "float":
        return (self.native_obj.Baseline1Cost)
        
    @baseline1Cost.setter     
    def _set_baseline1Cost(self, value):
        self.native_obj.Baseline1Cost = value
            
    # -> float            
    @property         
    def baseline1Work(self) -> "float":
        return (self.native_obj.Baseline1Work)
        
    @baseline1Work.setter     
    def _set_baseline1Work(self, value):
        self.native_obj.Baseline1Work = value
            
    # -> str            
    @property         
    def baseline2BudgetCost(self) -> "str":
        return (self.native_obj.Baseline2BudgetCost)
        
    @baseline2BudgetCost.setter     
    def _set_baseline2BudgetCost(self, value):
        self.native_obj.Baseline2BudgetCost = value
            
    # -> str            
    @property         
    def baseline2BudgetWork(self) -> "str":
        return (self.native_obj.Baseline2BudgetWork)
        
    @baseline2BudgetWork.setter     
    def _set_baseline2BudgetWork(self, value):
        self.native_obj.Baseline2BudgetWork = value
            
    # -> float            
    @property         
    def baseline2Cost(self) -> "float":
        return (self.native_obj.Baseline2Cost)
        
    @baseline2Cost.setter     
    def _set_baseline2Cost(self, value):
        self.native_obj.Baseline2Cost = value
            
    # -> float            
    @property         
    def baseline2Work(self) -> "float":
        return (self.native_obj.Baseline2Work)
        
    @baseline2Work.setter     
    def _set_baseline2Work(self, value):
        self.native_obj.Baseline2Work = value
            
    # -> str            
    @property         
    def baseline3BudgetCost(self) -> "str":
        return (self.native_obj.Baseline3BudgetCost)
        
    @baseline3BudgetCost.setter     
    def _set_baseline3BudgetCost(self, value):
        self.native_obj.Baseline3BudgetCost = value
            
    # -> str            
    @property         
    def baseline3BudgetWork(self) -> "str":
        return (self.native_obj.Baseline3BudgetWork)
        
    @baseline3BudgetWork.setter     
    def _set_baseline3BudgetWork(self, value):
        self.native_obj.Baseline3BudgetWork = value
            
    # -> float            
    @property         
    def baseline3Cost(self) -> "float":
        return (self.native_obj.Baseline3Cost)
        
    @baseline3Cost.setter     
    def _set_baseline3Cost(self, value):
        self.native_obj.Baseline3Cost = value
            
    # -> float            
    @property         
    def baseline3Work(self) -> "float":
        return (self.native_obj.Baseline3Work)
        
    @baseline3Work.setter     
    def _set_baseline3Work(self, value):
        self.native_obj.Baseline3Work = value
            
    # -> str            
    @property         
    def baseline4BudgetCost(self) -> "str":
        return (self.native_obj.Baseline4BudgetCost)
        
    @baseline4BudgetCost.setter     
    def _set_baseline4BudgetCost(self, value):
        self.native_obj.Baseline4BudgetCost = value
            
    # -> str            
    @property         
    def baseline4BudgetWork(self) -> "str":
        return (self.native_obj.Baseline4BudgetWork)
        
    @baseline4BudgetWork.setter     
    def _set_baseline4BudgetWork(self, value):
        self.native_obj.Baseline4BudgetWork = value
            
    # -> float            
    @property         
    def baseline4Cost(self) -> "float":
        return (self.native_obj.Baseline4Cost)
        
    @baseline4Cost.setter     
    def _set_baseline4Cost(self, value):
        self.native_obj.Baseline4Cost = value
            
    # -> float            
    @property         
    def baseline4Work(self) -> "float":
        return (self.native_obj.Baseline4Work)
        
    @baseline4Work.setter     
    def _set_baseline4Work(self, value):
        self.native_obj.Baseline4Work = value
            
    # -> str            
    @property         
    def baseline5BudgetCost(self) -> "str":
        return (self.native_obj.Baseline5BudgetCost)
        
    @baseline5BudgetCost.setter     
    def _set_baseline5BudgetCost(self, value):
        self.native_obj.Baseline5BudgetCost = value
            
    # -> str            
    @property         
    def baseline5BudgetWork(self) -> "str":
        return (self.native_obj.Baseline5BudgetWork)
        
    @baseline5BudgetWork.setter     
    def _set_baseline5BudgetWork(self, value):
        self.native_obj.Baseline5BudgetWork = value
            
    # -> float            
    @property         
    def baseline5Cost(self) -> "float":
        return (self.native_obj.Baseline5Cost)
        
    @baseline5Cost.setter     
    def _set_baseline5Cost(self, value):
        self.native_obj.Baseline5Cost = value
            
    # -> float            
    @property         
    def baseline5Work(self) -> "float":
        return (self.native_obj.Baseline5Work)
        
    @baseline5Work.setter     
    def _set_baseline5Work(self, value):
        self.native_obj.Baseline5Work = value
            
    # -> str            
    @property         
    def baseline6BudgetCost(self) -> "str":
        return (self.native_obj.Baseline6BudgetCost)
        
    @baseline6BudgetCost.setter     
    def _set_baseline6BudgetCost(self, value):
        self.native_obj.Baseline6BudgetCost = value
            
    # -> str            
    @property         
    def baseline6BudgetWork(self) -> "str":
        return (self.native_obj.Baseline6BudgetWork)
        
    @baseline6BudgetWork.setter     
    def _set_baseline6BudgetWork(self, value):
        self.native_obj.Baseline6BudgetWork = value
            
    # -> float            
    @property         
    def baseline6Cost(self) -> "float":
        return (self.native_obj.Baseline6Cost)
        
    @baseline6Cost.setter     
    def _set_baseline6Cost(self, value):
        self.native_obj.Baseline6Cost = value
            
    # -> float            
    @property         
    def baseline6Work(self) -> "float":
        return (self.native_obj.Baseline6Work)
        
    @baseline6Work.setter     
    def _set_baseline6Work(self, value):
        self.native_obj.Baseline6Work = value
            
    # -> str            
    @property         
    def baseline7BudgetCost(self) -> "str":
        return (self.native_obj.Baseline7BudgetCost)
        
    @baseline7BudgetCost.setter     
    def _set_baseline7BudgetCost(self, value):
        self.native_obj.Baseline7BudgetCost = value
            
    # -> str            
    @property         
    def baseline7BudgetWork(self) -> "str":
        return (self.native_obj.Baseline7BudgetWork)
        
    @baseline7BudgetWork.setter     
    def _set_baseline7BudgetWork(self, value):
        self.native_obj.Baseline7BudgetWork = value
            
    # -> float            
    @property         
    def baseline7Cost(self) -> "float":
        return (self.native_obj.Baseline7Cost)
        
    @baseline7Cost.setter     
    def _set_baseline7Cost(self, value):
        self.native_obj.Baseline7Cost = value
            
    # -> float            
    @property         
    def baseline7Work(self) -> "float":
        return (self.native_obj.Baseline7Work)
        
    @baseline7Work.setter     
    def _set_baseline7Work(self, value):
        self.native_obj.Baseline7Work = value
            
    # -> str            
    @property         
    def baseline8BudgetCost(self) -> "str":
        return (self.native_obj.Baseline8BudgetCost)
        
    @baseline8BudgetCost.setter     
    def _set_baseline8BudgetCost(self, value):
        self.native_obj.Baseline8BudgetCost = value
            
    # -> str            
    @property         
    def baseline8BudgetWork(self) -> "str":
        return (self.native_obj.Baseline8BudgetWork)
        
    @baseline8BudgetWork.setter     
    def _set_baseline8BudgetWork(self, value):
        self.native_obj.Baseline8BudgetWork = value
            
    # -> float            
    @property         
    def baseline8Cost(self) -> "float":
        return (self.native_obj.Baseline8Cost)
        
    @baseline8Cost.setter     
    def _set_baseline8Cost(self, value):
        self.native_obj.Baseline8Cost = value
            
    # -> float            
    @property         
    def baseline8Work(self) -> "float":
        return (self.native_obj.Baseline8Work)
        
    @baseline8Work.setter     
    def _set_baseline8Work(self, value):
        self.native_obj.Baseline8Work = value
            
    # -> str            
    @property         
    def baseline9BudgetCost(self) -> "str":
        return (self.native_obj.Baseline9BudgetCost)
        
    @baseline9BudgetCost.setter     
    def _set_baseline9BudgetCost(self, value):
        self.native_obj.Baseline9BudgetCost = value
            
    # -> str            
    @property         
    def baseline9BudgetWork(self) -> "str":
        return (self.native_obj.Baseline9BudgetWork)
        
    @baseline9BudgetWork.setter     
    def _set_baseline9BudgetWork(self, value):
        self.native_obj.Baseline9BudgetWork = value
            
    # -> float            
    @property         
    def baseline9Cost(self) -> "float":
        return (self.native_obj.Baseline9Cost)
        
    @baseline9Cost.setter     
    def _set_baseline9Cost(self, value):
        self.native_obj.Baseline9Cost = value
            
    # -> float            
    @property         
    def baseline9Work(self) -> "float":
        return (self.native_obj.Baseline9Work)
        
    @baseline9Work.setter     
    def _set_baseline9Work(self, value):
        self.native_obj.Baseline9Work = value
            
    # -> str            
    @property         
    def baselineBudgetCost(self) -> "str":
        return (self.native_obj.BaselineBudgetCost)
        
    @baselineBudgetCost.setter     
    def _set_baselineBudgetCost(self, value):
        self.native_obj.BaselineBudgetCost = value
            
    # -> str            
    @property         
    def baselineBudgetWork(self) -> "str":
        return (self.native_obj.BaselineBudgetWork)
        
    @baselineBudgetWork.setter     
    def _set_baselineBudgetWork(self, value):
        self.native_obj.BaselineBudgetWork = value
            
    # -> float            
    @property         
    def baselineCost(self) -> "float":
        return (self.native_obj.BaselineCost)
        
    @baselineCost.setter     
    def _set_baselineCost(self, value):
        self.native_obj.BaselineCost = value
            
    # -> float            
    @property         
    def baselineWork(self) -> "float":
        return (self.native_obj.BaselineWork)
        
    @baselineWork.setter     
    def _set_baselineWork(self, value):
        self.native_obj.BaselineWork = value
            
    # -> float            
    @property         
    def bCWP(self) -> "float":
        return (self.native_obj.BCWP)
        
    @bCWP.setter     
    def _set_bCWP(self, value):
        self.native_obj.BCWP = value
            
    # -> float            
    @property         
    def bCWS(self) -> "float":
        return (self.native_obj.BCWS)
        
    @bCWS.setter     
    def _set_bCWS(self, value):
        self.native_obj.BCWS = value
            
    # -> int            
    @property         
    def bookingType(self) -> "int":
        return (self.native_obj.BookingType)
        
    @bookingType.setter     
    def _set_bookingType(self, value):
        self.native_obj.BookingType = value
            
    # -> bool            
    @property         
    def budget(self) -> "bool":
        return (self.native_obj.Budget)
        
    @budget.setter     
    def _set_budget(self, value):
        self.native_obj.Budget = value
            
    # -> str            
    @property         
    def budgetCost(self) -> "str":
        return (self.native_obj.BudgetCost)
        
    @budgetCost.setter     
    def _set_budgetCost(self, value):
        self.native_obj.BudgetCost = value
            
    # -> str            
    @property         
    def budgetWork(self) -> "str":
        return (self.native_obj.BudgetWork)
        
    @budgetWork.setter     
    def _set_budgetWork(self, value):
        self.native_obj.BudgetWork = value
            
    # -> Calendar            
    @property         
    def calendar(self) -> "Calendar":
        return Calendar(self.native_obj.Calendar)
        
    @calendar.setter     
    def _set_calendar(self, value):
        self.native_obj.Calendar = value
            
    # -> str            
    @property         
    def calendarGuid(self) -> "str":
        return (self.native_obj.CalendarGuid)
        
    @calendarGuid.setter     
    def _set_calendarGuid(self, value):
        self.native_obj.CalendarGuid = value
            
    # -> bool            
    @property         
    def canLevel(self) -> "bool":
        return (self.native_obj.CanLevel)
        
    @canLevel.setter     
    def _set_canLevel(self, value):
        self.native_obj.CanLevel = value
            
    # -> str            
    @property         
    def code(self) -> "str":
        return (self.native_obj.Code)
        
    @code.setter     
    def _set_code(self, value):
        self.native_obj.Code = value
            
    # -> bool            
    @property         
    def compliant(self) -> "bool":
        return (self.native_obj.Compliant)
        
    @compliant.setter     
    def _set_compliant(self, value):
        self.native_obj.Compliant = value
            
    # -> bool            
    @property         
    def confirmed(self) -> "bool":
        return (self.native_obj.Confirmed)
        
    @confirmed.setter     
    def _set_confirmed(self, value):
        self.native_obj.Confirmed = value
            
    # -> float            
    @property         
    def cost(self) -> "float":
        return (self.native_obj.Cost)
        
    @cost.setter     
    def _set_cost(self, value):
        self.native_obj.Cost = value
            
    # -> float            
    @property         
    def cost1(self) -> "float":
        return (self.native_obj.Cost1)
        
    @cost1.setter     
    def _set_cost1(self, value):
        self.native_obj.Cost1 = value
            
    # -> float            
    @property         
    def cost10(self) -> "float":
        return (self.native_obj.Cost10)
        
    @cost10.setter     
    def _set_cost10(self, value):
        self.native_obj.Cost10 = value
            
    # -> float            
    @property         
    def cost2(self) -> "float":
        return (self.native_obj.Cost2)
        
    @cost2.setter     
    def _set_cost2(self, value):
        self.native_obj.Cost2 = value
            
    # -> float            
    @property         
    def cost3(self) -> "float":
        return (self.native_obj.Cost3)
        
    @cost3.setter     
    def _set_cost3(self, value):
        self.native_obj.Cost3 = value
            
    # -> float            
    @property         
    def cost4(self) -> "float":
        return (self.native_obj.Cost4)
        
    @cost4.setter     
    def _set_cost4(self, value):
        self.native_obj.Cost4 = value
            
    # -> float            
    @property         
    def cost5(self) -> "float":
        return (self.native_obj.Cost5)
        
    @cost5.setter     
    def _set_cost5(self, value):
        self.native_obj.Cost5 = value
            
    # -> float            
    @property         
    def cost6(self) -> "float":
        return (self.native_obj.Cost6)
        
    @cost6.setter     
    def _set_cost6(self, value):
        self.native_obj.Cost6 = value
            
    # -> float            
    @property         
    def cost7(self) -> "float":
        return (self.native_obj.Cost7)
        
    @cost7.setter     
    def _set_cost7(self, value):
        self.native_obj.Cost7 = value
            
    # -> float            
    @property         
    def cost8(self) -> "float":
        return (self.native_obj.Cost8)
        
    @cost8.setter     
    def _set_cost8(self, value):
        self.native_obj.Cost8 = value
            
    # -> float            
    @property         
    def cost9(self) -> "float":
        return (self.native_obj.Cost9)
        
    @cost9.setter     
    def _set_cost9(self, value):
        self.native_obj.Cost9 = value
            
    # -> str            
    @property         
    def costCenter(self) -> "str":
        return (self.native_obj.CostCenter)
        
    @costCenter.setter     
    def _set_costCenter(self, value):
        self.native_obj.CostCenter = value
            
    # -> float            
    @property         
    def costPerUse(self) -> "float":
        return (self.native_obj.CostPerUse)
        
    @costPerUse.setter     
    def _set_costPerUse(self, value):
        self.native_obj.CostPerUse = value
            
    # -> CostRateTables            
    @property         
    def costRateTables(self) -> "CostRateTables":
        return CostRateTables(self.native_obj.CostRateTables)
        
    @costRateTables.setter     
    def _set_costRateTables(self, value):
        self.native_obj.CostRateTables = value
            
    # -> float            
    @property         
    def costVariance(self) -> "float":
        return (self.native_obj.CostVariance)
        
    @costVariance.setter     
    def _set_costVariance(self, value):
        self.native_obj.CostVariance = value
            
    # -> pywintypes.datetime            
    @property         
    def created(self) -> "Any":
        return (self.native_obj.Created)
        
    @created.setter     
    def _set_created(self, value):
        self.native_obj.Created = value
            
    # -> float            
    @property         
    def cV(self) -> "float":
        return (self.native_obj.CV)
        
    @cV.setter     
    def _set_cV(self, value):
        self.native_obj.CV = value
            
    # -> str            
    @property         
    def date1(self) -> "str":
        return (self.native_obj.Date1)
        
    @date1.setter     
    def _set_date1(self, value):
        self.native_obj.Date1 = value
            
    # -> str            
    @property         
    def date10(self) -> "str":
        return (self.native_obj.Date10)
        
    @date10.setter     
    def _set_date10(self, value):
        self.native_obj.Date10 = value
            
    # -> str            
    @property         
    def date2(self) -> "str":
        return (self.native_obj.Date2)
        
    @date2.setter     
    def _set_date2(self, value):
        self.native_obj.Date2 = value
            
    # -> str            
    @property         
    def date3(self) -> "str":
        return (self.native_obj.Date3)
        
    @date3.setter     
    def _set_date3(self, value):
        self.native_obj.Date3 = value
            
    # -> str            
    @property         
    def date4(self) -> "str":
        return (self.native_obj.Date4)
        
    @date4.setter     
    def _set_date4(self, value):
        self.native_obj.Date4 = value
            
    # -> str            
    @property         
    def date5(self) -> "str":
        return (self.native_obj.Date5)
        
    @date5.setter     
    def _set_date5(self, value):
        self.native_obj.Date5 = value
            
    # -> str            
    @property         
    def date6(self) -> "str":
        return (self.native_obj.Date6)
        
    @date6.setter     
    def _set_date6(self, value):
        self.native_obj.Date6 = value
            
    # -> str            
    @property         
    def date7(self) -> "str":
        return (self.native_obj.Date7)
        
    @date7.setter     
    def _set_date7(self, value):
        self.native_obj.Date7 = value
            
    # -> str            
    @property         
    def date8(self) -> "str":
        return (self.native_obj.Date8)
        
    @date8.setter     
    def _set_date8(self, value):
        self.native_obj.Date8 = value
            
    # -> str            
    @property         
    def date9(self) -> "str":
        return (self.native_obj.Date9)
        
    @date9.setter     
    def _set_date9(self, value):
        self.native_obj.Date9 = value
            
    # -> str            
    @property         
    def defaultAssignmentOwner(self) -> "str":
        return (self.native_obj.DefaultAssignmentOwner)
        
    @defaultAssignmentOwner.setter     
    def _set_defaultAssignmentOwner(self, value):
        self.native_obj.DefaultAssignmentOwner = value
            
    # -> int            
    @property         
    def duration1(self) -> "int":
        return (self.native_obj.Duration1)
        
    @duration1.setter     
    def _set_duration1(self, value):
        self.native_obj.Duration1 = value
            
    # -> int            
    @property         
    def duration10(self) -> "int":
        return (self.native_obj.Duration10)
        
    @duration10.setter     
    def _set_duration10(self, value):
        self.native_obj.Duration10 = value
            
    # -> int            
    @property         
    def duration2(self) -> "int":
        return (self.native_obj.Duration2)
        
    @duration2.setter     
    def _set_duration2(self, value):
        self.native_obj.Duration2 = value
            
    # -> int            
    @property         
    def duration3(self) -> "int":
        return (self.native_obj.Duration3)
        
    @duration3.setter     
    def _set_duration3(self, value):
        self.native_obj.Duration3 = value
            
    # -> int            
    @property         
    def duration4(self) -> "int":
        return (self.native_obj.Duration4)
        
    @duration4.setter     
    def _set_duration4(self, value):
        self.native_obj.Duration4 = value
            
    # -> int            
    @property         
    def duration5(self) -> "int":
        return (self.native_obj.Duration5)
        
    @duration5.setter     
    def _set_duration5(self, value):
        self.native_obj.Duration5 = value
            
    # -> int            
    @property         
    def duration6(self) -> "int":
        return (self.native_obj.Duration6)
        
    @duration6.setter     
    def _set_duration6(self, value):
        self.native_obj.Duration6 = value
            
    # -> int            
    @property         
    def duration7(self) -> "int":
        return (self.native_obj.Duration7)
        
    @duration7.setter     
    def _set_duration7(self, value):
        self.native_obj.Duration7 = value
            
    # -> int            
    @property         
    def duration8(self) -> "int":
        return (self.native_obj.Duration8)
        
    @duration8.setter     
    def _set_duration8(self, value):
        self.native_obj.Duration8 = value
            
    # -> int            
    @property         
    def duration9(self) -> "int":
        return (self.native_obj.Duration9)
        
    @duration9.setter     
    def _set_duration9(self, value):
        self.native_obj.Duration9 = value
            
    # -> str            
    @property         
    def eMailAddress(self) -> "str":
        return (self.native_obj.EMailAddress)
        
    @eMailAddress.setter     
    def _set_eMailAddress(self, value):
        self.native_obj.EMailAddress = value
            
    # -> str            
    @property         
    def engagementCommittedFinish(self) -> "str":
        return (self.native_obj.EngagementCommittedFinish)
        
    @engagementCommittedFinish.setter     
    def _set_engagementCommittedFinish(self, value):
        self.native_obj.EngagementCommittedFinish = value
            
    # -> str            
    @property         
    def engagementCommittedMaxUnits(self) -> "str":
        return (self.native_obj.EngagementCommittedMaxUnits)
        
    @engagementCommittedMaxUnits.setter     
    def _set_engagementCommittedMaxUnits(self, value):
        self.native_obj.EngagementCommittedMaxUnits = value
            
    # -> str            
    @property         
    def engagementCommittedStart(self) -> "str":
        return (self.native_obj.EngagementCommittedStart)
        
    @engagementCommittedStart.setter     
    def _set_engagementCommittedStart(self, value):
        self.native_obj.EngagementCommittedStart = value
            
    # -> str            
    @property         
    def engagementCommittedWork(self) -> "str":
        return (self.native_obj.EngagementCommittedWork)
        
    @engagementCommittedWork.setter     
    def _set_engagementCommittedWork(self, value):
        self.native_obj.EngagementCommittedWork = value
            
    # -> str            
    @property         
    def engagementDraftFinish(self) -> "str":
        return (self.native_obj.EngagementDraftFinish)
        
    @engagementDraftFinish.setter     
    def _set_engagementDraftFinish(self, value):
        self.native_obj.EngagementDraftFinish = value
            
    # -> str            
    @property         
    def engagementDraftMaxUnits(self) -> "str":
        return (self.native_obj.EngagementDraftMaxUnits)
        
    @engagementDraftMaxUnits.setter     
    def _set_engagementDraftMaxUnits(self, value):
        self.native_obj.EngagementDraftMaxUnits = value
            
    # -> str            
    @property         
    def engagementDraftStart(self) -> "str":
        return (self.native_obj.EngagementDraftStart)
        
    @engagementDraftStart.setter     
    def _set_engagementDraftStart(self, value):
        self.native_obj.EngagementDraftStart = value
            
    # -> str            
    @property         
    def engagementDraftWork(self) -> "str":
        return (self.native_obj.EngagementDraftWork)
        
    @engagementDraftWork.setter     
    def _set_engagementDraftWork(self, value):
        self.native_obj.EngagementDraftWork = value
            
    # -> str            
    @property         
    def engagementProposedFinish(self) -> "str":
        return (self.native_obj.EngagementProposedFinish)
        
    @engagementProposedFinish.setter     
    def _set_engagementProposedFinish(self, value):
        self.native_obj.EngagementProposedFinish = value
            
    # -> str            
    @property         
    def engagementProposedMaxUnits(self) -> "str":
        return (self.native_obj.EngagementProposedMaxUnits)
        
    @engagementProposedMaxUnits.setter     
    def _set_engagementProposedMaxUnits(self, value):
        self.native_obj.EngagementProposedMaxUnits = value
            
    # -> str            
    @property         
    def engagementProposedStart(self) -> "str":
        return (self.native_obj.EngagementProposedStart)
        
    @engagementProposedStart.setter     
    def _set_engagementProposedStart(self, value):
        self.native_obj.EngagementProposedStart = value
            
    # -> str            
    @property         
    def engagementProposedWork(self) -> "str":
        return (self.native_obj.EngagementProposedWork)
        
    @engagementProposedWork.setter     
    def _set_engagementProposedWork(self, value):
        self.native_obj.EngagementProposedWork = value
            
    # -> bool            
    @property         
    def enterprise(self) -> "bool":
        return (self.native_obj.Enterprise)
        
    @enterprise.setter     
    def _set_enterprise(self, value):
        self.native_obj.Enterprise = value
            
    # -> bool            
    @property         
    def enterpriseBaseCalendar(self) -> "bool":
        return (self.native_obj.EnterpriseBaseCalendar)
        
    @enterpriseBaseCalendar.setter     
    def _set_enterpriseBaseCalendar(self, value):
        self.native_obj.EnterpriseBaseCalendar = value
            
    # -> str            
    @property         
    def enterpriseCheckedOutBy(self) -> "str":
        return (self.native_obj.EnterpriseCheckedOutBy)
        
    @enterpriseCheckedOutBy.setter     
    def _set_enterpriseCheckedOutBy(self, value):
        self.native_obj.EnterpriseCheckedOutBy = value
            
    # -> bool            
    @property         
    def enterpriseGeneric(self) -> "bool":
        return (self.native_obj.EnterpriseGeneric)
        
    @enterpriseGeneric.setter     
    def _set_enterpriseGeneric(self, value):
        self.native_obj.EnterpriseGeneric = value
            
    # -> bool            
    @property         
    def enterpriseInactive(self) -> "bool":
        return (self.native_obj.EnterpriseInactive)
        
    @enterpriseInactive.setter     
    def _set_enterpriseInactive(self, value):
        self.native_obj.EnterpriseInactive = value
            
    # -> bool            
    @property         
    def enterpriseIsCheckedOut(self) -> "bool":
        return (self.native_obj.EnterpriseIsCheckedOut)
        
    @enterpriseIsCheckedOut.setter     
    def _set_enterpriseIsCheckedOut(self, value):
        self.native_obj.EnterpriseIsCheckedOut = value
            
    # -> str            
    @property         
    def enterpriseLastModifiedDate(self) -> "str":
        return (self.native_obj.EnterpriseLastModifiedDate)
        
    @enterpriseLastModifiedDate.setter     
    def _set_enterpriseLastModifiedDate(self, value):
        self.native_obj.EnterpriseLastModifiedDate = value
            
    # -> bool            
    @property         
    def enterpriseNameUsed(self) -> "bool":
        return (self.native_obj.EnterpriseNameUsed)
        
    @enterpriseNameUsed.setter     
    def _set_enterpriseNameUsed(self, value):
        self.native_obj.EnterpriseNameUsed = value
            
    # -> bool            
    @property         
    def enterpriseRequiredValues(self) -> "bool":
        return (self.native_obj.EnterpriseRequiredValues)
        
    @enterpriseRequiredValues.setter     
    def _set_enterpriseRequiredValues(self, value):
        self.native_obj.EnterpriseRequiredValues = value
            
    # -> int            
    @property         
    def enterpriseUniqueID(self) -> "int":
        return (self.native_obj.EnterpriseUniqueID)
        
    @enterpriseUniqueID.setter     
    def _set_enterpriseUniqueID(self, value):
        self.native_obj.EnterpriseUniqueID = value
            
    # -> str            
    @property         
    def errorMessage(self) -> "str":
        return (self.native_obj.ErrorMessage)
        
    @errorMessage.setter     
    def _set_errorMessage(self, value):
        self.native_obj.ErrorMessage = value
            
    # -> str            
    @property         
    def finish1(self) -> "str":
        return (self.native_obj.Finish1)
        
    @finish1.setter     
    def _set_finish1(self, value):
        self.native_obj.Finish1 = value
            
    # -> str            
    @property         
    def finish10(self) -> "str":
        return (self.native_obj.Finish10)
        
    @finish10.setter     
    def _set_finish10(self, value):
        self.native_obj.Finish10 = value
            
    # -> str            
    @property         
    def finish2(self) -> "str":
        return (self.native_obj.Finish2)
        
    @finish2.setter     
    def _set_finish2(self, value):
        self.native_obj.Finish2 = value
            
    # -> str            
    @property         
    def finish3(self) -> "str":
        return (self.native_obj.Finish3)
        
    @finish3.setter     
    def _set_finish3(self, value):
        self.native_obj.Finish3 = value
            
    # -> str            
    @property         
    def finish4(self) -> "str":
        return (self.native_obj.Finish4)
        
    @finish4.setter     
    def _set_finish4(self, value):
        self.native_obj.Finish4 = value
            
    # -> str            
    @property         
    def finish5(self) -> "str":
        return (self.native_obj.Finish5)
        
    @finish5.setter     
    def _set_finish5(self, value):
        self.native_obj.Finish5 = value
            
    # -> str            
    @property         
    def finish6(self) -> "str":
        return (self.native_obj.Finish6)
        
    @finish6.setter     
    def _set_finish6(self, value):
        self.native_obj.Finish6 = value
            
    # -> str            
    @property         
    def finish7(self) -> "str":
        return (self.native_obj.Finish7)
        
    @finish7.setter     
    def _set_finish7(self, value):
        self.native_obj.Finish7 = value
            
    # -> str            
    @property         
    def finish8(self) -> "str":
        return (self.native_obj.Finish8)
        
    @finish8.setter     
    def _set_finish8(self, value):
        self.native_obj.Finish8 = value
            
    # -> str            
    @property         
    def finish9(self) -> "str":
        return (self.native_obj.Finish9)
        
    @finish9.setter     
    def _set_finish9(self, value):
        self.native_obj.Finish9 = value
            
    # -> bool            
    @property         
    def flag1(self) -> "bool":
        return (self.native_obj.Flag1)
        
    @flag1.setter     
    def _set_flag1(self, value):
        self.native_obj.Flag1 = value
            
    # -> bool            
    @property         
    def flag10(self) -> "bool":
        return (self.native_obj.Flag10)
        
    @flag10.setter     
    def _set_flag10(self, value):
        self.native_obj.Flag10 = value
            
    # -> bool            
    @property         
    def flag11(self) -> "bool":
        return (self.native_obj.Flag11)
        
    @flag11.setter     
    def _set_flag11(self, value):
        self.native_obj.Flag11 = value
            
    # -> bool            
    @property         
    def flag12(self) -> "bool":
        return (self.native_obj.Flag12)
        
    @flag12.setter     
    def _set_flag12(self, value):
        self.native_obj.Flag12 = value
            
    # -> bool            
    @property         
    def flag13(self) -> "bool":
        return (self.native_obj.Flag13)
        
    @flag13.setter     
    def _set_flag13(self, value):
        self.native_obj.Flag13 = value
            
    # -> bool            
    @property         
    def flag14(self) -> "bool":
        return (self.native_obj.Flag14)
        
    @flag14.setter     
    def _set_flag14(self, value):
        self.native_obj.Flag14 = value
            
    # -> bool            
    @property         
    def flag15(self) -> "bool":
        return (self.native_obj.Flag15)
        
    @flag15.setter     
    def _set_flag15(self, value):
        self.native_obj.Flag15 = value
            
    # -> bool            
    @property         
    def flag16(self) -> "bool":
        return (self.native_obj.Flag16)
        
    @flag16.setter     
    def _set_flag16(self, value):
        self.native_obj.Flag16 = value
            
    # -> bool            
    @property         
    def flag17(self) -> "bool":
        return (self.native_obj.Flag17)
        
    @flag17.setter     
    def _set_flag17(self, value):
        self.native_obj.Flag17 = value
            
    # -> bool            
    @property         
    def flag18(self) -> "bool":
        return (self.native_obj.Flag18)
        
    @flag18.setter     
    def _set_flag18(self, value):
        self.native_obj.Flag18 = value
            
    # -> bool            
    @property         
    def flag19(self) -> "bool":
        return (self.native_obj.Flag19)
        
    @flag19.setter     
    def _set_flag19(self, value):
        self.native_obj.Flag19 = value
            
    # -> bool            
    @property         
    def flag2(self) -> "bool":
        return (self.native_obj.Flag2)
        
    @flag2.setter     
    def _set_flag2(self, value):
        self.native_obj.Flag2 = value
            
    # -> bool            
    @property         
    def flag20(self) -> "bool":
        return (self.native_obj.Flag20)
        
    @flag20.setter     
    def _set_flag20(self, value):
        self.native_obj.Flag20 = value
            
    # -> bool            
    @property         
    def flag3(self) -> "bool":
        return (self.native_obj.Flag3)
        
    @flag3.setter     
    def _set_flag3(self, value):
        self.native_obj.Flag3 = value
            
    # -> bool            
    @property         
    def flag4(self) -> "bool":
        return (self.native_obj.Flag4)
        
    @flag4.setter     
    def _set_flag4(self, value):
        self.native_obj.Flag4 = value
            
    # -> bool            
    @property         
    def flag5(self) -> "bool":
        return (self.native_obj.Flag5)
        
    @flag5.setter     
    def _set_flag5(self, value):
        self.native_obj.Flag5 = value
            
    # -> bool            
    @property         
    def flag6(self) -> "bool":
        return (self.native_obj.Flag6)
        
    @flag6.setter     
    def _set_flag6(self, value):
        self.native_obj.Flag6 = value
            
    # -> bool            
    @property         
    def flag7(self) -> "bool":
        return (self.native_obj.Flag7)
        
    @flag7.setter     
    def _set_flag7(self, value):
        self.native_obj.Flag7 = value
            
    # -> bool            
    @property         
    def flag8(self) -> "bool":
        return (self.native_obj.Flag8)
        
    @flag8.setter     
    def _set_flag8(self, value):
        self.native_obj.Flag8 = value
            
    # -> bool            
    @property         
    def flag9(self) -> "bool":
        return (self.native_obj.Flag9)
        
    @flag9.setter     
    def _set_flag9(self, value):
        self.native_obj.Flag9 = value
            
    # -> str            
    @property         
    def group(self) -> "str":
        return (self.native_obj.Group)
        
    @group.setter     
    def _set_group(self, value):
        self.native_obj.Group = value
            
    # -> bool            
    @property         
    def groupBySummary(self) -> "bool":
        return (self.native_obj.GroupBySummary)
        
    @groupBySummary.setter     
    def _set_groupBySummary(self, value):
        self.native_obj.GroupBySummary = value
            
    # -> str            
    @property         
    def guid(self) -> "str":
        return (self.native_obj.Guid)
        
    @guid.setter     
    def _set_guid(self, value):
        self.native_obj.Guid = value
            
    # -> str            
    @property         
    def hyperlink(self) -> "str":
        return (self.native_obj.Hyperlink)
        
    @hyperlink.setter     
    def _set_hyperlink(self, value):
        self.native_obj.Hyperlink = value
            
    # -> str            
    @property         
    def hyperlinkAddress(self) -> "str":
        return (self.native_obj.HyperlinkAddress)
        
    @hyperlinkAddress.setter     
    def _set_hyperlinkAddress(self, value):
        self.native_obj.HyperlinkAddress = value
            
    # -> str            
    @property         
    def hyperlinkHREF(self) -> "str":
        return (self.native_obj.HyperlinkHREF)
        
    @hyperlinkHREF.setter     
    def _set_hyperlinkHREF(self, value):
        self.native_obj.HyperlinkHREF = value
            
    # -> str            
    @property         
    def hyperlinkScreenTip(self) -> "str":
        return (self.native_obj.HyperlinkScreenTip)
        
    @hyperlinkScreenTip.setter     
    def _set_hyperlinkScreenTip(self, value):
        self.native_obj.HyperlinkScreenTip = value
            
    # -> str            
    @property         
    def hyperlinkSubAddress(self) -> "str":
        return (self.native_obj.HyperlinkSubAddress)
        
    @hyperlinkSubAddress.setter     
    def _set_hyperlinkSubAddress(self, value):
        self.native_obj.HyperlinkSubAddress = value
            
    # -> int            
    @property         
    def iD(self) -> "int":
        return (self.native_obj.ID)
        
    @iD.setter     
    def _set_iD(self, value):
        self.native_obj.ID = value
            
    # -> bool            
    @property         
    def import_(self) -> "bool":
        return (self.native_obj.Import)
        
    @import_.setter     
    def _set_import_(self, value):
        self.native_obj.Import = value
            
    # -> int            
    @property         
    def index(self) -> "int":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> str            
    @property         
    def initials(self) -> "str":
        return (self.native_obj.Initials)
        
    @initials.setter     
    def _set_initials(self, value):
        self.native_obj.Initials = value
            
    # -> bool            
    @property         
    def isLocked(self) -> "bool":
        return (self.native_obj.IsLocked)
        
    @isLocked.setter     
    def _set_isLocked(self, value):
        self.native_obj.IsLocked = value
            
    # -> bool            
    @property         
    def isTeam(self) -> "bool":
        return (self.native_obj.IsTeam)
        
    @isTeam.setter     
    def _set_isTeam(self, value):
        self.native_obj.IsTeam = value
            
    # -> bool            
    @property         
    def linkedFields(self) -> "bool":
        return (self.native_obj.LinkedFields)
        
    @linkedFields.setter     
    def _set_linkedFields(self, value):
        self.native_obj.LinkedFields = value
            
    # -> str            
    @property         
    def materialLabel(self) -> "str":
        return (self.native_obj.MaterialLabel)
        
    @materialLabel.setter     
    def _set_materialLabel(self, value):
        self.native_obj.MaterialLabel = value
            
    # -> float            
    @property         
    def maxUnits(self) -> "float":
        return (self.native_obj.MaxUnits)
        
    @maxUnits.setter     
    def _set_maxUnits(self, value):
        self.native_obj.MaxUnits = value
            
    # -> str            
    @property         
    def name(self) -> "str":
        return (self.native_obj.Name)
        
    @name.setter     
    def _set_name(self, value):
        self.native_obj.Name = value
            
    # -> str            
    @property         
    def notes(self) -> "str":
        return (self.native_obj.Notes)
        
    @notes.setter     
    def _set_notes(self, value):
        self.native_obj.Notes = value
            
    # -> float            
    @property         
    def number1(self) -> "float":
        return (self.native_obj.Number1)
        
    @number1.setter     
    def _set_number1(self, value):
        self.native_obj.Number1 = value
            
    # -> float            
    @property         
    def number10(self) -> "float":
        return (self.native_obj.Number10)
        
    @number10.setter     
    def _set_number10(self, value):
        self.native_obj.Number10 = value
            
    # -> float            
    @property         
    def number11(self) -> "float":
        return (self.native_obj.Number11)
        
    @number11.setter     
    def _set_number11(self, value):
        self.native_obj.Number11 = value
            
    # -> float            
    @property         
    def number12(self) -> "float":
        return (self.native_obj.Number12)
        
    @number12.setter     
    def _set_number12(self, value):
        self.native_obj.Number12 = value
            
    # -> float            
    @property         
    def number13(self) -> "float":
        return (self.native_obj.Number13)
        
    @number13.setter     
    def _set_number13(self, value):
        self.native_obj.Number13 = value
            
    # -> float            
    @property         
    def number14(self) -> "float":
        return (self.native_obj.Number14)
        
    @number14.setter     
    def _set_number14(self, value):
        self.native_obj.Number14 = value
            
    # -> float            
    @property         
    def number15(self) -> "float":
        return (self.native_obj.Number15)
        
    @number15.setter     
    def _set_number15(self, value):
        self.native_obj.Number15 = value
            
    # -> float            
    @property         
    def number16(self) -> "float":
        return (self.native_obj.Number16)
        
    @number16.setter     
    def _set_number16(self, value):
        self.native_obj.Number16 = value
            
    # -> float            
    @property         
    def number17(self) -> "float":
        return (self.native_obj.Number17)
        
    @number17.setter     
    def _set_number17(self, value):
        self.native_obj.Number17 = value
            
    # -> float            
    @property         
    def number18(self) -> "float":
        return (self.native_obj.Number18)
        
    @number18.setter     
    def _set_number18(self, value):
        self.native_obj.Number18 = value
            
    # -> float            
    @property         
    def number19(self) -> "float":
        return (self.native_obj.Number19)
        
    @number19.setter     
    def _set_number19(self, value):
        self.native_obj.Number19 = value
            
    # -> float            
    @property         
    def number2(self) -> "float":
        return (self.native_obj.Number2)
        
    @number2.setter     
    def _set_number2(self, value):
        self.native_obj.Number2 = value
            
    # -> float            
    @property         
    def number20(self) -> "float":
        return (self.native_obj.Number20)
        
    @number20.setter     
    def _set_number20(self, value):
        self.native_obj.Number20 = value
            
    # -> float            
    @property         
    def number3(self) -> "float":
        return (self.native_obj.Number3)
        
    @number3.setter     
    def _set_number3(self, value):
        self.native_obj.Number3 = value
            
    # -> float            
    @property         
    def number4(self) -> "float":
        return (self.native_obj.Number4)
        
    @number4.setter     
    def _set_number4(self, value):
        self.native_obj.Number4 = value
            
    # -> float            
    @property         
    def number5(self) -> "float":
        return (self.native_obj.Number5)
        
    @number5.setter     
    def _set_number5(self, value):
        self.native_obj.Number5 = value
            
    # -> float            
    @property         
    def number6(self) -> "float":
        return (self.native_obj.Number6)
        
    @number6.setter     
    def _set_number6(self, value):
        self.native_obj.Number6 = value
            
    # -> float            
    @property         
    def number7(self) -> "float":
        return (self.native_obj.Number7)
        
    @number7.setter     
    def _set_number7(self, value):
        self.native_obj.Number7 = value
            
    # -> float            
    @property         
    def number8(self) -> "float":
        return (self.native_obj.Number8)
        
    @number8.setter     
    def _set_number8(self, value):
        self.native_obj.Number8 = value
            
    # -> float            
    @property         
    def number9(self) -> "float":
        return (self.native_obj.Number9)
        
    @number9.setter     
    def _set_number9(self, value):
        self.native_obj.Number9 = value
            
    # -> int            
    @property         
    def objects(self) -> "int":
        return (self.native_obj.Objects)
        
    @objects.setter     
    def _set_objects(self, value):
        self.native_obj.Objects = value
            
    # -> str            
    @property         
    def outlineCode1(self) -> "str":
        return (self.native_obj.OutlineCode1)
        
    @outlineCode1.setter     
    def _set_outlineCode1(self, value):
        self.native_obj.OutlineCode1 = value
            
    # -> str            
    @property         
    def outlineCode10(self) -> "str":
        return (self.native_obj.OutlineCode10)
        
    @outlineCode10.setter     
    def _set_outlineCode10(self, value):
        self.native_obj.OutlineCode10 = value
            
    # -> str            
    @property         
    def outlineCode2(self) -> "str":
        return (self.native_obj.OutlineCode2)
        
    @outlineCode2.setter     
    def _set_outlineCode2(self, value):
        self.native_obj.OutlineCode2 = value
            
    # -> str            
    @property         
    def outlineCode3(self) -> "str":
        return (self.native_obj.OutlineCode3)
        
    @outlineCode3.setter     
    def _set_outlineCode3(self, value):
        self.native_obj.OutlineCode3 = value
            
    # -> str            
    @property         
    def outlineCode4(self) -> "str":
        return (self.native_obj.OutlineCode4)
        
    @outlineCode4.setter     
    def _set_outlineCode4(self, value):
        self.native_obj.OutlineCode4 = value
            
    # -> str            
    @property         
    def outlineCode5(self) -> "str":
        return (self.native_obj.OutlineCode5)
        
    @outlineCode5.setter     
    def _set_outlineCode5(self, value):
        self.native_obj.OutlineCode5 = value
            
    # -> str            
    @property         
    def outlineCode6(self) -> "str":
        return (self.native_obj.OutlineCode6)
        
    @outlineCode6.setter     
    def _set_outlineCode6(self, value):
        self.native_obj.OutlineCode6 = value
            
    # -> str            
    @property         
    def outlineCode7(self) -> "str":
        return (self.native_obj.OutlineCode7)
        
    @outlineCode7.setter     
    def _set_outlineCode7(self, value):
        self.native_obj.OutlineCode7 = value
            
    # -> str            
    @property         
    def outlineCode8(self) -> "str":
        return (self.native_obj.OutlineCode8)
        
    @outlineCode8.setter     
    def _set_outlineCode8(self, value):
        self.native_obj.OutlineCode8 = value
            
    # -> str            
    @property         
    def outlineCode9(self) -> "str":
        return (self.native_obj.OutlineCode9)
        
    @outlineCode9.setter     
    def _set_outlineCode9(self, value):
        self.native_obj.OutlineCode9 = value
            
    # -> bool            
    @property         
    def overallocated(self) -> "bool":
        return (self.native_obj.Overallocated)
        
    @overallocated.setter     
    def _set_overallocated(self, value):
        self.native_obj.Overallocated = value
            
    # -> float            
    @property         
    def overtimeCost(self) -> "float":
        return (self.native_obj.OvertimeCost)
        
    @overtimeCost.setter     
    def _set_overtimeCost(self, value):
        self.native_obj.OvertimeCost = value
            
    # -> str            
    @property         
    def overtimeRate(self) -> "str":
        return (self.native_obj.OvertimeRate)
        
    @overtimeRate.setter     
    def _set_overtimeRate(self, value):
        self.native_obj.OvertimeRate = value
            
    # -> float            
    @property         
    def overtimeWork(self) -> "float":
        return (self.native_obj.OvertimeWork)
        
    @overtimeWork.setter     
    def _set_overtimeWork(self, value):
        self.native_obj.OvertimeWork = value
            
    # -> _IProjectDoc            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> PayRates            
    @property         
    def payRates(self) -> "PayRates":
        return PayRates(self.native_obj.PayRates)
        
    @payRates.setter     
    def _set_payRates(self, value):
        self.native_obj.PayRates = value
            
    # -> float            
    @property         
    def peakUnits(self) -> "float":
        return (self.native_obj.PeakUnits)
        
    @peakUnits.setter     
    def _set_peakUnits(self, value):
        self.native_obj.PeakUnits = value
            
    # -> int            
    @property         
    def percentWorkComplete(self) -> "int":
        return (self.native_obj.PercentWorkComplete)
        
    @percentWorkComplete.setter     
    def _set_percentWorkComplete(self, value):
        self.native_obj.PercentWorkComplete = value
            
    # -> str            
    @property         
    def phonetics(self) -> "str":
        return (self.native_obj.Phonetics)
        
    @phonetics.setter     
    def _set_phonetics(self, value):
        self.native_obj.Phonetics = value
            
    # -> str            
    @property         
    def project(self) -> "str":
        return (self.native_obj.Project)
        
    @project.setter     
    def _set_project(self, value):
        self.native_obj.Project = value
            
    # -> float            
    @property         
    def regularWork(self) -> "float":
        return (self.native_obj.RegularWork)
        
    @regularWork.setter     
    def _set_regularWork(self, value):
        self.native_obj.RegularWork = value
            
    # -> float            
    @property         
    def remainingCost(self) -> "float":
        return (self.native_obj.RemainingCost)
        
    @remainingCost.setter     
    def _set_remainingCost(self, value):
        self.native_obj.RemainingCost = value
            
    # -> float            
    @property         
    def remainingOvertimeCost(self) -> "float":
        return (self.native_obj.RemainingOvertimeCost)
        
    @remainingOvertimeCost.setter     
    def _set_remainingOvertimeCost(self, value):
        self.native_obj.RemainingOvertimeCost = value
            
    # -> float            
    @property         
    def remainingOvertimeWork(self) -> "float":
        return (self.native_obj.RemainingOvertimeWork)
        
    @remainingOvertimeWork.setter     
    def _set_remainingOvertimeWork(self, value):
        self.native_obj.RemainingOvertimeWork = value
            
    # -> float            
    @property         
    def remainingWork(self) -> "float":
        return (self.native_obj.RemainingWork)
        
    @remainingWork.setter     
    def _set_remainingWork(self, value):
        self.native_obj.RemainingWork = value
            
    # -> bool            
    @property         
    def responsePending(self) -> "bool":
        return (self.native_obj.ResponsePending)
        
    @responsePending.setter     
    def _set_responsePending(self, value):
        self.native_obj.ResponsePending = value
            
    # -> str            
    @property         
    def standardRate(self) -> "str":
        return (self.native_obj.StandardRate)
        
    @standardRate.setter     
    def _set_standardRate(self, value):
        self.native_obj.StandardRate = value
            
    # -> str            
    @property         
    def start1(self) -> "str":
        return (self.native_obj.Start1)
        
    @start1.setter     
    def _set_start1(self, value):
        self.native_obj.Start1 = value
            
    # -> str            
    @property         
    def start10(self) -> "str":
        return (self.native_obj.Start10)
        
    @start10.setter     
    def _set_start10(self, value):
        self.native_obj.Start10 = value
            
    # -> str            
    @property         
    def start2(self) -> "str":
        return (self.native_obj.Start2)
        
    @start2.setter     
    def _set_start2(self, value):
        self.native_obj.Start2 = value
            
    # -> str            
    @property         
    def start3(self) -> "str":
        return (self.native_obj.Start3)
        
    @start3.setter     
    def _set_start3(self, value):
        self.native_obj.Start3 = value
            
    # -> str            
    @property         
    def start4(self) -> "str":
        return (self.native_obj.Start4)
        
    @start4.setter     
    def _set_start4(self, value):
        self.native_obj.Start4 = value
            
    # -> str            
    @property         
    def start5(self) -> "str":
        return (self.native_obj.Start5)
        
    @start5.setter     
    def _set_start5(self, value):
        self.native_obj.Start5 = value
            
    # -> str            
    @property         
    def start6(self) -> "str":
        return (self.native_obj.Start6)
        
    @start6.setter     
    def _set_start6(self, value):
        self.native_obj.Start6 = value
            
    # -> str            
    @property         
    def start7(self) -> "str":
        return (self.native_obj.Start7)
        
    @start7.setter     
    def _set_start7(self, value):
        self.native_obj.Start7 = value
            
    # -> str            
    @property         
    def start8(self) -> "str":
        return (self.native_obj.Start8)
        
    @start8.setter     
    def _set_start8(self, value):
        self.native_obj.Start8 = value
            
    # -> str            
    @property         
    def start9(self) -> "str":
        return (self.native_obj.Start9)
        
    @start9.setter     
    def _set_start9(self, value):
        self.native_obj.Start9 = value
            
    # -> float            
    @property         
    def sV(self) -> "float":
        return (self.native_obj.SV)
        
    @sV.setter     
    def _set_sV(self, value):
        self.native_obj.SV = value
            
    # -> bool            
    @property         
    def teamStatusPending(self) -> "bool":
        return (self.native_obj.TeamStatusPending)
        
    @teamStatusPending.setter     
    def _set_teamStatusPending(self, value):
        self.native_obj.TeamStatusPending = value
            
    # -> str            
    @property         
    def text1(self) -> "str":
        return (self.native_obj.Text1)
        
    @text1.setter     
    def _set_text1(self, value):
        self.native_obj.Text1 = value
            
    # -> str            
    @property         
    def text10(self) -> "str":
        return (self.native_obj.Text10)
        
    @text10.setter     
    def _set_text10(self, value):
        self.native_obj.Text10 = value
            
    # -> str            
    @property         
    def text11(self) -> "str":
        return (self.native_obj.Text11)
        
    @text11.setter     
    def _set_text11(self, value):
        self.native_obj.Text11 = value
            
    # -> str            
    @property         
    def text12(self) -> "str":
        return (self.native_obj.Text12)
        
    @text12.setter     
    def _set_text12(self, value):
        self.native_obj.Text12 = value
            
    # -> str            
    @property         
    def text13(self) -> "str":
        return (self.native_obj.Text13)
        
    @text13.setter     
    def _set_text13(self, value):
        self.native_obj.Text13 = value
            
    # -> str            
    @property         
    def text14(self) -> "str":
        return (self.native_obj.Text14)
        
    @text14.setter     
    def _set_text14(self, value):
        self.native_obj.Text14 = value
            
    # -> str            
    @property         
    def text15(self) -> "str":
        return (self.native_obj.Text15)
        
    @text15.setter     
    def _set_text15(self, value):
        self.native_obj.Text15 = value
            
    # -> str            
    @property         
    def text16(self) -> "str":
        return (self.native_obj.Text16)
        
    @text16.setter     
    def _set_text16(self, value):
        self.native_obj.Text16 = value
            
    # -> str            
    @property         
    def text17(self) -> "str":
        return (self.native_obj.Text17)
        
    @text17.setter     
    def _set_text17(self, value):
        self.native_obj.Text17 = value
            
    # -> str            
    @property         
    def text18(self) -> "str":
        return (self.native_obj.Text18)
        
    @text18.setter     
    def _set_text18(self, value):
        self.native_obj.Text18 = value
            
    # -> str            
    @property         
    def text19(self) -> "str":
        return (self.native_obj.Text19)
        
    @text19.setter     
    def _set_text19(self, value):
        self.native_obj.Text19 = value
            
    # -> str            
    @property         
    def text2(self) -> "str":
        return (self.native_obj.Text2)
        
    @text2.setter     
    def _set_text2(self, value):
        self.native_obj.Text2 = value
            
    # -> str            
    @property         
    def text20(self) -> "str":
        return (self.native_obj.Text20)
        
    @text20.setter     
    def _set_text20(self, value):
        self.native_obj.Text20 = value
            
    # -> str            
    @property         
    def text21(self) -> "str":
        return (self.native_obj.Text21)
        
    @text21.setter     
    def _set_text21(self, value):
        self.native_obj.Text21 = value
            
    # -> str            
    @property         
    def text22(self) -> "str":
        return (self.native_obj.Text22)
        
    @text22.setter     
    def _set_text22(self, value):
        self.native_obj.Text22 = value
            
    # -> str            
    @property         
    def text23(self) -> "str":
        return (self.native_obj.Text23)
        
    @text23.setter     
    def _set_text23(self, value):
        self.native_obj.Text23 = value
            
    # -> str            
    @property         
    def text24(self) -> "str":
        return (self.native_obj.Text24)
        
    @text24.setter     
    def _set_text24(self, value):
        self.native_obj.Text24 = value
            
    # -> str            
    @property         
    def text25(self) -> "str":
        return (self.native_obj.Text25)
        
    @text25.setter     
    def _set_text25(self, value):
        self.native_obj.Text25 = value
            
    # -> str            
    @property         
    def text26(self) -> "str":
        return (self.native_obj.Text26)
        
    @text26.setter     
    def _set_text26(self, value):
        self.native_obj.Text26 = value
            
    # -> str            
    @property         
    def text27(self) -> "str":
        return (self.native_obj.Text27)
        
    @text27.setter     
    def _set_text27(self, value):
        self.native_obj.Text27 = value
            
    # -> str            
    @property         
    def text28(self) -> "str":
        return (self.native_obj.Text28)
        
    @text28.setter     
    def _set_text28(self, value):
        self.native_obj.Text28 = value
            
    # -> str            
    @property         
    def text29(self) -> "str":
        return (self.native_obj.Text29)
        
    @text29.setter     
    def _set_text29(self, value):
        self.native_obj.Text29 = value
            
    # -> str            
    @property         
    def text3(self) -> "str":
        return (self.native_obj.Text3)
        
    @text3.setter     
    def _set_text3(self, value):
        self.native_obj.Text3 = value
            
    # -> str            
    @property         
    def text30(self) -> "str":
        return (self.native_obj.Text30)
        
    @text30.setter     
    def _set_text30(self, value):
        self.native_obj.Text30 = value
            
    # -> str            
    @property         
    def text4(self) -> "str":
        return (self.native_obj.Text4)
        
    @text4.setter     
    def _set_text4(self, value):
        self.native_obj.Text4 = value
            
    # -> str            
    @property         
    def text5(self) -> "str":
        return (self.native_obj.Text5)
        
    @text5.setter     
    def _set_text5(self, value):
        self.native_obj.Text5 = value
            
    # -> str            
    @property         
    def text6(self) -> "str":
        return (self.native_obj.Text6)
        
    @text6.setter     
    def _set_text6(self, value):
        self.native_obj.Text6 = value
            
    # -> str            
    @property         
    def text7(self) -> "str":
        return (self.native_obj.Text7)
        
    @text7.setter     
    def _set_text7(self, value):
        self.native_obj.Text7 = value
            
    # -> str            
    @property         
    def text8(self) -> "str":
        return (self.native_obj.Text8)
        
    @text8.setter     
    def _set_text8(self, value):
        self.native_obj.Text8 = value
            
    # -> str            
    @property         
    def text9(self) -> "str":
        return (self.native_obj.Text9)
        
    @text9.setter     
    def _set_text9(self, value):
        self.native_obj.Text9 = value
            
    # -> int            
    @property         
    def type(self) -> "int":
        return (self.native_obj.Type)
        
    @type.setter     
    def _set_type(self, value):
        self.native_obj.Type = value
            
    # -> int            
    @property         
    def uniqueID(self) -> "int":
        return (self.native_obj.UniqueID)
        
    @uniqueID.setter     
    def _set_uniqueID(self, value):
        self.native_obj.UniqueID = value
            
    # -> bool            
    @property         
    def updateNeeded(self) -> "bool":
        return (self.native_obj.UpdateNeeded)
        
    @updateNeeded.setter     
    def _set_updateNeeded(self, value):
        self.native_obj.UpdateNeeded = value
            
    # -> float            
    @property         
    def vAC(self) -> "float":
        return (self.native_obj.VAC)
        
    @vAC.setter     
    def _set_vAC(self, value):
        self.native_obj.VAC = value
            
    # -> str            
    @property         
    def windowsUserAccount(self) -> "str":
        return (self.native_obj.WindowsUserAccount)
        
    @windowsUserAccount.setter     
    def _set_windowsUserAccount(self, value):
        self.native_obj.WindowsUserAccount = value
            
    # -> float            
    @property         
    def work(self) -> "float":
        return (self.native_obj.Work)
        
    @work.setter     
    def _set_work(self, value):
        self.native_obj.Work = value
            
    # -> float            
    @property         
    def workVariance(self) -> "float":
        return (self.native_obj.WorkVariance)
        
    @workVariance.setter     
    def _set_workVariance(self, value):
        self.native_obj.WorkVariance = value
            
# end "Resource"       
        