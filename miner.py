import os
import time
import cv2
import BGK

JumpOrePosException = Exception("跳跃矿带超时，出现异常")
ObserverSettingException = Exception("没有找到筛选条目 - 矿带或者矿石 ， 请看筛选条件是否设置完毕")
OpenBagException = Exception("点击背包找不到全选按钮，推荐重新更换背包图标")
DestroyedException = Exception("发现太空舱，可能被击毁了，开始换船")
NotFoundOreShipException = Exception("没有找到可以换的冲锋2 , 退出")
EndOpeartionImgNotFoundException = Exception("退出按钮没有找到")
CollectorNotFoundException = Exception("没有找到采矿激光器图标(无论工作与否) , 可能需要更换对应的图标")

class Miner:
    def __init__(self, windowName, test=False, WapenNum=3, MaxScrollNumber=7, ActionSleepNumber=3 , JumpSleepTime = 20):
        self.WindowActor = BGK.WindowActor(windowName= windowName , ActionSleepNumber= ActionSleepNumber)
        self.loadPictureAndGenPosList()
        self.test = test
        self.WapenNum = WapenNum
        self.MaxScrollNumber = MaxScrollNumber
        self.ActionSleepNumber = ActionSleepNumber
        self.JumpSleepTime = JumpSleepTime

    def loadPictureAndGenPosList(self):
        self.loadImageSuccess = True
        # change ship
        self.ShipHangarImg = self.loadImage("Tags\\ShipHangar.PNG")
        self.ActiveedShipHangarImg = self.loadImage("Tags\\ActiveShipHangar.PNG")
        self.OreShip2Img = self.loadImage("Tags\\OreShip2.PNG")
        self.ActiveShipImg = self.loadImage("Tags\\ActiveShip.PNG")

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
        self.SpaceBinImg = self.loadImage("Tags\\SpaceBin.PNG")
        self.AllSelectImg = self.loadImage("Tags\\AllSelect.PNG")
        self.MaterialsHangarImg = self.loadImage("Tags\\MaterialsHangar.PNG")
        self.MoveToImg = self.loadImage("Tags\\MoveTo.PNG")
        ## Stack All
        self.StackAllImg = self.loadImage("Tags\\StackAll.PNG")
        self.EndOperationImg = self.loadImage("Tags\\EndOperation.PNG")
        # gen MineOre
        self.ObservceEyeImg = self.loadImage("Tags\\ObserveEye.PNG")
        ## jump to planetary
        self.PlantaryObserveTagImg = self.loadImage("Tags\\PlantaryObserveTag.PNG")
        self.PlantaryObserveTagPos = [1370,200]
        self.OreObserverTagImg = self.loadImage("Tags\\OreObserveTag.PNG")
        self.OreObserverTagPos = [1370 , 290]

        self.PlanetaryClusterImg = self.loadImage("Tags\\PlanetaryCluster.PNG")
        self.PlanetaryQuesImg = self.loadImage("Tags\\PlanetaryQues.PNG")
        self.PlanetaryDsImg = self.loadImage("Tags\\PlanetaryDs.PNG")
        self.TransitionImg = self.loadImage("Tags\\Transition.PNG")
        self.OreTagImg = self.loadImage("Tags\\OreTag.PNG")
        self.OreTagPos = [1600, 150]
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
        if self.test:
            self.testRun()
            return
        if not self.loadImageSuccess:
            print("图片加载失败 , 程序退出")
            return False
        while True:
            try:
                self.BackStation()
                self.MineOre()
            except Exception as e:
                print("get exception : {}".format(e))
                if e == DestroyedException:
                    self.changeShip()
                else:
                    time.sleep(10)

    def changeShip(self):
        if not self.WindowActor.checkImgExist(self.ActiveedShipHangarImg):
            self.WindowActor.clickTargetImg(self.ShipHangarImg)
        if not self.WindowActor.checkImgExist(self.OreShip2Img):
            raise NotFoundOreShipException

        self.WindowActor.clickTargetImg(self.OreShip2Img)
        self.WindowActor.clickTargetImg(self.ActiveShipImg)
        time.sleep(6) # 等待切换舰船激活成功

        self.clickEndOpeartion()

    def clickEndOpeartion(self):
        count = 0
        while not self.WindowActor.clickTargetImg(self.EndOperationImg):
            time.sleep(1)
            count += 1
            if count == 8:
                raise EndOpeartionImgNotFoundException

    def testRun(self):
        # self.BackStation()
        # self.PackBag()
        # self.MineOre()
        # self.Mining()
        # self.FindOreAndLock()
        # print(self.isWorking())
        # if not self.isWorking():
        # self.WindowActor.clickTargetImg(self.CollectorNotWorkingTagImg)
        # self.WindowActor.clickTargetImg(self.CollectorNotWorkingTagImg)
        # if not self.isWorking():
        #    self.FindOreAndLock()
        print(str(Exception("dsdsds")))

    def BackStation(self):
        print("开始回站")
        self.clickJump(0)
        while not self.checkInStation():
            print("回站 等待")
            time.sleep(10)
        print("已经回到空间站")
        time.sleep(3)
        self.PackBag()

    def clickJump(self, jumpIndex):
        while not self.WindowActor.clickTargetImg(self.JumpTagImg):
            time.sleep(1)
        self.WindowActor.Click(self.JumpPoses[jumpIndex])
        self.WindowActor.clickTargetImg(self.ConfirmTagImg)

    def checkInStation(self):
        return self.WindowActor.checkImgExist(self.LeaveStationImg)

    def PackBag(self):
        print("开始整理背包")
        self.MoveToMateriesBin()
        print("开始堆叠所有")
        self.StackAll()
        self.clickEndOpeartion()

    def MoveToMateriesBin(self):
        self.WindowActor.clickTargetImg(self.BagImg)
        if not self.WindowActor.checkImgExist(self.AllSelectImg):
            raise OpenBagException
        if self.WindowActor.checkImgExist(self.SpaceBinImg):
            raise DestroyedException
        self.WindowActor.clickTargetImg(self.OreBinImg)
        self.WindowActor.clickTargetImg(self.AllSelectImg)
        self.WindowActor.clickTargetImg(self.MoveToImg)
        self.WindowActor.clickTargetImg(self.MaterialsHangarImg)

    def StackAll(self):
        self.WindowActor.clickTargetImg(self.AllSelectImg)
        self.WindowActor.clickTargetImg(self.StackAllImg)

    def MineOre(self):
        # self.WindowActor.clickTargetImg(self.LeaveStationImg)
        self.clickJump(1)
        time.sleep(self.JumpSleepTime)

        self.openObeserveTable()
        workingCount = 0 # 通过最大工作轮数来防止机器进入一些异常，因为目前很少需要挖40轮还没挖满
        while not self.isBagFull() and workingCount < 30:
            self.HasCollector()
            workingCount += 1
            if self.isWorking():
                time.sleep(60)
            else:
                if not self.WindowActor.checkImgExist(self.OreTagImg):
                    self.JumpToOrbPos()
                self.Mining()

    def openObeserveTable(self):
        while not self.WindowActor.checkImgExist(self.ObservceEyeImg):
            print("等待离站")
            time.sleep(5)
        time.sleep(10)
        _ , x, _ = self.WindowActor.GetTargetPos(self.ObservceEyeImg)
        if x > self.FirstOrePos[0]: ## 如果眼睛的横坐标 在 第一个矿石坐标的右边，
            self.WindowActor.clickTargetImg(self.ObservceEyeImg)
        time.sleep(6) # 等待总览图标缩回去

    def JumpToOrbPos(self):
        self.selectPlantaryObserve()
        print("寻找小行星集群带或者小行星带或者行星群")
        sleepCount = 0
        while not self.WindowActor.clickTargetImg(self.PlanetaryClusterImg) and not self.WindowActor.clickTargetImg(self.PlanetaryQuesImg) and not self.WindowActor.clickTargetImg(self.PlanetaryDsImg):
            time.sleep(1)
            sleepCount += 1
            if sleepCount == 40:
                raise JumpOrePosException
        time.sleep(self.ActionSleepNumber * 2)
        print("开始跃迁")
        while not self.WindowActor.clickTargetImg(self.TransitionImg):
            time.sleep(1)
        self.selectOreObserve()
        while not self.WindowActor.checkImgExist(self.OreTagImg):
            print("等待跃迁到矿带")
            time.sleep(3)
        self.WindowActor.Click(self.OreTagPos)
        time.sleep(5)

        self.selectOreObserve()
        return True

    def selectPlantaryObserve(self):
        print("切换标签为矿带")
        if not self.WindowActor.checkImgExist(self.PlantaryObserveTagImg) and not self.WindowActor.checkImgExist(self.OreObserverTagImg):
            raise ObserverSettingException
        if not self.WindowActor.checkImgExist(self.PlantaryObserveTagImg): # 如果没有找到矿带筛选
            self.WindowActor.clickTargetImg(self.OreObserverTagImg) # 点击筛选条目
            self.WindowActor.Click(self.PlantaryObserveTagPos) # 点击 矿带筛选条目

    def selectOreObserve(self):
        print("到达矿带，切换标签为为纯矿石")
        if not self.WindowActor.checkImgExist(self.PlantaryObserveTagImg) and not self.WindowActor.checkImgExist(self.OreObserverTagImg):
            raise ObserverSettingException
        if not self.WindowActor.checkImgExist(self.OreObserverTagImg): # 如果没有找到矿带筛选
            self.WindowActor.clickTargetImg(self.PlantaryObserveTagImg) # 点击筛选条目
            self.WindowActor.Click(self.OreObserverTagPos) # 点击 矿带筛选条目

    def Mining(self):
        if self.FindOreAndLock():
            self.ComingClose()
            self.StartMing()

    def FindOreAndLock(self):
        for index in range(len(self.oreList)):
            oreImg = self.oreList[index]
            for scrollIndex in range(self.MaxScrollNumber):
                self.WindowActor.Click(self.FirstOrePos) # show oreList
                if self.WindowActor.clickTargetImg(oreImg):
                    print("minging ore " + str(index))
                    self.WindowActor.clickTargetImg(self.LockImg) # lock ore
                    self.ScrollUpNOrePage(scrollIndex)
                    self.scrollIndex = scrollIndex + 1 # for calculate waiting time
                    return True
                self.ScrollDownOrePage()
            self.ScrollUpAllOrePage()
        return False

    def ComingClose(self):
        self.WindowActor.Click(self.LockOrePos)
        self.WindowActor.clickTargetImg(self.SpeedUpImg)
        self.WindowActor.clickTargetImg(self.ComingCloseImg)
        time.sleep(35 + self.scrollIndex * 10)
        self.WindowActor.clickTargetImg(self.SpeedUpImg)

    def StartMing(self):
        print("启动采集器")
        for i in range(self.WapenNum):
            self.WindowActor.clickTargetImg(self.CollectorNotWorkingTagImg)
        time.sleep(3)
        self.WindowActor.clickTargetImg(self.StopShipImg)

    def ScrollDownOrePage(self):
        x , y = self.FirstOrePos
        self.WindowActor.ScrollDownOrePage(x, y)

    def ScrollUpAllOrePage(self):
        self.ScrollUpNOrePage(self.MaxScrollNumber)

    def ScrollUpNOrePage(self, pageNumber):
        x, y = self.FirstOrePos
        self.WindowActor.ScrollUpOrePage(x, y)

    def HasCollector(self):
        if not self.WindowActor.checkImgExist(self.InWorkingImg) and not self.WindowActor.checkImgExist(self.CollectorNotWorkingTagImg):
            raise CollectorNotFoundException
        return True

    def isWorking(self):
        return self.WindowActor.checkImgExist(self.InWorkingImg)

    def isBagFull(self):
        return self.WindowActor.checkImgExist(self.BagFullImg)

    def loadImage(self , filename):
        imgLoadByCv2 = cv2.imread(filename)
        if imgLoadByCv2 is None:
            self.loadImageSuccess = False
            print("load img error : {}".format(filename))
        return imgLoadByCv2
