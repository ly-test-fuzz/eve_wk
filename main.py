import miner

if __name__ == '__main__':
    minerObj = miner.Miner(
        windowName="逍遥模拟器",  # 窗口名字，
        WapenNum=3,  # 采矿激光器数量， 可以多于现有数量，不要少
        MaxScrollNumber=7,  # 最大滚屏翻页页数
        ActionSleepNumber=4,  # 每一个点击操作的睡眠时间
        JumpSleepTime = 20, # 跃迁到矿区的时间
        # test=True,  # 是否是测试模块
    )
    minerObj.Run()
