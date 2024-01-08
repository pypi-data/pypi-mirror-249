

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Application:
    # Object "Application" class for software "Project"
    
    properties = ['activeCell', 'activeProject', 'activeSelection', 'activeWindow', 'aMText', 'application', 'askToUpdateLinks', 'assistance', 'autoClearLeveling', 'autoLevel', 'automaticallyFillPhoneticFields', 'automationSecurity', 'build', 'calculation', 'caption', 'cellDragAndDrop', 'cOMAddIns', 'commandBars', 'compareProjectsCurrentVersionName', 'compareProjectsPreviousVersionName', 'dateOrder', 'dateSeparator', 'dayLeadingZero', 'decimalSeparator', 'defaultAutoFilter', 'defaultDateFormat', 'defaultView', 'displayAlerts', 'displayEntryBar', 'displayOLEIndicator', 'displayPlanningWizard', 'displayProjectGuide', 'displayRecentFiles', 'displayScheduleMessages', 'displayScrollBars', 'displayStatusBar', 'displayViewBar', 'displayWindowsInTaskbar', 'displayWizardErrors', 'displayWizardScheduling', 'displayWizardUsage', 'edition', 'enableCancelKey', 'enableChangeHighlighting', 'enterpriseAllowLocalBaseCalendars', 'enterpriseListSeparator', 'enterpriseProtectActuals', 'fileBuildID', 'fileFormatID', 'getCacheStatusForProject', 'globalBaseCalendars', 'globalOutlineCodes', 'globalReports', 'globalResourceFilters', 'globalResourceTables', 'globalTaskFilters', 'globalTaskTables', 'globalViews', 'globalViewsCombination', 'globalViewsSingle', 'height', 'isCheckedOut', 'left', 'levelFreeformTasks', 'levelIndividualAssignments', 'levelingCanSplit', 'levelOrder', 'levelPeriodBasis', 'levelProposedBookings', 'levelWithinSlack', 'listSeparator', 'loadLastFile', 'monthLeadingZero', 'moveAfterReturn', 'name', 'newTasksEstimated', 'operatingSystem', 'panZoomFinish', 'panZoomStart', 'parent', 'path', 'pathSeparator', 'pMText', 'profiles', 'projects', 'promptForSummaryInfo', 'recentFilesMaximum', 'screenUpdating', 'showAssignmentUnitsAs', 'showEstimatedDuration', 'showWelcome', 'startWeekOn', 'startYearIn', 'statusBar', 'supportsMultipleDocuments', 'supportsMultipleWindows', 'thousandSeparator', 'timeLeadingZero', 'timescaleFinish', 'timescaleStart', 'timeSeparator', 'top', 'trustProjectServerAndWSSPages', 'twelveHourTimeFormat', 'undoLevels', 'usableHeight', 'usableWidth', 'use3DLook', 'useOMIDs', 'userControl', 'userName', 'vBE', 'version', 'visible', 'visualReportsAdditionalTemplatePath', 'visualReportTemplateList', 'width', 'windows', 'windows2', 'windowState']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def activeCell(self) -> "Any":
        return (self.native_obj.ActiveCell)
        
    @activeCell.setter     
    def _set_activeCell(self, value):
        self.native_obj.ActiveCell = value
            
    # -> Any            
    @property         
    def activeProject(self) -> "Any":
        return (self.native_obj.ActiveProject)
        
    @activeProject.setter     
    def _set_activeProject(self, value):
        self.native_obj.ActiveProject = value
            
    # -> Any            
    @property         
    def activeSelection(self) -> "Any":
        return (self.native_obj.ActiveSelection)
        
    @activeSelection.setter     
    def _set_activeSelection(self, value):
        self.native_obj.ActiveSelection = value
            
    # -> Any            
    @property         
    def activeWindow(self) -> "Any":
        return (self.native_obj.ActiveWindow)
        
    @activeWindow.setter     
    def _set_activeWindow(self, value):
        self.native_obj.ActiveWindow = value
            
    # -> Any            
    @property         
    def aMText(self) -> "Any":
        return (self.native_obj.AMText)
        
    @aMText.setter     
    def _set_aMText(self, value):
        self.native_obj.AMText = value
            
    # -> Any            
    @property         
    def application(self) -> "Any":
        return (self.native_obj.Application)
        
    @application.setter     
    def _set_application(self, value):
        self.native_obj.Application = value
            
    # -> Any            
    @property         
    def askToUpdateLinks(self) -> "Any":
        return (self.native_obj.AskToUpdateLinks)
        
    @askToUpdateLinks.setter     
    def _set_askToUpdateLinks(self, value):
        self.native_obj.AskToUpdateLinks = value
            
    # -> Any            
    @property         
    def assistance(self) -> "Any":
        return (self.native_obj.Assistance)
        
    @assistance.setter     
    def _set_assistance(self, value):
        self.native_obj.Assistance = value
            
    # -> Any            
    @property         
    def autoClearLeveling(self) -> "Any":
        return (self.native_obj.AutoClearLeveling)
        
    @autoClearLeveling.setter     
    def _set_autoClearLeveling(self, value):
        self.native_obj.AutoClearLeveling = value
            
    # -> Any            
    @property         
    def autoLevel(self) -> "Any":
        return (self.native_obj.AutoLevel)
        
    @autoLevel.setter     
    def _set_autoLevel(self, value):
        self.native_obj.AutoLevel = value
            
    # -> Any            
    @property         
    def automaticallyFillPhoneticFields(self) -> "Any":
        return (self.native_obj.AutomaticallyFillPhoneticFields)
        
    @automaticallyFillPhoneticFields.setter     
    def _set_automaticallyFillPhoneticFields(self, value):
        self.native_obj.AutomaticallyFillPhoneticFields = value
            
    # -> Any            
    @property         
    def automationSecurity(self) -> "Any":
        return (self.native_obj.AutomationSecurity)
        
    @automationSecurity.setter     
    def _set_automationSecurity(self, value):
        self.native_obj.AutomationSecurity = value
            
    # -> Any            
    @property         
    def build(self) -> "Any":
        return (self.native_obj.Build)
        
    @build.setter     
    def _set_build(self, value):
        self.native_obj.Build = value
            
    # -> Any            
    @property         
    def calculation(self) -> "Any":
        return (self.native_obj.Calculation)
        
    @calculation.setter     
    def _set_calculation(self, value):
        self.native_obj.Calculation = value
            
    # -> Any            
    @property         
    def caption(self) -> "Any":
        return (self.native_obj.Caption)
        
    @caption.setter     
    def _set_caption(self, value):
        self.native_obj.Caption = value
            
    # -> Any            
    @property         
    def cellDragAndDrop(self) -> "Any":
        return (self.native_obj.CellDragAndDrop)
        
    @cellDragAndDrop.setter     
    def _set_cellDragAndDrop(self, value):
        self.native_obj.CellDragAndDrop = value
            
    # -> Any            
    @property         
    def cOMAddIns(self) -> "Any":
        return (self.native_obj.COMAddIns)
        
    @cOMAddIns.setter     
    def _set_cOMAddIns(self, value):
        self.native_obj.COMAddIns = value
            
    # -> Any            
    @property         
    def commandBars(self) -> "Any":
        return (self.native_obj.CommandBars)
        
    @commandBars.setter     
    def _set_commandBars(self, value):
        self.native_obj.CommandBars = value
            
    # -> Any            
    @property         
    def compareProjectsCurrentVersionName(self) -> "Any":
        return (self.native_obj.CompareProjectsCurrentVersionName)
        
    @compareProjectsCurrentVersionName.setter     
    def _set_compareProjectsCurrentVersionName(self, value):
        self.native_obj.CompareProjectsCurrentVersionName = value
            
    # -> Any            
    @property         
    def compareProjectsPreviousVersionName(self) -> "Any":
        return (self.native_obj.CompareProjectsPreviousVersionName)
        
    @compareProjectsPreviousVersionName.setter     
    def _set_compareProjectsPreviousVersionName(self, value):
        self.native_obj.CompareProjectsPreviousVersionName = value
            
    # -> Any            
    @property         
    def dateOrder(self) -> "Any":
        return (self.native_obj.DateOrder)
        
    @dateOrder.setter     
    def _set_dateOrder(self, value):
        self.native_obj.DateOrder = value
            
    # -> Any            
    @property         
    def dateSeparator(self) -> "Any":
        return (self.native_obj.DateSeparator)
        
    @dateSeparator.setter     
    def _set_dateSeparator(self, value):
        self.native_obj.DateSeparator = value
            
    # -> Any            
    @property         
    def dayLeadingZero(self) -> "Any":
        return (self.native_obj.DayLeadingZero)
        
    @dayLeadingZero.setter     
    def _set_dayLeadingZero(self, value):
        self.native_obj.DayLeadingZero = value
            
    # -> Any            
    @property         
    def decimalSeparator(self) -> "Any":
        return (self.native_obj.DecimalSeparator)
        
    @decimalSeparator.setter     
    def _set_decimalSeparator(self, value):
        self.native_obj.DecimalSeparator = value
            
    # -> Any            
    @property         
    def defaultAutoFilter(self) -> "Any":
        return (self.native_obj.DefaultAutoFilter)
        
    @defaultAutoFilter.setter     
    def _set_defaultAutoFilter(self, value):
        self.native_obj.DefaultAutoFilter = value
            
    # -> Any            
    @property         
    def defaultDateFormat(self) -> "Any":
        return (self.native_obj.DefaultDateFormat)
        
    @defaultDateFormat.setter     
    def _set_defaultDateFormat(self, value):
        self.native_obj.DefaultDateFormat = value
            
    # -> Any            
    @property         
    def defaultView(self) -> "Any":
        return (self.native_obj.DefaultView)
        
    @defaultView.setter     
    def _set_defaultView(self, value):
        self.native_obj.DefaultView = value
            
    # -> Any            
    @property         
    def displayAlerts(self) -> "Any":
        return (self.native_obj.DisplayAlerts)
        
    @displayAlerts.setter     
    def _set_displayAlerts(self, value):
        self.native_obj.DisplayAlerts = value
            
    # -> Any            
    @property         
    def displayEntryBar(self) -> "Any":
        return (self.native_obj.DisplayEntryBar)
        
    @displayEntryBar.setter     
    def _set_displayEntryBar(self, value):
        self.native_obj.DisplayEntryBar = value
            
    # -> Any            
    @property         
    def displayOLEIndicator(self) -> "Any":
        return (self.native_obj.DisplayOLEIndicator)
        
    @displayOLEIndicator.setter     
    def _set_displayOLEIndicator(self, value):
        self.native_obj.DisplayOLEIndicator = value
            
    # -> Any            
    @property         
    def displayPlanningWizard(self) -> "Any":
        return (self.native_obj.DisplayPlanningWizard)
        
    @displayPlanningWizard.setter     
    def _set_displayPlanningWizard(self, value):
        self.native_obj.DisplayPlanningWizard = value
            
    # -> Any            
    @property         
    def displayProjectGuide(self) -> "Any":
        return (self.native_obj.DisplayProjectGuide)
        
    @displayProjectGuide.setter     
    def _set_displayProjectGuide(self, value):
        self.native_obj.DisplayProjectGuide = value
            
    # -> Any            
    @property         
    def displayRecentFiles(self) -> "Any":
        return (self.native_obj.DisplayRecentFiles)
        
    @displayRecentFiles.setter     
    def _set_displayRecentFiles(self, value):
        self.native_obj.DisplayRecentFiles = value
            
    # -> Any            
    @property         
    def displayScheduleMessages(self) -> "Any":
        return (self.native_obj.DisplayScheduleMessages)
        
    @displayScheduleMessages.setter     
    def _set_displayScheduleMessages(self, value):
        self.native_obj.DisplayScheduleMessages = value
            
    # -> Any            
    @property         
    def displayScrollBars(self) -> "Any":
        return (self.native_obj.DisplayScrollBars)
        
    @displayScrollBars.setter     
    def _set_displayScrollBars(self, value):
        self.native_obj.DisplayScrollBars = value
            
    # -> Any            
    @property         
    def displayStatusBar(self) -> "Any":
        return (self.native_obj.DisplayStatusBar)
        
    @displayStatusBar.setter     
    def _set_displayStatusBar(self, value):
        self.native_obj.DisplayStatusBar = value
            
    # -> Any            
    @property         
    def displayViewBar(self) -> "Any":
        return (self.native_obj.DisplayViewBar)
        
    @displayViewBar.setter     
    def _set_displayViewBar(self, value):
        self.native_obj.DisplayViewBar = value
            
    # -> Any            
    @property         
    def displayWindowsInTaskbar(self) -> "Any":
        return (self.native_obj.DisplayWindowsInTaskbar)
        
    @displayWindowsInTaskbar.setter     
    def _set_displayWindowsInTaskbar(self, value):
        self.native_obj.DisplayWindowsInTaskbar = value
            
    # -> Any            
    @property         
    def displayWizardErrors(self) -> "Any":
        return (self.native_obj.DisplayWizardErrors)
        
    @displayWizardErrors.setter     
    def _set_displayWizardErrors(self, value):
        self.native_obj.DisplayWizardErrors = value
            
    # -> Any            
    @property         
    def displayWizardScheduling(self) -> "Any":
        return (self.native_obj.DisplayWizardScheduling)
        
    @displayWizardScheduling.setter     
    def _set_displayWizardScheduling(self, value):
        self.native_obj.DisplayWizardScheduling = value
            
    # -> Any            
    @property         
    def displayWizardUsage(self) -> "Any":
        return (self.native_obj.DisplayWizardUsage)
        
    @displayWizardUsage.setter     
    def _set_displayWizardUsage(self, value):
        self.native_obj.DisplayWizardUsage = value
            
    # -> Any            
    @property         
    def edition(self) -> "Any":
        return (self.native_obj.Edition)
        
    @edition.setter     
    def _set_edition(self, value):
        self.native_obj.Edition = value
            
    # -> Any            
    @property         
    def enableCancelKey(self) -> "Any":
        return (self.native_obj.EnableCancelKey)
        
    @enableCancelKey.setter     
    def _set_enableCancelKey(self, value):
        self.native_obj.EnableCancelKey = value
            
    # -> Any            
    @property         
    def enableChangeHighlighting(self) -> "Any":
        return (self.native_obj.EnableChangeHighlighting)
        
    @enableChangeHighlighting.setter     
    def _set_enableChangeHighlighting(self, value):
        self.native_obj.EnableChangeHighlighting = value
            
    # -> Any            
    @property         
    def enterpriseAllowLocalBaseCalendars(self) -> "Any":
        return (self.native_obj.EnterpriseAllowLocalBaseCalendars)
        
    @enterpriseAllowLocalBaseCalendars.setter     
    def _set_enterpriseAllowLocalBaseCalendars(self, value):
        self.native_obj.EnterpriseAllowLocalBaseCalendars = value
            
    # -> Any            
    @property         
    def enterpriseListSeparator(self) -> "Any":
        return (self.native_obj.EnterpriseListSeparator)
        
    @enterpriseListSeparator.setter     
    def _set_enterpriseListSeparator(self, value):
        self.native_obj.EnterpriseListSeparator = value
            
    # -> Any            
    @property         
    def enterpriseProtectActuals(self) -> "Any":
        return (self.native_obj.EnterpriseProtectActuals)
        
    @enterpriseProtectActuals.setter     
    def _set_enterpriseProtectActuals(self, value):
        self.native_obj.EnterpriseProtectActuals = value
            
    # -> Any            
    @property         
    def fileBuildID(self) -> "Any":
        return (self.native_obj.FileBuildID)
        
    @fileBuildID.setter     
    def _set_fileBuildID(self, value):
        self.native_obj.FileBuildID = value
            
    # -> Any            
    @property         
    def fileFormatID(self) -> "Any":
        return (self.native_obj.FileFormatID)
        
    @fileFormatID.setter     
    def _set_fileFormatID(self, value):
        self.native_obj.FileFormatID = value
            
    # -> Any            
    @property         
    def getCacheStatusForProject(self) -> "Any":
        return (self.native_obj.GetCacheStatusForProject)
        
    @getCacheStatusForProject.setter     
    def _set_getCacheStatusForProject(self, value):
        self.native_obj.GetCacheStatusForProject = value
            
    # -> Any            
    @property         
    def globalBaseCalendars(self) -> "Any":
        return (self.native_obj.GlobalBaseCalendars)
        
    @globalBaseCalendars.setter     
    def _set_globalBaseCalendars(self, value):
        self.native_obj.GlobalBaseCalendars = value
            
    # -> Any            
    @property         
    def globalOutlineCodes(self) -> "Any":
        return (self.native_obj.GlobalOutlineCodes)
        
    @globalOutlineCodes.setter     
    def _set_globalOutlineCodes(self, value):
        self.native_obj.GlobalOutlineCodes = value
            
    # -> Any            
    @property         
    def globalReports(self) -> "Any":
        return (self.native_obj.GlobalReports)
        
    @globalReports.setter     
    def _set_globalReports(self, value):
        self.native_obj.GlobalReports = value
            
    # -> Any            
    @property         
    def globalResourceFilters(self) -> "Any":
        return (self.native_obj.GlobalResourceFilters)
        
    @globalResourceFilters.setter     
    def _set_globalResourceFilters(self, value):
        self.native_obj.GlobalResourceFilters = value
            
    # -> Any            
    @property         
    def globalResourceTables(self) -> "Any":
        return (self.native_obj.GlobalResourceTables)
        
    @globalResourceTables.setter     
    def _set_globalResourceTables(self, value):
        self.native_obj.GlobalResourceTables = value
            
    # -> Any            
    @property         
    def globalTaskFilters(self) -> "Any":
        return (self.native_obj.GlobalTaskFilters)
        
    @globalTaskFilters.setter     
    def _set_globalTaskFilters(self, value):
        self.native_obj.GlobalTaskFilters = value
            
    # -> Any            
    @property         
    def globalTaskTables(self) -> "Any":
        return (self.native_obj.GlobalTaskTables)
        
    @globalTaskTables.setter     
    def _set_globalTaskTables(self, value):
        self.native_obj.GlobalTaskTables = value
            
    # -> Any            
    @property         
    def globalViews(self) -> "Any":
        return (self.native_obj.GlobalViews)
        
    @globalViews.setter     
    def _set_globalViews(self, value):
        self.native_obj.GlobalViews = value
            
    # -> Any            
    @property         
    def globalViewsCombination(self) -> "Any":
        return (self.native_obj.GlobalViewsCombination)
        
    @globalViewsCombination.setter     
    def _set_globalViewsCombination(self, value):
        self.native_obj.GlobalViewsCombination = value
            
    # -> Any            
    @property         
    def globalViewsSingle(self) -> "Any":
        return (self.native_obj.GlobalViewsSingle)
        
    @globalViewsSingle.setter     
    def _set_globalViewsSingle(self, value):
        self.native_obj.GlobalViewsSingle = value
            
    # -> Any            
    @property         
    def height(self) -> "Any":
        return (self.native_obj.Height)
        
    @height.setter     
    def _set_height(self, value):
        self.native_obj.Height = value
            
    # -> Any            
    @property         
    def isCheckedOut(self) -> "Any":
        return (self.native_obj.IsCheckedOut)
        
    @isCheckedOut.setter     
    def _set_isCheckedOut(self, value):
        self.native_obj.IsCheckedOut = value
            
    # -> Any            
    @property         
    def left(self) -> "Any":
        return (self.native_obj.Left)
        
    @left.setter     
    def _set_left(self, value):
        self.native_obj.Left = value
            
    # -> Any            
    @property         
    def levelFreeformTasks(self) -> "Any":
        return (self.native_obj.LevelFreeformTasks)
        
    @levelFreeformTasks.setter     
    def _set_levelFreeformTasks(self, value):
        self.native_obj.LevelFreeformTasks = value
            
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
    def levelOrder(self) -> "Any":
        return (self.native_obj.LevelOrder)
        
    @levelOrder.setter     
    def _set_levelOrder(self, value):
        self.native_obj.LevelOrder = value
            
    # -> Any            
    @property         
    def levelPeriodBasis(self) -> "Any":
        return (self.native_obj.LevelPeriodBasis)
        
    @levelPeriodBasis.setter     
    def _set_levelPeriodBasis(self, value):
        self.native_obj.LevelPeriodBasis = value
            
    # -> Any            
    @property         
    def levelProposedBookings(self) -> "Any":
        return (self.native_obj.LevelProposedBookings)
        
    @levelProposedBookings.setter     
    def _set_levelProposedBookings(self, value):
        self.native_obj.LevelProposedBookings = value
            
    # -> Any            
    @property         
    def levelWithinSlack(self) -> "Any":
        return (self.native_obj.LevelWithinSlack)
        
    @levelWithinSlack.setter     
    def _set_levelWithinSlack(self, value):
        self.native_obj.LevelWithinSlack = value
            
    # -> Any            
    @property         
    def listSeparator(self) -> "Any":
        return (self.native_obj.ListSeparator)
        
    @listSeparator.setter     
    def _set_listSeparator(self, value):
        self.native_obj.ListSeparator = value
            
    # -> Any            
    @property         
    def loadLastFile(self) -> "Any":
        return (self.native_obj.LoadLastFile)
        
    @loadLastFile.setter     
    def _set_loadLastFile(self, value):
        self.native_obj.LoadLastFile = value
            
    # -> Any            
    @property         
    def monthLeadingZero(self) -> "Any":
        return (self.native_obj.MonthLeadingZero)
        
    @monthLeadingZero.setter     
    def _set_monthLeadingZero(self, value):
        self.native_obj.MonthLeadingZero = value
            
    # -> Any            
    @property         
    def moveAfterReturn(self) -> "Any":
        return (self.native_obj.MoveAfterReturn)
        
    @moveAfterReturn.setter     
    def _set_moveAfterReturn(self, value):
        self.native_obj.MoveAfterReturn = value
            
    # -> Any            
    @property         
    def name(self) -> "Any":
        return (self.native_obj.Name)
        
    @name.setter     
    def _set_name(self, value):
        self.native_obj.Name = value
            
    # -> Any            
    @property         
    def newTasksEstimated(self) -> "Any":
        return (self.native_obj.NewTasksEstimated)
        
    @newTasksEstimated.setter     
    def _set_newTasksEstimated(self, value):
        self.native_obj.NewTasksEstimated = value
            
    # -> Any            
    @property         
    def operatingSystem(self) -> "Any":
        return (self.native_obj.OperatingSystem)
        
    @operatingSystem.setter     
    def _set_operatingSystem(self, value):
        self.native_obj.OperatingSystem = value
            
    # -> Any            
    @property         
    def panZoomFinish(self) -> "Any":
        return (self.native_obj.PanZoomFinish)
        
    @panZoomFinish.setter     
    def _set_panZoomFinish(self, value):
        self.native_obj.PanZoomFinish = value
            
    # -> Any            
    @property         
    def panZoomStart(self) -> "Any":
        return (self.native_obj.PanZoomStart)
        
    @panZoomStart.setter     
    def _set_panZoomStart(self, value):
        self.native_obj.PanZoomStart = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def path(self) -> "Any":
        return (self.native_obj.Path)
        
    @path.setter     
    def _set_path(self, value):
        self.native_obj.Path = value
            
    # -> Any            
    @property         
    def pathSeparator(self) -> "Any":
        return (self.native_obj.PathSeparator)
        
    @pathSeparator.setter     
    def _set_pathSeparator(self, value):
        self.native_obj.PathSeparator = value
            
    # -> Any            
    @property         
    def pMText(self) -> "Any":
        return (self.native_obj.PMText)
        
    @pMText.setter     
    def _set_pMText(self, value):
        self.native_obj.PMText = value
            
    # -> Any            
    @property         
    def profiles(self) -> "Any":
        return (self.native_obj.Profiles)
        
    @profiles.setter     
    def _set_profiles(self, value):
        self.native_obj.Profiles = value
            
    # -> Any            
    @property         
    def projects(self) -> "Any":
        return (self.native_obj.Projects)
        
    @projects.setter     
    def _set_projects(self, value):
        self.native_obj.Projects = value
            
    # -> Any            
    @property         
    def promptForSummaryInfo(self) -> "Any":
        return (self.native_obj.PromptForSummaryInfo)
        
    @promptForSummaryInfo.setter     
    def _set_promptForSummaryInfo(self, value):
        self.native_obj.PromptForSummaryInfo = value
            
    # -> Any            
    @property         
    def recentFilesMaximum(self) -> "Any":
        return (self.native_obj.RecentFilesMaximum)
        
    @recentFilesMaximum.setter     
    def _set_recentFilesMaximum(self, value):
        self.native_obj.RecentFilesMaximum = value
            
    # -> Any            
    @property         
    def screenUpdating(self) -> "Any":
        return (self.native_obj.ScreenUpdating)
        
    @screenUpdating.setter     
    def _set_screenUpdating(self, value):
        self.native_obj.ScreenUpdating = value
            
    # -> Any            
    @property         
    def showAssignmentUnitsAs(self) -> "Any":
        return (self.native_obj.ShowAssignmentUnitsAs)
        
    @showAssignmentUnitsAs.setter     
    def _set_showAssignmentUnitsAs(self, value):
        self.native_obj.ShowAssignmentUnitsAs = value
            
    # -> Any            
    @property         
    def showEstimatedDuration(self) -> "Any":
        return (self.native_obj.ShowEstimatedDuration)
        
    @showEstimatedDuration.setter     
    def _set_showEstimatedDuration(self, value):
        self.native_obj.ShowEstimatedDuration = value
            
    # -> Any            
    @property         
    def showWelcome(self) -> "Any":
        return (self.native_obj.ShowWelcome)
        
    @showWelcome.setter     
    def _set_showWelcome(self, value):
        self.native_obj.ShowWelcome = value
            
    # -> Any            
    @property         
    def startWeekOn(self) -> "Any":
        return (self.native_obj.StartWeekOn)
        
    @startWeekOn.setter     
    def _set_startWeekOn(self, value):
        self.native_obj.StartWeekOn = value
            
    # -> Any            
    @property         
    def startYearIn(self) -> "Any":
        return (self.native_obj.StartYearIn)
        
    @startYearIn.setter     
    def _set_startYearIn(self, value):
        self.native_obj.StartYearIn = value
            
    # -> Any            
    @property         
    def statusBar(self) -> "Any":
        return (self.native_obj.StatusBar)
        
    @statusBar.setter     
    def _set_statusBar(self, value):
        self.native_obj.StatusBar = value
            
    # -> Any            
    @property         
    def supportsMultipleDocuments(self) -> "Any":
        return (self.native_obj.SupportsMultipleDocuments)
        
    @supportsMultipleDocuments.setter     
    def _set_supportsMultipleDocuments(self, value):
        self.native_obj.SupportsMultipleDocuments = value
            
    # -> Any            
    @property         
    def supportsMultipleWindows(self) -> "Any":
        return (self.native_obj.SupportsMultipleWindows)
        
    @supportsMultipleWindows.setter     
    def _set_supportsMultipleWindows(self, value):
        self.native_obj.SupportsMultipleWindows = value
            
    # -> Any            
    @property         
    def thousandSeparator(self) -> "Any":
        return (self.native_obj.ThousandSeparator)
        
    @thousandSeparator.setter     
    def _set_thousandSeparator(self, value):
        self.native_obj.ThousandSeparator = value
            
    # -> Any            
    @property         
    def timeLeadingZero(self) -> "Any":
        return (self.native_obj.TimeLeadingZero)
        
    @timeLeadingZero.setter     
    def _set_timeLeadingZero(self, value):
        self.native_obj.TimeLeadingZero = value
            
    # -> Any            
    @property         
    def timescaleFinish(self) -> "Any":
        return (self.native_obj.TimescaleFinish)
        
    @timescaleFinish.setter     
    def _set_timescaleFinish(self, value):
        self.native_obj.TimescaleFinish = value
            
    # -> Any            
    @property         
    def timescaleStart(self) -> "Any":
        return (self.native_obj.TimescaleStart)
        
    @timescaleStart.setter     
    def _set_timescaleStart(self, value):
        self.native_obj.TimescaleStart = value
            
    # -> Any            
    @property         
    def timeSeparator(self) -> "Any":
        return (self.native_obj.TimeSeparator)
        
    @timeSeparator.setter     
    def _set_timeSeparator(self, value):
        self.native_obj.TimeSeparator = value
            
    # -> Any            
    @property         
    def top(self) -> "Any":
        return (self.native_obj.Top)
        
    @top.setter     
    def _set_top(self, value):
        self.native_obj.Top = value
            
    # -> Any            
    @property         
    def trustProjectServerAndWSSPages(self) -> "Any":
        return (self.native_obj.TrustProjectServerAndWSSPages)
        
    @trustProjectServerAndWSSPages.setter     
    def _set_trustProjectServerAndWSSPages(self, value):
        self.native_obj.TrustProjectServerAndWSSPages = value
            
    # -> Any            
    @property         
    def twelveHourTimeFormat(self) -> "Any":
        return (self.native_obj.TwelveHourTimeFormat)
        
    @twelveHourTimeFormat.setter     
    def _set_twelveHourTimeFormat(self, value):
        self.native_obj.TwelveHourTimeFormat = value
            
    # -> Any            
    @property         
    def undoLevels(self) -> "Any":
        return (self.native_obj.UndoLevels)
        
    @undoLevels.setter     
    def _set_undoLevels(self, value):
        self.native_obj.UndoLevels = value
            
    # -> Any            
    @property         
    def usableHeight(self) -> "Any":
        return (self.native_obj.UsableHeight)
        
    @usableHeight.setter     
    def _set_usableHeight(self, value):
        self.native_obj.UsableHeight = value
            
    # -> Any            
    @property         
    def usableWidth(self) -> "Any":
        return (self.native_obj.UsableWidth)
        
    @usableWidth.setter     
    def _set_usableWidth(self, value):
        self.native_obj.UsableWidth = value
            
    # -> Any            
    @property         
    def use3DLook(self) -> "Any":
        return (self.native_obj.Use3DLook)
        
    @use3DLook.setter     
    def _set_use3DLook(self, value):
        self.native_obj.Use3DLook = value
            
    # -> Any            
    @property         
    def useOMIDs(self) -> "Any":
        return (self.native_obj.UseOMIDs)
        
    @useOMIDs.setter     
    def _set_useOMIDs(self, value):
        self.native_obj.UseOMIDs = value
            
    # -> Any            
    @property         
    def userControl(self) -> "Any":
        return (self.native_obj.UserControl)
        
    @userControl.setter     
    def _set_userControl(self, value):
        self.native_obj.UserControl = value
            
    # -> Any            
    @property         
    def userName(self) -> "Any":
        return (self.native_obj.UserName)
        
    @userName.setter     
    def _set_userName(self, value):
        self.native_obj.UserName = value
            
    # -> Any            
    @property         
    def vBE(self) -> "Any":
        return (self.native_obj.VBE)
        
    @vBE.setter     
    def _set_vBE(self, value):
        self.native_obj.VBE = value
            
    # -> Any            
    @property         
    def version(self) -> "Any":
        return (self.native_obj.Version)
        
    @version.setter     
    def _set_version(self, value):
        self.native_obj.Version = value
            
    # -> Any            
    @property         
    def visible(self) -> "Any":
        return (self.native_obj.Visible)
        
    @visible.setter     
    def _set_visible(self, value):
        self.native_obj.Visible = value
            
    # -> Any            
    @property         
    def visualReportsAdditionalTemplatePath(self) -> "Any":
        return (self.native_obj.VisualReportsAdditionalTemplatePath)
        
    @visualReportsAdditionalTemplatePath.setter     
    def _set_visualReportsAdditionalTemplatePath(self, value):
        self.native_obj.VisualReportsAdditionalTemplatePath = value
            
    # -> Any            
    @property         
    def visualReportTemplateList(self) -> "Any":
        return (self.native_obj.VisualReportTemplateList)
        
    @visualReportTemplateList.setter     
    def _set_visualReportTemplateList(self, value):
        self.native_obj.VisualReportTemplateList = value
            
    # -> Any            
    @property         
    def width(self) -> "Any":
        return (self.native_obj.Width)
        
    @width.setter     
    def _set_width(self, value):
        self.native_obj.Width = value
            
    # -> Any            
    @property         
    def windows(self) -> "Any":
        return (self.native_obj.Windows)
        
    @windows.setter     
    def _set_windows(self, value):
        self.native_obj.Windows = value
            
    # -> Any            
    @property         
    def windows2(self) -> "Any":
        return (self.native_obj.Windows2)
        
    @windows2.setter     
    def _set_windows2(self, value):
        self.native_obj.Windows2 = value
            
    # -> Any            
    @property         
    def windowState(self) -> "Any":
        return (self.native_obj.WindowState)
        
    @windowState.setter     
    def _set_windowState(self, value):
        self.native_obj.WindowState = value
            
# end "Application"       
        