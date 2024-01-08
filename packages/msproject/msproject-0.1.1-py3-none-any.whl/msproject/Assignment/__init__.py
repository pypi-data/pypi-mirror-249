

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Assignment:
    # Object "Assignment" class for software "Project"
    
    properties = ['actualCost', 'actualFinish', 'actualOvertimeCost', 'actualOvertimeWork', 'actualStart', 'actualWork', 'aCWP', 'application', 'baseline10BudgetCost', 'baseline10BudgetWork', 'baseline10Cost', 'baseline10Finish', 'baseline10Start', 'baseline10Work', 'baseline1BudgetCost', 'baseline1BudgetWork', 'baseline1Cost', 'baseline1Finish', 'baseline1Start', 'baseline1Work', 'baseline2BudgetCost', 'baseline2BudgetWork', 'baseline2Cost', 'baseline2Finish', 'baseline2Start', 'baseline2Work', 'baseline3BudgetCost', 'baseline3BudgetWork', 'baseline3Cost', 'baseline3Finish', 'baseline3Start', 'baseline3Work', 'baseline4BudgetCost', 'baseline4BudgetWork', 'baseline4Cost', 'baseline4Finish', 'baseline4Start', 'baseline4Work', 'baseline5BudgetCost', 'baseline5BudgetWork', 'baseline5Cost', 'baseline5Finish', 'baseline5Start', 'baseline5Work', 'baseline6BudgetCost', 'baseline6BudgetWork', 'baseline6Cost', 'baseline6Finish', 'baseline6Start', 'baseline6Work', 'baseline7BudgetCost', 'baseline7BudgetWork', 'baseline7Cost', 'baseline7Finish', 'baseline7Start', 'baseline7Work', 'baseline8BudgetCost', 'baseline8BudgetWork', 'baseline8Cost', 'baseline8Finish', 'baseline8Start', 'baseline8Work', 'baseline9BudgetCost', 'baseline9BudgetWork', 'baseline9Cost', 'baseline9Finish', 'baseline9Start', 'baseline9Work', 'baselineBudgetCost', 'baselineBudgetWork', 'baselineCost', 'baselineFinish', 'baselineStart', 'baselineWork', 'bCWP', 'bCWS', 'bookingType', 'budgetCost', 'budgetWork', 'compliant', 'confirmed', 'cost', 'cost1', 'cost10', 'cost2', 'cost3', 'cost4', 'cost5', 'cost6', 'cost7', 'cost8', 'cost9', 'costRateTable', 'costVariance', 'created', 'cV', 'date1', 'date10', 'date2', 'date3', 'date4', 'date5', 'date6', 'date7', 'date8', 'date9', 'delay', 'duration1', 'duration10', 'duration2', 'duration3', 'duration4', 'duration5', 'duration6', 'duration7', 'duration8', 'duration9', 'finish', 'finish1', 'finish10', 'finish2', 'finish3', 'finish4', 'finish5', 'finish6', 'finish7', 'finish8', 'finish9', 'finishVariance', 'fixedMaterialAssignment', 'flag1', 'flag10', 'flag11', 'flag12', 'flag13', 'flag14', 'flag15', 'flag16', 'flag17', 'flag18', 'flag19', 'flag2', 'flag20', 'flag3', 'flag4', 'flag5', 'flag6', 'flag7', 'flag8', 'flag9', 'guid', 'hyperlink', 'hyperlinkAddress', 'hyperlinkHREF', 'hyperlinkScreenTip', 'hyperlinkSubAddress', 'index', 'levelingDelay', 'linkedFields', 'notes', 'number1', 'number10', 'number11', 'number12', 'number13', 'number14', 'number15', 'number16', 'number17', 'number18', 'number19', 'number2', 'number20', 'number3', 'number4', 'number5', 'number6', 'number7', 'number8', 'number9', 'overallocated', 'overtimeCost', 'overtimeWork', 'owner', 'parent', 'peak', 'percentWorkComplete', 'project', 'regularWork', 'remainingCost', 'remainingOvertimeCost', 'remainingOvertimeWork', 'remainingWork', 'resource', 'resourceGuid', 'resourceID', 'resourceName', 'resourceRequestType', 'resourceType', 'resourceUniqueID', 'responsePending', 'start', 'start1', 'start10', 'start2', 'start3', 'start4', 'start5', 'start6', 'start7', 'start8', 'start9', 'startVariance', 'summary', 'sV', 'task', 'taskGuid', 'taskID', 'taskName', 'taskOutlineNumber', 'taskSummaryName', 'taskUniqueID', 'teamStatusPending', 'text1', 'text10', 'text11', 'text12', 'text13', 'text14', 'text15', 'text16', 'text17', 'text18', 'text19', 'text2', 'text20', 'text21', 'text22', 'text23', 'text24', 'text25', 'text26', 'text27', 'text28', 'text29', 'text3', 'text30', 'text4', 'text5', 'text6', 'text7', 'text8', 'text9', 'uniqueID', 'units', 'updateNeeded', 'vAC', 'wBS', 'work', 'workContour', 'workVariance']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def actualCost(self) -> "Any":
        return (self.native_obj.ActualCost)
        
    @actualCost.setter     
    def _set_actualCost(self, value):
        self.native_obj.ActualCost = value
            
    # -> Any            
    @property         
    def actualFinish(self) -> "Any":
        return (self.native_obj.ActualFinish)
        
    @actualFinish.setter     
    def _set_actualFinish(self, value):
        self.native_obj.ActualFinish = value
            
    # -> Any            
    @property         
    def actualOvertimeCost(self) -> "Any":
        return (self.native_obj.ActualOvertimeCost)
        
    @actualOvertimeCost.setter     
    def _set_actualOvertimeCost(self, value):
        self.native_obj.ActualOvertimeCost = value
            
    # -> Any            
    @property         
    def actualOvertimeWork(self) -> "Any":
        return (self.native_obj.ActualOvertimeWork)
        
    @actualOvertimeWork.setter     
    def _set_actualOvertimeWork(self, value):
        self.native_obj.ActualOvertimeWork = value
            
    # -> Any            
    @property         
    def actualStart(self) -> "Any":
        return (self.native_obj.ActualStart)
        
    @actualStart.setter     
    def _set_actualStart(self, value):
        self.native_obj.ActualStart = value
            
    # -> Any            
    @property         
    def actualWork(self) -> "Any":
        return (self.native_obj.ActualWork)
        
    @actualWork.setter     
    def _set_actualWork(self, value):
        self.native_obj.ActualWork = value
            
    # -> Any            
    @property         
    def aCWP(self) -> "Any":
        return (self.native_obj.ACWP)
        
    @aCWP.setter     
    def _set_aCWP(self, value):
        self.native_obj.ACWP = value
            
    # -> Any            
    @property         
    def application(self) -> "Any":
        return (self.native_obj.Application)
        
    @application.setter     
    def _set_application(self, value):
        self.native_obj.Application = value
            
    # -> Any            
    @property         
    def baseline10BudgetCost(self) -> "Any":
        return (self.native_obj.Baseline10BudgetCost)
        
    @baseline10BudgetCost.setter     
    def _set_baseline10BudgetCost(self, value):
        self.native_obj.Baseline10BudgetCost = value
            
    # -> Any            
    @property         
    def baseline10BudgetWork(self) -> "Any":
        return (self.native_obj.Baseline10BudgetWork)
        
    @baseline10BudgetWork.setter     
    def _set_baseline10BudgetWork(self, value):
        self.native_obj.Baseline10BudgetWork = value
            
    # -> Any            
    @property         
    def baseline10Cost(self) -> "Any":
        return (self.native_obj.Baseline10Cost)
        
    @baseline10Cost.setter     
    def _set_baseline10Cost(self, value):
        self.native_obj.Baseline10Cost = value
            
    # -> Any            
    @property         
    def baseline10Finish(self) -> "Any":
        return (self.native_obj.Baseline10Finish)
        
    @baseline10Finish.setter     
    def _set_baseline10Finish(self, value):
        self.native_obj.Baseline10Finish = value
            
    # -> Any            
    @property         
    def baseline10Start(self) -> "Any":
        return (self.native_obj.Baseline10Start)
        
    @baseline10Start.setter     
    def _set_baseline10Start(self, value):
        self.native_obj.Baseline10Start = value
            
    # -> Any            
    @property         
    def baseline10Work(self) -> "Any":
        return (self.native_obj.Baseline10Work)
        
    @baseline10Work.setter     
    def _set_baseline10Work(self, value):
        self.native_obj.Baseline10Work = value
            
    # -> Any            
    @property         
    def baseline1BudgetCost(self) -> "Any":
        return (self.native_obj.Baseline1BudgetCost)
        
    @baseline1BudgetCost.setter     
    def _set_baseline1BudgetCost(self, value):
        self.native_obj.Baseline1BudgetCost = value
            
    # -> Any            
    @property         
    def baseline1BudgetWork(self) -> "Any":
        return (self.native_obj.Baseline1BudgetWork)
        
    @baseline1BudgetWork.setter     
    def _set_baseline1BudgetWork(self, value):
        self.native_obj.Baseline1BudgetWork = value
            
    # -> Any            
    @property         
    def baseline1Cost(self) -> "Any":
        return (self.native_obj.Baseline1Cost)
        
    @baseline1Cost.setter     
    def _set_baseline1Cost(self, value):
        self.native_obj.Baseline1Cost = value
            
    # -> Any            
    @property         
    def baseline1Finish(self) -> "Any":
        return (self.native_obj.Baseline1Finish)
        
    @baseline1Finish.setter     
    def _set_baseline1Finish(self, value):
        self.native_obj.Baseline1Finish = value
            
    # -> Any            
    @property         
    def baseline1Start(self) -> "Any":
        return (self.native_obj.Baseline1Start)
        
    @baseline1Start.setter     
    def _set_baseline1Start(self, value):
        self.native_obj.Baseline1Start = value
            
    # -> Any            
    @property         
    def baseline1Work(self) -> "Any":
        return (self.native_obj.Baseline1Work)
        
    @baseline1Work.setter     
    def _set_baseline1Work(self, value):
        self.native_obj.Baseline1Work = value
            
    # -> Any            
    @property         
    def baseline2BudgetCost(self) -> "Any":
        return (self.native_obj.Baseline2BudgetCost)
        
    @baseline2BudgetCost.setter     
    def _set_baseline2BudgetCost(self, value):
        self.native_obj.Baseline2BudgetCost = value
            
    # -> Any            
    @property         
    def baseline2BudgetWork(self) -> "Any":
        return (self.native_obj.Baseline2BudgetWork)
        
    @baseline2BudgetWork.setter     
    def _set_baseline2BudgetWork(self, value):
        self.native_obj.Baseline2BudgetWork = value
            
    # -> Any            
    @property         
    def baseline2Cost(self) -> "Any":
        return (self.native_obj.Baseline2Cost)
        
    @baseline2Cost.setter     
    def _set_baseline2Cost(self, value):
        self.native_obj.Baseline2Cost = value
            
    # -> Any            
    @property         
    def baseline2Finish(self) -> "Any":
        return (self.native_obj.Baseline2Finish)
        
    @baseline2Finish.setter     
    def _set_baseline2Finish(self, value):
        self.native_obj.Baseline2Finish = value
            
    # -> Any            
    @property         
    def baseline2Start(self) -> "Any":
        return (self.native_obj.Baseline2Start)
        
    @baseline2Start.setter     
    def _set_baseline2Start(self, value):
        self.native_obj.Baseline2Start = value
            
    # -> Any            
    @property         
    def baseline2Work(self) -> "Any":
        return (self.native_obj.Baseline2Work)
        
    @baseline2Work.setter     
    def _set_baseline2Work(self, value):
        self.native_obj.Baseline2Work = value
            
    # -> Any            
    @property         
    def baseline3BudgetCost(self) -> "Any":
        return (self.native_obj.Baseline3BudgetCost)
        
    @baseline3BudgetCost.setter     
    def _set_baseline3BudgetCost(self, value):
        self.native_obj.Baseline3BudgetCost = value
            
    # -> Any            
    @property         
    def baseline3BudgetWork(self) -> "Any":
        return (self.native_obj.Baseline3BudgetWork)
        
    @baseline3BudgetWork.setter     
    def _set_baseline3BudgetWork(self, value):
        self.native_obj.Baseline3BudgetWork = value
            
    # -> Any            
    @property         
    def baseline3Cost(self) -> "Any":
        return (self.native_obj.Baseline3Cost)
        
    @baseline3Cost.setter     
    def _set_baseline3Cost(self, value):
        self.native_obj.Baseline3Cost = value
            
    # -> Any            
    @property         
    def baseline3Finish(self) -> "Any":
        return (self.native_obj.Baseline3Finish)
        
    @baseline3Finish.setter     
    def _set_baseline3Finish(self, value):
        self.native_obj.Baseline3Finish = value
            
    # -> Any            
    @property         
    def baseline3Start(self) -> "Any":
        return (self.native_obj.Baseline3Start)
        
    @baseline3Start.setter     
    def _set_baseline3Start(self, value):
        self.native_obj.Baseline3Start = value
            
    # -> Any            
    @property         
    def baseline3Work(self) -> "Any":
        return (self.native_obj.Baseline3Work)
        
    @baseline3Work.setter     
    def _set_baseline3Work(self, value):
        self.native_obj.Baseline3Work = value
            
    # -> Any            
    @property         
    def baseline4BudgetCost(self) -> "Any":
        return (self.native_obj.Baseline4BudgetCost)
        
    @baseline4BudgetCost.setter     
    def _set_baseline4BudgetCost(self, value):
        self.native_obj.Baseline4BudgetCost = value
            
    # -> Any            
    @property         
    def baseline4BudgetWork(self) -> "Any":
        return (self.native_obj.Baseline4BudgetWork)
        
    @baseline4BudgetWork.setter     
    def _set_baseline4BudgetWork(self, value):
        self.native_obj.Baseline4BudgetWork = value
            
    # -> Any            
    @property         
    def baseline4Cost(self) -> "Any":
        return (self.native_obj.Baseline4Cost)
        
    @baseline4Cost.setter     
    def _set_baseline4Cost(self, value):
        self.native_obj.Baseline4Cost = value
            
    # -> Any            
    @property         
    def baseline4Finish(self) -> "Any":
        return (self.native_obj.Baseline4Finish)
        
    @baseline4Finish.setter     
    def _set_baseline4Finish(self, value):
        self.native_obj.Baseline4Finish = value
            
    # -> Any            
    @property         
    def baseline4Start(self) -> "Any":
        return (self.native_obj.Baseline4Start)
        
    @baseline4Start.setter     
    def _set_baseline4Start(self, value):
        self.native_obj.Baseline4Start = value
            
    # -> Any            
    @property         
    def baseline4Work(self) -> "Any":
        return (self.native_obj.Baseline4Work)
        
    @baseline4Work.setter     
    def _set_baseline4Work(self, value):
        self.native_obj.Baseline4Work = value
            
    # -> Any            
    @property         
    def baseline5BudgetCost(self) -> "Any":
        return (self.native_obj.Baseline5BudgetCost)
        
    @baseline5BudgetCost.setter     
    def _set_baseline5BudgetCost(self, value):
        self.native_obj.Baseline5BudgetCost = value
            
    # -> Any            
    @property         
    def baseline5BudgetWork(self) -> "Any":
        return (self.native_obj.Baseline5BudgetWork)
        
    @baseline5BudgetWork.setter     
    def _set_baseline5BudgetWork(self, value):
        self.native_obj.Baseline5BudgetWork = value
            
    # -> Any            
    @property         
    def baseline5Cost(self) -> "Any":
        return (self.native_obj.Baseline5Cost)
        
    @baseline5Cost.setter     
    def _set_baseline5Cost(self, value):
        self.native_obj.Baseline5Cost = value
            
    # -> Any            
    @property         
    def baseline5Finish(self) -> "Any":
        return (self.native_obj.Baseline5Finish)
        
    @baseline5Finish.setter     
    def _set_baseline5Finish(self, value):
        self.native_obj.Baseline5Finish = value
            
    # -> Any            
    @property         
    def baseline5Start(self) -> "Any":
        return (self.native_obj.Baseline5Start)
        
    @baseline5Start.setter     
    def _set_baseline5Start(self, value):
        self.native_obj.Baseline5Start = value
            
    # -> Any            
    @property         
    def baseline5Work(self) -> "Any":
        return (self.native_obj.Baseline5Work)
        
    @baseline5Work.setter     
    def _set_baseline5Work(self, value):
        self.native_obj.Baseline5Work = value
            
    # -> Any            
    @property         
    def baseline6BudgetCost(self) -> "Any":
        return (self.native_obj.Baseline6BudgetCost)
        
    @baseline6BudgetCost.setter     
    def _set_baseline6BudgetCost(self, value):
        self.native_obj.Baseline6BudgetCost = value
            
    # -> Any            
    @property         
    def baseline6BudgetWork(self) -> "Any":
        return (self.native_obj.Baseline6BudgetWork)
        
    @baseline6BudgetWork.setter     
    def _set_baseline6BudgetWork(self, value):
        self.native_obj.Baseline6BudgetWork = value
            
    # -> Any            
    @property         
    def baseline6Cost(self) -> "Any":
        return (self.native_obj.Baseline6Cost)
        
    @baseline6Cost.setter     
    def _set_baseline6Cost(self, value):
        self.native_obj.Baseline6Cost = value
            
    # -> Any            
    @property         
    def baseline6Finish(self) -> "Any":
        return (self.native_obj.Baseline6Finish)
        
    @baseline6Finish.setter     
    def _set_baseline6Finish(self, value):
        self.native_obj.Baseline6Finish = value
            
    # -> Any            
    @property         
    def baseline6Start(self) -> "Any":
        return (self.native_obj.Baseline6Start)
        
    @baseline6Start.setter     
    def _set_baseline6Start(self, value):
        self.native_obj.Baseline6Start = value
            
    # -> Any            
    @property         
    def baseline6Work(self) -> "Any":
        return (self.native_obj.Baseline6Work)
        
    @baseline6Work.setter     
    def _set_baseline6Work(self, value):
        self.native_obj.Baseline6Work = value
            
    # -> Any            
    @property         
    def baseline7BudgetCost(self) -> "Any":
        return (self.native_obj.Baseline7BudgetCost)
        
    @baseline7BudgetCost.setter     
    def _set_baseline7BudgetCost(self, value):
        self.native_obj.Baseline7BudgetCost = value
            
    # -> Any            
    @property         
    def baseline7BudgetWork(self) -> "Any":
        return (self.native_obj.Baseline7BudgetWork)
        
    @baseline7BudgetWork.setter     
    def _set_baseline7BudgetWork(self, value):
        self.native_obj.Baseline7BudgetWork = value
            
    # -> Any            
    @property         
    def baseline7Cost(self) -> "Any":
        return (self.native_obj.Baseline7Cost)
        
    @baseline7Cost.setter     
    def _set_baseline7Cost(self, value):
        self.native_obj.Baseline7Cost = value
            
    # -> Any            
    @property         
    def baseline7Finish(self) -> "Any":
        return (self.native_obj.Baseline7Finish)
        
    @baseline7Finish.setter     
    def _set_baseline7Finish(self, value):
        self.native_obj.Baseline7Finish = value
            
    # -> Any            
    @property         
    def baseline7Start(self) -> "Any":
        return (self.native_obj.Baseline7Start)
        
    @baseline7Start.setter     
    def _set_baseline7Start(self, value):
        self.native_obj.Baseline7Start = value
            
    # -> Any            
    @property         
    def baseline7Work(self) -> "Any":
        return (self.native_obj.Baseline7Work)
        
    @baseline7Work.setter     
    def _set_baseline7Work(self, value):
        self.native_obj.Baseline7Work = value
            
    # -> Any            
    @property         
    def baseline8BudgetCost(self) -> "Any":
        return (self.native_obj.Baseline8BudgetCost)
        
    @baseline8BudgetCost.setter     
    def _set_baseline8BudgetCost(self, value):
        self.native_obj.Baseline8BudgetCost = value
            
    # -> Any            
    @property         
    def baseline8BudgetWork(self) -> "Any":
        return (self.native_obj.Baseline8BudgetWork)
        
    @baseline8BudgetWork.setter     
    def _set_baseline8BudgetWork(self, value):
        self.native_obj.Baseline8BudgetWork = value
            
    # -> Any            
    @property         
    def baseline8Cost(self) -> "Any":
        return (self.native_obj.Baseline8Cost)
        
    @baseline8Cost.setter     
    def _set_baseline8Cost(self, value):
        self.native_obj.Baseline8Cost = value
            
    # -> Any            
    @property         
    def baseline8Finish(self) -> "Any":
        return (self.native_obj.Baseline8Finish)
        
    @baseline8Finish.setter     
    def _set_baseline8Finish(self, value):
        self.native_obj.Baseline8Finish = value
            
    # -> Any            
    @property         
    def baseline8Start(self) -> "Any":
        return (self.native_obj.Baseline8Start)
        
    @baseline8Start.setter     
    def _set_baseline8Start(self, value):
        self.native_obj.Baseline8Start = value
            
    # -> Any            
    @property         
    def baseline8Work(self) -> "Any":
        return (self.native_obj.Baseline8Work)
        
    @baseline8Work.setter     
    def _set_baseline8Work(self, value):
        self.native_obj.Baseline8Work = value
            
    # -> Any            
    @property         
    def baseline9BudgetCost(self) -> "Any":
        return (self.native_obj.Baseline9BudgetCost)
        
    @baseline9BudgetCost.setter     
    def _set_baseline9BudgetCost(self, value):
        self.native_obj.Baseline9BudgetCost = value
            
    # -> Any            
    @property         
    def baseline9BudgetWork(self) -> "Any":
        return (self.native_obj.Baseline9BudgetWork)
        
    @baseline9BudgetWork.setter     
    def _set_baseline9BudgetWork(self, value):
        self.native_obj.Baseline9BudgetWork = value
            
    # -> Any            
    @property         
    def baseline9Cost(self) -> "Any":
        return (self.native_obj.Baseline9Cost)
        
    @baseline9Cost.setter     
    def _set_baseline9Cost(self, value):
        self.native_obj.Baseline9Cost = value
            
    # -> Any            
    @property         
    def baseline9Finish(self) -> "Any":
        return (self.native_obj.Baseline9Finish)
        
    @baseline9Finish.setter     
    def _set_baseline9Finish(self, value):
        self.native_obj.Baseline9Finish = value
            
    # -> Any            
    @property         
    def baseline9Start(self) -> "Any":
        return (self.native_obj.Baseline9Start)
        
    @baseline9Start.setter     
    def _set_baseline9Start(self, value):
        self.native_obj.Baseline9Start = value
            
    # -> Any            
    @property         
    def baseline9Work(self) -> "Any":
        return (self.native_obj.Baseline9Work)
        
    @baseline9Work.setter     
    def _set_baseline9Work(self, value):
        self.native_obj.Baseline9Work = value
            
    # -> Any            
    @property         
    def baselineBudgetCost(self) -> "Any":
        return (self.native_obj.BaselineBudgetCost)
        
    @baselineBudgetCost.setter     
    def _set_baselineBudgetCost(self, value):
        self.native_obj.BaselineBudgetCost = value
            
    # -> Any            
    @property         
    def baselineBudgetWork(self) -> "Any":
        return (self.native_obj.BaselineBudgetWork)
        
    @baselineBudgetWork.setter     
    def _set_baselineBudgetWork(self, value):
        self.native_obj.BaselineBudgetWork = value
            
    # -> Any            
    @property         
    def baselineCost(self) -> "Any":
        return (self.native_obj.BaselineCost)
        
    @baselineCost.setter     
    def _set_baselineCost(self, value):
        self.native_obj.BaselineCost = value
            
    # -> Any            
    @property         
    def baselineFinish(self) -> "Any":
        return (self.native_obj.BaselineFinish)
        
    @baselineFinish.setter     
    def _set_baselineFinish(self, value):
        self.native_obj.BaselineFinish = value
            
    # -> Any            
    @property         
    def baselineStart(self) -> "Any":
        return (self.native_obj.BaselineStart)
        
    @baselineStart.setter     
    def _set_baselineStart(self, value):
        self.native_obj.BaselineStart = value
            
    # -> Any            
    @property         
    def baselineWork(self) -> "Any":
        return (self.native_obj.BaselineWork)
        
    @baselineWork.setter     
    def _set_baselineWork(self, value):
        self.native_obj.BaselineWork = value
            
    # -> Any            
    @property         
    def bCWP(self) -> "Any":
        return (self.native_obj.BCWP)
        
    @bCWP.setter     
    def _set_bCWP(self, value):
        self.native_obj.BCWP = value
            
    # -> Any            
    @property         
    def bCWS(self) -> "Any":
        return (self.native_obj.BCWS)
        
    @bCWS.setter     
    def _set_bCWS(self, value):
        self.native_obj.BCWS = value
            
    # -> Any            
    @property         
    def bookingType(self) -> "Any":
        return (self.native_obj.BookingType)
        
    @bookingType.setter     
    def _set_bookingType(self, value):
        self.native_obj.BookingType = value
            
    # -> Any            
    @property         
    def budgetCost(self) -> "Any":
        return (self.native_obj.BudgetCost)
        
    @budgetCost.setter     
    def _set_budgetCost(self, value):
        self.native_obj.BudgetCost = value
            
    # -> Any            
    @property         
    def budgetWork(self) -> "Any":
        return (self.native_obj.BudgetWork)
        
    @budgetWork.setter     
    def _set_budgetWork(self, value):
        self.native_obj.BudgetWork = value
            
    # -> Any            
    @property         
    def compliant(self) -> "Any":
        return (self.native_obj.Compliant)
        
    @compliant.setter     
    def _set_compliant(self, value):
        self.native_obj.Compliant = value
            
    # -> Any            
    @property         
    def confirmed(self) -> "Any":
        return (self.native_obj.Confirmed)
        
    @confirmed.setter     
    def _set_confirmed(self, value):
        self.native_obj.Confirmed = value
            
    # -> Any            
    @property         
    def cost(self) -> "Any":
        return (self.native_obj.Cost)
        
    @cost.setter     
    def _set_cost(self, value):
        self.native_obj.Cost = value
            
    # -> Any            
    @property         
    def cost1(self) -> "Any":
        return (self.native_obj.Cost1)
        
    @cost1.setter     
    def _set_cost1(self, value):
        self.native_obj.Cost1 = value
            
    # -> Any            
    @property         
    def cost10(self) -> "Any":
        return (self.native_obj.Cost10)
        
    @cost10.setter     
    def _set_cost10(self, value):
        self.native_obj.Cost10 = value
            
    # -> Any            
    @property         
    def cost2(self) -> "Any":
        return (self.native_obj.Cost2)
        
    @cost2.setter     
    def _set_cost2(self, value):
        self.native_obj.Cost2 = value
            
    # -> Any            
    @property         
    def cost3(self) -> "Any":
        return (self.native_obj.Cost3)
        
    @cost3.setter     
    def _set_cost3(self, value):
        self.native_obj.Cost3 = value
            
    # -> Any            
    @property         
    def cost4(self) -> "Any":
        return (self.native_obj.Cost4)
        
    @cost4.setter     
    def _set_cost4(self, value):
        self.native_obj.Cost4 = value
            
    # -> Any            
    @property         
    def cost5(self) -> "Any":
        return (self.native_obj.Cost5)
        
    @cost5.setter     
    def _set_cost5(self, value):
        self.native_obj.Cost5 = value
            
    # -> Any            
    @property         
    def cost6(self) -> "Any":
        return (self.native_obj.Cost6)
        
    @cost6.setter     
    def _set_cost6(self, value):
        self.native_obj.Cost6 = value
            
    # -> Any            
    @property         
    def cost7(self) -> "Any":
        return (self.native_obj.Cost7)
        
    @cost7.setter     
    def _set_cost7(self, value):
        self.native_obj.Cost7 = value
            
    # -> Any            
    @property         
    def cost8(self) -> "Any":
        return (self.native_obj.Cost8)
        
    @cost8.setter     
    def _set_cost8(self, value):
        self.native_obj.Cost8 = value
            
    # -> Any            
    @property         
    def cost9(self) -> "Any":
        return (self.native_obj.Cost9)
        
    @cost9.setter     
    def _set_cost9(self, value):
        self.native_obj.Cost9 = value
            
    # -> Any            
    @property         
    def costRateTable(self) -> "Any":
        return (self.native_obj.CostRateTable)
        
    @costRateTable.setter     
    def _set_costRateTable(self, value):
        self.native_obj.CostRateTable = value
            
    # -> Any            
    @property         
    def costVariance(self) -> "Any":
        return (self.native_obj.CostVariance)
        
    @costVariance.setter     
    def _set_costVariance(self, value):
        self.native_obj.CostVariance = value
            
    # -> Any            
    @property         
    def created(self) -> "Any":
        return (self.native_obj.Created)
        
    @created.setter     
    def _set_created(self, value):
        self.native_obj.Created = value
            
    # -> Any            
    @property         
    def cV(self) -> "Any":
        return (self.native_obj.CV)
        
    @cV.setter     
    def _set_cV(self, value):
        self.native_obj.CV = value
            
    # -> Any            
    @property         
    def date1(self) -> "Any":
        return (self.native_obj.Date1)
        
    @date1.setter     
    def _set_date1(self, value):
        self.native_obj.Date1 = value
            
    # -> Any            
    @property         
    def date10(self) -> "Any":
        return (self.native_obj.Date10)
        
    @date10.setter     
    def _set_date10(self, value):
        self.native_obj.Date10 = value
            
    # -> Any            
    @property         
    def date2(self) -> "Any":
        return (self.native_obj.Date2)
        
    @date2.setter     
    def _set_date2(self, value):
        self.native_obj.Date2 = value
            
    # -> Any            
    @property         
    def date3(self) -> "Any":
        return (self.native_obj.Date3)
        
    @date3.setter     
    def _set_date3(self, value):
        self.native_obj.Date3 = value
            
    # -> Any            
    @property         
    def date4(self) -> "Any":
        return (self.native_obj.Date4)
        
    @date4.setter     
    def _set_date4(self, value):
        self.native_obj.Date4 = value
            
    # -> Any            
    @property         
    def date5(self) -> "Any":
        return (self.native_obj.Date5)
        
    @date5.setter     
    def _set_date5(self, value):
        self.native_obj.Date5 = value
            
    # -> Any            
    @property         
    def date6(self) -> "Any":
        return (self.native_obj.Date6)
        
    @date6.setter     
    def _set_date6(self, value):
        self.native_obj.Date6 = value
            
    # -> Any            
    @property         
    def date7(self) -> "Any":
        return (self.native_obj.Date7)
        
    @date7.setter     
    def _set_date7(self, value):
        self.native_obj.Date7 = value
            
    # -> Any            
    @property         
    def date8(self) -> "Any":
        return (self.native_obj.Date8)
        
    @date8.setter     
    def _set_date8(self, value):
        self.native_obj.Date8 = value
            
    # -> Any            
    @property         
    def date9(self) -> "Any":
        return (self.native_obj.Date9)
        
    @date9.setter     
    def _set_date9(self, value):
        self.native_obj.Date9 = value
            
    # -> Any            
    @property         
    def delay(self) -> "Any":
        return (self.native_obj.Delay)
        
    @delay.setter     
    def _set_delay(self, value):
        self.native_obj.Delay = value
            
    # -> Any            
    @property         
    def duration1(self) -> "Any":
        return (self.native_obj.Duration1)
        
    @duration1.setter     
    def _set_duration1(self, value):
        self.native_obj.Duration1 = value
            
    # -> Any            
    @property         
    def duration10(self) -> "Any":
        return (self.native_obj.Duration10)
        
    @duration10.setter     
    def _set_duration10(self, value):
        self.native_obj.Duration10 = value
            
    # -> Any            
    @property         
    def duration2(self) -> "Any":
        return (self.native_obj.Duration2)
        
    @duration2.setter     
    def _set_duration2(self, value):
        self.native_obj.Duration2 = value
            
    # -> Any            
    @property         
    def duration3(self) -> "Any":
        return (self.native_obj.Duration3)
        
    @duration3.setter     
    def _set_duration3(self, value):
        self.native_obj.Duration3 = value
            
    # -> Any            
    @property         
    def duration4(self) -> "Any":
        return (self.native_obj.Duration4)
        
    @duration4.setter     
    def _set_duration4(self, value):
        self.native_obj.Duration4 = value
            
    # -> Any            
    @property         
    def duration5(self) -> "Any":
        return (self.native_obj.Duration5)
        
    @duration5.setter     
    def _set_duration5(self, value):
        self.native_obj.Duration5 = value
            
    # -> Any            
    @property         
    def duration6(self) -> "Any":
        return (self.native_obj.Duration6)
        
    @duration6.setter     
    def _set_duration6(self, value):
        self.native_obj.Duration6 = value
            
    # -> Any            
    @property         
    def duration7(self) -> "Any":
        return (self.native_obj.Duration7)
        
    @duration7.setter     
    def _set_duration7(self, value):
        self.native_obj.Duration7 = value
            
    # -> Any            
    @property         
    def duration8(self) -> "Any":
        return (self.native_obj.Duration8)
        
    @duration8.setter     
    def _set_duration8(self, value):
        self.native_obj.Duration8 = value
            
    # -> Any            
    @property         
    def duration9(self) -> "Any":
        return (self.native_obj.Duration9)
        
    @duration9.setter     
    def _set_duration9(self, value):
        self.native_obj.Duration9 = value
            
    # -> Any            
    @property         
    def finish(self) -> "Any":
        return (self.native_obj.Finish)
        
    @finish.setter     
    def _set_finish(self, value):
        self.native_obj.Finish = value
            
    # -> Any            
    @property         
    def finish1(self) -> "Any":
        return (self.native_obj.Finish1)
        
    @finish1.setter     
    def _set_finish1(self, value):
        self.native_obj.Finish1 = value
            
    # -> Any            
    @property         
    def finish10(self) -> "Any":
        return (self.native_obj.Finish10)
        
    @finish10.setter     
    def _set_finish10(self, value):
        self.native_obj.Finish10 = value
            
    # -> Any            
    @property         
    def finish2(self) -> "Any":
        return (self.native_obj.Finish2)
        
    @finish2.setter     
    def _set_finish2(self, value):
        self.native_obj.Finish2 = value
            
    # -> Any            
    @property         
    def finish3(self) -> "Any":
        return (self.native_obj.Finish3)
        
    @finish3.setter     
    def _set_finish3(self, value):
        self.native_obj.Finish3 = value
            
    # -> Any            
    @property         
    def finish4(self) -> "Any":
        return (self.native_obj.Finish4)
        
    @finish4.setter     
    def _set_finish4(self, value):
        self.native_obj.Finish4 = value
            
    # -> Any            
    @property         
    def finish5(self) -> "Any":
        return (self.native_obj.Finish5)
        
    @finish5.setter     
    def _set_finish5(self, value):
        self.native_obj.Finish5 = value
            
    # -> Any            
    @property         
    def finish6(self) -> "Any":
        return (self.native_obj.Finish6)
        
    @finish6.setter     
    def _set_finish6(self, value):
        self.native_obj.Finish6 = value
            
    # -> Any            
    @property         
    def finish7(self) -> "Any":
        return (self.native_obj.Finish7)
        
    @finish7.setter     
    def _set_finish7(self, value):
        self.native_obj.Finish7 = value
            
    # -> Any            
    @property         
    def finish8(self) -> "Any":
        return (self.native_obj.Finish8)
        
    @finish8.setter     
    def _set_finish8(self, value):
        self.native_obj.Finish8 = value
            
    # -> Any            
    @property         
    def finish9(self) -> "Any":
        return (self.native_obj.Finish9)
        
    @finish9.setter     
    def _set_finish9(self, value):
        self.native_obj.Finish9 = value
            
    # -> Any            
    @property         
    def finishVariance(self) -> "Any":
        return (self.native_obj.FinishVariance)
        
    @finishVariance.setter     
    def _set_finishVariance(self, value):
        self.native_obj.FinishVariance = value
            
    # -> Any            
    @property         
    def fixedMaterialAssignment(self) -> "Any":
        return (self.native_obj.FixedMaterialAssignment)
        
    @fixedMaterialAssignment.setter     
    def _set_fixedMaterialAssignment(self, value):
        self.native_obj.FixedMaterialAssignment = value
            
    # -> Any            
    @property         
    def flag1(self) -> "Any":
        return (self.native_obj.Flag1)
        
    @flag1.setter     
    def _set_flag1(self, value):
        self.native_obj.Flag1 = value
            
    # -> Any            
    @property         
    def flag10(self) -> "Any":
        return (self.native_obj.Flag10)
        
    @flag10.setter     
    def _set_flag10(self, value):
        self.native_obj.Flag10 = value
            
    # -> Any            
    @property         
    def flag11(self) -> "Any":
        return (self.native_obj.Flag11)
        
    @flag11.setter     
    def _set_flag11(self, value):
        self.native_obj.Flag11 = value
            
    # -> Any            
    @property         
    def flag12(self) -> "Any":
        return (self.native_obj.Flag12)
        
    @flag12.setter     
    def _set_flag12(self, value):
        self.native_obj.Flag12 = value
            
    # -> Any            
    @property         
    def flag13(self) -> "Any":
        return (self.native_obj.Flag13)
        
    @flag13.setter     
    def _set_flag13(self, value):
        self.native_obj.Flag13 = value
            
    # -> Any            
    @property         
    def flag14(self) -> "Any":
        return (self.native_obj.Flag14)
        
    @flag14.setter     
    def _set_flag14(self, value):
        self.native_obj.Flag14 = value
            
    # -> Any            
    @property         
    def flag15(self) -> "Any":
        return (self.native_obj.Flag15)
        
    @flag15.setter     
    def _set_flag15(self, value):
        self.native_obj.Flag15 = value
            
    # -> Any            
    @property         
    def flag16(self) -> "Any":
        return (self.native_obj.Flag16)
        
    @flag16.setter     
    def _set_flag16(self, value):
        self.native_obj.Flag16 = value
            
    # -> Any            
    @property         
    def flag17(self) -> "Any":
        return (self.native_obj.Flag17)
        
    @flag17.setter     
    def _set_flag17(self, value):
        self.native_obj.Flag17 = value
            
    # -> Any            
    @property         
    def flag18(self) -> "Any":
        return (self.native_obj.Flag18)
        
    @flag18.setter     
    def _set_flag18(self, value):
        self.native_obj.Flag18 = value
            
    # -> Any            
    @property         
    def flag19(self) -> "Any":
        return (self.native_obj.Flag19)
        
    @flag19.setter     
    def _set_flag19(self, value):
        self.native_obj.Flag19 = value
            
    # -> Any            
    @property         
    def flag2(self) -> "Any":
        return (self.native_obj.Flag2)
        
    @flag2.setter     
    def _set_flag2(self, value):
        self.native_obj.Flag2 = value
            
    # -> Any            
    @property         
    def flag20(self) -> "Any":
        return (self.native_obj.Flag20)
        
    @flag20.setter     
    def _set_flag20(self, value):
        self.native_obj.Flag20 = value
            
    # -> Any            
    @property         
    def flag3(self) -> "Any":
        return (self.native_obj.Flag3)
        
    @flag3.setter     
    def _set_flag3(self, value):
        self.native_obj.Flag3 = value
            
    # -> Any            
    @property         
    def flag4(self) -> "Any":
        return (self.native_obj.Flag4)
        
    @flag4.setter     
    def _set_flag4(self, value):
        self.native_obj.Flag4 = value
            
    # -> Any            
    @property         
    def flag5(self) -> "Any":
        return (self.native_obj.Flag5)
        
    @flag5.setter     
    def _set_flag5(self, value):
        self.native_obj.Flag5 = value
            
    # -> Any            
    @property         
    def flag6(self) -> "Any":
        return (self.native_obj.Flag6)
        
    @flag6.setter     
    def _set_flag6(self, value):
        self.native_obj.Flag6 = value
            
    # -> Any            
    @property         
    def flag7(self) -> "Any":
        return (self.native_obj.Flag7)
        
    @flag7.setter     
    def _set_flag7(self, value):
        self.native_obj.Flag7 = value
            
    # -> Any            
    @property         
    def flag8(self) -> "Any":
        return (self.native_obj.Flag8)
        
    @flag8.setter     
    def _set_flag8(self, value):
        self.native_obj.Flag8 = value
            
    # -> Any            
    @property         
    def flag9(self) -> "Any":
        return (self.native_obj.Flag9)
        
    @flag9.setter     
    def _set_flag9(self, value):
        self.native_obj.Flag9 = value
            
    # -> Any            
    @property         
    def guid(self) -> "Any":
        return (self.native_obj.Guid)
        
    @guid.setter     
    def _set_guid(self, value):
        self.native_obj.Guid = value
            
    # -> Any            
    @property         
    def hyperlink(self) -> "Any":
        return (self.native_obj.Hyperlink)
        
    @hyperlink.setter     
    def _set_hyperlink(self, value):
        self.native_obj.Hyperlink = value
            
    # -> Any            
    @property         
    def hyperlinkAddress(self) -> "Any":
        return (self.native_obj.HyperlinkAddress)
        
    @hyperlinkAddress.setter     
    def _set_hyperlinkAddress(self, value):
        self.native_obj.HyperlinkAddress = value
            
    # -> Any            
    @property         
    def hyperlinkHREF(self) -> "Any":
        return (self.native_obj.HyperlinkHREF)
        
    @hyperlinkHREF.setter     
    def _set_hyperlinkHREF(self, value):
        self.native_obj.HyperlinkHREF = value
            
    # -> Any            
    @property         
    def hyperlinkScreenTip(self) -> "Any":
        return (self.native_obj.HyperlinkScreenTip)
        
    @hyperlinkScreenTip.setter     
    def _set_hyperlinkScreenTip(self, value):
        self.native_obj.HyperlinkScreenTip = value
            
    # -> Any            
    @property         
    def hyperlinkSubAddress(self) -> "Any":
        return (self.native_obj.HyperlinkSubAddress)
        
    @hyperlinkSubAddress.setter     
    def _set_hyperlinkSubAddress(self, value):
        self.native_obj.HyperlinkSubAddress = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def levelingDelay(self) -> "Any":
        return (self.native_obj.LevelingDelay)
        
    @levelingDelay.setter     
    def _set_levelingDelay(self, value):
        self.native_obj.LevelingDelay = value
            
    # -> Any            
    @property         
    def linkedFields(self) -> "Any":
        return (self.native_obj.LinkedFields)
        
    @linkedFields.setter     
    def _set_linkedFields(self, value):
        self.native_obj.LinkedFields = value
            
    # -> Any            
    @property         
    def notes(self) -> "Any":
        return (self.native_obj.Notes)
        
    @notes.setter     
    def _set_notes(self, value):
        self.native_obj.Notes = value
            
    # -> Any            
    @property         
    def number1(self) -> "Any":
        return (self.native_obj.Number1)
        
    @number1.setter     
    def _set_number1(self, value):
        self.native_obj.Number1 = value
            
    # -> Any            
    @property         
    def number10(self) -> "Any":
        return (self.native_obj.Number10)
        
    @number10.setter     
    def _set_number10(self, value):
        self.native_obj.Number10 = value
            
    # -> Any            
    @property         
    def number11(self) -> "Any":
        return (self.native_obj.Number11)
        
    @number11.setter     
    def _set_number11(self, value):
        self.native_obj.Number11 = value
            
    # -> Any            
    @property         
    def number12(self) -> "Any":
        return (self.native_obj.Number12)
        
    @number12.setter     
    def _set_number12(self, value):
        self.native_obj.Number12 = value
            
    # -> Any            
    @property         
    def number13(self) -> "Any":
        return (self.native_obj.Number13)
        
    @number13.setter     
    def _set_number13(self, value):
        self.native_obj.Number13 = value
            
    # -> Any            
    @property         
    def number14(self) -> "Any":
        return (self.native_obj.Number14)
        
    @number14.setter     
    def _set_number14(self, value):
        self.native_obj.Number14 = value
            
    # -> Any            
    @property         
    def number15(self) -> "Any":
        return (self.native_obj.Number15)
        
    @number15.setter     
    def _set_number15(self, value):
        self.native_obj.Number15 = value
            
    # -> Any            
    @property         
    def number16(self) -> "Any":
        return (self.native_obj.Number16)
        
    @number16.setter     
    def _set_number16(self, value):
        self.native_obj.Number16 = value
            
    # -> Any            
    @property         
    def number17(self) -> "Any":
        return (self.native_obj.Number17)
        
    @number17.setter     
    def _set_number17(self, value):
        self.native_obj.Number17 = value
            
    # -> Any            
    @property         
    def number18(self) -> "Any":
        return (self.native_obj.Number18)
        
    @number18.setter     
    def _set_number18(self, value):
        self.native_obj.Number18 = value
            
    # -> Any            
    @property         
    def number19(self) -> "Any":
        return (self.native_obj.Number19)
        
    @number19.setter     
    def _set_number19(self, value):
        self.native_obj.Number19 = value
            
    # -> Any            
    @property         
    def number2(self) -> "Any":
        return (self.native_obj.Number2)
        
    @number2.setter     
    def _set_number2(self, value):
        self.native_obj.Number2 = value
            
    # -> Any            
    @property         
    def number20(self) -> "Any":
        return (self.native_obj.Number20)
        
    @number20.setter     
    def _set_number20(self, value):
        self.native_obj.Number20 = value
            
    # -> Any            
    @property         
    def number3(self) -> "Any":
        return (self.native_obj.Number3)
        
    @number3.setter     
    def _set_number3(self, value):
        self.native_obj.Number3 = value
            
    # -> Any            
    @property         
    def number4(self) -> "Any":
        return (self.native_obj.Number4)
        
    @number4.setter     
    def _set_number4(self, value):
        self.native_obj.Number4 = value
            
    # -> Any            
    @property         
    def number5(self) -> "Any":
        return (self.native_obj.Number5)
        
    @number5.setter     
    def _set_number5(self, value):
        self.native_obj.Number5 = value
            
    # -> Any            
    @property         
    def number6(self) -> "Any":
        return (self.native_obj.Number6)
        
    @number6.setter     
    def _set_number6(self, value):
        self.native_obj.Number6 = value
            
    # -> Any            
    @property         
    def number7(self) -> "Any":
        return (self.native_obj.Number7)
        
    @number7.setter     
    def _set_number7(self, value):
        self.native_obj.Number7 = value
            
    # -> Any            
    @property         
    def number8(self) -> "Any":
        return (self.native_obj.Number8)
        
    @number8.setter     
    def _set_number8(self, value):
        self.native_obj.Number8 = value
            
    # -> Any            
    @property         
    def number9(self) -> "Any":
        return (self.native_obj.Number9)
        
    @number9.setter     
    def _set_number9(self, value):
        self.native_obj.Number9 = value
            
    # -> Any            
    @property         
    def overallocated(self) -> "Any":
        return (self.native_obj.Overallocated)
        
    @overallocated.setter     
    def _set_overallocated(self, value):
        self.native_obj.Overallocated = value
            
    # -> Any            
    @property         
    def overtimeCost(self) -> "Any":
        return (self.native_obj.OvertimeCost)
        
    @overtimeCost.setter     
    def _set_overtimeCost(self, value):
        self.native_obj.OvertimeCost = value
            
    # -> Any            
    @property         
    def overtimeWork(self) -> "Any":
        return (self.native_obj.OvertimeWork)
        
    @overtimeWork.setter     
    def _set_overtimeWork(self, value):
        self.native_obj.OvertimeWork = value
            
    # -> Any            
    @property         
    def owner(self) -> "Any":
        return (self.native_obj.Owner)
        
    @owner.setter     
    def _set_owner(self, value):
        self.native_obj.Owner = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def peak(self) -> "Any":
        return (self.native_obj.Peak)
        
    @peak.setter     
    def _set_peak(self, value):
        self.native_obj.Peak = value
            
    # -> Any            
    @property         
    def percentWorkComplete(self) -> "Any":
        return (self.native_obj.PercentWorkComplete)
        
    @percentWorkComplete.setter     
    def _set_percentWorkComplete(self, value):
        self.native_obj.PercentWorkComplete = value
            
    # -> Any            
    @property         
    def project(self) -> "Any":
        return (self.native_obj.Project)
        
    @project.setter     
    def _set_project(self, value):
        self.native_obj.Project = value
            
    # -> Any            
    @property         
    def regularWork(self) -> "Any":
        return (self.native_obj.RegularWork)
        
    @regularWork.setter     
    def _set_regularWork(self, value):
        self.native_obj.RegularWork = value
            
    # -> Any            
    @property         
    def remainingCost(self) -> "Any":
        return (self.native_obj.RemainingCost)
        
    @remainingCost.setter     
    def _set_remainingCost(self, value):
        self.native_obj.RemainingCost = value
            
    # -> Any            
    @property         
    def remainingOvertimeCost(self) -> "Any":
        return (self.native_obj.RemainingOvertimeCost)
        
    @remainingOvertimeCost.setter     
    def _set_remainingOvertimeCost(self, value):
        self.native_obj.RemainingOvertimeCost = value
            
    # -> Any            
    @property         
    def remainingOvertimeWork(self) -> "Any":
        return (self.native_obj.RemainingOvertimeWork)
        
    @remainingOvertimeWork.setter     
    def _set_remainingOvertimeWork(self, value):
        self.native_obj.RemainingOvertimeWork = value
            
    # -> Any            
    @property         
    def remainingWork(self) -> "Any":
        return (self.native_obj.RemainingWork)
        
    @remainingWork.setter     
    def _set_remainingWork(self, value):
        self.native_obj.RemainingWork = value
            
    # -> Any            
    @property         
    def resource(self) -> "Any":
        return (self.native_obj.Resource)
        
    @resource.setter     
    def _set_resource(self, value):
        self.native_obj.Resource = value
            
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
    def resourceRequestType(self) -> "Any":
        return (self.native_obj.ResourceRequestType)
        
    @resourceRequestType.setter     
    def _set_resourceRequestType(self, value):
        self.native_obj.ResourceRequestType = value
            
    # -> Any            
    @property         
    def resourceType(self) -> "Any":
        return (self.native_obj.ResourceType)
        
    @resourceType.setter     
    def _set_resourceType(self, value):
        self.native_obj.ResourceType = value
            
    # -> Any            
    @property         
    def resourceUniqueID(self) -> "Any":
        return (self.native_obj.ResourceUniqueID)
        
    @resourceUniqueID.setter     
    def _set_resourceUniqueID(self, value):
        self.native_obj.ResourceUniqueID = value
            
    # -> Any            
    @property         
    def responsePending(self) -> "Any":
        return (self.native_obj.ResponsePending)
        
    @responsePending.setter     
    def _set_responsePending(self, value):
        self.native_obj.ResponsePending = value
            
    # -> Any            
    @property         
    def start(self) -> "Any":
        return (self.native_obj.Start)
        
    @start.setter     
    def _set_start(self, value):
        self.native_obj.Start = value
            
    # -> Any            
    @property         
    def start1(self) -> "Any":
        return (self.native_obj.Start1)
        
    @start1.setter     
    def _set_start1(self, value):
        self.native_obj.Start1 = value
            
    # -> Any            
    @property         
    def start10(self) -> "Any":
        return (self.native_obj.Start10)
        
    @start10.setter     
    def _set_start10(self, value):
        self.native_obj.Start10 = value
            
    # -> Any            
    @property         
    def start2(self) -> "Any":
        return (self.native_obj.Start2)
        
    @start2.setter     
    def _set_start2(self, value):
        self.native_obj.Start2 = value
            
    # -> Any            
    @property         
    def start3(self) -> "Any":
        return (self.native_obj.Start3)
        
    @start3.setter     
    def _set_start3(self, value):
        self.native_obj.Start3 = value
            
    # -> Any            
    @property         
    def start4(self) -> "Any":
        return (self.native_obj.Start4)
        
    @start4.setter     
    def _set_start4(self, value):
        self.native_obj.Start4 = value
            
    # -> Any            
    @property         
    def start5(self) -> "Any":
        return (self.native_obj.Start5)
        
    @start5.setter     
    def _set_start5(self, value):
        self.native_obj.Start5 = value
            
    # -> Any            
    @property         
    def start6(self) -> "Any":
        return (self.native_obj.Start6)
        
    @start6.setter     
    def _set_start6(self, value):
        self.native_obj.Start6 = value
            
    # -> Any            
    @property         
    def start7(self) -> "Any":
        return (self.native_obj.Start7)
        
    @start7.setter     
    def _set_start7(self, value):
        self.native_obj.Start7 = value
            
    # -> Any            
    @property         
    def start8(self) -> "Any":
        return (self.native_obj.Start8)
        
    @start8.setter     
    def _set_start8(self, value):
        self.native_obj.Start8 = value
            
    # -> Any            
    @property         
    def start9(self) -> "Any":
        return (self.native_obj.Start9)
        
    @start9.setter     
    def _set_start9(self, value):
        self.native_obj.Start9 = value
            
    # -> Any            
    @property         
    def startVariance(self) -> "Any":
        return (self.native_obj.StartVariance)
        
    @startVariance.setter     
    def _set_startVariance(self, value):
        self.native_obj.StartVariance = value
            
    # -> Any            
    @property         
    def summary(self) -> "Any":
        return (self.native_obj.Summary)
        
    @summary.setter     
    def _set_summary(self, value):
        self.native_obj.Summary = value
            
    # -> Any            
    @property         
    def sV(self) -> "Any":
        return (self.native_obj.SV)
        
    @sV.setter     
    def _set_sV(self, value):
        self.native_obj.SV = value
            
    # -> Any            
    @property         
    def task(self) -> "Any":
        return (self.native_obj.Task)
        
    @task.setter     
    def _set_task(self, value):
        self.native_obj.Task = value
            
    # -> Any            
    @property         
    def taskGuid(self) -> "Any":
        return (self.native_obj.TaskGuid)
        
    @taskGuid.setter     
    def _set_taskGuid(self, value):
        self.native_obj.TaskGuid = value
            
    # -> Any            
    @property         
    def taskID(self) -> "Any":
        return (self.native_obj.TaskID)
        
    @taskID.setter     
    def _set_taskID(self, value):
        self.native_obj.TaskID = value
            
    # -> Any            
    @property         
    def taskName(self) -> "Any":
        return (self.native_obj.TaskName)
        
    @taskName.setter     
    def _set_taskName(self, value):
        self.native_obj.TaskName = value
            
    # -> Any            
    @property         
    def taskOutlineNumber(self) -> "Any":
        return (self.native_obj.TaskOutlineNumber)
        
    @taskOutlineNumber.setter     
    def _set_taskOutlineNumber(self, value):
        self.native_obj.TaskOutlineNumber = value
            
    # -> Any            
    @property         
    def taskSummaryName(self) -> "Any":
        return (self.native_obj.TaskSummaryName)
        
    @taskSummaryName.setter     
    def _set_taskSummaryName(self, value):
        self.native_obj.TaskSummaryName = value
            
    # -> Any            
    @property         
    def taskUniqueID(self) -> "Any":
        return (self.native_obj.TaskUniqueID)
        
    @taskUniqueID.setter     
    def _set_taskUniqueID(self, value):
        self.native_obj.TaskUniqueID = value
            
    # -> Any            
    @property         
    def teamStatusPending(self) -> "Any":
        return (self.native_obj.TeamStatusPending)
        
    @teamStatusPending.setter     
    def _set_teamStatusPending(self, value):
        self.native_obj.TeamStatusPending = value
            
    # -> Any            
    @property         
    def text1(self) -> "Any":
        return (self.native_obj.Text1)
        
    @text1.setter     
    def _set_text1(self, value):
        self.native_obj.Text1 = value
            
    # -> Any            
    @property         
    def text10(self) -> "Any":
        return (self.native_obj.Text10)
        
    @text10.setter     
    def _set_text10(self, value):
        self.native_obj.Text10 = value
            
    # -> Any            
    @property         
    def text11(self) -> "Any":
        return (self.native_obj.Text11)
        
    @text11.setter     
    def _set_text11(self, value):
        self.native_obj.Text11 = value
            
    # -> Any            
    @property         
    def text12(self) -> "Any":
        return (self.native_obj.Text12)
        
    @text12.setter     
    def _set_text12(self, value):
        self.native_obj.Text12 = value
            
    # -> Any            
    @property         
    def text13(self) -> "Any":
        return (self.native_obj.Text13)
        
    @text13.setter     
    def _set_text13(self, value):
        self.native_obj.Text13 = value
            
    # -> Any            
    @property         
    def text14(self) -> "Any":
        return (self.native_obj.Text14)
        
    @text14.setter     
    def _set_text14(self, value):
        self.native_obj.Text14 = value
            
    # -> Any            
    @property         
    def text15(self) -> "Any":
        return (self.native_obj.Text15)
        
    @text15.setter     
    def _set_text15(self, value):
        self.native_obj.Text15 = value
            
    # -> Any            
    @property         
    def text16(self) -> "Any":
        return (self.native_obj.Text16)
        
    @text16.setter     
    def _set_text16(self, value):
        self.native_obj.Text16 = value
            
    # -> Any            
    @property         
    def text17(self) -> "Any":
        return (self.native_obj.Text17)
        
    @text17.setter     
    def _set_text17(self, value):
        self.native_obj.Text17 = value
            
    # -> Any            
    @property         
    def text18(self) -> "Any":
        return (self.native_obj.Text18)
        
    @text18.setter     
    def _set_text18(self, value):
        self.native_obj.Text18 = value
            
    # -> Any            
    @property         
    def text19(self) -> "Any":
        return (self.native_obj.Text19)
        
    @text19.setter     
    def _set_text19(self, value):
        self.native_obj.Text19 = value
            
    # -> Any            
    @property         
    def text2(self) -> "Any":
        return (self.native_obj.Text2)
        
    @text2.setter     
    def _set_text2(self, value):
        self.native_obj.Text2 = value
            
    # -> Any            
    @property         
    def text20(self) -> "Any":
        return (self.native_obj.Text20)
        
    @text20.setter     
    def _set_text20(self, value):
        self.native_obj.Text20 = value
            
    # -> Any            
    @property         
    def text21(self) -> "Any":
        return (self.native_obj.Text21)
        
    @text21.setter     
    def _set_text21(self, value):
        self.native_obj.Text21 = value
            
    # -> Any            
    @property         
    def text22(self) -> "Any":
        return (self.native_obj.Text22)
        
    @text22.setter     
    def _set_text22(self, value):
        self.native_obj.Text22 = value
            
    # -> Any            
    @property         
    def text23(self) -> "Any":
        return (self.native_obj.Text23)
        
    @text23.setter     
    def _set_text23(self, value):
        self.native_obj.Text23 = value
            
    # -> Any            
    @property         
    def text24(self) -> "Any":
        return (self.native_obj.Text24)
        
    @text24.setter     
    def _set_text24(self, value):
        self.native_obj.Text24 = value
            
    # -> Any            
    @property         
    def text25(self) -> "Any":
        return (self.native_obj.Text25)
        
    @text25.setter     
    def _set_text25(self, value):
        self.native_obj.Text25 = value
            
    # -> Any            
    @property         
    def text26(self) -> "Any":
        return (self.native_obj.Text26)
        
    @text26.setter     
    def _set_text26(self, value):
        self.native_obj.Text26 = value
            
    # -> Any            
    @property         
    def text27(self) -> "Any":
        return (self.native_obj.Text27)
        
    @text27.setter     
    def _set_text27(self, value):
        self.native_obj.Text27 = value
            
    # -> Any            
    @property         
    def text28(self) -> "Any":
        return (self.native_obj.Text28)
        
    @text28.setter     
    def _set_text28(self, value):
        self.native_obj.Text28 = value
            
    # -> Any            
    @property         
    def text29(self) -> "Any":
        return (self.native_obj.Text29)
        
    @text29.setter     
    def _set_text29(self, value):
        self.native_obj.Text29 = value
            
    # -> Any            
    @property         
    def text3(self) -> "Any":
        return (self.native_obj.Text3)
        
    @text3.setter     
    def _set_text3(self, value):
        self.native_obj.Text3 = value
            
    # -> Any            
    @property         
    def text30(self) -> "Any":
        return (self.native_obj.Text30)
        
    @text30.setter     
    def _set_text30(self, value):
        self.native_obj.Text30 = value
            
    # -> Any            
    @property         
    def text4(self) -> "Any":
        return (self.native_obj.Text4)
        
    @text4.setter     
    def _set_text4(self, value):
        self.native_obj.Text4 = value
            
    # -> Any            
    @property         
    def text5(self) -> "Any":
        return (self.native_obj.Text5)
        
    @text5.setter     
    def _set_text5(self, value):
        self.native_obj.Text5 = value
            
    # -> Any            
    @property         
    def text6(self) -> "Any":
        return (self.native_obj.Text6)
        
    @text6.setter     
    def _set_text6(self, value):
        self.native_obj.Text6 = value
            
    # -> Any            
    @property         
    def text7(self) -> "Any":
        return (self.native_obj.Text7)
        
    @text7.setter     
    def _set_text7(self, value):
        self.native_obj.Text7 = value
            
    # -> Any            
    @property         
    def text8(self) -> "Any":
        return (self.native_obj.Text8)
        
    @text8.setter     
    def _set_text8(self, value):
        self.native_obj.Text8 = value
            
    # -> Any            
    @property         
    def text9(self) -> "Any":
        return (self.native_obj.Text9)
        
    @text9.setter     
    def _set_text9(self, value):
        self.native_obj.Text9 = value
            
    # -> Any            
    @property         
    def uniqueID(self) -> "Any":
        return (self.native_obj.UniqueID)
        
    @uniqueID.setter     
    def _set_uniqueID(self, value):
        self.native_obj.UniqueID = value
            
    # -> Any            
    @property         
    def units(self) -> "Any":
        return (self.native_obj.Units)
        
    @units.setter     
    def _set_units(self, value):
        self.native_obj.Units = value
            
    # -> Any            
    @property         
    def updateNeeded(self) -> "Any":
        return (self.native_obj.UpdateNeeded)
        
    @updateNeeded.setter     
    def _set_updateNeeded(self, value):
        self.native_obj.UpdateNeeded = value
            
    # -> Any            
    @property         
    def vAC(self) -> "Any":
        return (self.native_obj.VAC)
        
    @vAC.setter     
    def _set_vAC(self, value):
        self.native_obj.VAC = value
            
    # -> Any            
    @property         
    def wBS(self) -> "Any":
        return (self.native_obj.WBS)
        
    @wBS.setter     
    def _set_wBS(self, value):
        self.native_obj.WBS = value
            
    # -> Any            
    @property         
    def work(self) -> "Any":
        return (self.native_obj.Work)
        
    @work.setter     
    def _set_work(self, value):
        self.native_obj.Work = value
            
    # -> Any            
    @property         
    def workContour(self) -> "Any":
        return (self.native_obj.WorkContour)
        
    @workContour.setter     
    def _set_workContour(self, value):
        self.native_obj.WorkContour = value
            
    # -> Any            
    @property         
    def workVariance(self) -> "Any":
        return (self.native_obj.WorkVariance)
        
    @workVariance.setter     
    def _set_workVariance(self, value):
        self.native_obj.WorkVariance = value
            
# end "Assignment"       
        