import uiautomation as auto
from plyer import notification
from time import sleep

unread_messages = {}  # 未读消息
#获取微信窗口
wechat_win = auto.WindowControl(searchDepth=1, Name="微信", ClassName="WeChatMainWndForPC")

#发送Windows通知
def send_notification(title, message):
    notification.notify(
        title=title, #标题
        message=message, #文本
        app_name = 'WechatMsgToast', #程序名(在windows中似乎不生效)
        app_icon = 'wechat.ico', #图标
        timeout=2,  # 通知持续时间，单位为秒
    )

#处理消息是否未读(是否发送过Toast通知)
def check_messages(new_message):

    # 昵称
    name = new_message.ButtonControl(foundIndex=1).Name

    #如果昵称不在unread_messages{}中
    if name not in unread_messages:

        #将控件名称中的昵称去掉保留‘n条新消息’
        count_msg = new_message.Name.replace(name,"")

        #将昵称存为键，‘n条新消息’存为键值
        unread_messages[name] = count_msg

        #返回
        return new_message

    #如果昵称在unread_messages{}中
    else:
        #将控件名称中的昵称去掉保留‘n条新消息’
        count_msg = new_message.Name.replace(name,"")

        #判断现在的‘n条新消息’与unread_messages{}中存储的‘n条新消息’是否一致
        if unread_messages[name] != count_msg:
            #将键值改为最新的‘n条新消息’
            unread_messages[name] = count_msg
            #返回
            return new_message
        else:
            return False




if __name__ == "__main__":
    #检测微信窗口
    if wechat_win.Exists(0,0):
        try:
            #开始提示
            send_notification('开始运行', '等待消息中....')
            while True:
                # 获取消息列表
                List_messages = wechat_win.ListControl(Name="会话").GetChildren()

                # 获取消息列表
                for list_message in List_messages:
                    # 遍历未读消息列表
                    if '条新消息' in list_message.Name:
                        #检查消息是否通知
                        new_message = check_messages(list_message)

                        if new_message:
                            name = new_message.ButtonControl(foundIndex=1).Name #昵称
                            msg = new_message.TextControl(foundIndex=3).Name    #消息文本
                            send_notification(name, msg) #发送通知
                            sleep(2)  #每2秒检测
                            #打印测试
                            print(new_message.Name + '\n' + name + ':\t' +msg + '\n_________________')


        #异常处理
        except KeyboardInterrupt:
            print("程序退出")

        except Exception as e:
            print(f"程序执行出现了问题: {str(e)}")
    #未检测到微信窗口
    else:
        print("未检测到微信窗口")
        send_notification('未检测到微信窗口', '请打开微信重试')