# ADB-Auto-Daily

一个通过ADB的方式来控制安卓手机或安卓模拟器来完成自动化任务的脚本

## 使用方法
1. 请配置好adb的环境变量，或者修改config.json中的adb路径
2. 如果需要使用设备自动解锁的任务，需要在项目根目录下新建.env文件，设置UNLOCK_PASSWORD环境变量为你的设备解锁密码。如UNLOCK_PASSWORD=114514
3. 在adbAutoDaily.py中添加任务