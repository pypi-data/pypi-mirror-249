

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Task:
    # Object "Task" class for software "Project"
    
    properties = ['active', 'actualCost', 'actualDuration', 'actualFinish', 'actualOvertimeCost', 'actualOvertimeWork', 'actualStart', 'actualWork', 'aCWP', 'application', 'assignments', 'baseline10BudgetCost', 'baseline10BudgetWork', 'baseline10Cost', 'baseline10DeliverableFinish', 'baseline10DeliverableStart', 'baseline10Duration', 'baseline10DurationEstimated', 'baseline10DurationText', 'baseline10Finish', 'baseline10FinishText', 'baseline10FixedCost', 'baseline10FixedCostAccrual', 'baseline10Start', 'baseline10StartText', 'baseline10Work', 'baseline1BudgetCost', 'baseline1BudgetWork', 'baseline1Cost', 'baseline1DeliverableFinish', 'baseline1DeliverableStart', 'baseline1Duration', 'baseline1DurationEstimated', 'baseline1DurationText', 'baseline1Finish', 'baseline1FinishText', 'baseline1FixedCost', 'baseline1FixedCostAccrual', 'baseline1Start', 'baseline1StartText', 'baseline1Work', 'baseline2BudgetCost', 'baseline2BudgetWork', 'baseline2Cost', 'baseline2DeliverableFinish', 'baseline2DeliverableStart', 'baseline2Duration', 'baseline2DurationEstimated', 'baseline2DurationText', 'baseline2Finish', 'baseline2FinishText', 'baseline2FixedCost', 'baseline2FixedCostAccrual', 'baseline2Start', 'baseline2StartText', 'baseline2Work', 'baseline3BudgetCost', 'baseline3BudgetWork', 'baseline3Cost', 'baseline3DeliverableFinish', 'baseline3DeliverableStart', 'baseline3Duration', 'baseline3DurationEstimated', 'baseline3DurationText', 'baseline3Finish', 'baseline3FinishText', 'baseline3FixedCost', 'baseline3FixedCostAccrual', 'baseline3Start', 'baseline3StartText', 'baseline3Work', 'baseline4BudgetCost', 'baseline4BudgetWork', 'baseline4Cost', 'baseline4DeliverableFinish', 'baseline4DeliverableStart', 'baseline4Duration', 'baseline4DurationEstimated', 'baseline4DurationText', 'baseline4Finish', 'baseline4FinishText', 'baseline4FixedCost', 'baseline4FixedCostAccrual', 'baseline4Start', 'baseline4StartText', 'baseline4Work', 'baseline5BudgetCost', 'baseline5BudgetWork', 'baseline5Cost', 'baseline5DeliverableFinish', 'baseline5DeliverableStart', 'baseline5Duration', 'baseline5DurationEstimated', 'baseline5DurationText', 'baseline5Finish', 'baseline5FinishText', 'baseline5FixedCost', 'baseline5FixedCostAccrual', 'baseline5Start', 'baseline5StartText', 'baseline5Work', 'baseline6BudgetCost', 'baseline6BudgetWork', 'baseline6Cost', 'baseline6DeliverableFinish', 'baseline6DeliverableStart', 'baseline6Duration', 'baseline6DurationEstimated', 'baseline6DurationText', 'baseline6Finish', 'baseline6FinishText', 'baseline6FixedCost', 'baseline6FixedCostAccrual', 'baseline6Start', 'baseline6StartText', 'baseline6Work', 'baseline7BudgetCost', 'baseline7BudgetWork', 'baseline7Cost', 'baseline7DeliverableFinish', 'baseline7DeliverableStart', 'baseline7Duration', 'baseline7DurationEstimated', 'baseline7DurationText', 'baseline7Finish', 'baseline7FinishText', 'baseline7FixedCost', 'baseline7FixedCostAccrual', 'baseline7Start', 'baseline7StartText', 'baseline7Work', 'baseline8BudgetCost', 'baseline8BudgetWork', 'baseline8Cost', 'baseline8DeliverableFinish', 'baseline8DeliverableStart', 'baseline8Duration', 'baseline8DurationEstimated', 'baseline8DurationText', 'baseline8Finish', 'baseline8FinishText', 'baseline8FixedCost', 'baseline8FixedCostAccrual', 'baseline8Start', 'baseline8StartText', 'baseline8Work', 'baseline9BudgetCost', 'baseline9BudgetWork', 'baseline9Cost', 'baseline9DeliverableFinish', 'baseline9DeliverableStart', 'baseline9Duration', 'baseline9DurationEstimated', 'baseline9DurationText', 'baseline9Finish', 'baseline9FinishText', 'baseline9FixedCost', 'baseline9FixedCostAccrual', 'baseline9Start', 'baseline9StartText', 'baseline9Work', 'baselineBudgetCost', 'baselineBudgetWork', 'baselineCost', 'baselineDeliverableFinish', 'baselineDeliverableStart', 'baselineDuration', 'baselineDurationEstimated', 'baselineDurationText', 'baselineFinish', 'baselineFinishText', 'baselineFixedCost', 'baselineFixedCostAccrual', 'baselineStart', 'baselineStartText', 'baselineWork', 'bCWP', 'bCWS', 'budgetCost', 'budgetWork', 'calendar', 'calendarGuid', 'calendarObject', 'compliant', 'confirmed', 'constraintDate', 'constraintType', 'contact', 'cost', 'cost1', 'cost10', 'cost2', 'cost3', 'cost4', 'cost5', 'cost6', 'cost7', 'cost8', 'cost9', 'costVariance', 'cPI', 'created', 'critical', 'cV', 'cVPercent', 'date1', 'date10', 'date2', 'date3', 'date4', 'date5', 'date6', 'date7', 'date8', 'date9', 'deadline', 'deliverableFinish', 'deliverableGuid', 'deliverableName', 'deliverableStart', 'deliverableType', 'duration', 'duration1', 'duration10', 'duration10Estimated', 'duration1Estimated', 'duration2', 'duration2Estimated', 'duration3', 'duration3Estimated', 'duration4', 'duration4Estimated', 'duration5', 'duration5Estimated', 'duration6', 'duration6Estimated', 'duration7', 'duration7Estimated', 'duration8', 'duration8Estimated', 'duration9', 'duration9Estimated', 'durationText', 'durationVariance', 'eAC', 'earlyFinish', 'earlyStart', 'earnedValueMethod', 'effortDriven', 'errorMessage', 'estimated', 'externalTask', 'finish', 'finish1', 'finish10', 'finish2', 'finish3', 'finish4', 'finish5', 'finish6', 'finish7', 'finish8', 'finish9', 'finishSlack', 'finishText', 'finishVariance', 'fixedCost', 'fixedCostAccrual', 'flag1', 'flag10', 'flag11', 'flag12', 'flag13', 'flag14', 'flag15', 'flag16', 'flag17', 'flag18', 'flag19', 'flag2', 'flag20', 'flag3', 'flag4', 'flag5', 'flag6', 'flag7', 'flag8', 'flag9', 'freeSlack', 'groupBySummary', 'guid', 'hideBar', 'hyperlink', 'hyperlinkAddress', 'hyperlinkHREF', 'hyperlinkScreenTip', 'hyperlinkSubAddress', 'iD', 'ignoreResourceCalendar', 'ignoreWarnings', 'index', 'isDurationValid', 'isFinishValid', 'isPublished', 'isStartValid', 'lateFinish', 'lateStart', 'levelIndividualAssignments', 'levelingCanSplit', 'levelingDelay', 'linkedFields', 'manual', 'marked', 'milestone', 'name', 'notes', 'number1', 'number10', 'number11', 'number12', 'number13', 'number14', 'number15', 'number16', 'number17', 'number18', 'number19', 'number2', 'number20', 'number3', 'number4', 'number5', 'number6', 'number7', 'number8', 'number9', 'objects', 'outlineChildren', 'outlineCode1', 'outlineCode10', 'outlineCode2', 'outlineCode3', 'outlineCode4', 'outlineCode5', 'outlineCode6', 'outlineCode7', 'outlineCode8', 'outlineCode9', 'outlineLevel', 'outlineNumber', 'outlineParent', 'overallocated', 'overtimeCost', 'overtimeWork', 'parent', 'pathDrivenSuccessor', 'pathDrivingPredecessor', 'pathPredecessor', 'pathSuccessor', 'percentComplete', 'percentWorkComplete', 'physicalPercentComplete', 'placeholder', 'predecessors', 'predecessorTasks', 'preleveledFinish', 'preleveledStart', 'priority', 'project', 'recalcFlags', 'recurring', 'regularWork', 'remainingCost', 'remainingDuration', 'remainingOvertimeCost', 'remainingOvertimeWork', 'remainingWork', 'resourceGroup', 'resourceInitials', 'resourceNames', 'resourcePhonetics', 'resources', 'responsePending', 'resume', 'rollup', 'scheduledDuration', 'scheduledFinish', 'scheduledStart', 'sPI', 'splitParts', 'start', 'start1', 'start10', 'start2', 'start3', 'start4', 'start5', 'start6', 'start7', 'start8', 'start9', 'startDriver', 'startSlack', 'startText', 'startVariance', 'status', 'statusManagerName', 'stop', 'subproject', 'subProjectReadOnly', 'successors', 'successorTasks', 'summary', 'sV', 'sVPercent', 'taskDependencies', 'tCPI', 'teamStatusPending', 'text1', 'text10', 'text11', 'text12', 'text13', 'text14', 'text15', 'text16', 'text17', 'text18', 'text19', 'text2', 'text20', 'text21', 'text22', 'text23', 'text24', 'text25', 'text26', 'text27', 'text28', 'text29', 'text3', 'text30', 'text4', 'text5', 'text6', 'text7', 'text8', 'text9', 'totalSlack', 'type', 'uniqueID', 'uniqueIDPredecessors', 'uniqueIDSuccessors', 'updateNeeded', 'vAC', 'warning', 'wBS', 'wBSPredecessors', 'wBSSuccessors', 'work', 'workVariance']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def active(self) -> "Any":
        return (self.native_obj.Active)
        
    @active.setter     
    def _set_active(self, value):
        self.native_obj.Active = value
            
    # -> Any            
    @property         
    def actualCost(self) -> "Any":
        return (self.native_obj.ActualCost)
        
    @actualCost.setter     
    def _set_actualCost(self, value):
        self.native_obj.ActualCost = value
            
    # -> Any            
    @property         
    def actualDuration(self) -> "Any":
        return (self.native_obj.ActualDuration)
        
    @actualDuration.setter     
    def _set_actualDuration(self, value):
        self.native_obj.ActualDuration = value
            
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
    def assignments(self) -> "Any":
        return (self.native_obj.Assignments)
        
    @assignments.setter     
    def _set_assignments(self, value):
        self.native_obj.Assignments = value
            
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
    def baseline10DeliverableFinish(self) -> "Any":
        return (self.native_obj.Baseline10DeliverableFinish)
        
    @baseline10DeliverableFinish.setter     
    def _set_baseline10DeliverableFinish(self, value):
        self.native_obj.Baseline10DeliverableFinish = value
            
    # -> Any            
    @property         
    def baseline10DeliverableStart(self) -> "Any":
        return (self.native_obj.Baseline10DeliverableStart)
        
    @baseline10DeliverableStart.setter     
    def _set_baseline10DeliverableStart(self, value):
        self.native_obj.Baseline10DeliverableStart = value
            
    # -> Any            
    @property         
    def baseline10Duration(self) -> "Any":
        return (self.native_obj.Baseline10Duration)
        
    @baseline10Duration.setter     
    def _set_baseline10Duration(self, value):
        self.native_obj.Baseline10Duration = value
            
    # -> Any            
    @property         
    def baseline10DurationEstimated(self) -> "Any":
        return (self.native_obj.Baseline10DurationEstimated)
        
    @baseline10DurationEstimated.setter     
    def _set_baseline10DurationEstimated(self, value):
        self.native_obj.Baseline10DurationEstimated = value
            
    # -> Any            
    @property         
    def baseline10DurationText(self) -> "Any":
        return (self.native_obj.Baseline10DurationText)
        
    @baseline10DurationText.setter     
    def _set_baseline10DurationText(self, value):
        self.native_obj.Baseline10DurationText = value
            
    # -> Any            
    @property         
    def baseline10Finish(self) -> "Any":
        return (self.native_obj.Baseline10Finish)
        
    @baseline10Finish.setter     
    def _set_baseline10Finish(self, value):
        self.native_obj.Baseline10Finish = value
            
    # -> Any            
    @property         
    def baseline10FinishText(self) -> "Any":
        return (self.native_obj.Baseline10FinishText)
        
    @baseline10FinishText.setter     
    def _set_baseline10FinishText(self, value):
        self.native_obj.Baseline10FinishText = value
            
    # -> Any            
    @property         
    def baseline10FixedCost(self) -> "Any":
        return (self.native_obj.Baseline10FixedCost)
        
    @baseline10FixedCost.setter     
    def _set_baseline10FixedCost(self, value):
        self.native_obj.Baseline10FixedCost = value
            
    # -> Any            
    @property         
    def baseline10FixedCostAccrual(self) -> "Any":
        return (self.native_obj.Baseline10FixedCostAccrual)
        
    @baseline10FixedCostAccrual.setter     
    def _set_baseline10FixedCostAccrual(self, value):
        self.native_obj.Baseline10FixedCostAccrual = value
            
    # -> Any            
    @property         
    def baseline10Start(self) -> "Any":
        return (self.native_obj.Baseline10Start)
        
    @baseline10Start.setter     
    def _set_baseline10Start(self, value):
        self.native_obj.Baseline10Start = value
            
    # -> Any            
    @property         
    def baseline10StartText(self) -> "Any":
        return (self.native_obj.Baseline10StartText)
        
    @baseline10StartText.setter     
    def _set_baseline10StartText(self, value):
        self.native_obj.Baseline10StartText = value
            
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
    def baseline1DeliverableFinish(self) -> "Any":
        return (self.native_obj.Baseline1DeliverableFinish)
        
    @baseline1DeliverableFinish.setter     
    def _set_baseline1DeliverableFinish(self, value):
        self.native_obj.Baseline1DeliverableFinish = value
            
    # -> Any            
    @property         
    def baseline1DeliverableStart(self) -> "Any":
        return (self.native_obj.Baseline1DeliverableStart)
        
    @baseline1DeliverableStart.setter     
    def _set_baseline1DeliverableStart(self, value):
        self.native_obj.Baseline1DeliverableStart = value
            
    # -> Any            
    @property         
    def baseline1Duration(self) -> "Any":
        return (self.native_obj.Baseline1Duration)
        
    @baseline1Duration.setter     
    def _set_baseline1Duration(self, value):
        self.native_obj.Baseline1Duration = value
            
    # -> Any            
    @property         
    def baseline1DurationEstimated(self) -> "Any":
        return (self.native_obj.Baseline1DurationEstimated)
        
    @baseline1DurationEstimated.setter     
    def _set_baseline1DurationEstimated(self, value):
        self.native_obj.Baseline1DurationEstimated = value
            
    # -> Any            
    @property         
    def baseline1DurationText(self) -> "Any":
        return (self.native_obj.Baseline1DurationText)
        
    @baseline1DurationText.setter     
    def _set_baseline1DurationText(self, value):
        self.native_obj.Baseline1DurationText = value
            
    # -> Any            
    @property         
    def baseline1Finish(self) -> "Any":
        return (self.native_obj.Baseline1Finish)
        
    @baseline1Finish.setter     
    def _set_baseline1Finish(self, value):
        self.native_obj.Baseline1Finish = value
            
    # -> Any            
    @property         
    def baseline1FinishText(self) -> "Any":
        return (self.native_obj.Baseline1FinishText)
        
    @baseline1FinishText.setter     
    def _set_baseline1FinishText(self, value):
        self.native_obj.Baseline1FinishText = value
            
    # -> Any            
    @property         
    def baseline1FixedCost(self) -> "Any":
        return (self.native_obj.Baseline1FixedCost)
        
    @baseline1FixedCost.setter     
    def _set_baseline1FixedCost(self, value):
        self.native_obj.Baseline1FixedCost = value
            
    # -> Any            
    @property         
    def baseline1FixedCostAccrual(self) -> "Any":
        return (self.native_obj.Baseline1FixedCostAccrual)
        
    @baseline1FixedCostAccrual.setter     
    def _set_baseline1FixedCostAccrual(self, value):
        self.native_obj.Baseline1FixedCostAccrual = value
            
    # -> Any            
    @property         
    def baseline1Start(self) -> "Any":
        return (self.native_obj.Baseline1Start)
        
    @baseline1Start.setter     
    def _set_baseline1Start(self, value):
        self.native_obj.Baseline1Start = value
            
    # -> Any            
    @property         
    def baseline1StartText(self) -> "Any":
        return (self.native_obj.Baseline1StartText)
        
    @baseline1StartText.setter     
    def _set_baseline1StartText(self, value):
        self.native_obj.Baseline1StartText = value
            
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
    def baseline2DeliverableFinish(self) -> "Any":
        return (self.native_obj.Baseline2DeliverableFinish)
        
    @baseline2DeliverableFinish.setter     
    def _set_baseline2DeliverableFinish(self, value):
        self.native_obj.Baseline2DeliverableFinish = value
            
    # -> Any            
    @property         
    def baseline2DeliverableStart(self) -> "Any":
        return (self.native_obj.Baseline2DeliverableStart)
        
    @baseline2DeliverableStart.setter     
    def _set_baseline2DeliverableStart(self, value):
        self.native_obj.Baseline2DeliverableStart = value
            
    # -> Any            
    @property         
    def baseline2Duration(self) -> "Any":
        return (self.native_obj.Baseline2Duration)
        
    @baseline2Duration.setter     
    def _set_baseline2Duration(self, value):
        self.native_obj.Baseline2Duration = value
            
    # -> Any            
    @property         
    def baseline2DurationEstimated(self) -> "Any":
        return (self.native_obj.Baseline2DurationEstimated)
        
    @baseline2DurationEstimated.setter     
    def _set_baseline2DurationEstimated(self, value):
        self.native_obj.Baseline2DurationEstimated = value
            
    # -> Any            
    @property         
    def baseline2DurationText(self) -> "Any":
        return (self.native_obj.Baseline2DurationText)
        
    @baseline2DurationText.setter     
    def _set_baseline2DurationText(self, value):
        self.native_obj.Baseline2DurationText = value
            
    # -> Any            
    @property         
    def baseline2Finish(self) -> "Any":
        return (self.native_obj.Baseline2Finish)
        
    @baseline2Finish.setter     
    def _set_baseline2Finish(self, value):
        self.native_obj.Baseline2Finish = value
            
    # -> Any            
    @property         
    def baseline2FinishText(self) -> "Any":
        return (self.native_obj.Baseline2FinishText)
        
    @baseline2FinishText.setter     
    def _set_baseline2FinishText(self, value):
        self.native_obj.Baseline2FinishText = value
            
    # -> Any            
    @property         
    def baseline2FixedCost(self) -> "Any":
        return (self.native_obj.Baseline2FixedCost)
        
    @baseline2FixedCost.setter     
    def _set_baseline2FixedCost(self, value):
        self.native_obj.Baseline2FixedCost = value
            
    # -> Any            
    @property         
    def baseline2FixedCostAccrual(self) -> "Any":
        return (self.native_obj.Baseline2FixedCostAccrual)
        
    @baseline2FixedCostAccrual.setter     
    def _set_baseline2FixedCostAccrual(self, value):
        self.native_obj.Baseline2FixedCostAccrual = value
            
    # -> Any            
    @property         
    def baseline2Start(self) -> "Any":
        return (self.native_obj.Baseline2Start)
        
    @baseline2Start.setter     
    def _set_baseline2Start(self, value):
        self.native_obj.Baseline2Start = value
            
    # -> Any            
    @property         
    def baseline2StartText(self) -> "Any":
        return (self.native_obj.Baseline2StartText)
        
    @baseline2StartText.setter     
    def _set_baseline2StartText(self, value):
        self.native_obj.Baseline2StartText = value
            
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
    def baseline3DeliverableFinish(self) -> "Any":
        return (self.native_obj.Baseline3DeliverableFinish)
        
    @baseline3DeliverableFinish.setter     
    def _set_baseline3DeliverableFinish(self, value):
        self.native_obj.Baseline3DeliverableFinish = value
            
    # -> Any            
    @property         
    def baseline3DeliverableStart(self) -> "Any":
        return (self.native_obj.Baseline3DeliverableStart)
        
    @baseline3DeliverableStart.setter     
    def _set_baseline3DeliverableStart(self, value):
        self.native_obj.Baseline3DeliverableStart = value
            
    # -> Any            
    @property         
    def baseline3Duration(self) -> "Any":
        return (self.native_obj.Baseline3Duration)
        
    @baseline3Duration.setter     
    def _set_baseline3Duration(self, value):
        self.native_obj.Baseline3Duration = value
            
    # -> Any            
    @property         
    def baseline3DurationEstimated(self) -> "Any":
        return (self.native_obj.Baseline3DurationEstimated)
        
    @baseline3DurationEstimated.setter     
    def _set_baseline3DurationEstimated(self, value):
        self.native_obj.Baseline3DurationEstimated = value
            
    # -> Any            
    @property         
    def baseline3DurationText(self) -> "Any":
        return (self.native_obj.Baseline3DurationText)
        
    @baseline3DurationText.setter     
    def _set_baseline3DurationText(self, value):
        self.native_obj.Baseline3DurationText = value
            
    # -> Any            
    @property         
    def baseline3Finish(self) -> "Any":
        return (self.native_obj.Baseline3Finish)
        
    @baseline3Finish.setter     
    def _set_baseline3Finish(self, value):
        self.native_obj.Baseline3Finish = value
            
    # -> Any            
    @property         
    def baseline3FinishText(self) -> "Any":
        return (self.native_obj.Baseline3FinishText)
        
    @baseline3FinishText.setter     
    def _set_baseline3FinishText(self, value):
        self.native_obj.Baseline3FinishText = value
            
    # -> Any            
    @property         
    def baseline3FixedCost(self) -> "Any":
        return (self.native_obj.Baseline3FixedCost)
        
    @baseline3FixedCost.setter     
    def _set_baseline3FixedCost(self, value):
        self.native_obj.Baseline3FixedCost = value
            
    # -> Any            
    @property         
    def baseline3FixedCostAccrual(self) -> "Any":
        return (self.native_obj.Baseline3FixedCostAccrual)
        
    @baseline3FixedCostAccrual.setter     
    def _set_baseline3FixedCostAccrual(self, value):
        self.native_obj.Baseline3FixedCostAccrual = value
            
    # -> Any            
    @property         
    def baseline3Start(self) -> "Any":
        return (self.native_obj.Baseline3Start)
        
    @baseline3Start.setter     
    def _set_baseline3Start(self, value):
        self.native_obj.Baseline3Start = value
            
    # -> Any            
    @property         
    def baseline3StartText(self) -> "Any":
        return (self.native_obj.Baseline3StartText)
        
    @baseline3StartText.setter     
    def _set_baseline3StartText(self, value):
        self.native_obj.Baseline3StartText = value
            
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
    def baseline4DeliverableFinish(self) -> "Any":
        return (self.native_obj.Baseline4DeliverableFinish)
        
    @baseline4DeliverableFinish.setter     
    def _set_baseline4DeliverableFinish(self, value):
        self.native_obj.Baseline4DeliverableFinish = value
            
    # -> Any            
    @property         
    def baseline4DeliverableStart(self) -> "Any":
        return (self.native_obj.Baseline4DeliverableStart)
        
    @baseline4DeliverableStart.setter     
    def _set_baseline4DeliverableStart(self, value):
        self.native_obj.Baseline4DeliverableStart = value
            
    # -> Any            
    @property         
    def baseline4Duration(self) -> "Any":
        return (self.native_obj.Baseline4Duration)
        
    @baseline4Duration.setter     
    def _set_baseline4Duration(self, value):
        self.native_obj.Baseline4Duration = value
            
    # -> Any            
    @property         
    def baseline4DurationEstimated(self) -> "Any":
        return (self.native_obj.Baseline4DurationEstimated)
        
    @baseline4DurationEstimated.setter     
    def _set_baseline4DurationEstimated(self, value):
        self.native_obj.Baseline4DurationEstimated = value
            
    # -> Any            
    @property         
    def baseline4DurationText(self) -> "Any":
        return (self.native_obj.Baseline4DurationText)
        
    @baseline4DurationText.setter     
    def _set_baseline4DurationText(self, value):
        self.native_obj.Baseline4DurationText = value
            
    # -> Any            
    @property         
    def baseline4Finish(self) -> "Any":
        return (self.native_obj.Baseline4Finish)
        
    @baseline4Finish.setter     
    def _set_baseline4Finish(self, value):
        self.native_obj.Baseline4Finish = value
            
    # -> Any            
    @property         
    def baseline4FinishText(self) -> "Any":
        return (self.native_obj.Baseline4FinishText)
        
    @baseline4FinishText.setter     
    def _set_baseline4FinishText(self, value):
        self.native_obj.Baseline4FinishText = value
            
    # -> Any            
    @property         
    def baseline4FixedCost(self) -> "Any":
        return (self.native_obj.Baseline4FixedCost)
        
    @baseline4FixedCost.setter     
    def _set_baseline4FixedCost(self, value):
        self.native_obj.Baseline4FixedCost = value
            
    # -> Any            
    @property         
    def baseline4FixedCostAccrual(self) -> "Any":
        return (self.native_obj.Baseline4FixedCostAccrual)
        
    @baseline4FixedCostAccrual.setter     
    def _set_baseline4FixedCostAccrual(self, value):
        self.native_obj.Baseline4FixedCostAccrual = value
            
    # -> Any            
    @property         
    def baseline4Start(self) -> "Any":
        return (self.native_obj.Baseline4Start)
        
    @baseline4Start.setter     
    def _set_baseline4Start(self, value):
        self.native_obj.Baseline4Start = value
            
    # -> Any            
    @property         
    def baseline4StartText(self) -> "Any":
        return (self.native_obj.Baseline4StartText)
        
    @baseline4StartText.setter     
    def _set_baseline4StartText(self, value):
        self.native_obj.Baseline4StartText = value
            
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
    def baseline5DeliverableFinish(self) -> "Any":
        return (self.native_obj.Baseline5DeliverableFinish)
        
    @baseline5DeliverableFinish.setter     
    def _set_baseline5DeliverableFinish(self, value):
        self.native_obj.Baseline5DeliverableFinish = value
            
    # -> Any            
    @property         
    def baseline5DeliverableStart(self) -> "Any":
        return (self.native_obj.Baseline5DeliverableStart)
        
    @baseline5DeliverableStart.setter     
    def _set_baseline5DeliverableStart(self, value):
        self.native_obj.Baseline5DeliverableStart = value
            
    # -> Any            
    @property         
    def baseline5Duration(self) -> "Any":
        return (self.native_obj.Baseline5Duration)
        
    @baseline5Duration.setter     
    def _set_baseline5Duration(self, value):
        self.native_obj.Baseline5Duration = value
            
    # -> Any            
    @property         
    def baseline5DurationEstimated(self) -> "Any":
        return (self.native_obj.Baseline5DurationEstimated)
        
    @baseline5DurationEstimated.setter     
    def _set_baseline5DurationEstimated(self, value):
        self.native_obj.Baseline5DurationEstimated = value
            
    # -> Any            
    @property         
    def baseline5DurationText(self) -> "Any":
        return (self.native_obj.Baseline5DurationText)
        
    @baseline5DurationText.setter     
    def _set_baseline5DurationText(self, value):
        self.native_obj.Baseline5DurationText = value
            
    # -> Any            
    @property         
    def baseline5Finish(self) -> "Any":
        return (self.native_obj.Baseline5Finish)
        
    @baseline5Finish.setter     
    def _set_baseline5Finish(self, value):
        self.native_obj.Baseline5Finish = value
            
    # -> Any            
    @property         
    def baseline5FinishText(self) -> "Any":
        return (self.native_obj.Baseline5FinishText)
        
    @baseline5FinishText.setter     
    def _set_baseline5FinishText(self, value):
        self.native_obj.Baseline5FinishText = value
            
    # -> Any            
    @property         
    def baseline5FixedCost(self) -> "Any":
        return (self.native_obj.Baseline5FixedCost)
        
    @baseline5FixedCost.setter     
    def _set_baseline5FixedCost(self, value):
        self.native_obj.Baseline5FixedCost = value
            
    # -> Any            
    @property         
    def baseline5FixedCostAccrual(self) -> "Any":
        return (self.native_obj.Baseline5FixedCostAccrual)
        
    @baseline5FixedCostAccrual.setter     
    def _set_baseline5FixedCostAccrual(self, value):
        self.native_obj.Baseline5FixedCostAccrual = value
            
    # -> Any            
    @property         
    def baseline5Start(self) -> "Any":
        return (self.native_obj.Baseline5Start)
        
    @baseline5Start.setter     
    def _set_baseline5Start(self, value):
        self.native_obj.Baseline5Start = value
            
    # -> Any            
    @property         
    def baseline5StartText(self) -> "Any":
        return (self.native_obj.Baseline5StartText)
        
    @baseline5StartText.setter     
    def _set_baseline5StartText(self, value):
        self.native_obj.Baseline5StartText = value
            
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
    def baseline6DeliverableFinish(self) -> "Any":
        return (self.native_obj.Baseline6DeliverableFinish)
        
    @baseline6DeliverableFinish.setter     
    def _set_baseline6DeliverableFinish(self, value):
        self.native_obj.Baseline6DeliverableFinish = value
            
    # -> Any            
    @property         
    def baseline6DeliverableStart(self) -> "Any":
        return (self.native_obj.Baseline6DeliverableStart)
        
    @baseline6DeliverableStart.setter     
    def _set_baseline6DeliverableStart(self, value):
        self.native_obj.Baseline6DeliverableStart = value
            
    # -> Any            
    @property         
    def baseline6Duration(self) -> "Any":
        return (self.native_obj.Baseline6Duration)
        
    @baseline6Duration.setter     
    def _set_baseline6Duration(self, value):
        self.native_obj.Baseline6Duration = value
            
    # -> Any            
    @property         
    def baseline6DurationEstimated(self) -> "Any":
        return (self.native_obj.Baseline6DurationEstimated)
        
    @baseline6DurationEstimated.setter     
    def _set_baseline6DurationEstimated(self, value):
        self.native_obj.Baseline6DurationEstimated = value
            
    # -> Any            
    @property         
    def baseline6DurationText(self) -> "Any":
        return (self.native_obj.Baseline6DurationText)
        
    @baseline6DurationText.setter     
    def _set_baseline6DurationText(self, value):
        self.native_obj.Baseline6DurationText = value
            
    # -> Any            
    @property         
    def baseline6Finish(self) -> "Any":
        return (self.native_obj.Baseline6Finish)
        
    @baseline6Finish.setter     
    def _set_baseline6Finish(self, value):
        self.native_obj.Baseline6Finish = value
            
    # -> Any            
    @property         
    def baseline6FinishText(self) -> "Any":
        return (self.native_obj.Baseline6FinishText)
        
    @baseline6FinishText.setter     
    def _set_baseline6FinishText(self, value):
        self.native_obj.Baseline6FinishText = value
            
    # -> Any            
    @property         
    def baseline6FixedCost(self) -> "Any":
        return (self.native_obj.Baseline6FixedCost)
        
    @baseline6FixedCost.setter     
    def _set_baseline6FixedCost(self, value):
        self.native_obj.Baseline6FixedCost = value
            
    # -> Any            
    @property         
    def baseline6FixedCostAccrual(self) -> "Any":
        return (self.native_obj.Baseline6FixedCostAccrual)
        
    @baseline6FixedCostAccrual.setter     
    def _set_baseline6FixedCostAccrual(self, value):
        self.native_obj.Baseline6FixedCostAccrual = value
            
    # -> Any            
    @property         
    def baseline6Start(self) -> "Any":
        return (self.native_obj.Baseline6Start)
        
    @baseline6Start.setter     
    def _set_baseline6Start(self, value):
        self.native_obj.Baseline6Start = value
            
    # -> Any            
    @property         
    def baseline6StartText(self) -> "Any":
        return (self.native_obj.Baseline6StartText)
        
    @baseline6StartText.setter     
    def _set_baseline6StartText(self, value):
        self.native_obj.Baseline6StartText = value
            
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
    def baseline7DeliverableFinish(self) -> "Any":
        return (self.native_obj.Baseline7DeliverableFinish)
        
    @baseline7DeliverableFinish.setter     
    def _set_baseline7DeliverableFinish(self, value):
        self.native_obj.Baseline7DeliverableFinish = value
            
    # -> Any            
    @property         
    def baseline7DeliverableStart(self) -> "Any":
        return (self.native_obj.Baseline7DeliverableStart)
        
    @baseline7DeliverableStart.setter     
    def _set_baseline7DeliverableStart(self, value):
        self.native_obj.Baseline7DeliverableStart = value
            
    # -> Any            
    @property         
    def baseline7Duration(self) -> "Any":
        return (self.native_obj.Baseline7Duration)
        
    @baseline7Duration.setter     
    def _set_baseline7Duration(self, value):
        self.native_obj.Baseline7Duration = value
            
    # -> Any            
    @property         
    def baseline7DurationEstimated(self) -> "Any":
        return (self.native_obj.Baseline7DurationEstimated)
        
    @baseline7DurationEstimated.setter     
    def _set_baseline7DurationEstimated(self, value):
        self.native_obj.Baseline7DurationEstimated = value
            
    # -> Any            
    @property         
    def baseline7DurationText(self) -> "Any":
        return (self.native_obj.Baseline7DurationText)
        
    @baseline7DurationText.setter     
    def _set_baseline7DurationText(self, value):
        self.native_obj.Baseline7DurationText = value
            
    # -> Any            
    @property         
    def baseline7Finish(self) -> "Any":
        return (self.native_obj.Baseline7Finish)
        
    @baseline7Finish.setter     
    def _set_baseline7Finish(self, value):
        self.native_obj.Baseline7Finish = value
            
    # -> Any            
    @property         
    def baseline7FinishText(self) -> "Any":
        return (self.native_obj.Baseline7FinishText)
        
    @baseline7FinishText.setter     
    def _set_baseline7FinishText(self, value):
        self.native_obj.Baseline7FinishText = value
            
    # -> Any            
    @property         
    def baseline7FixedCost(self) -> "Any":
        return (self.native_obj.Baseline7FixedCost)
        
    @baseline7FixedCost.setter     
    def _set_baseline7FixedCost(self, value):
        self.native_obj.Baseline7FixedCost = value
            
    # -> Any            
    @property         
    def baseline7FixedCostAccrual(self) -> "Any":
        return (self.native_obj.Baseline7FixedCostAccrual)
        
    @baseline7FixedCostAccrual.setter     
    def _set_baseline7FixedCostAccrual(self, value):
        self.native_obj.Baseline7FixedCostAccrual = value
            
    # -> Any            
    @property         
    def baseline7Start(self) -> "Any":
        return (self.native_obj.Baseline7Start)
        
    @baseline7Start.setter     
    def _set_baseline7Start(self, value):
        self.native_obj.Baseline7Start = value
            
    # -> Any            
    @property         
    def baseline7StartText(self) -> "Any":
        return (self.native_obj.Baseline7StartText)
        
    @baseline7StartText.setter     
    def _set_baseline7StartText(self, value):
        self.native_obj.Baseline7StartText = value
            
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
    def baseline8DeliverableFinish(self) -> "Any":
        return (self.native_obj.Baseline8DeliverableFinish)
        
    @baseline8DeliverableFinish.setter     
    def _set_baseline8DeliverableFinish(self, value):
        self.native_obj.Baseline8DeliverableFinish = value
            
    # -> Any            
    @property         
    def baseline8DeliverableStart(self) -> "Any":
        return (self.native_obj.Baseline8DeliverableStart)
        
    @baseline8DeliverableStart.setter     
    def _set_baseline8DeliverableStart(self, value):
        self.native_obj.Baseline8DeliverableStart = value
            
    # -> Any            
    @property         
    def baseline8Duration(self) -> "Any":
        return (self.native_obj.Baseline8Duration)
        
    @baseline8Duration.setter     
    def _set_baseline8Duration(self, value):
        self.native_obj.Baseline8Duration = value
            
    # -> Any            
    @property         
    def baseline8DurationEstimated(self) -> "Any":
        return (self.native_obj.Baseline8DurationEstimated)
        
    @baseline8DurationEstimated.setter     
    def _set_baseline8DurationEstimated(self, value):
        self.native_obj.Baseline8DurationEstimated = value
            
    # -> Any            
    @property         
    def baseline8DurationText(self) -> "Any":
        return (self.native_obj.Baseline8DurationText)
        
    @baseline8DurationText.setter     
    def _set_baseline8DurationText(self, value):
        self.native_obj.Baseline8DurationText = value
            
    # -> Any            
    @property         
    def baseline8Finish(self) -> "Any":
        return (self.native_obj.Baseline8Finish)
        
    @baseline8Finish.setter     
    def _set_baseline8Finish(self, value):
        self.native_obj.Baseline8Finish = value
            
    # -> Any            
    @property         
    def baseline8FinishText(self) -> "Any":
        return (self.native_obj.Baseline8FinishText)
        
    @baseline8FinishText.setter     
    def _set_baseline8FinishText(self, value):
        self.native_obj.Baseline8FinishText = value
            
    # -> Any            
    @property         
    def baseline8FixedCost(self) -> "Any":
        return (self.native_obj.Baseline8FixedCost)
        
    @baseline8FixedCost.setter     
    def _set_baseline8FixedCost(self, value):
        self.native_obj.Baseline8FixedCost = value
            
    # -> Any            
    @property         
    def baseline8FixedCostAccrual(self) -> "Any":
        return (self.native_obj.Baseline8FixedCostAccrual)
        
    @baseline8FixedCostAccrual.setter     
    def _set_baseline8FixedCostAccrual(self, value):
        self.native_obj.Baseline8FixedCostAccrual = value
            
    # -> Any            
    @property         
    def baseline8Start(self) -> "Any":
        return (self.native_obj.Baseline8Start)
        
    @baseline8Start.setter     
    def _set_baseline8Start(self, value):
        self.native_obj.Baseline8Start = value
            
    # -> Any            
    @property         
    def baseline8StartText(self) -> "Any":
        return (self.native_obj.Baseline8StartText)
        
    @baseline8StartText.setter     
    def _set_baseline8StartText(self, value):
        self.native_obj.Baseline8StartText = value
            
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
    def baseline9DeliverableFinish(self) -> "Any":
        return (self.native_obj.Baseline9DeliverableFinish)
        
    @baseline9DeliverableFinish.setter     
    def _set_baseline9DeliverableFinish(self, value):
        self.native_obj.Baseline9DeliverableFinish = value
            
    # -> Any            
    @property         
    def baseline9DeliverableStart(self) -> "Any":
        return (self.native_obj.Baseline9DeliverableStart)
        
    @baseline9DeliverableStart.setter     
    def _set_baseline9DeliverableStart(self, value):
        self.native_obj.Baseline9DeliverableStart = value
            
    # -> Any            
    @property         
    def baseline9Duration(self) -> "Any":
        return (self.native_obj.Baseline9Duration)
        
    @baseline9Duration.setter     
    def _set_baseline9Duration(self, value):
        self.native_obj.Baseline9Duration = value
            
    # -> Any            
    @property         
    def baseline9DurationEstimated(self) -> "Any":
        return (self.native_obj.Baseline9DurationEstimated)
        
    @baseline9DurationEstimated.setter     
    def _set_baseline9DurationEstimated(self, value):
        self.native_obj.Baseline9DurationEstimated = value
            
    # -> Any            
    @property         
    def baseline9DurationText(self) -> "Any":
        return (self.native_obj.Baseline9DurationText)
        
    @baseline9DurationText.setter     
    def _set_baseline9DurationText(self, value):
        self.native_obj.Baseline9DurationText = value
            
    # -> Any            
    @property         
    def baseline9Finish(self) -> "Any":
        return (self.native_obj.Baseline9Finish)
        
    @baseline9Finish.setter     
    def _set_baseline9Finish(self, value):
        self.native_obj.Baseline9Finish = value
            
    # -> Any            
    @property         
    def baseline9FinishText(self) -> "Any":
        return (self.native_obj.Baseline9FinishText)
        
    @baseline9FinishText.setter     
    def _set_baseline9FinishText(self, value):
        self.native_obj.Baseline9FinishText = value
            
    # -> Any            
    @property         
    def baseline9FixedCost(self) -> "Any":
        return (self.native_obj.Baseline9FixedCost)
        
    @baseline9FixedCost.setter     
    def _set_baseline9FixedCost(self, value):
        self.native_obj.Baseline9FixedCost = value
            
    # -> Any            
    @property         
    def baseline9FixedCostAccrual(self) -> "Any":
        return (self.native_obj.Baseline9FixedCostAccrual)
        
    @baseline9FixedCostAccrual.setter     
    def _set_baseline9FixedCostAccrual(self, value):
        self.native_obj.Baseline9FixedCostAccrual = value
            
    # -> Any            
    @property         
    def baseline9Start(self) -> "Any":
        return (self.native_obj.Baseline9Start)
        
    @baseline9Start.setter     
    def _set_baseline9Start(self, value):
        self.native_obj.Baseline9Start = value
            
    # -> Any            
    @property         
    def baseline9StartText(self) -> "Any":
        return (self.native_obj.Baseline9StartText)
        
    @baseline9StartText.setter     
    def _set_baseline9StartText(self, value):
        self.native_obj.Baseline9StartText = value
            
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
    def baselineDeliverableFinish(self) -> "Any":
        return (self.native_obj.BaselineDeliverableFinish)
        
    @baselineDeliverableFinish.setter     
    def _set_baselineDeliverableFinish(self, value):
        self.native_obj.BaselineDeliverableFinish = value
            
    # -> Any            
    @property         
    def baselineDeliverableStart(self) -> "Any":
        return (self.native_obj.BaselineDeliverableStart)
        
    @baselineDeliverableStart.setter     
    def _set_baselineDeliverableStart(self, value):
        self.native_obj.BaselineDeliverableStart = value
            
    # -> Any            
    @property         
    def baselineDuration(self) -> "Any":
        return (self.native_obj.BaselineDuration)
        
    @baselineDuration.setter     
    def _set_baselineDuration(self, value):
        self.native_obj.BaselineDuration = value
            
    # -> Any            
    @property         
    def baselineDurationEstimated(self) -> "Any":
        return (self.native_obj.BaselineDurationEstimated)
        
    @baselineDurationEstimated.setter     
    def _set_baselineDurationEstimated(self, value):
        self.native_obj.BaselineDurationEstimated = value
            
    # -> Any            
    @property         
    def baselineDurationText(self) -> "Any":
        return (self.native_obj.BaselineDurationText)
        
    @baselineDurationText.setter     
    def _set_baselineDurationText(self, value):
        self.native_obj.BaselineDurationText = value
            
    # -> Any            
    @property         
    def baselineFinish(self) -> "Any":
        return (self.native_obj.BaselineFinish)
        
    @baselineFinish.setter     
    def _set_baselineFinish(self, value):
        self.native_obj.BaselineFinish = value
            
    # -> Any            
    @property         
    def baselineFinishText(self) -> "Any":
        return (self.native_obj.BaselineFinishText)
        
    @baselineFinishText.setter     
    def _set_baselineFinishText(self, value):
        self.native_obj.BaselineFinishText = value
            
    # -> Any            
    @property         
    def baselineFixedCost(self) -> "Any":
        return (self.native_obj.BaselineFixedCost)
        
    @baselineFixedCost.setter     
    def _set_baselineFixedCost(self, value):
        self.native_obj.BaselineFixedCost = value
            
    # -> Any            
    @property         
    def baselineFixedCostAccrual(self) -> "Any":
        return (self.native_obj.BaselineFixedCostAccrual)
        
    @baselineFixedCostAccrual.setter     
    def _set_baselineFixedCostAccrual(self, value):
        self.native_obj.BaselineFixedCostAccrual = value
            
    # -> Any            
    @property         
    def baselineStart(self) -> "Any":
        return (self.native_obj.BaselineStart)
        
    @baselineStart.setter     
    def _set_baselineStart(self, value):
        self.native_obj.BaselineStart = value
            
    # -> Any            
    @property         
    def baselineStartText(self) -> "Any":
        return (self.native_obj.BaselineStartText)
        
    @baselineStartText.setter     
    def _set_baselineStartText(self, value):
        self.native_obj.BaselineStartText = value
            
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
    def calendar(self) -> "Any":
        return (self.native_obj.Calendar)
        
    @calendar.setter     
    def _set_calendar(self, value):
        self.native_obj.Calendar = value
            
    # -> Any            
    @property         
    def calendarGuid(self) -> "Any":
        return (self.native_obj.CalendarGuid)
        
    @calendarGuid.setter     
    def _set_calendarGuid(self, value):
        self.native_obj.CalendarGuid = value
            
    # -> Any            
    @property         
    def calendarObject(self) -> "Any":
        return (self.native_obj.CalendarObject)
        
    @calendarObject.setter     
    def _set_calendarObject(self, value):
        self.native_obj.CalendarObject = value
            
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
    def constraintDate(self) -> "Any":
        return (self.native_obj.ConstraintDate)
        
    @constraintDate.setter     
    def _set_constraintDate(self, value):
        self.native_obj.ConstraintDate = value
            
    # -> Any            
    @property         
    def constraintType(self) -> "Any":
        return (self.native_obj.ConstraintType)
        
    @constraintType.setter     
    def _set_constraintType(self, value):
        self.native_obj.ConstraintType = value
            
    # -> Any            
    @property         
    def contact(self) -> "Any":
        return (self.native_obj.Contact)
        
    @contact.setter     
    def _set_contact(self, value):
        self.native_obj.Contact = value
            
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
    def costVariance(self) -> "Any":
        return (self.native_obj.CostVariance)
        
    @costVariance.setter     
    def _set_costVariance(self, value):
        self.native_obj.CostVariance = value
            
    # -> Any            
    @property         
    def cPI(self) -> "Any":
        return (self.native_obj.CPI)
        
    @cPI.setter     
    def _set_cPI(self, value):
        self.native_obj.CPI = value
            
    # -> Any            
    @property         
    def created(self) -> "Any":
        return (self.native_obj.Created)
        
    @created.setter     
    def _set_created(self, value):
        self.native_obj.Created = value
            
    # -> Any            
    @property         
    def critical(self) -> "Any":
        return (self.native_obj.Critical)
        
    @critical.setter     
    def _set_critical(self, value):
        self.native_obj.Critical = value
            
    # -> Any            
    @property         
    def cV(self) -> "Any":
        return (self.native_obj.CV)
        
    @cV.setter     
    def _set_cV(self, value):
        self.native_obj.CV = value
            
    # -> Any            
    @property         
    def cVPercent(self) -> "Any":
        return (self.native_obj.CVPercent)
        
    @cVPercent.setter     
    def _set_cVPercent(self, value):
        self.native_obj.CVPercent = value
            
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
    def deadline(self) -> "Any":
        return (self.native_obj.Deadline)
        
    @deadline.setter     
    def _set_deadline(self, value):
        self.native_obj.Deadline = value
            
    # -> Any            
    @property         
    def deliverableFinish(self) -> "Any":
        return (self.native_obj.DeliverableFinish)
        
    @deliverableFinish.setter     
    def _set_deliverableFinish(self, value):
        self.native_obj.DeliverableFinish = value
            
    # -> Any            
    @property         
    def deliverableGuid(self) -> "Any":
        return (self.native_obj.DeliverableGuid)
        
    @deliverableGuid.setter     
    def _set_deliverableGuid(self, value):
        self.native_obj.DeliverableGuid = value
            
    # -> Any            
    @property         
    def deliverableName(self) -> "Any":
        return (self.native_obj.DeliverableName)
        
    @deliverableName.setter     
    def _set_deliverableName(self, value):
        self.native_obj.DeliverableName = value
            
    # -> Any            
    @property         
    def deliverableStart(self) -> "Any":
        return (self.native_obj.DeliverableStart)
        
    @deliverableStart.setter     
    def _set_deliverableStart(self, value):
        self.native_obj.DeliverableStart = value
            
    # -> Any            
    @property         
    def deliverableType(self) -> "Any":
        return (self.native_obj.DeliverableType)
        
    @deliverableType.setter     
    def _set_deliverableType(self, value):
        self.native_obj.DeliverableType = value
            
    # -> Any            
    @property         
    def duration(self) -> "Any":
        return (self.native_obj.Duration)
        
    @duration.setter     
    def _set_duration(self, value):
        self.native_obj.Duration = value
            
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
    def duration10Estimated(self) -> "Any":
        return (self.native_obj.Duration10Estimated)
        
    @duration10Estimated.setter     
    def _set_duration10Estimated(self, value):
        self.native_obj.Duration10Estimated = value
            
    # -> Any            
    @property         
    def duration1Estimated(self) -> "Any":
        return (self.native_obj.Duration1Estimated)
        
    @duration1Estimated.setter     
    def _set_duration1Estimated(self, value):
        self.native_obj.Duration1Estimated = value
            
    # -> Any            
    @property         
    def duration2(self) -> "Any":
        return (self.native_obj.Duration2)
        
    @duration2.setter     
    def _set_duration2(self, value):
        self.native_obj.Duration2 = value
            
    # -> Any            
    @property         
    def duration2Estimated(self) -> "Any":
        return (self.native_obj.Duration2Estimated)
        
    @duration2Estimated.setter     
    def _set_duration2Estimated(self, value):
        self.native_obj.Duration2Estimated = value
            
    # -> Any            
    @property         
    def duration3(self) -> "Any":
        return (self.native_obj.Duration3)
        
    @duration3.setter     
    def _set_duration3(self, value):
        self.native_obj.Duration3 = value
            
    # -> Any            
    @property         
    def duration3Estimated(self) -> "Any":
        return (self.native_obj.Duration3Estimated)
        
    @duration3Estimated.setter     
    def _set_duration3Estimated(self, value):
        self.native_obj.Duration3Estimated = value
            
    # -> Any            
    @property         
    def duration4(self) -> "Any":
        return (self.native_obj.Duration4)
        
    @duration4.setter     
    def _set_duration4(self, value):
        self.native_obj.Duration4 = value
            
    # -> Any            
    @property         
    def duration4Estimated(self) -> "Any":
        return (self.native_obj.Duration4Estimated)
        
    @duration4Estimated.setter     
    def _set_duration4Estimated(self, value):
        self.native_obj.Duration4Estimated = value
            
    # -> Any            
    @property         
    def duration5(self) -> "Any":
        return (self.native_obj.Duration5)
        
    @duration5.setter     
    def _set_duration5(self, value):
        self.native_obj.Duration5 = value
            
    # -> Any            
    @property         
    def duration5Estimated(self) -> "Any":
        return (self.native_obj.Duration5Estimated)
        
    @duration5Estimated.setter     
    def _set_duration5Estimated(self, value):
        self.native_obj.Duration5Estimated = value
            
    # -> Any            
    @property         
    def duration6(self) -> "Any":
        return (self.native_obj.Duration6)
        
    @duration6.setter     
    def _set_duration6(self, value):
        self.native_obj.Duration6 = value
            
    # -> Any            
    @property         
    def duration6Estimated(self) -> "Any":
        return (self.native_obj.Duration6Estimated)
        
    @duration6Estimated.setter     
    def _set_duration6Estimated(self, value):
        self.native_obj.Duration6Estimated = value
            
    # -> Any            
    @property         
    def duration7(self) -> "Any":
        return (self.native_obj.Duration7)
        
    @duration7.setter     
    def _set_duration7(self, value):
        self.native_obj.Duration7 = value
            
    # -> Any            
    @property         
    def duration7Estimated(self) -> "Any":
        return (self.native_obj.Duration7Estimated)
        
    @duration7Estimated.setter     
    def _set_duration7Estimated(self, value):
        self.native_obj.Duration7Estimated = value
            
    # -> Any            
    @property         
    def duration8(self) -> "Any":
        return (self.native_obj.Duration8)
        
    @duration8.setter     
    def _set_duration8(self, value):
        self.native_obj.Duration8 = value
            
    # -> Any            
    @property         
    def duration8Estimated(self) -> "Any":
        return (self.native_obj.Duration8Estimated)
        
    @duration8Estimated.setter     
    def _set_duration8Estimated(self, value):
        self.native_obj.Duration8Estimated = value
            
    # -> Any            
    @property         
    def duration9(self) -> "Any":
        return (self.native_obj.Duration9)
        
    @duration9.setter     
    def _set_duration9(self, value):
        self.native_obj.Duration9 = value
            
    # -> Any            
    @property         
    def duration9Estimated(self) -> "Any":
        return (self.native_obj.Duration9Estimated)
        
    @duration9Estimated.setter     
    def _set_duration9Estimated(self, value):
        self.native_obj.Duration9Estimated = value
            
    # -> Any            
    @property         
    def durationText(self) -> "Any":
        return (self.native_obj.DurationText)
        
    @durationText.setter     
    def _set_durationText(self, value):
        self.native_obj.DurationText = value
            
    # -> Any            
    @property         
    def durationVariance(self) -> "Any":
        return (self.native_obj.DurationVariance)
        
    @durationVariance.setter     
    def _set_durationVariance(self, value):
        self.native_obj.DurationVariance = value
            
    # -> Any            
    @property         
    def eAC(self) -> "Any":
        return (self.native_obj.EAC)
        
    @eAC.setter     
    def _set_eAC(self, value):
        self.native_obj.EAC = value
            
    # -> Any            
    @property         
    def earlyFinish(self) -> "Any":
        return (self.native_obj.EarlyFinish)
        
    @earlyFinish.setter     
    def _set_earlyFinish(self, value):
        self.native_obj.EarlyFinish = value
            
    # -> Any            
    @property         
    def earlyStart(self) -> "Any":
        return (self.native_obj.EarlyStart)
        
    @earlyStart.setter     
    def _set_earlyStart(self, value):
        self.native_obj.EarlyStart = value
            
    # -> Any            
    @property         
    def earnedValueMethod(self) -> "Any":
        return (self.native_obj.EarnedValueMethod)
        
    @earnedValueMethod.setter     
    def _set_earnedValueMethod(self, value):
        self.native_obj.EarnedValueMethod = value
            
    # -> Any            
    @property         
    def effortDriven(self) -> "Any":
        return (self.native_obj.EffortDriven)
        
    @effortDriven.setter     
    def _set_effortDriven(self, value):
        self.native_obj.EffortDriven = value
            
    # -> Any            
    @property         
    def errorMessage(self) -> "Any":
        return (self.native_obj.ErrorMessage)
        
    @errorMessage.setter     
    def _set_errorMessage(self, value):
        self.native_obj.ErrorMessage = value
            
    # -> Any            
    @property         
    def estimated(self) -> "Any":
        return (self.native_obj.Estimated)
        
    @estimated.setter     
    def _set_estimated(self, value):
        self.native_obj.Estimated = value
            
    # -> Any            
    @property         
    def externalTask(self) -> "Any":
        return (self.native_obj.ExternalTask)
        
    @externalTask.setter     
    def _set_externalTask(self, value):
        self.native_obj.ExternalTask = value
            
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
    def finishSlack(self) -> "Any":
        return (self.native_obj.FinishSlack)
        
    @finishSlack.setter     
    def _set_finishSlack(self, value):
        self.native_obj.FinishSlack = value
            
    # -> Any            
    @property         
    def finishText(self) -> "Any":
        return (self.native_obj.FinishText)
        
    @finishText.setter     
    def _set_finishText(self, value):
        self.native_obj.FinishText = value
            
    # -> Any            
    @property         
    def finishVariance(self) -> "Any":
        return (self.native_obj.FinishVariance)
        
    @finishVariance.setter     
    def _set_finishVariance(self, value):
        self.native_obj.FinishVariance = value
            
    # -> Any            
    @property         
    def fixedCost(self) -> "Any":
        return (self.native_obj.FixedCost)
        
    @fixedCost.setter     
    def _set_fixedCost(self, value):
        self.native_obj.FixedCost = value
            
    # -> Any            
    @property         
    def fixedCostAccrual(self) -> "Any":
        return (self.native_obj.FixedCostAccrual)
        
    @fixedCostAccrual.setter     
    def _set_fixedCostAccrual(self, value):
        self.native_obj.FixedCostAccrual = value
            
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
    def freeSlack(self) -> "Any":
        return (self.native_obj.FreeSlack)
        
    @freeSlack.setter     
    def _set_freeSlack(self, value):
        self.native_obj.FreeSlack = value
            
    # -> Any            
    @property         
    def groupBySummary(self) -> "Any":
        return (self.native_obj.GroupBySummary)
        
    @groupBySummary.setter     
    def _set_groupBySummary(self, value):
        self.native_obj.GroupBySummary = value
            
    # -> Any            
    @property         
    def guid(self) -> "Any":
        return (self.native_obj.Guid)
        
    @guid.setter     
    def _set_guid(self, value):
        self.native_obj.Guid = value
            
    # -> Any            
    @property         
    def hideBar(self) -> "Any":
        return (self.native_obj.HideBar)
        
    @hideBar.setter     
    def _set_hideBar(self, value):
        self.native_obj.HideBar = value
            
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
    def iD(self) -> "Any":
        return (self.native_obj.ID)
        
    @iD.setter     
    def _set_iD(self, value):
        self.native_obj.ID = value
            
    # -> Any            
    @property         
    def ignoreResourceCalendar(self) -> "Any":
        return (self.native_obj.IgnoreResourceCalendar)
        
    @ignoreResourceCalendar.setter     
    def _set_ignoreResourceCalendar(self, value):
        self.native_obj.IgnoreResourceCalendar = value
            
    # -> Any            
    @property         
    def ignoreWarnings(self) -> "Any":
        return (self.native_obj.IgnoreWarnings)
        
    @ignoreWarnings.setter     
    def _set_ignoreWarnings(self, value):
        self.native_obj.IgnoreWarnings = value
            
    # -> Any            
    @property         
    def index(self) -> "Any":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> Any            
    @property         
    def isDurationValid(self) -> "Any":
        return (self.native_obj.IsDurationValid)
        
    @isDurationValid.setter     
    def _set_isDurationValid(self, value):
        self.native_obj.IsDurationValid = value
            
    # -> Any            
    @property         
    def isFinishValid(self) -> "Any":
        return (self.native_obj.IsFinishValid)
        
    @isFinishValid.setter     
    def _set_isFinishValid(self, value):
        self.native_obj.IsFinishValid = value
            
    # -> Any            
    @property         
    def isPublished(self) -> "Any":
        return (self.native_obj.IsPublished)
        
    @isPublished.setter     
    def _set_isPublished(self, value):
        self.native_obj.IsPublished = value
            
    # -> Any            
    @property         
    def isStartValid(self) -> "Any":
        return (self.native_obj.IsStartValid)
        
    @isStartValid.setter     
    def _set_isStartValid(self, value):
        self.native_obj.IsStartValid = value
            
    # -> Any            
    @property         
    def lateFinish(self) -> "Any":
        return (self.native_obj.LateFinish)
        
    @lateFinish.setter     
    def _set_lateFinish(self, value):
        self.native_obj.LateFinish = value
            
    # -> Any            
    @property         
    def lateStart(self) -> "Any":
        return (self.native_obj.LateStart)
        
    @lateStart.setter     
    def _set_lateStart(self, value):
        self.native_obj.LateStart = value
            
    # -> Any            
    @property         
    def levelIndividualAssignments(self) -> "Any":
        return (self.native_obj.LevelIndividualAssignments)
        
    @levelIndividualAssignments.setter     
    def _set_levelIndividualAssignments(self, value):
        self.native_obj.LevelIndividualAssignments = value
            
    # -> Any            
    @property         
    def levelingCanSplit(self) -> "Any":
        return (self.native_obj.LevelingCanSplit)
        
    @levelingCanSplit.setter     
    def _set_levelingCanSplit(self, value):
        self.native_obj.LevelingCanSplit = value
            
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
    def manual(self) -> "Any":
        return (self.native_obj.Manual)
        
    @manual.setter     
    def _set_manual(self, value):
        self.native_obj.Manual = value
            
    # -> Any            
    @property         
    def marked(self) -> "Any":
        return (self.native_obj.Marked)
        
    @marked.setter     
    def _set_marked(self, value):
        self.native_obj.Marked = value
            
    # -> Any            
    @property         
    def milestone(self) -> "Any":
        return (self.native_obj.Milestone)
        
    @milestone.setter     
    def _set_milestone(self, value):
        self.native_obj.Milestone = value
            
    # -> Any            
    @property         
    def name(self) -> "Any":
        return (self.native_obj.Name)
        
    @name.setter     
    def _set_name(self, value):
        self.native_obj.Name = value
            
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
    def objects(self) -> "Any":
        return (self.native_obj.Objects)
        
    @objects.setter     
    def _set_objects(self, value):
        self.native_obj.Objects = value
            
    # -> Any            
    @property         
    def outlineChildren(self) -> "Any":
        return (self.native_obj.OutlineChildren)
        
    @outlineChildren.setter     
    def _set_outlineChildren(self, value):
        self.native_obj.OutlineChildren = value
            
    # -> Any            
    @property         
    def outlineCode1(self) -> "Any":
        return (self.native_obj.OutlineCode1)
        
    @outlineCode1.setter     
    def _set_outlineCode1(self, value):
        self.native_obj.OutlineCode1 = value
            
    # -> Any            
    @property         
    def outlineCode10(self) -> "Any":
        return (self.native_obj.OutlineCode10)
        
    @outlineCode10.setter     
    def _set_outlineCode10(self, value):
        self.native_obj.OutlineCode10 = value
            
    # -> Any            
    @property         
    def outlineCode2(self) -> "Any":
        return (self.native_obj.OutlineCode2)
        
    @outlineCode2.setter     
    def _set_outlineCode2(self, value):
        self.native_obj.OutlineCode2 = value
            
    # -> Any            
    @property         
    def outlineCode3(self) -> "Any":
        return (self.native_obj.OutlineCode3)
        
    @outlineCode3.setter     
    def _set_outlineCode3(self, value):
        self.native_obj.OutlineCode3 = value
            
    # -> Any            
    @property         
    def outlineCode4(self) -> "Any":
        return (self.native_obj.OutlineCode4)
        
    @outlineCode4.setter     
    def _set_outlineCode4(self, value):
        self.native_obj.OutlineCode4 = value
            
    # -> Any            
    @property         
    def outlineCode5(self) -> "Any":
        return (self.native_obj.OutlineCode5)
        
    @outlineCode5.setter     
    def _set_outlineCode5(self, value):
        self.native_obj.OutlineCode5 = value
            
    # -> Any            
    @property         
    def outlineCode6(self) -> "Any":
        return (self.native_obj.OutlineCode6)
        
    @outlineCode6.setter     
    def _set_outlineCode6(self, value):
        self.native_obj.OutlineCode6 = value
            
    # -> Any            
    @property         
    def outlineCode7(self) -> "Any":
        return (self.native_obj.OutlineCode7)
        
    @outlineCode7.setter     
    def _set_outlineCode7(self, value):
        self.native_obj.OutlineCode7 = value
            
    # -> Any            
    @property         
    def outlineCode8(self) -> "Any":
        return (self.native_obj.OutlineCode8)
        
    @outlineCode8.setter     
    def _set_outlineCode8(self, value):
        self.native_obj.OutlineCode8 = value
            
    # -> Any            
    @property         
    def outlineCode9(self) -> "Any":
        return (self.native_obj.OutlineCode9)
        
    @outlineCode9.setter     
    def _set_outlineCode9(self, value):
        self.native_obj.OutlineCode9 = value
            
    # -> Any            
    @property         
    def outlineLevel(self) -> "Any":
        return (self.native_obj.OutlineLevel)
        
    @outlineLevel.setter     
    def _set_outlineLevel(self, value):
        self.native_obj.OutlineLevel = value
            
    # -> Any            
    @property         
    def outlineNumber(self) -> "Any":
        return (self.native_obj.OutlineNumber)
        
    @outlineNumber.setter     
    def _set_outlineNumber(self, value):
        self.native_obj.OutlineNumber = value
            
    # -> Any            
    @property         
    def outlineParent(self) -> "Any":
        return (self.native_obj.OutlineParent)
        
    @outlineParent.setter     
    def _set_outlineParent(self, value):
        self.native_obj.OutlineParent = value
            
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
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def pathDrivenSuccessor(self) -> "Any":
        return (self.native_obj.PathDrivenSuccessor)
        
    @pathDrivenSuccessor.setter     
    def _set_pathDrivenSuccessor(self, value):
        self.native_obj.PathDrivenSuccessor = value
            
    # -> Any            
    @property         
    def pathDrivingPredecessor(self) -> "Any":
        return (self.native_obj.PathDrivingPredecessor)
        
    @pathDrivingPredecessor.setter     
    def _set_pathDrivingPredecessor(self, value):
        self.native_obj.PathDrivingPredecessor = value
            
    # -> Any            
    @property         
    def pathPredecessor(self) -> "Any":
        return (self.native_obj.PathPredecessor)
        
    @pathPredecessor.setter     
    def _set_pathPredecessor(self, value):
        self.native_obj.PathPredecessor = value
            
    # -> Any            
    @property         
    def pathSuccessor(self) -> "Any":
        return (self.native_obj.PathSuccessor)
        
    @pathSuccessor.setter     
    def _set_pathSuccessor(self, value):
        self.native_obj.PathSuccessor = value
            
    # -> Any            
    @property         
    def percentComplete(self) -> "Any":
        return (self.native_obj.PercentComplete)
        
    @percentComplete.setter     
    def _set_percentComplete(self, value):
        self.native_obj.PercentComplete = value
            
    # -> Any            
    @property         
    def percentWorkComplete(self) -> "Any":
        return (self.native_obj.PercentWorkComplete)
        
    @percentWorkComplete.setter     
    def _set_percentWorkComplete(self, value):
        self.native_obj.PercentWorkComplete = value
            
    # -> Any            
    @property         
    def physicalPercentComplete(self) -> "Any":
        return (self.native_obj.PhysicalPercentComplete)
        
    @physicalPercentComplete.setter     
    def _set_physicalPercentComplete(self, value):
        self.native_obj.PhysicalPercentComplete = value
            
    # -> Any            
    @property         
    def placeholder(self) -> "Any":
        return (self.native_obj.Placeholder)
        
    @placeholder.setter     
    def _set_placeholder(self, value):
        self.native_obj.Placeholder = value
            
    # -> Any            
    @property         
    def predecessors(self) -> "Any":
        return (self.native_obj.Predecessors)
        
    @predecessors.setter     
    def _set_predecessors(self, value):
        self.native_obj.Predecessors = value
            
    # -> Any            
    @property         
    def predecessorTasks(self) -> "Any":
        return (self.native_obj.PredecessorTasks)
        
    @predecessorTasks.setter     
    def _set_predecessorTasks(self, value):
        self.native_obj.PredecessorTasks = value
            
    # -> Any            
    @property         
    def preleveledFinish(self) -> "Any":
        return (self.native_obj.PreleveledFinish)
        
    @preleveledFinish.setter     
    def _set_preleveledFinish(self, value):
        self.native_obj.PreleveledFinish = value
            
    # -> Any            
    @property         
    def preleveledStart(self) -> "Any":
        return (self.native_obj.PreleveledStart)
        
    @preleveledStart.setter     
    def _set_preleveledStart(self, value):
        self.native_obj.PreleveledStart = value
            
    # -> Any            
    @property         
    def priority(self) -> "Any":
        return (self.native_obj.Priority)
        
    @priority.setter     
    def _set_priority(self, value):
        self.native_obj.Priority = value
            
    # -> Any            
    @property         
    def project(self) -> "Any":
        return (self.native_obj.Project)
        
    @project.setter     
    def _set_project(self, value):
        self.native_obj.Project = value
            
    # -> Any            
    @property         
    def recalcFlags(self) -> "Any":
        return (self.native_obj.RecalcFlags)
        
    @recalcFlags.setter     
    def _set_recalcFlags(self, value):
        self.native_obj.RecalcFlags = value
            
    # -> Any            
    @property         
    def recurring(self) -> "Any":
        return (self.native_obj.Recurring)
        
    @recurring.setter     
    def _set_recurring(self, value):
        self.native_obj.Recurring = value
            
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
    def remainingDuration(self) -> "Any":
        return (self.native_obj.RemainingDuration)
        
    @remainingDuration.setter     
    def _set_remainingDuration(self, value):
        self.native_obj.RemainingDuration = value
            
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
    def resourceGroup(self) -> "Any":
        return (self.native_obj.ResourceGroup)
        
    @resourceGroup.setter     
    def _set_resourceGroup(self, value):
        self.native_obj.ResourceGroup = value
            
    # -> Any            
    @property         
    def resourceInitials(self) -> "Any":
        return (self.native_obj.ResourceInitials)
        
    @resourceInitials.setter     
    def _set_resourceInitials(self, value):
        self.native_obj.ResourceInitials = value
            
    # -> Any            
    @property         
    def resourceNames(self) -> "Any":
        return (self.native_obj.ResourceNames)
        
    @resourceNames.setter     
    def _set_resourceNames(self, value):
        self.native_obj.ResourceNames = value
            
    # -> Any            
    @property         
    def resourcePhonetics(self) -> "Any":
        return (self.native_obj.ResourcePhonetics)
        
    @resourcePhonetics.setter     
    def _set_resourcePhonetics(self, value):
        self.native_obj.ResourcePhonetics = value
            
    # -> Any            
    @property         
    def resources(self) -> "Any":
        return (self.native_obj.Resources)
        
    @resources.setter     
    def _set_resources(self, value):
        self.native_obj.Resources = value
            
    # -> Any            
    @property         
    def responsePending(self) -> "Any":
        return (self.native_obj.ResponsePending)
        
    @responsePending.setter     
    def _set_responsePending(self, value):
        self.native_obj.ResponsePending = value
            
    # -> Any            
    @property         
    def resume(self) -> "Any":
        return (self.native_obj.Resume)
        
    @resume.setter     
    def _set_resume(self, value):
        self.native_obj.Resume = value
            
    # -> Any            
    @property         
    def rollup(self) -> "Any":
        return (self.native_obj.Rollup)
        
    @rollup.setter     
    def _set_rollup(self, value):
        self.native_obj.Rollup = value
            
    # -> Any            
    @property         
    def scheduledDuration(self) -> "Any":
        return (self.native_obj.ScheduledDuration)
        
    @scheduledDuration.setter     
    def _set_scheduledDuration(self, value):
        self.native_obj.ScheduledDuration = value
            
    # -> Any            
    @property         
    def scheduledFinish(self) -> "Any":
        return (self.native_obj.ScheduledFinish)
        
    @scheduledFinish.setter     
    def _set_scheduledFinish(self, value):
        self.native_obj.ScheduledFinish = value
            
    # -> Any            
    @property         
    def scheduledStart(self) -> "Any":
        return (self.native_obj.ScheduledStart)
        
    @scheduledStart.setter     
    def _set_scheduledStart(self, value):
        self.native_obj.ScheduledStart = value
            
    # -> Any            
    @property         
    def sPI(self) -> "Any":
        return (self.native_obj.SPI)
        
    @sPI.setter     
    def _set_sPI(self, value):
        self.native_obj.SPI = value
            
    # -> Any            
    @property         
    def splitParts(self) -> "Any":
        return (self.native_obj.SplitParts)
        
    @splitParts.setter     
    def _set_splitParts(self, value):
        self.native_obj.SplitParts = value
            
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
    def startDriver(self) -> "Any":
        return (self.native_obj.StartDriver)
        
    @startDriver.setter     
    def _set_startDriver(self, value):
        self.native_obj.StartDriver = value
            
    # -> Any            
    @property         
    def startSlack(self) -> "Any":
        return (self.native_obj.StartSlack)
        
    @startSlack.setter     
    def _set_startSlack(self, value):
        self.native_obj.StartSlack = value
            
    # -> Any            
    @property         
    def startText(self) -> "Any":
        return (self.native_obj.StartText)
        
    @startText.setter     
    def _set_startText(self, value):
        self.native_obj.StartText = value
            
    # -> Any            
    @property         
    def startVariance(self) -> "Any":
        return (self.native_obj.StartVariance)
        
    @startVariance.setter     
    def _set_startVariance(self, value):
        self.native_obj.StartVariance = value
            
    # -> Any            
    @property         
    def status(self) -> "Any":
        return (self.native_obj.Status)
        
    @status.setter     
    def _set_status(self, value):
        self.native_obj.Status = value
            
    # -> Any            
    @property         
    def statusManagerName(self) -> "Any":
        return (self.native_obj.StatusManagerName)
        
    @statusManagerName.setter     
    def _set_statusManagerName(self, value):
        self.native_obj.StatusManagerName = value
            
    # -> Any            
    @property         
    def stop(self) -> "Any":
        return (self.native_obj.Stop)
        
    @stop.setter     
    def _set_stop(self, value):
        self.native_obj.Stop = value
            
    # -> Any            
    @property         
    def subproject(self) -> "Any":
        return (self.native_obj.Subproject)
        
    @subproject.setter     
    def _set_subproject(self, value):
        self.native_obj.Subproject = value
            
    # -> Any            
    @property         
    def subProjectReadOnly(self) -> "Any":
        return (self.native_obj.SubProjectReadOnly)
        
    @subProjectReadOnly.setter     
    def _set_subProjectReadOnly(self, value):
        self.native_obj.SubProjectReadOnly = value
            
    # -> Any            
    @property         
    def successors(self) -> "Any":
        return (self.native_obj.Successors)
        
    @successors.setter     
    def _set_successors(self, value):
        self.native_obj.Successors = value
            
    # -> Any            
    @property         
    def successorTasks(self) -> "Any":
        return (self.native_obj.SuccessorTasks)
        
    @successorTasks.setter     
    def _set_successorTasks(self, value):
        self.native_obj.SuccessorTasks = value
            
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
    def sVPercent(self) -> "Any":
        return (self.native_obj.SVPercent)
        
    @sVPercent.setter     
    def _set_sVPercent(self, value):
        self.native_obj.SVPercent = value
            
    # -> Any            
    @property         
    def taskDependencies(self) -> "Any":
        return (self.native_obj.TaskDependencies)
        
    @taskDependencies.setter     
    def _set_taskDependencies(self, value):
        self.native_obj.TaskDependencies = value
            
    # -> Any            
    @property         
    def tCPI(self) -> "Any":
        return (self.native_obj.TCPI)
        
    @tCPI.setter     
    def _set_tCPI(self, value):
        self.native_obj.TCPI = value
            
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
    def totalSlack(self) -> "Any":
        return (self.native_obj.TotalSlack)
        
    @totalSlack.setter     
    def _set_totalSlack(self, value):
        self.native_obj.TotalSlack = value
            
    # -> Any            
    @property         
    def type(self) -> "Any":
        return (self.native_obj.Type)
        
    @type.setter     
    def _set_type(self, value):
        self.native_obj.Type = value
            
    # -> Any            
    @property         
    def uniqueID(self) -> "Any":
        return (self.native_obj.UniqueID)
        
    @uniqueID.setter     
    def _set_uniqueID(self, value):
        self.native_obj.UniqueID = value
            
    # -> Any            
    @property         
    def uniqueIDPredecessors(self) -> "Any":
        return (self.native_obj.UniqueIDPredecessors)
        
    @uniqueIDPredecessors.setter     
    def _set_uniqueIDPredecessors(self, value):
        self.native_obj.UniqueIDPredecessors = value
            
    # -> Any            
    @property         
    def uniqueIDSuccessors(self) -> "Any":
        return (self.native_obj.UniqueIDSuccessors)
        
    @uniqueIDSuccessors.setter     
    def _set_uniqueIDSuccessors(self, value):
        self.native_obj.UniqueIDSuccessors = value
            
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
    def warning(self) -> "Any":
        return (self.native_obj.Warning)
        
    @warning.setter     
    def _set_warning(self, value):
        self.native_obj.Warning = value
            
    # -> Any            
    @property         
    def wBS(self) -> "Any":
        return (self.native_obj.WBS)
        
    @wBS.setter     
    def _set_wBS(self, value):
        self.native_obj.WBS = value
            
    # -> Any            
    @property         
    def wBSPredecessors(self) -> "Any":
        return (self.native_obj.WBSPredecessors)
        
    @wBSPredecessors.setter     
    def _set_wBSPredecessors(self, value):
        self.native_obj.WBSPredecessors = value
            
    # -> Any            
    @property         
    def wBSSuccessors(self) -> "Any":
        return (self.native_obj.WBSSuccessors)
        
    @wBSSuccessors.setter     
    def _set_wBSSuccessors(self, value):
        self.native_obj.WBSSuccessors = value
            
    # -> Any            
    @property         
    def work(self) -> "Any":
        return (self.native_obj.Work)
        
    @work.setter     
    def _set_work(self, value):
        self.native_obj.Work = value
            
    # -> Any            
    @property         
    def workVariance(self) -> "Any":
        return (self.native_obj.WorkVariance)
        
    @workVariance.setter     
    def _set_workVariance(self, value):
        self.native_obj.WorkVariance = value
            
# end "Task"       
        