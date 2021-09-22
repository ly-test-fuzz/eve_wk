import os
import time

import win32gui
import win32api
import win32con
import cv2
import BGK


class Miner:
    def __init__(self, windowName, test=False , WapenNum = 3 , MaxScrollNumber = 7):
        self.windowName = windowName
        self.hWnd = win32gui.FindWindow('Qt5QWindowIcon', '逍遥模拟器')
        self.loadPictureAndGenPosList()
        self.test = test
        self.WapenNum = WapenNum
        self.MaxScrollNumber = MaxScrollNumber

    def loadPictureAndGenPosList(self):
        # gen Jump
        self.JumpTagImg = cv2.imread("Tags\\JumpTag.PNG")
        self.ConfirmTagImg = cv2.imread("Tags\\ConfirmTag.PNG")
        self.LeaveStationImg = cv2.imread("Tags\\LeaveStation.PNG")
        self.JumpPoses = []
        for i in range(2):
            self.JumpPoses.append([350, 437 + 120 * i])
        # gen packBag
        ## move to MaterialsHangar
        self.BagImg = cv2.imread("Tags\\Bag.PNG")
        self.OreBinImg = cv2.imread("Tags\\oreBin.PNG")
        self.AllSelectImg = cv2.imread("Tags\\AllSelect.PNG")
        self.MaterialsHangarImg = cv2.imread("Tags\\MaterialsHangar.PNG")
        self.MoveToImg = cv2.imread("Tags\\MoveTo.PNG")
        ## Stack All
        self.StackAllImg = cv2.imread("Tags\\StackAll.PNG")
        self.EndOperationImg = cv2.imread("Tags\\EndOperation.PNG")
        # gen MineOre
        self.ObservceEyeImg = cv2.imread("Tags\\ObserveEye.PNG")
        ## jump to planetary
        self.PlantaryTagImg = cv2.imread("Tags\\PlantaryTag.PNG")
        self.PlanetaryClusterImg = cv2.imread("Tags\\PlanetaryCluster.PNG")
        self.PlanetaryQuesImg = cv2.imread("Tags\\PlanetaryQues.PNG")
        self.PlanetaryDsImg = cv2.imread("Tags\\PlanetaryDs.PNG")
        self.TransitionImg = cv2.imread("Tags\\Transition.PNG")
        self.OreTagImg = cv2.imread("Tags\\OreTag.PNG")
        self.OreTagPos = [1600, 230]
        ## Mining
        self.FirstOrePos = [1400, 120]
        self.LockImg = cv2.imread("Tags\\Lock.PNG")
        self.InWorkingImg = cv2.imread("Tags\\InWorking.PNG")
        self.CollerterImg = cv2.imread("Tags\\Collecter.PNG")
        self.CollectorNotWorkingTagImg = cv2.imread("Tags\\CollectorNotWorkingTag.PNG")
        self.ComingCloseImg = cv2.imread("Tags\\ComingClose.png")
        self.AroundImg = cv2.imread("Tags\\Around.png")
        self.StopShipImg = cv2.imread("Tags\\StopShip.PNG")
        self.LockOrePos = [1200 , 80]
        self.BagFullImg = cv2.imread("Tags\\BagFull.PNG")
        # gen OreImg
        self.oreList = []
        self.oreImgPathList = os.listdir("Tags\\oreList\\")
        for oreImgPath in self.oreImgPathList:
            self.oreList.append(cv2.imread("Tags\\oreList\\" + oreImgPath))
        print("load {} ore".format(len(self.oreList)))

    def Run(self):
        if self.test == True:
            self.testRun()
            return
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
        self.FindOreAndLock()
        # print(self.isWorking())
        # if not self.isWorking():
            # self.clickTargetImg(self.CollectorNotWorkingTagImg)
            # self.clickTargetImg(self.CollectorNotWorkingTagImg)
        #if not self.isWorking():
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
        self.clickTargetImg(self.LeaveStationImg)
        while self.checkImgExist(self.ObservceEyeImg) == False:
            print("等待离站")
            time.sleep(5)
        time.sleep(10)
        self.openObeserveTable()
        workingCount = 0
        while not self.isBagFull() and workingCount < 40:
            workingCount+=1
            if not self.checkImgExist(self.OreTagImg):
                self.JumpToOrbPos()
            if not self.isWorking():
                self.Mining()
                continue
            time.sleep(60)
    
    def openObeserveTable(self):
        if not self.checkImgExist(self.PlantaryTagImg):
            self.clickTargetImg(self.ObservceEyeImg)
        

    def JumpToOrbPos(self):
        print("找到小行星集群带或者小行星带或者行星群")
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
            x , y = self.OreTagPos
            self.Click([x , y - 90])

    def Mining(self):
        self.FindOreAndLock()
        self.ComingClose()
        self.StartMing()

    def FindOreAndLock(self):
        for index in range(len(self.oreList)):
            oreImg = self.oreList[index]
            for i in range(self.MaxScrollNumber):
                self.Click(self.FirstOrePos) # show oreList
                if self.clickTargetImg(oreImg):
                    print("minging ore " + str(index))
                    self.clickTargetImg(self.LockImg) # lock ore
                    return True
                self.ScrollDownOrePage()
            self.ScrollAllOrePage()
        return False

    def ComingClose(self):
        self.Click(self.LockOrePos)
        self.clickTargetImg(self.ComingCloseImg)
        time.sleep(70)
        
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
        x , y = self.FirstOrePos
        BGK.scroll_down(self.hWnd , x , y , 9)
        time.sleep(1)

    def ScrollAllOrePage(self):
        for i in range(self.MaxScrollNumber):
            self.ScrollUpOrePage()

    def ScrollUpOrePage(self):
        for i in range(4):
            self.ScrollUp2OreTag()

    def ScrollUp2OreTag(self):
        x , y = self.FirstOrePos
        BGK.scroll_up(self.hWnd , x , y , 9)
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
