import miner

if __name__ == '__main__':
    # minerObj = miner.Miner("逍遥模拟器",WapenNum = 3 , test = False)
    setting = {
        "windowName" : "逍遥模拟器",
        "WapenNUm" : 3,
    }
    minerObj = miner.Miner(
        windowName="逍遥模拟器",
        WapenNum = 3 ,
        MaxScrollNumber=7,
        test = True,
    )
    minerObj.Run()