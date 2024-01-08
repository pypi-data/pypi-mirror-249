

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class Chart:
    # Object "Chart" class for software "Project"
    
    properties = ['application', 'autoScaling', 'backWall', 'barShape', 'chartArea', 'chartColor', 'chartData', 'chartGroups', 'chartStyle', 'chartTitle', 'chartType', 'creator', 'dataTable', 'depthPercent', 'displayBlanksAs', 'elevation', 'floor', 'format', 'gapDepth', 'hasAxis', 'hasDataTable', 'hasLegend', 'hasTitle', 'heightPercent', 'legend', 'parent', 'perspective', 'pivotLayout', 'plotArea', 'plotBy', 'plotVisibleOnly', 'rightAngleAxes', 'rotation', 'shapes', 'showAllFieldButtons', 'showAxisFieldButtons', 'showDataLabelsOverMaximum', 'showLegendFieldButtons', 'showReportFilterFieldButtons', 'showValueFieldButtons', 'sideWall', 'walls']
    
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
    def autoScaling(self) -> "Any":
        return (self.native_obj.AutoScaling)
        
    @autoScaling.setter     
    def _set_autoScaling(self, value):
        self.native_obj.AutoScaling = value
            
    # -> Any            
    @property         
    def backWall(self) -> "Any":
        return (self.native_obj.BackWall)
        
    @backWall.setter     
    def _set_backWall(self, value):
        self.native_obj.BackWall = value
            
    # -> Any            
    @property         
    def barShape(self) -> "Any":
        return (self.native_obj.BarShape)
        
    @barShape.setter     
    def _set_barShape(self, value):
        self.native_obj.BarShape = value
            
    # -> Any            
    @property         
    def chartArea(self) -> "Any":
        return (self.native_obj.ChartArea)
        
    @chartArea.setter     
    def _set_chartArea(self, value):
        self.native_obj.ChartArea = value
            
    # -> Any            
    @property         
    def chartColor(self) -> "Any":
        return (self.native_obj.ChartColor)
        
    @chartColor.setter     
    def _set_chartColor(self, value):
        self.native_obj.ChartColor = value
            
    # -> Any            
    @property         
    def chartData(self) -> "Any":
        return (self.native_obj.ChartData)
        
    @chartData.setter     
    def _set_chartData(self, value):
        self.native_obj.ChartData = value
            
    # -> Any            
    @property         
    def chartGroups(self) -> "Any":
        return (self.native_obj.ChartGroups)
        
    @chartGroups.setter     
    def _set_chartGroups(self, value):
        self.native_obj.ChartGroups = value
            
    # -> Any            
    @property         
    def chartStyle(self) -> "Any":
        return (self.native_obj.ChartStyle)
        
    @chartStyle.setter     
    def _set_chartStyle(self, value):
        self.native_obj.ChartStyle = value
            
    # -> Any            
    @property         
    def chartTitle(self) -> "Any":
        return (self.native_obj.ChartTitle)
        
    @chartTitle.setter     
    def _set_chartTitle(self, value):
        self.native_obj.ChartTitle = value
            
    # -> Any            
    @property         
    def chartType(self) -> "Any":
        return (self.native_obj.ChartType)
        
    @chartType.setter     
    def _set_chartType(self, value):
        self.native_obj.ChartType = value
            
    # -> Any            
    @property         
    def creator(self) -> "Any":
        return (self.native_obj.Creator)
        
    @creator.setter     
    def _set_creator(self, value):
        self.native_obj.Creator = value
            
    # -> Any            
    @property         
    def dataTable(self) -> "Any":
        return (self.native_obj.DataTable)
        
    @dataTable.setter     
    def _set_dataTable(self, value):
        self.native_obj.DataTable = value
            
    # -> Any            
    @property         
    def depthPercent(self) -> "Any":
        return (self.native_obj.DepthPercent)
        
    @depthPercent.setter     
    def _set_depthPercent(self, value):
        self.native_obj.DepthPercent = value
            
    # -> Any            
    @property         
    def displayBlanksAs(self) -> "Any":
        return (self.native_obj.DisplayBlanksAs)
        
    @displayBlanksAs.setter     
    def _set_displayBlanksAs(self, value):
        self.native_obj.DisplayBlanksAs = value
            
    # -> Any            
    @property         
    def elevation(self) -> "Any":
        return (self.native_obj.Elevation)
        
    @elevation.setter     
    def _set_elevation(self, value):
        self.native_obj.Elevation = value
            
    # -> Any            
    @property         
    def floor(self) -> "Any":
        return (self.native_obj.Floor)
        
    @floor.setter     
    def _set_floor(self, value):
        self.native_obj.Floor = value
            
    # -> Any            
    @property         
    def format(self) -> "Any":
        return (self.native_obj.Format)
        
    @format.setter     
    def _set_format(self, value):
        self.native_obj.Format = value
            
    # -> Any            
    @property         
    def gapDepth(self) -> "Any":
        return (self.native_obj.GapDepth)
        
    @gapDepth.setter     
    def _set_gapDepth(self, value):
        self.native_obj.GapDepth = value
            
    # -> Any            
    @property         
    def hasAxis(self) -> "Any":
        return (self.native_obj.HasAxis)
        
    @hasAxis.setter     
    def _set_hasAxis(self, value):
        self.native_obj.HasAxis = value
            
    # -> Any            
    @property         
    def hasDataTable(self) -> "Any":
        return (self.native_obj.HasDataTable)
        
    @hasDataTable.setter     
    def _set_hasDataTable(self, value):
        self.native_obj.HasDataTable = value
            
    # -> Any            
    @property         
    def hasLegend(self) -> "Any":
        return (self.native_obj.HasLegend)
        
    @hasLegend.setter     
    def _set_hasLegend(self, value):
        self.native_obj.HasLegend = value
            
    # -> Any            
    @property         
    def hasTitle(self) -> "Any":
        return (self.native_obj.HasTitle)
        
    @hasTitle.setter     
    def _set_hasTitle(self, value):
        self.native_obj.HasTitle = value
            
    # -> Any            
    @property         
    def heightPercent(self) -> "Any":
        return (self.native_obj.HeightPercent)
        
    @heightPercent.setter     
    def _set_heightPercent(self, value):
        self.native_obj.HeightPercent = value
            
    # -> Any            
    @property         
    def legend(self) -> "Any":
        return (self.native_obj.Legend)
        
    @legend.setter     
    def _set_legend(self, value):
        self.native_obj.Legend = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def perspective(self) -> "Any":
        return (self.native_obj.Perspective)
        
    @perspective.setter     
    def _set_perspective(self, value):
        self.native_obj.Perspective = value
            
    # -> Any            
    @property         
    def pivotLayout(self) -> "Any":
        return (self.native_obj.PivotLayout)
        
    @pivotLayout.setter     
    def _set_pivotLayout(self, value):
        self.native_obj.PivotLayout = value
            
    # -> Any            
    @property         
    def plotArea(self) -> "Any":
        return (self.native_obj.PlotArea)
        
    @plotArea.setter     
    def _set_plotArea(self, value):
        self.native_obj.PlotArea = value
            
    # -> Any            
    @property         
    def plotBy(self) -> "Any":
        return (self.native_obj.PlotBy)
        
    @plotBy.setter     
    def _set_plotBy(self, value):
        self.native_obj.PlotBy = value
            
    # -> Any            
    @property         
    def plotVisibleOnly(self) -> "Any":
        return (self.native_obj.PlotVisibleOnly)
        
    @plotVisibleOnly.setter     
    def _set_plotVisibleOnly(self, value):
        self.native_obj.PlotVisibleOnly = value
            
    # -> Any            
    @property         
    def rightAngleAxes(self) -> "Any":
        return (self.native_obj.RightAngleAxes)
        
    @rightAngleAxes.setter     
    def _set_rightAngleAxes(self, value):
        self.native_obj.RightAngleAxes = value
            
    # -> Any            
    @property         
    def rotation(self) -> "Any":
        return (self.native_obj.Rotation)
        
    @rotation.setter     
    def _set_rotation(self, value):
        self.native_obj.Rotation = value
            
    # -> Any            
    @property         
    def shapes(self) -> "Any":
        return (self.native_obj.Shapes)
        
    @shapes.setter     
    def _set_shapes(self, value):
        self.native_obj.Shapes = value
            
    # -> Any            
    @property         
    def showAllFieldButtons(self) -> "Any":
        return (self.native_obj.ShowAllFieldButtons)
        
    @showAllFieldButtons.setter     
    def _set_showAllFieldButtons(self, value):
        self.native_obj.ShowAllFieldButtons = value
            
    # -> Any            
    @property         
    def showAxisFieldButtons(self) -> "Any":
        return (self.native_obj.ShowAxisFieldButtons)
        
    @showAxisFieldButtons.setter     
    def _set_showAxisFieldButtons(self, value):
        self.native_obj.ShowAxisFieldButtons = value
            
    # -> Any            
    @property         
    def showDataLabelsOverMaximum(self) -> "Any":
        return (self.native_obj.ShowDataLabelsOverMaximum)
        
    @showDataLabelsOverMaximum.setter     
    def _set_showDataLabelsOverMaximum(self, value):
        self.native_obj.ShowDataLabelsOverMaximum = value
            
    # -> Any            
    @property         
    def showLegendFieldButtons(self) -> "Any":
        return (self.native_obj.ShowLegendFieldButtons)
        
    @showLegendFieldButtons.setter     
    def _set_showLegendFieldButtons(self, value):
        self.native_obj.ShowLegendFieldButtons = value
            
    # -> Any            
    @property         
    def showReportFilterFieldButtons(self) -> "Any":
        return (self.native_obj.ShowReportFilterFieldButtons)
        
    @showReportFilterFieldButtons.setter     
    def _set_showReportFilterFieldButtons(self, value):
        self.native_obj.ShowReportFilterFieldButtons = value
            
    # -> Any            
    @property         
    def showValueFieldButtons(self) -> "Any":
        return (self.native_obj.ShowValueFieldButtons)
        
    @showValueFieldButtons.setter     
    def _set_showValueFieldButtons(self, value):
        self.native_obj.ShowValueFieldButtons = value
            
    # -> Any            
    @property         
    def sideWall(self) -> "Any":
        return (self.native_obj.SideWall)
        
    @sideWall.setter     
    def _set_sideWall(self, value):
        self.native_obj.SideWall = value
            
    # -> Any            
    @property         
    def walls(self) -> "Any":
        return (self.native_obj.Walls)
        
    @walls.setter     
    def _set_walls(self, value):
        self.native_obj.Walls = value
            
# end "Chart"       
        