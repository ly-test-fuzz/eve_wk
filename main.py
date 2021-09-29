import miner

if __name__ == '__main__':
    minerObj = miner.Miner(
        windowName="逍遥模拟器",  # 窗口名字，
        MaxScrollNumber=5,  # 最大滚屏翻页页数
        ActionSleepNumber=3,  # 每一个点击操作的睡眠时间
        JumpSleepTime=20,  # 跃迁到矿区的时间
        ShipType="c2",  # 可以选择的舰船类型 c2 - 冲2 | c3 - 冲3
        # test=True,  # 是否是测试模块
    )
    minerObj.Run()
