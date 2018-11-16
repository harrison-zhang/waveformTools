# -*- coding: utf-8 -*-
import wx
import numpy as np
import pandas as pd
import matplotlib

# matplotlib采用WXAgg为后台,将matplotlib嵌入wxPython中
matplotlib.use("WXAgg")

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.ticker import MultipleLocator, FuncFormatter

import pylab
from matplotlib import pyplot
from dateutil.parser import parse


######################################################################################
class MPL_Panel_base(wx.Panel):
    ''''' #MPL_Panel_base面板,可以继承或者创建实例'''

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=-1)

        self.Figure = matplotlib.figure.Figure(figsize=(20, 10))
        self.axes = self.Figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.FigureCanvas = FigureCanvas(self, -1, self.Figure)

        self.NavigationToolbar = NavigationToolbar(self.FigureCanvas)

        self.StaticText = wx.StaticText(self, -1, label='     提示：先从菜单栏打开要展示的csv文件')

        self.SubBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SubBoxSizer.Add(self.NavigationToolbar, proportion=0, border=2, flag=wx.ALL | wx.EXPAND)
        self.SubBoxSizer.Add(self.StaticText, proportion=-1, border=2, flag=wx.ALL | wx.EXPAND)

        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.TopBoxSizer.Add(self.SubBoxSizer, proportion=-1, border=2, flag=wx.ALL | wx.EXPAND)
        self.TopBoxSizer.Add(self.FigureCanvas, proportion=-10, border=2, flag=wx.ALL | wx.EXPAND)

        self.SetSizer(self.TopBoxSizer)

        ###方便调用
        self.pylab = pylab
        self.pl = pylab
        self.pyplot = pyplot
        self.numpy = np
        self.np = np
        self.plt = pyplot

    def UpdatePlot(self):
        '''''#修改图形的任何属性后都必须使用self.UpdatePlot()更新GUI界面 '''
        self.FigureCanvas.draw()

    def plot(self, *args, **kwargs):
        '''''#最常用的绘图命令plot '''
        self.axes.plot(*args, **kwargs)
        self.UpdatePlot()

    def semilogx(self, *args, **kwargs):
        ''''' #对数坐标绘图命令 '''
        self.axes.semilogx(*args, **kwargs)
        self.UpdatePlot()

    def semilogy(self, *args, **kwargs):
        ''''' #对数坐标绘图命令 '''
        self.axes.semilogy(*args, **kwargs)
        self.UpdatePlot()

    def loglog(self, *args, **kwargs):
        ''''' #对数坐标绘图命令 '''
        self.axes.loglog(*args, **kwargs)
        self.UpdatePlot()

    def grid(self, flag=True):
        ''''' ##显示网格  '''
        if flag:
            self.axes.grid()
        else:
            self.axes.grid(False)

    def legend(self):
        self.axes.legend(loc='best')

    def title_MPL(self, TitleString="wxMatPlotLib Example In wxPython"):
        ''''' # 给图像添加一个标题   '''
        self.axes.set_title(TitleString)

    def xlabel(self, XabelString="X"):
        ''''' # Add xlabel to the plotting    '''
        self.axes.set_xlabel(XabelString)

    def ylabel(self, YabelString="Y"):
        ''''' # Add ylabel to the plotting '''
        self.axes.set_ylabel(YabelString)

    def xticker(self, major_ticker=1.0, minor_ticker=0.1):
        ''''' # 设置X轴的刻度大小 '''
        self.axes.xaxis.set_major_locator(MultipleLocator(major_ticker))
        self.axes.xaxis.set_minor_locator(MultipleLocator(minor_ticker))

    def yticker(self, major_ticker=1.0, minor_ticker=0.1):
        ''''' # 设置Y轴的刻度大小 '''
        self.axes.yaxis.set_major_locator(MultipleLocator(major_ticker))
        self.axes.yaxis.set_minor_locator(MultipleLocator(minor_ticker))

    def legend(self, *args, **kwargs):
        ''''' #图例legend for the plotting  '''
        self.axes.legend(*args, **kwargs)

    def xlim(self, x_min, x_max):
        ''' # 设置x轴的显示范围  '''
        self.axes.set_xlim(x_min, x_max)

    def ylim(self, y_min, y_max):
        ''' # 设置y轴的显示范围   '''
        self.axes.set_ylim(y_min, y_max)

    def savefig(self, *args, **kwargs):
        ''' #保存图形到文件 '''
        self.Figure.savefig(*args, **kwargs)

    def cla(self):
        ''' # 再次画图前,必须调用该命令清空原来的图形  '''
        self.axes.clear()
        self.Figure.set_canvas(self.FigureCanvas)
        self.UpdatePlot()

    def ShowHelpString(self, HelpString="Show Help String"):
        ''''' #可以用它来显示一些帮助信息,如鼠标位置等 '''
        self.StaticText.SetLabel(HelpString)

class MPL_Frame(wx.Frame):
    """MPL_Frame可以继承,并可修改,或者直接使用"""

    def __init__(self, title="WaveformToools", size=(1100, 700)):
        wx.Frame.__init__(self, parent=None, title=title, size=size)

        # 创建菜单
        self.menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu2 = wx.Menu()
        open = menu1.Append(wx.ID_OPEN, 'Open', 'open the wave form csv')
        self.Bind(wx.EVT_MENU, self.openCsv, open)
        helpMenu = menu2.Append(wx.ID_ABORT, 'Help', '帮助文档')
        self.Bind(wx.EVT_MENU, self.showHelp, helpMenu)
        self.menuBar.Append(menu1, 'File')
        self.menuBar.Append(menu2, 'Help')

        # 创建分割器
        splitter = wx.SplitterWindow(self, -1)

        # 波形面板
        self.MPL = MPL_Panel_base(splitter)
        # 右面板
        self.RightPanel = wx.Panel(splitter, -1)

        # 创建FlexGridSizer
        self.FlexGridSizer = wx.FlexGridSizer(rows=9, cols=1, vgap=5, hgap=5)
        self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)

        # StaticBox
        staticBox0 = wx.StaticBox(self.RightPanel, -1, '波形选取')
        checkListBoxSizer = wx.StaticBoxSizer(staticBox0, wx.VERTICAL)

        # CheckListBox
        self.checkListBox = wx.CheckListBox(self.RightPanel, choices=['波形1', '波形2'])
        self.Bind(wx.EVT_CHECKLISTBOX, self.onCheckListBoxSelect, self.checkListBox)
        checkListBoxSizer.Add(self.checkListBox, proportion=1, border=5, flag=wx.EXPAND)

        # Slider
        self.smallValue = 1             # 波形x轴的上下限
        self.bigValue = 50

        self.sld1 = wx.Slider(self.RightPanel, value=self.smallValue, minValue=1, maxValue=100,
                              size=(150, 10), style=wx.SL_HORIZONTAL|wx.SL_MIN_MAX_LABELS)
        self.sld2 = wx.Slider(self.RightPanel, value=self.bigValue, minValue=1, maxValue=100,
                              size=(150, 10), style=wx.SL_HORIZONTAL | wx.SL_MIN_MAX_LABELS)
        self.sld1.Bind(wx.EVT_SLIDER, self.onSliderScroll1)
        self.sld2.Bind(wx.EVT_SLIDER, self.onSliderScroll2)

        # sliderSizer
        staticBox = wx.StaticBox(self.RightPanel, -1, 'X轴刻度')
        sliderSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        # sliderSizer.SetFlexibleDirection(wx.BOTH)

        sldLbl1 = wx.StaticText(self.RightPanel, -1, style=wx.ALIGN_LEFT)
        sldLbl2 = wx.StaticText(self.RightPanel, -1, style=wx.ALIGN_LEFT)
        sldFont = wx.Font(13, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        sldLbl1.SetFont(sldFont)
        sldLbl2.SetFont(sldFont)
        sldLbl1.SetLabel('左刻度:')
        sldLbl2.SetLabel('右刻度:')

        # SpinCtrl
        self.spinCtrl1 = wx.SpinCtrl(self.RightPanel, -1, value='1', size=(20, 10),
                                     style=wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER, min=1, max=100, initial=1)
        self.spinCtrl2 = wx.SpinCtrl(self.RightPanel, -1, value='2', size=(20, 10),
                                     style=wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER, min=1, max=100, initial=50)
        self.spinCtrl1.Bind(wx.EVT_SPINCTRL, self.onSpinCtrlEvt1)
        self.spinCtrl1.Bind(wx.EVT_TEXT_ENTER, self.onSpinCtrlEvt1)
        self.spinCtrl2.Bind(wx.EVT_SPINCTRL, self.onSpinCtrlEvt2)
        self.spinCtrl1.Bind(wx.EVT_TEXT_ENTER, self.onSpinCtrlEvt2)

        showBtn = wx.Button(self.RightPanel, -1, "Done", size=(60, 40))
        showBtn.Bind(wx.EVT_BUTTON, self.showEvent)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.sld1, proportion=1, border=5, flag=wx.EXPAND)
        hbox1.Add(self.spinCtrl1, proportion=1, border=5, flag=wx.EXPAND)
        hbox2.Add(self.sld2, proportion=1, border=5, flag=wx.EXPAND)
        hbox2.Add(self.spinCtrl2, proportion=1, border=5, flag=wx.EXPAND)

        sliderSizer.Add(sldLbl1, proportion=1, border=5, flag=wx.EXPAND)
        sliderSizer.Add(hbox1, proportion=1, border=5, flag=wx.EXPAND)
        sliderSizer.Add(sldLbl2, proportion=1, border=5, flag=wx.EXPAND)
        sliderSizer.Add(hbox2, proportion=1, border=5, flag=wx.EXPAND)
        sliderSizer.Add(showBtn, proportion=1, border=5, flag=wx.ALIGN_RIGHT)


        # StaticText
        lbl1 = wx.StaticText(self.RightPanel, -1, style=wx.ALIGN_LEFT)
        lbl2 = wx.StaticText(self.RightPanel, -1, style=wx.ALIGN_LEFT)
        font = wx.Font(16, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        lbl1.SetFont(font)
        lbl1.SetLabel('')
        lbl2.SetFont(font)
        lbl2.SetForegroundColour((0, 0, 255))       # 设置字体颜色
        # lbl2.SetBackgroundColour((255, 0, 0))     # 设置字体背景颜色
        lbl2.SetLabel('控制面板')

        # showOutButton
        showOutBtn = wx.Button(self.RightPanel, -1, 'ShowOut', size=(75, 40))
        showOutBtn.Bind(wx.EVT_BUTTON, self.onShowOutEvent)

        # 加入Sizer中
        self.FlexGridSizer.Add(lbl1, proportion=1, border=5, flag=wx.EXPAND)
        self.FlexGridSizer.Add(lbl2, proportion=1, border=5, flag=wx.EXPAND)
        self.FlexGridSizer.Add(checkListBoxSizer, proportion=1, border=5, flag= wx.EXPAND)
        self.FlexGridSizer.Add(sliderSizer, proportion=1, border=5, flag=wx.EXPAND)
        self.FlexGridSizer.Add(showOutBtn, proportion=1, border=5, flag=wx.ALIGN_RIGHT)

        self.RightPanel.SetSizer(self.FlexGridSizer)
        splitter.SplitVertically(self.MPL, self.RightPanel, sashPosition=-240)

        # self.BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.BoxSizer.Add(self.MPL, proportion=-10, border=2, flag=wx.ALL | wx.EXPAND)
        # self.BoxSizer.Add(self.RightPanel, proportion=0, border=2, flag=wx.ALL | wx.EXPAND)
        # self.SetSizer(splitter)

        # 状态栏
        self.StatusBar()
        #菜单栏
        self.SetMenuBar(self.menuBar)

        # MPL_Frame界面居中显示
        self.Centre(wx.BOTH)

    # 菜单事件，用于打开csv
    def openCsv(self, event):
        self.MPL.ShowHelpString("  提示：正在加载cvs数据，请稍候...")
        filesFilter = 'CSV (*.csv)|*.csv'
        fileDialog = wx.FileDialog(self, message='选择一个csv文件', wildcard=filesFilter, style=wx.FD_OPEN)
        if fileDialog.ShowModal() == wx.ID_OK:
            path = fileDialog.GetPath()
            try:
                # 用pandas打开csv文件
                self.data = pd.read_csv(path)
            except:
                dlg = wx.MessageDialog(self, 'Error opening file\n')
                dlg.ShowModal()
        fileDialog.Destroy()

        # 设置CheckListBox和slider,spinCtrl
        self.dataLen = len(self.data)                           # 数据列数
        self.checkList = [index for index in self.data.columns]

        self.sld1.SetMax(self.dataLen)
        self.sld2.SetMax(self.dataLen)
        self.checkListBox.Clear()
        self.checkListBox.Append(self.checkList)
        self.spinCtrl1.SetMax(self.dataLen)
        self.spinCtrl2.SetMax(self.dataLen)

        a = self.data['Time'].values
        self.dataTime = [parse(i) for i in a]

        self.MPL.ShowHelpString("  提示：在右侧波形选取框勾选需要分析的波形")

    # 复选框选中取消事件
    def onCheckListBoxSelect(self, event):
        self.checkedColumns = [column for column in self.checkListBox.GetCheckedStrings()]
        self.showWaveform()

    # 滑块移动事件
    def onSliderScroll1(self, event):
        self.smallValue = self.sld1.GetValue()
        self.spinCtrl1.SetValue(self.smallValue)
        # self.showWaveform()


    def onSliderScroll2(self, event):
        self.bigValue = self.sld2.GetValue()
        self.spinCtrl2.SetValue(self.bigValue)
        # self.showWaveform()

    # spinCtrl事件
    def onSpinCtrlEvt1(self, event):
        self.smallValue = self.spinCtrl1.GetValue()
        self.sld1.SetValue(self.spinCtrl1.GetValue())

    def onSpinCtrlEvt2(self, event):
        self.bigValue = self.spinCtrl2.GetValue()
        self.sld2.SetValue(self.spinCtrl2.GetValue())

    def onSpinCtrlEnter(self, event):
        self.sld1.SetValue(self.spinCtrl1.GetValue())

    # 按钮事件
    def showEvent(self, event):
        self.showWaveform()

    def onShowOutEvent(self, event):
        fig, ax = pyplot.subplots(figsize=(11, 6))
        # if self.smallValue >= self.bigValue:
        #     xrange = np.arange(self.bigValue, self.smallValue, int((self.smallValue - self.bigValue) / 10))
        # else:
        #     xrange = np.arange(self.smallValue, self.bigValue, int((self.bigValue - self.smallValue) / 10))

        for column in self.checkedColumns:
            if self.smallValue >= self.bigValue:
                x = self.dataTime[self.bigValue:self.smallValue]
                y = self.data[column][self.bigValue:self.smallValue]
                ax.plot(x, y, alpha=0.7, label=column)
            else:
                x = self.dataTime[self.smallValue:self.bigValue]
                y = self.data[column][self.smallValue:self.bigValue]
                ax.plot(x, y, alpha=0.7, label=column)
        # ax.set_xticks(xrange)                                         # 设置坐标刻度
        # ax.set_xticklabels(self.data['Time'][xrange], rotation=90)    # 设置坐标刻度值
        pyplot.grid(True)
        pyplot.legend(loc='best')
        pyplot.show()

    # def Button1Event(self, event):
    #     self.MPL.cla()                  # 必须清理图形,才能显示下一幅图
    #     # x = np.arange(-10, 10, 0.25)
    #     # y = np.cos(x)
    #     # self.MPL.plot(x, y, '--*g')
    #     # self.MPL.xticker(2.0, 0.5)
    #     # self.MPL.yticker(0.5, 0.1)
    #     # self.MPL.title_MPL("MPL1")
    #     # self.MPL.ShowHelpString("You Can Show MPL Helpful String Here !")
    #     # self.MPL.grid()
    #     # self.MPL.UpdatePlot()  # 必须刷新才能显示
    #
    #     x = np.arange(1000)
    #     y = self.data['HV'][:1000]
    #     y2 = self.data['STATUS'][:1000]
    #     self.MPL.plot(x, y, alpha=0.6)
    #     self.MPL.plot(x, y2, alpha=0.6)
    #     # self.MPL.yticker(5.0, 1.0)
    #     self.MPL.title_MPL('HV')
    #     self.MPL.grid()
    #     self.MPL.UpdatePlot()

    def showWaveform(self):
        if self.smallValue > self.bigValue:
            self.plot(self.bigValue, self.smallValue, self.checkedColumns)
        else:
            self.plot(self.smallValue, self.bigValue, self.checkedColumns)

    def plot(self, min, max, checkedColumns):
        self.MPL.cla()
        for column in checkedColumns:
            x = np.arange(min, max)
            y = self.data[column][min:max]
            self.MPL.plot(x, y, alpha=0.7, label=column)
        self.MPL.grid()
        self.MPL.legend()
        self.MPL.UpdatePlot()

    # 自动创建状态栏
    def StatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-2, -2, -1])

    # About对话框
    def showHelp(self, event):
        dlg = wx.MessageDialog(self,
                               "1.先在菜单栏打开需要分析的csv文件（文件大的情况可能打开较慢）\n"
                               "2.控制面板波形选取框可勾选想要展示的波形 \n"
                               "3.控制面板两个滑块可选择想要的X轴上下限，按'Done'按钮绘制波形 \n"
                               "4.控制面板'ShowOut'按钮用于展示带时间刻度的X轴，并附加有X,Y游标",
                               'WaveformTools Help', wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

if __name__ == '__main__':
    app = wx.App()
    frame = MPL_Frame()
    frame.Center()
    frame.Show()
    app.MainLoop()