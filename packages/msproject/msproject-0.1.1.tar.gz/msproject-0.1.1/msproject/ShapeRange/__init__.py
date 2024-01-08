

from pathlib import Path
import win32com
import win32com.client
from typing import List, Dict, Any
import pywintypes
from msproject import *

        
class ShapeRange:
    # Object "ShapeRange" class for software "Project"
    
    properties = ['adjustments', 'alternativeText', 'application', 'autoShapeType', 'backgroundStyle', 'blackWhiteMode', 'callout', 'chart', 'child', 'connectionSiteCount', 'connector', 'connectorFormat', 'count', 'fill', 'glow', 'groupItems', 'hasChart', 'hasTable', 'height', 'horizontalFlip', 'iD', 'left', 'line', 'lockAspectRatio', 'name', 'nodes', 'parent', 'parentGroup', 'reflection', 'rotation', 'script', 'shadow', 'shapeStyle', 'softEdge', 'table', 'textEffect', 'textFrame', 'textFrame2', 'threeD', 'title', 'top', 'type', 'value', 'verticalFlip', 'vertices', 'visible', 'width', 'zOrderPosition']
    
    def __init__(self, native_obj):
        self.native_obj = native_obj    
        
    
    # -> Any            
    @property         
    def adjustments(self) -> "Any":
        return (self.native_obj.Adjustments)
        
    @adjustments.setter     
    def _set_adjustments(self, value):
        self.native_obj.Adjustments = value
            
    # -> Any            
    @property         
    def alternativeText(self) -> "Any":
        return (self.native_obj.AlternativeText)
        
    @alternativeText.setter     
    def _set_alternativeText(self, value):
        self.native_obj.AlternativeText = value
            
    # -> Any            
    @property         
    def application(self) -> "Any":
        return (self.native_obj.Application)
        
    @application.setter     
    def _set_application(self, value):
        self.native_obj.Application = value
            
    # -> Any            
    @property         
    def autoShapeType(self) -> "Any":
        return (self.native_obj.AutoShapeType)
        
    @autoShapeType.setter     
    def _set_autoShapeType(self, value):
        self.native_obj.AutoShapeType = value
            
    # -> Any            
    @property         
    def backgroundStyle(self) -> "Any":
        return (self.native_obj.BackgroundStyle)
        
    @backgroundStyle.setter     
    def _set_backgroundStyle(self, value):
        self.native_obj.BackgroundStyle = value
            
    # -> Any            
    @property         
    def blackWhiteMode(self) -> "Any":
        return (self.native_obj.BlackWhiteMode)
        
    @blackWhiteMode.setter     
    def _set_blackWhiteMode(self, value):
        self.native_obj.BlackWhiteMode = value
            
    # -> Any            
    @property         
    def callout(self) -> "Any":
        return (self.native_obj.Callout)
        
    @callout.setter     
    def _set_callout(self, value):
        self.native_obj.Callout = value
            
    # -> Any            
    @property         
    def chart(self) -> "Any":
        return (self.native_obj.Chart)
        
    @chart.setter     
    def _set_chart(self, value):
        self.native_obj.Chart = value
            
    # -> Any            
    @property         
    def child(self) -> "Any":
        return (self.native_obj.Child)
        
    @child.setter     
    def _set_child(self, value):
        self.native_obj.Child = value
            
    # -> Any            
    @property         
    def connectionSiteCount(self) -> "Any":
        return (self.native_obj.ConnectionSiteCount)
        
    @connectionSiteCount.setter     
    def _set_connectionSiteCount(self, value):
        self.native_obj.ConnectionSiteCount = value
            
    # -> Any            
    @property         
    def connector(self) -> "Any":
        return (self.native_obj.Connector)
        
    @connector.setter     
    def _set_connector(self, value):
        self.native_obj.Connector = value
            
    # -> Any            
    @property         
    def connectorFormat(self) -> "Any":
        return (self.native_obj.ConnectorFormat)
        
    @connectorFormat.setter     
    def _set_connectorFormat(self, value):
        self.native_obj.ConnectorFormat = value
            
    # -> Any            
    @property         
    def count(self) -> "Any":
        return (self.native_obj.Count)
        
    @count.setter     
    def _set_count(self, value):
        self.native_obj.Count = value
            
    # -> Any            
    @property         
    def fill(self) -> "Any":
        return (self.native_obj.Fill)
        
    @fill.setter     
    def _set_fill(self, value):
        self.native_obj.Fill = value
            
    # -> Any            
    @property         
    def glow(self) -> "Any":
        return (self.native_obj.Glow)
        
    @glow.setter     
    def _set_glow(self, value):
        self.native_obj.Glow = value
            
    # -> Any            
    @property         
    def groupItems(self) -> "Any":
        return (self.native_obj.GroupItems)
        
    @groupItems.setter     
    def _set_groupItems(self, value):
        self.native_obj.GroupItems = value
            
    # -> Any            
    @property         
    def hasChart(self) -> "Any":
        return (self.native_obj.HasChart)
        
    @hasChart.setter     
    def _set_hasChart(self, value):
        self.native_obj.HasChart = value
            
    # -> Any            
    @property         
    def hasTable(self) -> "Any":
        return (self.native_obj.HasTable)
        
    @hasTable.setter     
    def _set_hasTable(self, value):
        self.native_obj.HasTable = value
            
    # -> Any            
    @property         
    def height(self) -> "Any":
        return (self.native_obj.Height)
        
    @height.setter     
    def _set_height(self, value):
        self.native_obj.Height = value
            
    # -> Any            
    @property         
    def horizontalFlip(self) -> "Any":
        return (self.native_obj.HorizontalFlip)
        
    @horizontalFlip.setter     
    def _set_horizontalFlip(self, value):
        self.native_obj.HorizontalFlip = value
            
    # -> Any            
    @property         
    def iD(self) -> "Any":
        return (self.native_obj.ID)
        
    @iD.setter     
    def _set_iD(self, value):
        self.native_obj.ID = value
            
    # -> Any            
    @property         
    def left(self) -> "Any":
        return (self.native_obj.Left)
        
    @left.setter     
    def _set_left(self, value):
        self.native_obj.Left = value
            
    # -> Any            
    @property         
    def line(self) -> "Any":
        return (self.native_obj.Line)
        
    @line.setter     
    def _set_line(self, value):
        self.native_obj.Line = value
            
    # -> Any            
    @property         
    def lockAspectRatio(self) -> "Any":
        return (self.native_obj.LockAspectRatio)
        
    @lockAspectRatio.setter     
    def _set_lockAspectRatio(self, value):
        self.native_obj.LockAspectRatio = value
            
    # -> Any            
    @property         
    def name(self) -> "Any":
        return (self.native_obj.Name)
        
    @name.setter     
    def _set_name(self, value):
        self.native_obj.Name = value
            
    # -> Any            
    @property         
    def nodes(self) -> "Any":
        return (self.native_obj.Nodes)
        
    @nodes.setter     
    def _set_nodes(self, value):
        self.native_obj.Nodes = value
            
    # -> Any            
    @property         
    def parent(self) -> "Any":
        return (self.native_obj.Parent)
        
    @parent.setter     
    def _set_parent(self, value):
        self.native_obj.Parent = value
            
    # -> Any            
    @property         
    def parentGroup(self) -> "Any":
        return (self.native_obj.ParentGroup)
        
    @parentGroup.setter     
    def _set_parentGroup(self, value):
        self.native_obj.ParentGroup = value
            
    # -> Any            
    @property         
    def reflection(self) -> "Any":
        return (self.native_obj.Reflection)
        
    @reflection.setter     
    def _set_reflection(self, value):
        self.native_obj.Reflection = value
            
    # -> Any            
    @property         
    def rotation(self) -> "Any":
        return (self.native_obj.Rotation)
        
    @rotation.setter     
    def _set_rotation(self, value):
        self.native_obj.Rotation = value
            
    # -> Any            
    @property         
    def script(self) -> "Any":
        return (self.native_obj.Script)
        
    @script.setter     
    def _set_script(self, value):
        self.native_obj.Script = value
            
    # -> Any            
    @property         
    def shadow(self) -> "Any":
        return (self.native_obj.Shadow)
        
    @shadow.setter     
    def _set_shadow(self, value):
        self.native_obj.Shadow = value
            
    # -> Any            
    @property         
    def shapeStyle(self) -> "Any":
        return (self.native_obj.ShapeStyle)
        
    @shapeStyle.setter     
    def _set_shapeStyle(self, value):
        self.native_obj.ShapeStyle = value
            
    # -> Any            
    @property         
    def softEdge(self) -> "Any":
        return (self.native_obj.SoftEdge)
        
    @softEdge.setter     
    def _set_softEdge(self, value):
        self.native_obj.SoftEdge = value
            
    # -> Any            
    @property         
    def table(self) -> "Any":
        return (self.native_obj.Table)
        
    @table.setter     
    def _set_table(self, value):
        self.native_obj.Table = value
            
    # -> Any            
    @property         
    def textEffect(self) -> "Any":
        return (self.native_obj.TextEffect)
        
    @textEffect.setter     
    def _set_textEffect(self, value):
        self.native_obj.TextEffect = value
            
    # -> Any            
    @property         
    def textFrame(self) -> "Any":
        return (self.native_obj.TextFrame)
        
    @textFrame.setter     
    def _set_textFrame(self, value):
        self.native_obj.TextFrame = value
            
    # -> Any            
    @property         
    def textFrame2(self) -> "Any":
        return (self.native_obj.TextFrame2)
        
    @textFrame2.setter     
    def _set_textFrame2(self, value):
        self.native_obj.TextFrame2 = value
            
    # -> Any            
    @property         
    def threeD(self) -> "Any":
        return (self.native_obj.ThreeD)
        
    @threeD.setter     
    def _set_threeD(self, value):
        self.native_obj.ThreeD = value
            
    # -> Any            
    @property         
    def title(self) -> "Any":
        return (self.native_obj.Title)
        
    @title.setter     
    def _set_title(self, value):
        self.native_obj.Title = value
            
    # -> Any            
    @property         
    def top(self) -> "Any":
        return (self.native_obj.Top)
        
    @top.setter     
    def _set_top(self, value):
        self.native_obj.Top = value
            
    # -> Any            
    @property         
    def type(self) -> "Any":
        return (self.native_obj.Type)
        
    @type.setter     
    def _set_type(self, value):
        self.native_obj.Type = value
            
    # -> Any            
    @property         
    def value(self) -> "Any":
        return (self.native_obj.Value)
        
    @value.setter     
    def _set_value(self, value):
        self.native_obj.Value = value
            
    # -> Any            
    @property         
    def verticalFlip(self) -> "Any":
        return (self.native_obj.VerticalFlip)
        
    @verticalFlip.setter     
    def _set_verticalFlip(self, value):
        self.native_obj.VerticalFlip = value
            
    # -> Any            
    @property         
    def vertices(self) -> "Any":
        return (self.native_obj.Vertices)
        
    @vertices.setter     
    def _set_vertices(self, value):
        self.native_obj.Vertices = value
            
    # -> Any            
    @property         
    def visible(self) -> "Any":
        return (self.native_obj.Visible)
        
    @visible.setter     
    def _set_visible(self, value):
        self.native_obj.Visible = value
            
    # -> Any            
    @property         
    def width(self) -> "Any":
        return (self.native_obj.Width)
        
    @width.setter     
    def _set_width(self, value):
        self.native_obj.Width = value
            
    # -> Any            
    @property         
    def zOrderPosition(self) -> "Any":
        return (self.native_obj.ZOrderPosition)
        
    @zOrderPosition.setter     
    def _set_zOrderPosition(self, value):
        self.native_obj.ZOrderPosition = value
            
# end "ShapeRange"       
        