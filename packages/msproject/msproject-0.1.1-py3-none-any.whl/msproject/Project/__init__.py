

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Project:
    # Object "Project" class for software "Project"

    properties = ['acceptNewExternalData', 'administrativeProject', 'allowTaskDelegation', 'andMoveCompleted', 'andMoveRemaining', 'application', 'askForCompletedWork', 'autoAddResources', 'autoCalcCosts', 'autoFilter', 'autoLinkTasks', 'autoSplitTasks', 'autoTrack', 'baseCalendars', 'baselineSavedDate', 'builtinDocumentProperties', 'calendar', 'canCheckIn', 'codeName', 'commandBars', 'container', 'creationDate', 'currencyCode', 'currencyDigits', 'currencySymbol', 'currencySymbolPosition', 'currentDate', 'currentFilter', 'currentGroup', 'currentTable', 'currentView', 'customDocumentProperties', 'databaseProjectUniqueID', 'dayLabelDisplay', 'daysPerMonth', 'defaultDurationUnits', 'defaultEarnedValueMethod', 'defaultEffortDriven', 'defaultFinishTime', 'defaultFixedCostAccrual', 'defaultResourceOvertimeRate', 'defaultResourceStandardRate', 'defaultStartTime', 'defaultTaskType', 'defaultWorkUnits', 'detectCycle', 'displayProjectSummaryTask', 'documentLibraryVersions', 'earnedValueBaseline', 'engagements', 'enterpriseActualsSynched', 'expandDatabaseTimephasedData', 'followedHyperlinkColor', 'followedHyperlinkColorEx', 'fullName', 'hasPassword', 'honorConstraints', 'hourLabelDisplay', 'hoursPerDay', 'hoursPerWeek', 'hyperlinkColor', 'hyperlinkColorEx', 'iD', 'index', 'isCheckoutMsgBarVisible', 'isCheckoutOSVisible', 'isTemplate', 'keepTaskOnNearestWorkingTimeWhenMadeAutoScheduled', 'lastPrintedDate', 'lastSaveDate', 'lastSavedBy', 'lastWssSyncDate', 'levelEntireProject', 'levelFromDate', 'levelToDate', 'manuallyScheduledTasksAutoRespectLinks', 'mapList', 'minuteLabelDisplay', 'monthLabelDisplay', 'moveCompleted', 'moveRemaining', 'multipleCriticalPaths', 'name', 'newTasksCreatedAsManual', 'newTasksEstimated', 'numberOfResources', 'numberOfTasks', 'outlineChildren', 'outlineCodes', 'parent', 'path', 'phoneticType', 'projectFinish', 'projectGuideContent', 'projectGuideFunctionalLayoutPage', 'projectGuideSaveBuffer', 'projectGuideUseDefaultContent', 'projectGuideUseDefaultFunctionalLayoutPage', 'projectNamePrefix', 'projectNotes', 'projectServerUsedForTracking', 'projectStart', 'projectSummaryTask', 'readOnly', 'readOnlyRecommended', 'receiveNotifications', 'removeFileProperties', 'reportList', 'reports', 'resourceFilterList', 'resourceFilters', 'resourceGroupList', 'resourceGroups', 'resourceGroups2', 'resourcePoolName', 'resources', 'resourceTableList', 'resourceTables', 'resourceViewList', 'revisionNumber', 'saved', 'scheduleFromStart', 'sendHyperlinkNote', 'serverIdentification', 'serverURL', 'sharedWorkspace', 'showCriticalSlack', 'showCrossProjectLinksInfo', 'showEstimatedDuration', 'showExternalPredecessors', 'showExternalSuccessors', 'showTaskSuggestions', 'showTaskWarnings', 'spaceBeforeTimeLabels', 'spreadCostsToStatusDate', 'spreadPercentCompleteToStatusDate', 'startOnCurrentDate', 'startWeekOn', 'startYearIn', 'statusDate', 'subprojects', 'taskErrorCount', 'taskFilterList', 'taskFilters', 'taskGroupList', 'taskGroups', 'taskGroups2', 'tasks', 'taskTableList', 'taskTables', 'taskViewList', 'template', 'timeline', 'trackingMethod', 'type', 'underlineHyperlinks', 'uniqueID', 'updateProjOnSave', 'useFYStartYear', 'userControl', 'utilizationDate', 'utilizationType', 'vBASigned', 'vBProject', 'versionName', 'viewList', 'views', 'viewsCombination', 'viewsSingle', 'wBSCodeGenerate', 'wBSVerifyUniqueness', 'weekLabelDisplay', 'windows', 'windows2', 'writeReserved', 'yearLabelDisplay']
    
    def __init__(self, path, visible=False):
        self.msproject_instance = win32com.client.gencache.EnsureDispatch('MSProject.Application')
        self.msproject_instance.Visible = visible
        is_open = self.msproject_instance.FileOpen(path)
        self.native_obj = self.msproject_instance.ActiveProject
        assert Path(self.native_obj.Path, self.native_obj.Name) == Path(path)    
        
    def __del__(self):
        try:
            self.msproject_instance.Quit()
        finally:
            pass
        
    
    # -> bool            
    @property         
    def acceptNewExternalData(self) -> "bool":
        return (self.native_obj.AcceptNewExternalData)
        
    @acceptNewExternalData.setter     
    def _set_acceptNewExternalData(self, value):
        self.native_obj.AcceptNewExternalData = value
            
    # -> bool            
    @property         
    def administrativeProject(self) -> "bool":
        return (self.native_obj.AdministrativeProject)
        
    @administrativeProject.setter     
    def _set_administrativeProject(self, value):
        self.native_obj.AdministrativeProject = value
            
    # -> bool            
    @property         
    def allowTaskDelegation(self) -> "bool":
        return (self.native_obj.AllowTaskDelegation)
        
    @allowTaskDelegation.setter     
    def _set_allowTaskDelegation(self, value):
        self.native_obj.AllowTaskDelegation = value
            
    # -> bool            
    @property         
    def andMoveCompleted(self) -> "bool":
        return (self.native_obj.AndMoveCompleted)
        
    @andMoveCompleted.setter     
    def _set_andMoveCompleted(self, value):
        self.native_obj.AndMoveCompleted = value
            
    # -> bool            
    @property         
    def andMoveRemaining(self) -> "bool":
        return (self.native_obj.AndMoveRemaining)
        
    @andMoveRemaining.setter     
    def _set_andMoveRemaining(self, value):
        self.native_obj.AndMoveRemaining = value
            
    # -> Application            
    @property         
    def application(self) -> "Application":
        return Application(self.native_obj.Application)
        
    @application.setter     
    def _set_application(self, value):
        self.native_obj.Application = value
            
    # -> int            
    @property         
    def askForCompletedWork(self) -> "int":
        return (self.native_obj.AskForCompletedWork)
        
    @askForCompletedWork.setter     
    def _set_askForCompletedWork(self, value):
        self.native_obj.AskForCompletedWork = value
            
    # -> bool            
    @property         
    def autoAddResources(self) -> "bool":
        return (self.native_obj.AutoAddResources)
        
    @autoAddResources.setter     
    def _set_autoAddResources(self, value):
        self.native_obj.AutoAddResources = value
            
    # -> bool            
    @property         
    def autoCalcCosts(self) -> "bool":
        return (self.native_obj.AutoCalcCosts)
        
    @autoCalcCosts.setter     
    def _set_autoCalcCosts(self, value):
        self.native_obj.AutoCalcCosts = value
            
    # -> bool            
    @property         
    def autoFilter(self) -> "bool":
        return (self.native_obj.AutoFilter)
        
    @autoFilter.setter     
    def _set_autoFilter(self, value):
        self.native_obj.AutoFilter = value
            
    # -> bool            
    @property         
    def autoLinkTasks(self) -> "bool":
        return (self.native_obj.AutoLinkTasks)
        
    @autoLinkTasks.setter     
    def _set_autoLinkTasks(self, value):
        self.native_obj.AutoLinkTasks = value
            
    # -> bool            
    @property         
    def autoSplitTasks(self) -> "bool":
        return (self.native_obj.AutoSplitTasks)
        
    @autoSplitTasks.setter     
    def _set_autoSplitTasks(self, value):
        self.native_obj.AutoSplitTasks = value
            
    # -> bool            
    @property         
    def autoTrack(self) -> "bool":
        return (self.native_obj.AutoTrack)
        
    @autoTrack.setter     
    def _set_autoTrack(self, value):
        self.native_obj.AutoTrack = value
            
    # -> Calendars            
    @property         
    def baseCalendars(self) -> "Calendars":
        return Calendars(self.native_obj.BaseCalendars)
        
    @baseCalendars.setter     
    def _set_baseCalendars(self, value):
        self.native_obj.BaseCalendars = value
            
    # -> <class 'method            
    @property         
    def baselineSavedDate(self) -> "Any":
        return (self.native_obj.BaselineSavedDate)
        
    @baselineSavedDate.setter     
    def _set_baselineSavedDate(self, value):
        self.native_obj.BaselineSavedDate = value
            
    # -> CDispatch            
    @property         
    def builtinDocumentProperties(self) -> "Any":
        return (self.native_obj.BuiltinDocumentProperties)
        
    @builtinDocumentProperties.setter     
    def _set_builtinDocumentProperties(self, value):
        self.native_obj.BuiltinDocumentProperties = value
            
    # -> Calendar            
    @property         
    def calendar(self) -> "Calendar":
        return Calendar(self.native_obj.Calendar)
        
    @calendar.setter     
    def _set_calendar(self, value):
        self.native_obj.Calendar = value
            
    # -> int            
    @property         
    def canCheckIn(self) -> "int":
        return (self.native_obj.CanCheckIn)
        
    @canCheckIn.setter     
    def _set_canCheckIn(self, value):
        self.native_obj.CanCheckIn = value
            
    # -> str            
    @property         
    def codeName(self) -> "str":
        return (self.native_obj.CodeName)
        
    @codeName.setter     
    def _set_codeName(self, value):
        self.native_obj.CodeName = value
            
    # -> CDispatch            
    @property         
    def commandBars(self) -> "Any":
        return (self.native_obj.CommandBars)
        
    @commandBars.setter     
    def _set_commandBars(self, value):
        self.native_obj.CommandBars = value
            
    # -> Any            
    @property         
    def container(self) -> "Any":
        return (self.native_obj.Container)
        
    @container.setter     
    def _set_container(self, value):
        self.native_obj.Container = value
            
    # -> pywintypes.datetime            
    @property         
    def creationDate(self) -> "Any":
        return (self.native_obj.CreationDate)
        
    @creationDate.setter     
    def _set_creationDate(self, value):
        self.native_obj.CreationDate = value
            
    # -> str            
    @property         
    def currencyCode(self) -> "str":
        return (self.native_obj.CurrencyCode)
        
    @currencyCode.setter     
    def _set_currencyCode(self, value):
        self.native_obj.CurrencyCode = value
            
    # -> int            
    @property         
    def currencyDigits(self) -> "int":
        return (self.native_obj.CurrencyDigits)
        
    @currencyDigits.setter     
    def _set_currencyDigits(self, value):
        self.native_obj.CurrencyDigits = value
            
    # -> str            
    @property         
    def currencySymbol(self) -> "str":
        return (self.native_obj.CurrencySymbol)
        
    @currencySymbol.setter     
    def _set_currencySymbol(self, value):
        self.native_obj.CurrencySymbol = value
            
    # -> int            
    @property         
    def currencySymbolPosition(self) -> "int":
        return (self.native_obj.CurrencySymbolPosition)
        
    @currencySymbolPosition.setter     
    def _set_currencySymbolPosition(self, value):
        self.native_obj.CurrencySymbolPosition = value
            
    # -> pywintypes.datetime            
    @property         
    def currentDate(self) -> "Any":
        return (self.native_obj.CurrentDate)
        
    @currentDate.setter     
    def _set_currentDate(self, value):
        self.native_obj.CurrentDate = value
            
    # -> str            
    @property         
    def currentFilter(self) -> "str":
        return (self.native_obj.CurrentFilter)
        
    @currentFilter.setter     
    def _set_currentFilter(self, value):
        self.native_obj.CurrentFilter = value
            
    # -> str            
    @property         
    def currentGroup(self) -> "str":
        return (self.native_obj.CurrentGroup)
        
    @currentGroup.setter     
    def _set_currentGroup(self, value):
        self.native_obj.CurrentGroup = value
            
    # -> str            
    @property         
    def currentTable(self) -> "str":
        return (self.native_obj.CurrentTable)
        
    @currentTable.setter     
    def _set_currentTable(self, value):
        self.native_obj.CurrentTable = value
            
    # -> str            
    @property         
    def currentView(self) -> "str":
        return (self.native_obj.CurrentView)
        
    @currentView.setter     
    def _set_currentView(self, value):
        self.native_obj.CurrentView = value
            
    # -> CDispatch            
    @property         
    def customDocumentProperties(self) -> "Any":
        return (self.native_obj.CustomDocumentProperties)
        
    @customDocumentProperties.setter     
    def _set_customDocumentProperties(self, value):
        self.native_obj.CustomDocumentProperties = value
            
    # -> int            
    @property         
    def databaseProjectUniqueID(self) -> "int":
        return (self.native_obj.DatabaseProjectUniqueID)
        
    @databaseProjectUniqueID.setter     
    def _set_databaseProjectUniqueID(self, value):
        self.native_obj.DatabaseProjectUniqueID = value
            
    # -> int            
    @property         
    def dayLabelDisplay(self) -> "int":
        return (self.native_obj.DayLabelDisplay)
        
    @dayLabelDisplay.setter     
    def _set_dayLabelDisplay(self, value):
        self.native_obj.DayLabelDisplay = value
            
    # -> int            
    @property         
    def daysPerMonth(self) -> "int":
        return (self.native_obj.DaysPerMonth)
        
    @daysPerMonth.setter     
    def _set_daysPerMonth(self, value):
        self.native_obj.DaysPerMonth = value
            
    # -> int            
    @property         
    def defaultDurationUnits(self) -> "int":
        return (self.native_obj.DefaultDurationUnits)
        
    @defaultDurationUnits.setter     
    def _set_defaultDurationUnits(self, value):
        self.native_obj.DefaultDurationUnits = value
            
    # -> int            
    @property         
    def defaultEarnedValueMethod(self) -> "int":
        return (self.native_obj.DefaultEarnedValueMethod)
        
    @defaultEarnedValueMethod.setter     
    def _set_defaultEarnedValueMethod(self, value):
        self.native_obj.DefaultEarnedValueMethod = value
            
    # -> bool            
    @property         
    def defaultEffortDriven(self) -> "bool":
        return (self.native_obj.DefaultEffortDriven)
        
    @defaultEffortDriven.setter     
    def _set_defaultEffortDriven(self, value):
        self.native_obj.DefaultEffortDriven = value
            
    # -> pywintypes.datetime            
    @property         
    def defaultFinishTime(self) -> "Any":
        return (self.native_obj.DefaultFinishTime)
        
    @defaultFinishTime.setter     
    def _set_defaultFinishTime(self, value):
        self.native_obj.DefaultFinishTime = value
            
    # -> int            
    @property         
    def defaultFixedCostAccrual(self) -> "int":
        return (self.native_obj.DefaultFixedCostAccrual)
        
    @defaultFixedCostAccrual.setter     
    def _set_defaultFixedCostAccrual(self, value):
        self.native_obj.DefaultFixedCostAccrual = value
            
    # -> str            
    @property         
    def defaultResourceOvertimeRate(self) -> "str":
        return (self.native_obj.DefaultResourceOvertimeRate)
        
    @defaultResourceOvertimeRate.setter     
    def _set_defaultResourceOvertimeRate(self, value):
        self.native_obj.DefaultResourceOvertimeRate = value
            
    # -> str            
    @property         
    def defaultResourceStandardRate(self) -> "str":
        return (self.native_obj.DefaultResourceStandardRate)
        
    @defaultResourceStandardRate.setter     
    def _set_defaultResourceStandardRate(self, value):
        self.native_obj.DefaultResourceStandardRate = value
            
    # -> pywintypes.datetime            
    @property         
    def defaultStartTime(self) -> "Any":
        return (self.native_obj.DefaultStartTime)
        
    @defaultStartTime.setter     
    def _set_defaultStartTime(self, value):
        self.native_obj.DefaultStartTime = value
            
    # -> int            
    @property         
    def defaultTaskType(self) -> "int":
        return (self.native_obj.DefaultTaskType)
        
    @defaultTaskType.setter     
    def _set_defaultTaskType(self, value):
        self.native_obj.DefaultTaskType = value
            
    # -> int            
    @property         
    def defaultWorkUnits(self) -> "int":
        return (self.native_obj.DefaultWorkUnits)
        
    @defaultWorkUnits.setter     
    def _set_defaultWorkUnits(self, value):
        self.native_obj.DefaultWorkUnits = value
            
    # -> Tasks            
    @property         
    def detectCycle(self) -> "Tasks":
        return Tasks(self.native_obj.DetectCycle)
        
    @detectCycle.setter     
    def _set_detectCycle(self, value):
        self.native_obj.DetectCycle = value
            
    # -> bool            
    @property         
    def displayProjectSummaryTask(self) -> "bool":
        return (self.native_obj.DisplayProjectSummaryTask)
        
    @displayProjectSummaryTask.setter     
    def _set_displayProjectSummaryTask(self, value):
        self.native_obj.DisplayProjectSummaryTask = value
            
    # -> NoneType            
    @property         
    def documentLibraryVersions(self) -> "Any":
        return (self.native_obj.DocumentLibraryVersions)
        
    @documentLibraryVersions.setter     
    def _set_documentLibraryVersions(self, value):
        self.native_obj.DocumentLibraryVersions = value
            
    # -> int            
    @property         
    def earnedValueBaseline(self) -> "int":
        return (self.native_obj.EarnedValueBaseline)
        
    @earnedValueBaseline.setter     
    def _set_earnedValueBaseline(self, value):
        self.native_obj.EarnedValueBaseline = value
            
    # -> Engagements            
    @property         
    def engagements(self) -> "Engagements":
        return Engagements(self.native_obj.Engagements)
        
    @engagements.setter     
    def _set_engagements(self, value):
        self.native_obj.Engagements = value
            
    # -> bool            
    @property         
    def enterpriseActualsSynched(self) -> "bool":
        return (self.native_obj.EnterpriseActualsSynched)
        
    @enterpriseActualsSynched.setter     
    def _set_enterpriseActualsSynched(self, value):
        self.native_obj.EnterpriseActualsSynched = value
            
    # -> bool            
    @property         
    def expandDatabaseTimephasedData(self) -> "bool":
        return (self.native_obj.ExpandDatabaseTimephasedData)
        
    @expandDatabaseTimephasedData.setter     
    def _set_expandDatabaseTimephasedData(self, value):
        self.native_obj.ExpandDatabaseTimephasedData = value
            
    # -> int            
    @property         
    def followedHyperlinkColor(self) -> "int":
        return (self.native_obj.FollowedHyperlinkColor)
        
    @followedHyperlinkColor.setter     
    def _set_followedHyperlinkColor(self, value):
        self.native_obj.FollowedHyperlinkColor = value
            
    # -> int            
    @property         
    def followedHyperlinkColorEx(self) -> "int":
        return (self.native_obj.FollowedHyperlinkColorEx)
        
    @followedHyperlinkColorEx.setter     
    def _set_followedHyperlinkColorEx(self, value):
        self.native_obj.FollowedHyperlinkColorEx = value
            
    # -> str            
    @property         
    def fullName(self) -> "str":
        return (self.native_obj.FullName)
        
    @fullName.setter     
    def _set_fullName(self, value):
        self.native_obj.FullName = value
            
    # -> bool            
    @property         
    def hasPassword(self) -> "bool":
        return (self.native_obj.HasPassword)
        
    @hasPassword.setter     
    def _set_hasPassword(self, value):
        self.native_obj.HasPassword = value
            
    # -> bool            
    @property         
    def honorConstraints(self) -> "bool":
        return (self.native_obj.HonorConstraints)
        
    @honorConstraints.setter     
    def _set_honorConstraints(self, value):
        self.native_obj.HonorConstraints = value
            
    # -> int            
    @property         
    def hourLabelDisplay(self) -> "int":
        return (self.native_obj.HourLabelDisplay)
        
    @hourLabelDisplay.setter     
    def _set_hourLabelDisplay(self, value):
        self.native_obj.HourLabelDisplay = value
            
    # -> float            
    @property         
    def hoursPerDay(self) -> "float":
        return (self.native_obj.HoursPerDay)
        
    @hoursPerDay.setter     
    def _set_hoursPerDay(self, value):
        self.native_obj.HoursPerDay = value
            
    # -> float            
    @property         
    def hoursPerWeek(self) -> "float":
        return (self.native_obj.HoursPerWeek)
        
    @hoursPerWeek.setter     
    def _set_hoursPerWeek(self, value):
        self.native_obj.HoursPerWeek = value
            
    # -> int            
    @property         
    def hyperlinkColor(self) -> "int":
        return (self.native_obj.HyperlinkColor)
        
    @hyperlinkColor.setter     
    def _set_hyperlinkColor(self, value):
        self.native_obj.HyperlinkColor = value
            
    # -> int            
    @property         
    def hyperlinkColorEx(self) -> "int":
        return (self.native_obj.HyperlinkColorEx)
        
    @hyperlinkColorEx.setter     
    def _set_hyperlinkColorEx(self, value):
        self.native_obj.HyperlinkColorEx = value
            
    # -> int            
    @property         
    def iD(self) -> "int":
        return (self.native_obj.ID)
        
    @iD.setter     
    def _set_iD(self, value):
        self.native_obj.ID = value
            
    # -> int            
    @property         
    def index(self) -> "int":
        return (self.native_obj.Index)
        
    @index.setter     
    def _set_index(self, value):
        self.native_obj.Index = value
            
    # -> bool            
    @property         
    def isCheckoutMsgBarVisible(self) -> "bool":
        return (self.native_obj.IsCheckoutMsgBarVisible)
        
    @isCheckoutMsgBarVisible.setter     
    def _set_isCheckoutMsgBarVisible(self, value):
        self.native_obj.IsCheckoutMsgBarVisible = value
            
    # -> bool            
    @property         
    def isCheckoutOSVisible(self) -> "bool":
        return (self.native_obj.IsCheckoutOSVisible)
        
    @isCheckoutOSVisible.setter     
    def _set_isCheckoutOSVisible(self, value):
        self.native_obj.IsCheckoutOSVisible = value
            
    # -> bool            
    @property         
    def isTemplate(self) -> "bool":
        return (self.native_obj.IsTemplate)
        
    @isTemplate.setter     
    def _set_isTemplate(self, value):
        self.native_obj.IsTemplate = value
            
    # -> bool            
    @property         
    def keepTaskOnNearestWorkingTimeWhenMadeAutoScheduled(self) -> "bool":
        return (self.native_obj.KeepTaskOnNearestWorkingTimeWhenMadeAutoScheduled)
        
    @keepTaskOnNearestWorkingTimeWhenMadeAutoScheduled.setter     
    def _set_keepTaskOnNearestWorkingTimeWhenMadeAutoScheduled(self, value):
        self.native_obj.KeepTaskOnNearestWorkingTimeWhenMadeAutoScheduled = value
            
    # -> pywintypes.datetime            
    @property         
    def lastPrintedDate(self) -> "Any":
        return (self.native_obj.LastPrintedDate)
        
    @lastPrintedDate.setter     
    def _set_lastPrintedDate(self, value):
        self.native_obj.LastPrintedDate = value
            
    # -> pywintypes.datetime            
    @property         
    def lastSaveDate(self) -> "Any":
        return (self.native_obj.LastSaveDate)
        
    @lastSaveDate.setter     
    def _set_lastSaveDate(self, value):
        self.native_obj.LastSaveDate = value
            
    # -> str            
    @property         
    def lastSavedBy(self) -> "str":
        return (self.native_obj.LastSavedBy)
        
    @lastSavedBy.setter     
    def _set_lastSavedBy(self, value):
        self.native_obj.LastSavedBy = value
            
    # -> <class 'method            
    @property         
    def lastWssSyncDate(self) -> "Any":
        return (self.native_obj.LastWssSyncDate)
        
    @lastWssSyncDate.setter     
    def _set_lastWssSyncDate(self, value):
        self.native_obj.LastWssSyncDate = value
            
    # -> bool            
    @property         
    def levelEntireProject(self) -> "bool":
        return (self.native_obj.LevelEntireProject)
        
    @levelEntireProject.setter     
    def _set_levelEntireProject(self, value):
        self.native_obj.LevelEntireProject = value
            
    # -> pywintypes.datetime            
    @property         
    def levelFromDate(self) -> "Any":
        return (self.native_obj.LevelFromDate)
        
    @levelFromDate.setter     
    def _set_levelFromDate(self, value):
        self.native_obj.LevelFromDate = value
            
    # -> pywintypes.datetime            
    @property         
    def levelToDate(self) -> "Any":
        return (self.native_obj.LevelToDate)
        
    @levelToDate.setter     
    def _set_levelToDate(self, value):
        self.native_obj.LevelToDate = value
            
    # -> bool            
    @property         
    def manuallyScheduledTasksAutoRespectLinks(self) -> "bool":
        return (self.native_obj.ManuallyScheduledTasksAutoRespectLinks)
        
    @manuallyScheduledTasksAutoRespectLinks.setter     
    def _set_manuallyScheduledTasksAutoRespectLinks(self, value):
        self.native_obj.ManuallyScheduledTasksAutoRespectLinks = value
            
    # -> List            
    @property         
    def mapList(self) -> "List":
        return List(self.native_obj.MapList)
        
    @mapList.setter     
    def _set_mapList(self, value):
        self.native_obj.MapList = value
            
    # -> int            
    @property         
    def minuteLabelDisplay(self) -> "int":
        return (self.native_obj.MinuteLabelDisplay)
        
    @minuteLabelDisplay.setter     
    def _set_minuteLabelDisplay(self, value):
        self.native_obj.MinuteLabelDisplay = value
            
    # -> int            
    @property         
    def monthLabelDisplay(self) -> "int":
        return (self.native_obj.MonthLabelDisplay)
        
    @monthLabelDisplay.setter     
    def _set_monthLabelDisplay(self, value):
        self.native_obj.MonthLabelDisplay = value
            
    # -> bool            
    @property         
    def moveCompleted(self) -> "bool":
        return (self.native_obj.MoveCompleted)
        
    @moveCompleted.setter     
    def _set_moveCompleted(self, value):
        self.native_obj.MoveCompleted = value
            
    # -> bool            
    @property         
    def moveRemaining(self) -> "bool":
        return (self.native_obj.MoveRemaining)
        
    @moveRemaining.setter     
    def _set_moveRemaining(self, value):
        self.native_obj.MoveRemaining = value
            
    # -> bool            
    @property         
    def multipleCriticalPaths(self) -> "bool":
        return (self.native_obj.MultipleCriticalPaths)
        
    @multipleCriticalPaths.setter     
    def _set_multipleCriticalPaths(self, value):
        self.native_obj.MultipleCriticalPaths = value
            
    # -> str            
    @property         
    def name(self) -> "str":
        return (self.native_obj.Name)
        
    @name.setter     
    def _set_name(self, value):
        self.native_obj.Name = value
            
    # -> bool            
    @property         
    def newTasksCreatedAsManual(self) -> "bool":
        return (self.native_obj.NewTasksCreatedAsManual)
        
    @newTasksCreatedAsManual.setter     
    def _set_newTasksCreatedAsManual(self, value):
        self.native_obj.NewTasksCreatedAsManual = value
            
    # -> bool            
    @property         
    def newTasksEstimated(self) -> "bool":
        return (self.native_obj.NewTasksEstimated)
        
    @newTasksEstimated.setter     
    def _set_newTasksEstimated(self, value):
        self.native_obj.NewTasksEstimated = value
            
    # -> int            
    @property         
    def numberOfResources(self) -> "int":
        return (self.native_obj.NumberOfResources)
        
    @numberOfResources.setter     
    def _set_numberOfResources(self, value):
        self.native_obj.NumberOfResources = value
            
    # -> int            
    @property         
    def numberOfTasks(self) -> "int":
        return (self.native_obj.NumberOfTasks)
        
    @numberOfTasks.setter     
    def _set_numberOfTasks(self, value):
        self.native_obj.NumberOfTasks = value
            
    # -> Tasks            
    @property         
    def outlineChildren(self) -> "Tasks":
        return Tasks(self.native_obj.OutlineChildren)
        
    @outlineChildren.setter     
    def _set_outlineChildren(self, value):
        self.native_obj.OutlineChildren = value
            
    # -> OutlineCodes            
    @property         
    def outlineCodes(self) -> "OutlineCodes":
        return OutlineCodes(self.native_obj.OutlineCodes)
        
    @outlineCodes.setter     
    def _set_outlineCodes(self, value):
        self.native_obj.OutlineCodes = value
            
    # -> _MSProject            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> str            
    @property         
    def path(self) -> "str":
        return (self.native_obj.Path)
        
    @path.setter     
    def _set_path(self, value):
        self.native_obj.Path = value
            
    # -> int            
    @property         
    def phoneticType(self) -> "int":
        return (self.native_obj.PhoneticType)
        
    @phoneticType.setter     
    def _set_phoneticType(self, value):
        self.native_obj.PhoneticType = value
            
    # -> pywintypes.datetime            
    @property         
    def projectFinish(self) -> "Any":
        return (self.native_obj.ProjectFinish)
        
    @projectFinish.setter     
    def _set_projectFinish(self, value):
        self.native_obj.ProjectFinish = value
            
    # -> str            
    @property         
    def projectGuideContent(self) -> "str":
        return (self.native_obj.ProjectGuideContent)
        
    @projectGuideContent.setter     
    def _set_projectGuideContent(self, value):
        self.native_obj.ProjectGuideContent = value
            
    # -> str            
    @property         
    def projectGuideFunctionalLayoutPage(self) -> "str":
        return (self.native_obj.ProjectGuideFunctionalLayoutPage)
        
    @projectGuideFunctionalLayoutPage.setter     
    def _set_projectGuideFunctionalLayoutPage(self, value):
        self.native_obj.ProjectGuideFunctionalLayoutPage = value
            
    # -> str            
    @property         
    def projectGuideSaveBuffer(self) -> "str":
        return (self.native_obj.ProjectGuideSaveBuffer)
        
    @projectGuideSaveBuffer.setter     
    def _set_projectGuideSaveBuffer(self, value):
        self.native_obj.ProjectGuideSaveBuffer = value
            
    # -> bool            
    @property         
    def projectGuideUseDefaultContent(self) -> "bool":
        return (self.native_obj.ProjectGuideUseDefaultContent)
        
    @projectGuideUseDefaultContent.setter     
    def _set_projectGuideUseDefaultContent(self, value):
        self.native_obj.ProjectGuideUseDefaultContent = value
            
    # -> bool            
    @property         
    def projectGuideUseDefaultFunctionalLayoutPage(self) -> "bool":
        return (self.native_obj.ProjectGuideUseDefaultFunctionalLayoutPage)
        
    @projectGuideUseDefaultFunctionalLayoutPage.setter     
    def _set_projectGuideUseDefaultFunctionalLayoutPage(self, value):
        self.native_obj.ProjectGuideUseDefaultFunctionalLayoutPage = value
            
    # -> str            
    @property         
    def projectNamePrefix(self) -> "str":
        return (self.native_obj.ProjectNamePrefix)
        
    @projectNamePrefix.setter     
    def _set_projectNamePrefix(self, value):
        self.native_obj.ProjectNamePrefix = value
            
    # -> str            
    @property         
    def projectNotes(self) -> "str":
        return (self.native_obj.ProjectNotes)
        
    @projectNotes.setter     
    def _set_projectNotes(self, value):
        self.native_obj.ProjectNotes = value
            
    # -> bool            
    @property         
    def projectServerUsedForTracking(self) -> "bool":
        return (self.native_obj.ProjectServerUsedForTracking)
        
    @projectServerUsedForTracking.setter     
    def _set_projectServerUsedForTracking(self, value):
        self.native_obj.ProjectServerUsedForTracking = value
            
    # -> pywintypes.datetime            
    @property         
    def projectStart(self) -> "Any":
        return (self.native_obj.ProjectStart)
        
    @projectStart.setter     
    def _set_projectStart(self, value):
        self.native_obj.ProjectStart = value
            
    # -> Task            
    @property         
    def projectSummaryTask(self) -> "Task":
        return Task(self.native_obj.ProjectSummaryTask)
        
    @projectSummaryTask.setter     
    def _set_projectSummaryTask(self, value):
        self.native_obj.ProjectSummaryTask = value
            
    # -> bool            
    @property         
    def readOnly(self) -> "bool":
        return (self.native_obj.ReadOnly)
        
    @readOnly.setter     
    def _set_readOnly(self, value):
        self.native_obj.ReadOnly = value
            
    # -> bool            
    @property         
    def readOnlyRecommended(self) -> "bool":
        return (self.native_obj.ReadOnlyRecommended)
        
    @readOnlyRecommended.setter     
    def _set_readOnlyRecommended(self, value):
        self.native_obj.ReadOnlyRecommended = value
            
    # -> bool            
    @property         
    def receiveNotifications(self) -> "bool":
        return (self.native_obj.ReceiveNotifications)
        
    @receiveNotifications.setter     
    def _set_receiveNotifications(self, value):
        self.native_obj.ReceiveNotifications = value
            
    # -> bool            
    @property         
    def removeFileProperties(self) -> "bool":
        return (self.native_obj.RemoveFileProperties)
        
    @removeFileProperties.setter     
    def _set_removeFileProperties(self, value):
        self.native_obj.RemoveFileProperties = value
            
    # -> List            
    @property         
    def reportList(self) -> "List":
        return List(self.native_obj.ReportList)
        
    @reportList.setter     
    def _set_reportList(self, value):
        self.native_obj.ReportList = value
            
    # -> Reports            
    @property         
    def reports(self) -> "Reports":
        return Reports(self.native_obj.Reports)
        
    @reports.setter     
    def _set_reports(self, value):
        self.native_obj.Reports = value
            
    # -> List            
    @property         
    def resourceFilterList(self) -> "List":
        return List(self.native_obj.ResourceFilterList)
        
    @resourceFilterList.setter     
    def _set_resourceFilterList(self, value):
        self.native_obj.ResourceFilterList = value
            
    # -> Filters            
    @property         
    def resourceFilters(self) -> "Filters":
        return Filters(self.native_obj.ResourceFilters)
        
    @resourceFilters.setter     
    def _set_resourceFilters(self, value):
        self.native_obj.ResourceFilters = value
            
    # -> List            
    @property         
    def resourceGroupList(self) -> "List":
        return List(self.native_obj.ResourceGroupList)
        
    @resourceGroupList.setter     
    def _set_resourceGroupList(self, value):
        self.native_obj.ResourceGroupList = value
            
    # -> ResourceGroups            
    @property         
    def resourceGroups(self) -> "ResourceGroups":
        return ResourceGroups(self.native_obj.ResourceGroups)
        
    @resourceGroups.setter     
    def _set_resourceGroups(self, value):
        self.native_obj.ResourceGroups = value
            
    # -> ResourceGroups2            
    @property         
    def resourceGroups2(self) -> "ResourceGroups2":
        return ResourceGroups2(self.native_obj.ResourceGroups2)
        
    @resourceGroups2.setter     
    def _set_resourceGroups2(self, value):
        self.native_obj.ResourceGroups2 = value
            
    # -> str            
    @property         
    def resourcePoolName(self) -> "str":
        return (self.native_obj.ResourcePoolName)
        
    @resourcePoolName.setter     
    def _set_resourcePoolName(self, value):
        self.native_obj.ResourcePoolName = value
            
    # -> Resources            
    @property         
    def resources(self) -> "Resources":
        return Resources(self.native_obj.Resources)
        
    @resources.setter     
    def _set_resources(self, value):
        self.native_obj.Resources = value
            
    # -> List            
    @property         
    def resourceTableList(self) -> "List":
        return List(self.native_obj.ResourceTableList)
        
    @resourceTableList.setter     
    def _set_resourceTableList(self, value):
        self.native_obj.ResourceTableList = value
            
    # -> Tables            
    @property         
    def resourceTables(self) -> "Tables":
        return Tables(self.native_obj.ResourceTables)
        
    @resourceTables.setter     
    def _set_resourceTables(self, value):
        self.native_obj.ResourceTables = value
            
    # -> List            
    @property         
    def resourceViewList(self) -> "List":
        return List(self.native_obj.ResourceViewList)
        
    @resourceViewList.setter     
    def _set_resourceViewList(self, value):
        self.native_obj.ResourceViewList = value
            
    # -> str            
    @property         
    def revisionNumber(self) -> "str":
        return (self.native_obj.RevisionNumber)
        
    @revisionNumber.setter     
    def _set_revisionNumber(self, value):
        self.native_obj.RevisionNumber = value
            
    # -> bool            
    @property         
    def saved(self) -> "bool":
        return (self.native_obj.Saved)
        
    @saved.setter     
    def _set_saved(self, value):
        self.native_obj.Saved = value
            
    # -> bool            
    @property         
    def scheduleFromStart(self) -> "bool":
        return (self.native_obj.ScheduleFromStart)
        
    @scheduleFromStart.setter     
    def _set_scheduleFromStart(self, value):
        self.native_obj.ScheduleFromStart = value
            
    # -> bool            
    @property         
    def sendHyperlinkNote(self) -> "bool":
        return (self.native_obj.SendHyperlinkNote)
        
    @sendHyperlinkNote.setter     
    def _set_sendHyperlinkNote(self, value):
        self.native_obj.SendHyperlinkNote = value
            
    # -> int            
    @property         
    def serverIdentification(self) -> "int":
        return (self.native_obj.ServerIdentification)
        
    @serverIdentification.setter     
    def _set_serverIdentification(self, value):
        self.native_obj.ServerIdentification = value
            
    # -> str            
    @property         
    def serverURL(self) -> "str":
        return (self.native_obj.ServerURL)
        
    @serverURL.setter     
    def _set_serverURL(self, value):
        self.native_obj.ServerURL = value
            
    # -> NoneType            
    @property         
    def sharedWorkspace(self) -> "Any":
        return (self.native_obj.SharedWorkspace)
        
    @sharedWorkspace.setter     
    def _set_sharedWorkspace(self, value):
        self.native_obj.SharedWorkspace = value
            
    # -> int            
    @property         
    def showCriticalSlack(self) -> "int":
        return (self.native_obj.ShowCriticalSlack)
        
    @showCriticalSlack.setter     
    def _set_showCriticalSlack(self, value):
        self.native_obj.ShowCriticalSlack = value
            
    # -> bool            
    @property         
    def showCrossProjectLinksInfo(self) -> "bool":
        return (self.native_obj.ShowCrossProjectLinksInfo)
        
    @showCrossProjectLinksInfo.setter     
    def _set_showCrossProjectLinksInfo(self, value):
        self.native_obj.ShowCrossProjectLinksInfo = value
            
    # -> bool            
    @property         
    def showEstimatedDuration(self) -> "bool":
        return (self.native_obj.ShowEstimatedDuration)
        
    @showEstimatedDuration.setter     
    def _set_showEstimatedDuration(self, value):
        self.native_obj.ShowEstimatedDuration = value
            
    # -> bool            
    @property         
    def showExternalPredecessors(self) -> "bool":
        return (self.native_obj.ShowExternalPredecessors)
        
    @showExternalPredecessors.setter     
    def _set_showExternalPredecessors(self, value):
        self.native_obj.ShowExternalPredecessors = value
            
    # -> bool            
    @property         
    def showExternalSuccessors(self) -> "bool":
        return (self.native_obj.ShowExternalSuccessors)
        
    @showExternalSuccessors.setter     
    def _set_showExternalSuccessors(self, value):
        self.native_obj.ShowExternalSuccessors = value
            
    # -> bool            
    @property         
    def showTaskSuggestions(self) -> "bool":
        return (self.native_obj.ShowTaskSuggestions)
        
    @showTaskSuggestions.setter     
    def _set_showTaskSuggestions(self, value):
        self.native_obj.ShowTaskSuggestions = value
            
    # -> bool            
    @property         
    def showTaskWarnings(self) -> "bool":
        return (self.native_obj.ShowTaskWarnings)
        
    @showTaskWarnings.setter     
    def _set_showTaskWarnings(self, value):
        self.native_obj.ShowTaskWarnings = value
            
    # -> bool            
    @property         
    def spaceBeforeTimeLabels(self) -> "bool":
        return (self.native_obj.SpaceBeforeTimeLabels)
        
    @spaceBeforeTimeLabels.setter     
    def _set_spaceBeforeTimeLabels(self, value):
        self.native_obj.SpaceBeforeTimeLabels = value
            
    # -> bool            
    @property         
    def spreadCostsToStatusDate(self) -> "bool":
        return (self.native_obj.SpreadCostsToStatusDate)
        
    @spreadCostsToStatusDate.setter     
    def _set_spreadCostsToStatusDate(self, value):
        self.native_obj.SpreadCostsToStatusDate = value
            
    # -> bool            
    @property         
    def spreadPercentCompleteToStatusDate(self) -> "bool":
        return (self.native_obj.SpreadPercentCompleteToStatusDate)
        
    @spreadPercentCompleteToStatusDate.setter     
    def _set_spreadPercentCompleteToStatusDate(self, value):
        self.native_obj.SpreadPercentCompleteToStatusDate = value
            
    # -> bool            
    @property         
    def startOnCurrentDate(self) -> "bool":
        return (self.native_obj.StartOnCurrentDate)
        
    @startOnCurrentDate.setter     
    def _set_startOnCurrentDate(self, value):
        self.native_obj.StartOnCurrentDate = value
            
    # -> int            
    @property         
    def startWeekOn(self) -> "int":
        return (self.native_obj.StartWeekOn)
        
    @startWeekOn.setter     
    def _set_startWeekOn(self, value):
        self.native_obj.StartWeekOn = value
            
    # -> int            
    @property         
    def startYearIn(self) -> "int":
        return (self.native_obj.StartYearIn)
        
    @startYearIn.setter     
    def _set_startYearIn(self, value):
        self.native_obj.StartYearIn = value
            
    # -> str            
    @property         
    def statusDate(self) -> "str":
        return (self.native_obj.StatusDate)
        
    @statusDate.setter     
    def _set_statusDate(self, value):
        self.native_obj.StatusDate = value
            
    # -> Subprojects            
    @property         
    def subprojects(self) -> "Subprojects":
        return Subprojects(self.native_obj.Subprojects)
        
    @subprojects.setter     
    def _set_subprojects(self, value):
        self.native_obj.Subprojects = value
            
    # -> int            
    @property         
    def taskErrorCount(self) -> "int":
        return (self.native_obj.TaskErrorCount)
        
    @taskErrorCount.setter     
    def _set_taskErrorCount(self, value):
        self.native_obj.TaskErrorCount = value
            
    # -> List            
    @property         
    def taskFilterList(self) -> "List":
        return List(self.native_obj.TaskFilterList)
        
    @taskFilterList.setter     
    def _set_taskFilterList(self, value):
        self.native_obj.TaskFilterList = value
            
    # -> Filters            
    @property         
    def taskFilters(self) -> "Filters":
        return Filters(self.native_obj.TaskFilters)
        
    @taskFilters.setter     
    def _set_taskFilters(self, value):
        self.native_obj.TaskFilters = value
            
    # -> List            
    @property         
    def taskGroupList(self) -> "List":
        return List(self.native_obj.TaskGroupList)
        
    @taskGroupList.setter     
    def _set_taskGroupList(self, value):
        self.native_obj.TaskGroupList = value
            
    # -> TaskGroups            
    @property         
    def taskGroups(self) -> "TaskGroups":
        return TaskGroups(self.native_obj.TaskGroups)
        
    @taskGroups.setter     
    def _set_taskGroups(self, value):
        self.native_obj.TaskGroups = value
            
    # -> TaskGroups2            
    @property         
    def taskGroups2(self) -> "TaskGroups2":
        return TaskGroups2(self.native_obj.TaskGroups2)
        
    @taskGroups2.setter     
    def _set_taskGroups2(self, value):
        self.native_obj.TaskGroups2 = value
            
    # -> Tasks            
    @property         
    def tasks(self) -> "Tasks":
        return Tasks(self.native_obj.Tasks)
        
    @tasks.setter     
    def _set_tasks(self, value):
        self.native_obj.Tasks = value
            
    # -> List            
    @property         
    def taskTableList(self) -> "List":
        return List(self.native_obj.TaskTableList)
        
    @taskTableList.setter     
    def _set_taskTableList(self, value):
        self.native_obj.TaskTableList = value
            
    # -> Tables            
    @property         
    def taskTables(self) -> "Tables":
        return Tables(self.native_obj.TaskTables)
        
    @taskTables.setter     
    def _set_taskTables(self, value):
        self.native_obj.TaskTables = value
            
    # -> List            
    @property         
    def taskViewList(self) -> "List":
        return List(self.native_obj.TaskViewList)
        
    @taskViewList.setter     
    def _set_taskViewList(self, value):
        self.native_obj.TaskViewList = value
            
    # -> str            
    @property         
    def template(self) -> "str":
        return (self.native_obj.Template)
        
    @template.setter     
    def _set_template(self, value):
        self.native_obj.Template = value
            
    # -> Timeline            
    @property         
    def timeline(self) -> "Timeline":
        return Timeline(self.native_obj.Timeline)
        
    @timeline.setter     
    def _set_timeline(self, value):
        self.native_obj.Timeline = value
            
    # -> int            
    @property         
    def trackingMethod(self) -> "int":
        return (self.native_obj.TrackingMethod)
        
    @trackingMethod.setter     
    def _set_trackingMethod(self, value):
        self.native_obj.TrackingMethod = value
            
    # -> int            
    @property         
    def type(self) -> "int":
        return (self.native_obj.Type)
        
    @type.setter     
    def _set_type(self, value):
        self.native_obj.Type = value
            
    # -> bool            
    @property         
    def underlineHyperlinks(self) -> "bool":
        return (self.native_obj.UnderlineHyperlinks)
        
    @underlineHyperlinks.setter     
    def _set_underlineHyperlinks(self, value):
        self.native_obj.UnderlineHyperlinks = value
            
    # -> int            
    @property         
    def uniqueID(self) -> "int":
        return (self.native_obj.UniqueID)
        
    @uniqueID.setter     
    def _set_uniqueID(self, value):
        self.native_obj.UniqueID = value
            
    # -> bool            
    @property         
    def updateProjOnSave(self) -> "bool":
        return (self.native_obj.UpdateProjOnSave)
        
    @updateProjOnSave.setter     
    def _set_updateProjOnSave(self, value):
        self.native_obj.UpdateProjOnSave = value
            
    # -> bool            
    @property         
    def useFYStartYear(self) -> "bool":
        return (self.native_obj.UseFYStartYear)
        
    @useFYStartYear.setter     
    def _set_useFYStartYear(self, value):
        self.native_obj.UseFYStartYear = value
            
    # -> bool            
    @property         
    def userControl(self) -> "bool":
        return (self.native_obj.UserControl)
        
    @userControl.setter     
    def _set_userControl(self, value):
        self.native_obj.UserControl = value
            
    # -> NoneType            
    @property         
    def utilizationDate(self) -> "Any":
        return (self.native_obj.UtilizationDate)
        
    @utilizationDate.setter     
    def _set_utilizationDate(self, value):
        self.native_obj.UtilizationDate = value
            
    # -> NoneType            
    @property         
    def utilizationType(self) -> "Any":
        return (self.native_obj.UtilizationType)
        
    @utilizationType.setter     
    def _set_utilizationType(self, value):
        self.native_obj.UtilizationType = value
            
    # -> bool            
    @property         
    def vBASigned(self) -> "bool":
        return (self.native_obj.VBASigned)
        
    @vBASigned.setter     
    def _set_vBASigned(self, value):
        self.native_obj.VBASigned = value
            
    # -> CDispatch            
    @property         
    def vBProject(self) -> "Any":
        return (self.native_obj.VBProject)
        
    @vBProject.setter     
    def _set_vBProject(self, value):
        self.native_obj.VBProject = value
            
    # -> str            
    @property         
    def versionName(self) -> "str":
        return (self.native_obj.VersionName)
        
    @versionName.setter     
    def _set_versionName(self, value):
        self.native_obj.VersionName = value
            
    # -> List            
    @property         
    def viewList(self) -> "List":
        return List(self.native_obj.ViewList)
        
    @viewList.setter     
    def _set_viewList(self, value):
        self.native_obj.ViewList = value
            
    # -> Views            
    @property         
    def views(self) -> "Views":
        return Views(self.native_obj.Views)
        
    @views.setter     
    def _set_views(self, value):
        self.native_obj.Views = value
            
    # -> ViewsCombination            
    @property         
    def viewsCombination(self) -> "ViewsCombination":
        return ViewsCombination(self.native_obj.ViewsCombination)
        
    @viewsCombination.setter     
    def _set_viewsCombination(self, value):
        self.native_obj.ViewsCombination = value
            
    # -> ViewsSingle            
    @property         
    def viewsSingle(self) -> "ViewsSingle":
        return ViewsSingle(self.native_obj.ViewsSingle)
        
    @viewsSingle.setter     
    def _set_viewsSingle(self, value):
        self.native_obj.ViewsSingle = value
            
    # -> bool            
    @property         
    def wBSCodeGenerate(self) -> "bool":
        return (self.native_obj.WBSCodeGenerate)
        
    @wBSCodeGenerate.setter     
    def _set_wBSCodeGenerate(self, value):
        self.native_obj.WBSCodeGenerate = value
            
    # -> bool            
    @property         
    def wBSVerifyUniqueness(self) -> "bool":
        return (self.native_obj.WBSVerifyUniqueness)
        
    @wBSVerifyUniqueness.setter     
    def _set_wBSVerifyUniqueness(self, value):
        self.native_obj.WBSVerifyUniqueness = value
            
    # -> int            
    @property         
    def weekLabelDisplay(self) -> "int":
        return (self.native_obj.WeekLabelDisplay)
        
    @weekLabelDisplay.setter     
    def _set_weekLabelDisplay(self, value):
        self.native_obj.WeekLabelDisplay = value
            
    # -> Windows            
    @property         
    def windows(self) -> "Windows":
        return Windows(self.native_obj.Windows)
        
    @windows.setter     
    def _set_windows(self, value):
        self.native_obj.Windows = value
            
    # -> Windows2            
    @property         
    def windows2(self) -> "Windows2":
        return Windows2(self.native_obj.Windows2)
        
    @windows2.setter     
    def _set_windows2(self, value):
        self.native_obj.Windows2 = value
            
    # -> bool            
    @property         
    def writeReserved(self) -> "bool":
        return (self.native_obj.WriteReserved)
        
    @writeReserved.setter     
    def _set_writeReserved(self, value):
        self.native_obj.WriteReserved = value
            
    # -> int            
    @property         
    def yearLabelDisplay(self) -> "int":
        return (self.native_obj.YearLabelDisplay)
        
    @yearLabelDisplay.setter     
    def _set_yearLabelDisplay(self, value):
        self.native_obj.YearLabelDisplay = value
            
# end "Project"       
        