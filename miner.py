import os
import time

import win32gui
import win32api
import win32con
import cv2
import BGK


class Miner:
    def __init__(self, windowName, test=False, WapenNum=3, MaxScrollNumber=7):
        self.hWnd = win32gui.FindWindow('Qt5QWindowIcon', windowName)
        self.loadPictureAndGenPosList()
        self.test = test
        self.WapenNum = WapenNum
        self.MaxScrollNumber = MaxScrollNumber

    def loadPictureAndGenPosList(self):
        self.loadImageSuccess = True
        # gen Jump
        self.JumpTagImg = self.loadImage("Tags\\JumpTag.PNG")
        self.ConfirmTagImg = self.loadImage("Tags\\ConfirmTag.PNG")
        self.LeaveStationImg = self.loadImage("Tags\\LeaveStation.PNG")
        self.JumpPoses = []
        for i in range(2):
            self.JumpPoses.append([350, 437 + 120 * i])
        # gen packBag
        ## move to MaterialsHangar
        self.BagImg = self.loadImage("Tags\\Bag.PNG")
        self.OreBinImg = self.loadImage("Tags\\oreBin.PNG")
        self.AllSelectImg = self.loadImage("Tags\\AllSelect.PNG")
        self.MaterialsHangarImg = self.loadImage("Tags\\MaterialsHangar.PNG")
        self.MoveToImg = self.loadImage("Tags\\MoveTo.PNG")
        ## Stack All
        self.StackAllImg = self.loadImage("Tags\\StackAll.PNG")
        self.EndOperationImg = self.loadImage("Tags\\EndOperation.PNG")
        # gen MineOre
        self.ObservceEyeImg = self.loadImage("Tags\\ObserveEye.PNG")
        ## jump to planetary
        self.PlantaryTagImg = self.loadImage("Tags\\PlantaryTag.PNG")
        self.PlanetaryClusterImg = self.loadImage("Tags\\PlanetaryCluster.PNG")
        self.PlanetaryQuesImg = self.loadImage("Tags\\PlanetaryQues.PNG")
        self.PlanetaryDsImg = self.loadImage("Tags\\PlanetaryDs.PNG")
        self.TransitionImg = self.loadImage("Tags\\Transition.PNG")
        self.OreTagImg = self.loadImage("Tags\\OreTag.PNG")
        self.OreTagPos = [1600, 230]
        ## Mining
        ### find and lock
        self.FirstOrePos = [1400, 120]
        self.LockImg = self.loadImage("Tags\\Lock.PNG")
        ### coming close
        self.SpeedUpImg = self.loadImage("Tags\\SpeedUp.PNG")
        self.InWorkingImg = self.loadImage("Tags\\InWorking.PNG")
        self.CollectorNotWorkingTagImg = self.loadImage("Tags\\CollectorNotWorkingTag.PNG")
        self.ComingCloseImg = self.loadImage("Tags\\ComingClose.png")
        self.AroundImg = self.loadImage("Tags\\Around.png")
        self.StopShipImg = self.loadImage("Tags\\StopShip.PNG")
        self.LockOrePos = [1200, 80]
        self.BagFullImg = self.loadImage("Tags\\BagFull.PNG")
        # gen OreImg
        self.oreList = []
        self.oreImgPathList = os.listdir("Tags\\oreList\\")
        for oreImgPath in self.oreImgPathList:
            self.oreList.append(self.loadImage("Tags\\oreList\\" + oreImgPath))
        print("load {} ore".format(len(self.oreList)))


    def Run(self):
        if self.test == True:
            self.testRun()
            return
        if not self.loadImageSuccess:
            print("图片加载失败 , 程序退出")
            return False
        while True:
            self.MineOre()
            self.BackStation()
            self.PackBag()

    def testRun(self):
        # self.BackStation()
        # self.PackBag()
        # self.MineOre()
        # self.Mining()
        # self.Click(self.FirstOrePos)
        # self.ScrollDownOrePage()
        # self.ScrollUpOrePage()
        print(cv2.imread("notExist.PNG"))
        # self.FindOreAndLock()
        # print(self.isWorking())
        # if not self.isWorking():
        # self.clickTargetImg(self.CollectorNotWorkingTagImg)
        # self.clickTargetImg(self.CollectorNotWorkingTagImg)
        # if not self.isWorking():
        #    self.FindOreAndLock()

    def BackStation(self):
        print("开始回站")
        self.clickJump(0)
        while self.checkInStation() == False:
            print("回站 等待")
            time.sleep(10)
        print("已经回到空间站")
        time.sleep(3)

    def clickJump(self, jumpIndex):
        if self.clickTargetImg(self.JumpTagImg) == False:
            print("not found JumpTag")
            return
        self.Click(self.JumpPoses[jumpIndex])
        self.clickTargetImg(self.ConfirmTagImg)

    def checkInStation(self):
        return self.checkImgExist(self.LeaveStationImg)

    def PackBag(self):
        print("开始整理背包")
        self.MoveToMateriesBin()
        print("开始堆叠所有")
        self.StackAll()
        self.clickTargetImg(self.EndOperationImg)

    def MoveToMateriesBin(self):
        self.clickTargetImg(self.BagImg)
        self.clickTargetImg(self.OreBinImg)
        self.clickTargetImg(self.AllSelectImg)
        self.clickTargetImg(self.MoveToImg)
        self.clickTargetImg(self.MaterialsHangarImg)

    def StackAll(self):
        self.clickTargetImg(self.AllSelectImg)
        self.clickTargetImg(self.StackAllImg)

    def MineOre(self):
        # self.clickTargetImg(self.LeaveStationImg)
        self.clickJump(1)
        time.sleep(20)
        while self.checkImgExist(self.ObservceEyeImg) == False:
            print("等待离站")
            time.sleep(5)
        time.sleep(10)
        self.openObeserveTable()
        workingCount = 0 # 通过最大工作轮数来防止机器进入一些异常，因为目前很少需要挖40轮还没挖满
        while not self.isBagFull() and workingCount < 40:
            workingCount += 1
            if not self.checkImgExist(self.OreTagImg):
                self.JumpToOrbPos()
            if self.isWorking():
                time.sleep(60)
            else:
                self.Mining()

    def openObeserveTable(self):
        if not self.checkImgExist(self.PlantaryTagImg):
            self.clickTargetImg(self.ObservceEyeImg)

    def JumpToOrbPos(self):
        print("寻找小行星集群带或者小行星带或者行星群")
        while not self.clickTargetImg(self.PlanetaryClusterImg) and not self.clickTargetImg(self.PlanetaryQuesImg) and not self.clickTargetImg(self.PlanetaryDsImg):
            time.sleep(1)
        print("开始跃迁")
        while not self.clickTargetImg(self.TransitionImg):
            time.sleep(1)
        while not self.checkImgExist(self.OreTagImg):
            print("等待跃迁到矿带")
            time.sleep(3)
        time.sleep(5)
        print("到达矿带，切换标签为为纯矿石")
        self.Click(self.OreTagPos)
        if self.checkImgExist(self.OreTagImg) == False:
            x, y = self.OreTagPos
            self.Click([x, y - 90])

    def Mining(self):
        self.FindOreAndLock()
        self.ComingClose()
        self.StartMing()

    def FindOreAndLock(self):
        for index in range(len(self.oreList)):
            oreImg = self.oreList[index]
            for scrollIndex in range(self.MaxScrollNumber):
                self.Click(self.FirstOrePos) # show oreList
                if self.clickTargetImg(oreImg):
                    print("minging ore " + str(index))
                    self.clickTargetImg(self.LockImg) # lock ore
                    self.ScrollUpNOrePage(scrollIndex)
                    self.scrollIndex = scrollIndex + 1 # for calculate waiting time
                    return True
                self.ScrollDownOrePage()
            self.ScrollUpAllOrePage()
        return False

    def ComingClose(self):
        self.Click(self.LockOrePos)
        self.clickTargetImg(self.SpeedUpImg)
        self.clickTargetImg(self.ComingCloseImg)
        time.sleep(35 + self.scrollIndex * 10)
        self.clickTargetImg(self.SpeedUpImg)


    def StartMing(self):
        print("启动采集器")
        for i in range(self.WapenNum):
            self.clickTargetImg(self.CollectorNotWorkingTagImg)
        time.sleep(3)
        self.clickTargetImg(self.StopShipImg)

    def ScrollDownOrePage(self):
        for i in range(4):
            self.ScrollDown2OreTag()

    def ScrollDown2OreTag(self):
        x, y = self.FirstOrePos
        BGK.scroll_down(self.hWnd, x, y, 9)
        time.sleep(1)

    def ScrollUpAllOrePage(self):
        self.ScrollUpNOrePage(self.MaxScrollNumber)

    def ScrollUpNOrePage(self, pageNumber):
        for i in range(pageNumber):
            self.ScrollUpOrePage()
    def ScrollUpOrePage(self):
        for i in range(4):
            self.ScrollUp2OreTag()

    def ScrollUp2OreTag(self):
        x, y = self.FirstOrePos
        BGK.scroll_up(self.hWnd, x, y, 9)
        time.sleep(1)

    def isWorking(self):
        return self.checkImgExist(self.InWorkingImg)

    def isBagFull(self):
        return self.checkImgExist(self.BagFullImg)

    def clickTargetImg(self, targetImg):
        bImgExist, imgX, imgY = self.GetTargetPos(targetImg)
        if bImgExist:
            self.Click([imgX, imgY])
            return True
        else:
            return False

    def checkImgExist(self, targetImg):
        imgExist, _, _ = self.GetTargetPos(targetImg)
        return imgExist

    def GetTargetPos(self, targetimg, rate=0.94):
        img = BGK.captureWnd(self.hWnd)
        screen = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        result = cv2.matchTemplate(screen, targetimg, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # print(max_val)
        if (max_val > rate):
            x = int(max_loc[0] + targetimg.shape[1] / 2)
            y = int(max_loc[1] + targetimg.shape[0] / 2)
            return True, x, y
        else:
            # print(max_val)
            return False, 0, 0

    def Click(self, pos):
        x, y = pos
        lParam = win32api.MAKELONG(x, y)
        win32gui.PostMessage(self.hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.PostMessage(self.hWnd, win32con.WM_LBUTTONUP, 0, lParam)
        time.sleep(4)

    def loadImage(self , filename):
        imgLoadByCv2 = cv2.imread(filename)
        if imgLoadByCv2 is None:
            self.loadImageSuccess = False
            print("load img error : {}".format(filename))
        return imgLoadByCv2
