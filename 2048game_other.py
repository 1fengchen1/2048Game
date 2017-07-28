# -*- coding: utf-8 -*-
# =====================================
# name: 2048.py
# version: 1.0.0
# coder: 律酱大爱
# =====================================
# version: 1.0.1
# coder: heibanke
# =====================================
# version: 1.0.2
# coder: 风尘
# add content: 1,对每一行详细注释;2,将难读的代码替换为易懂代码
# QQ:75886823
# QQ群：585499566
#学习代码耗时：【3周】
#学习代码方式：在本地实现实验楼的学习路径
#实验楼地址：https://www.shiyanlou.com/courses/427
# =====================================
#第一位作者的代码地址：https://pan.baidu.com/s/1mgMBNg0
#第二位作者的代码地址：http://study.163.com/course/courseLearn.htm?courseId=1263029#/learn/video?lessonId=1507383&courseId=1263029
#第三位作者的代码地址：
#第一位作者：应该是wxPython实现2048游戏的创始人，因为是在百度贴吧找到的，无法联系到作者(作者的贴吧账号无法关注，私信)，个人认为创始人是个低调，所以无法联系到啊
#第二位作者：是网易云课堂的讲师，有视频对第一位作者的2048进行改进和视频讲解，不过不适合新手，很多地方的基础没有讲到
#第三位作者：就是本人了哈，主要是对前两个人代码进行逐行的解释，本人在找Python实战项目的时候，找到代码的路径是：知乎->实验楼(实验楼用的是第二作者的代码)->百度贴吧(第三作者)
#======================================
#人世间都是一粒风尘，聚尘成山
#感谢前两位作者的努力，鉴于以后其他初学小伙伴能够更好的阅读2048的代码，本人就“高调”的写上自己的注释哈，有不对的地方多多指正，我来进行修改哈
#======================================

import wx
import os
import random
import copy

#设置游戏窗口wx.Window是所有窗口的基类，表示任何可见的对象在屏幕上
class Window(wx.Window):
    """
    __init__(self, Window parent, int id=-1, Point pos=DefaultPosition, 
            Size size=DefaultSize, long style=0, String name=PanelNameStr) -> Window
    构建并显示一个通用窗口。parent代表父窗口
    """
    def __init__(self, parent):
        #继承wx.Window的初始化
        super(Window, self).__init__(parent)

        # 设置每个数字的颜色，并初始化（我觉得可以删除一些，没有必要写这么多的，就删除多余的了）
        self.colors = {0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
                       16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59), 128: (237, 207, 114),
                       256: (237, 207, 114), 512: (237, 207, 114), 1024: (237, 207, 114), 2048: (237, 207, 114),
                       4096: (237, 207, 114), 8192: (237, 207, 114), 16384: (237, 207, 114), 32768: (237, 207, 114),
                       }

        self.initGame()     #对游戏界面（窗体）初始化
        self.initBuffer()   #对面板初始化

        self.Bind(wx.EVT_SIZE, self.onSize)  #绑定onSize行为，use wx.BufferedPaintDC
        self.Bind(wx.EVT_PAINT, self.onPaint)   #绑定onPaint行为
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)  ##绑定按键行为

    def loadScore(self):
        if os.path.exists("bestscore.ini"):
            ff = open("bestscore.ini")
            self.bstScore = ff.read()
            ff.close()

    def saveScore(self):
        ff = open("bestscore.ini", "w")
        ff.write(str(self.bstScore))
        ff.close()

    def initGame(self):
        self.bgFont = wx.Font(50, wx.SWISS, wx.NORMAL, wx.BOLD, face=u"Roboto")
        self.scFont = wx.Font(36, wx.SWISS, wx.NORMAL, wx.BOLD, face=u"Roboto")
        self.smFont = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL, face=u"Roboto")
        self.curScore = 0
        self.bstScore = 0
        self.loadScore()
        self.data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        count = 0
        while count < 2:
            row = random.randint(0, len(self.data) - 1)
            col = random.randint(0, len(self.data[0]) - 1)
            if self.data[row][col] != 0: continue
            self.data[row][col] = 2 if random.randint(0, 1) else 4
            count += 1

    def initBuffer(self):
        w, h = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(w, h)

    def onSize(self, event):
        self.initBuffer()
        self.drawAll()

    def onPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)

    def putTile(self):
        available = []
        for row in range(len(self.data)):
            for col in range(len(self.data[0])):
                if self.data[row][col] == 0: available.append((row, col))
        if available:
            row, col = available[random.randint(0, len(available) - 1)]
            self.data[row][col] = 2 if random.randint(0, 1) else 4
            return True
        return False

    def update(self, vlist, direct):
        score = 0
        if direct:  # up or left
            i = 1
            while i < len(vlist):
                if vlist[i - 1] == vlist[i]:
                    del vlist[i]
                    vlist[i - 1] *= 2
                    score += vlist[i - 1]
                    i += 1
                i += 1
        else:
            i = len(vlist) - 1
            while i > 0:
                if vlist[i - 1] == vlist[i]:
                    del vlist[i]
                    vlist[i - 1] *= 2
                    score += vlist[i - 1]
                    i -= 1
                i -= 1
                # print self.data
        return score

    def slideUpDown(self, up):
        score = 0
        numCols = len(self.data[0])
        numRows = len(self.data)
        oldData = copy.deepcopy(self.data)

        for col in range(numCols):
            cvl = [self.data[row][col] for row in range(numRows) if self.data[row][col] != 0]

            if len(cvl) >= 2:
                score += self.update(cvl, up)
            for i in range(numRows - len(cvl)):
                if up:
                    cvl.append(0)
                else:
                    cvl.insert(0, 0)
            for row in range(numRows): self.data[row][col] = cvl[row]
        return oldData != self.data, score

    def slideLeftRight(self, left):
        score = 0
        numRows = len(self.data)
        numCols = len(self.data[0])
        oldData = copy.deepcopy(self.data)

        for row in range(numRows):
            rvl = [self.data[row][col] for col in range(numCols) if self.data[row][col] != 0]

            if len(rvl) >= 2:
                score += self.update(rvl, left)
            for i in range(numCols - len(rvl)):
                if left:
                    rvl.append(0)
                else:
                    rvl.insert(0, 0)
            for col in range(numCols): self.data[row][col] = rvl[col]
        return oldData != self.data, score

    def isGameOver(self):
        copyData = copy.deepcopy(self.data)

        flag = False
        if not self.slideUpDown(True)[0] and not self.slideUpDown(False)[0] and not self.slideLeftRight(True)[0] and not \
        self.slideLeftRight(False)[0]:
            flag = True
        if not flag: self.data = copyData
        return flag

    def doMove(self, move, score):
        if move:
            self.putTile()
            self.drawChange(score)
            if self.isGameOver():
                if wx.MessageBox(u"游戏结束，是否重新开始？", u"哈哈", wx.YES_NO | wx.ICON_INFORMATION) == wx.YES:
                    bstScore = self.bstScore
                    self.initGame()
                    self.bstScore = bstScore
                    self.drawAll()

    def onKeyDown(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_UP:
            self.doMove(*self.slideUpDown(True))
        elif keyCode == wx.WXK_DOWN:
            self.doMove(*self.slideUpDown(False))
        elif keyCode == wx.WXK_LEFT:
            self.doMove(*self.slideLeftRight(True))
        elif keyCode == wx.WXK_RIGHT:
            self.doMove(*self.slideLeftRight(False))

    def drawBg(self, dc):
        dc.SetBackground(wx.Brush((250, 248, 239)))
        dc.Clear()
        dc.SetBrush(wx.Brush((187, 173, 160)))
        dc.SetPen(wx.Pen((187, 173, 160)))
        dc.DrawRoundedRectangle(15, 150, 475, 475, 5)

    def drawLogo(self, dc):
        dc.SetFont(self.bgFont)
        dc.SetTextForeground((119, 110, 101))
        dc.DrawText(u"2048", 15, 26)

    def drawLabel(self, dc):
        dc.SetFont(self.smFont)
        dc.SetTextForeground((119, 110, 101))
        dc.DrawText(u"合并相同数字，得到2048吧!", 15, 114)
        dc.DrawText(u"怎么玩: \n用-> <- 上下左右箭头按键来移动方块. \n当两个相同数字的方块碰到一起时，会合成一个!", 15, 639)

    def drawScore(self, dc):
        dc.SetFont(self.smFont)
        scoreLabelSize = dc.GetTextExtent(u"SCORE")
        bestLabelSize = dc.GetTextExtent(u"BEST")
        curScoreBoardMinW = 15 * 2 + scoreLabelSize[0]
        bstScoreBoardMinW = 15 * 2 + bestLabelSize[0]
        curScoreSize = dc.GetTextExtent(str(self.curScore))
        bstScoreSize = dc.GetTextExtent(str(self.bstScore))
        curScoreBoardNedW = 10 + curScoreSize[0]
        bstScoreBoardNedW = 10 + bstScoreSize[0]
        curScoreBoardW = max(curScoreBoardMinW, curScoreBoardNedW)
        bstScoreBoardW = max(bstScoreBoardMinW, bstScoreBoardNedW)
        dc.SetBrush(wx.Brush((187, 173, 160)))
        dc.SetPen(wx.Pen((187, 173, 160)))
        dc.DrawRoundedRectangle(505 - 15 - bstScoreBoardW, 40, bstScoreBoardW, 50, 3)
        dc.DrawRoundedRectangle(505 - 15 - bstScoreBoardW - 5 - curScoreBoardW, 40, curScoreBoardW, 50, 3)
        dc.SetTextForeground((238, 228, 218))
        dc.DrawText(u"BEST", 505 - 15 - bstScoreBoardW + (bstScoreBoardW - bestLabelSize[0]) / 2, 48)
        dc.DrawText(u"SCORE", 505 - 15 - bstScoreBoardW - 5 - curScoreBoardW + (curScoreBoardW - scoreLabelSize[0]) / 2,
                    48)
        dc.SetTextForeground((255, 255, 255))
        dc.DrawText(str(self.bstScore), 505 - 15 - bstScoreBoardW + (bstScoreBoardW - bstScoreSize[0]) / 2, 68)
        dc.DrawText(str(self.curScore),
                    505 - 15 - bstScoreBoardW - 5 - curScoreBoardW + (curScoreBoardW - curScoreSize[0]) / 2, 68)

    def drawTiles(self, dc):
        dc.SetFont(self.scFont)
        for row in range(4):
            for col in range(4):
                value = self.data[row][col]
                color = self.colors[value]
                if value == 2 or value == 4:
                    dc.SetTextForeground((119, 110, 101))
                else:
                    dc.SetTextForeground((255, 255, 255))
                dc.SetBrush(wx.Brush(color))
                dc.SetPen(wx.Pen(color))
                dc.DrawRoundedRectangle(30 + col * 115, 165 + row * 115, 100, 100, 2)
                size = dc.GetTextExtent(str(value))
                while size[0] > 100 - 15 * 2:
                    self.scFont = wx.Font(self.scFont.GetPointSize() * 4 / 5, wx.SWISS, wx.NORMAL, wx.BOLD,
                                          face=u"Roboto")
                    dc.SetFont(self.scFont)
                    size = dc.GetTextExtent(str(value))
                if value != 0: dc.DrawText(str(value), 30 + col * 115 + (100 - size[0]) / 2,
                                           165 + row * 115 + (100 - size[1]) / 2)

    def drawAll(self):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.drawBg(dc)
        self.drawLogo(dc)
        self.drawLabel(dc)
        self.drawScore(dc)
        self.drawTiles(dc)

    def drawChange(self, score):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        if score:
            self.curScore += score
            if self.curScore > self.bstScore:
                self.bstScore = self.curScore
            self.drawScore(dc)
        self.drawTiles(dc)

#自定义Frame类
class Frame(wx.Frame):

    #初始化传入title参数
    def __init__(self, title):
        super(Frame, self).__init__(None, -1, title, style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)
        self.setIcon()  #初始化图标
        self.window = Window(self)  #初始化基础窗体
        self.Bind(wx.EVT_CLOSE, self.onClose)   #初始化绑定onCLose行为

    def onClose(self, event):
        self.window.saveScore()
        self.Destroy()

    def setIcon(self):
        icon = wx.Icon("icon.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

#wxPython定制类，
class App(wx.App):
    '''
    1,初始化：wxPython定制的类的所需的初始化通常都由OnInit()方法管理,而不在Python的__init__方法中
    2,这个方法不要求参数并返回一个布尔值,如果所返回的值是False,则应用程序将立即退出。
    '''
    def OnInit(self):
        self.frame = Frame(u"2048 v1.0.1 by heibanke")  #对Frame类进行初始化
        self.frame.SetClientSize((505, 720))    #对窗体尺寸进行初始化
        self.frame.Center() #对窗体位置进行初始化
        self.frame.Show()   #对窗体是否展示进行初始化
        return True     #返回True，继续执行


if __name__ == "__main__":
    app = App()
    app.MainLoop()