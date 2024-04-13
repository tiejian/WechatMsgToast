import uiautomation as auto
from plyer import notification
from time import sleep

unread_messages = {}  # 未读消息
#获取微信窗口
wechat_win = auto.WindowControl(searchDepth=1, Name="微信", ClassName="WeChatMainWndForPC")

#发送Windows通知
def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name = 'WechatMsgToast',
        app_icon = 'wechat.ico',
        timeout=2,  # 通知持续时间，单位为秒
    )

#检查未读消息
def check_unread_messages():

    #获取消息列表
    List_messages = wechat_win.ListControl(Name = "会话")

    #获取未读消息列表
    for list_message in List_messages.GetChildren():
        if('条新消息' in list_message.Name):
            #返回最新未读消息
            return list_message
        return False

#处理消息是否未读
def process_messages(new_message):

    # 昵称
    name = new_message.ButtonControl(foundIndex=1).Name

    if name not in unread_messages:

        #‘n条新消息’
        count_msg = new_message.Name.replace(name,"")

        unread_messages[name] = count_msg

        return new_message
    else:

        #‘n条新消息’
        count_msg = new_message.Name.replace(name,"")

        if unread_messages[name] != count_msg:


            unread_messages[name] = count_msg
            return new_message
        else:
            return False




if __name__ == "__main__":
    if not wechat_win.Exists(0,0):
        print("未检测到微信窗口")
        send_notification('未检测到微信窗口', '请打开微信重试')
    else:
        try:
            send_notification('开始运行', '等待消息中....')
            while True:
                new_message = check_unread_messages()
                if new_message:
                    if process_messages(new_message):
                        name = new_message.ButtonControl(foundIndex=1).Name
                        msg = new_message.TextControl(foundIndex=3).Name
                        send_notification(name, msg)
                    sleep(2)  # 每n秒检测一次UI组件
        except KeyboardInterrupt:
            print("程序退出")
            send_notification('结束','程序退出')
        except Exception as e:
            send_notification('错误',str(e))
            print(f"程序执行出现了问题: {str(e)}")
