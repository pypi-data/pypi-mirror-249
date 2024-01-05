import re
from datetime import datetime
import pandas as pd
import pythoncom
import pyttsx3
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL
"""
lyyapp是具有独立功能的实用程序，而lyytools是服务于其它的。
如果仔细分析，界线也没那么清楚，考虑到放一起肯定不够，所以先计划2类。

"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def email_notice(username, receiver_email, subject="邮件主题", message="邮件内容"):

    # 邮件内容
    sender_email = username + '@189.cn'  # 发件人邮箱地址
    # 收件人邮箱地址
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # 添加邮件内容
    msg.attach(MIMEText(message, 'plain'))

    # 邮件服务器的配置
    smtp_server = 'smtp.189.cn'  # 邮件服务器的地址
    smtp_port = 587  # 邮件服务器的端口
    password = 'pA*9cU@7C@8xQ*8g'  # 邮箱密码

    # 发送邮件
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败：{e}")
    finally:
        server.quit()


def format_ocr_text(text):
    symbols = ['1、', '2、', '3、', '4、', '5、', '6、', '7、', '8、', '9、', '10、', '11、', '12、', '一、', '二、', '三、']
    pattern = '|'.join(re.escape(symbol) for symbol in symbols)
    paragraphs = re.split('(' + pattern + ')', text)
    formatted_text = ''
    indent = False
    for i, paragraph in enumerate(paragraphs):
        if paragraph.strip() != '':
            formatted_paragraph = paragraph.strip()
            if formatted_paragraph.startswith(('一、', '二、', '三、')):
                if formatted_text and formatted_text[-1] != '\n':
                    formatted_text += '\n'
                formatted_text += formatted_paragraph + '\n'
                indent = False
            elif formatted_paragraph.startswith(('1、', '2、', '3、', '4、', '5、', '6、', '7、', '8、', '9、', '10、', '11、', '12、')):
                if formatted_text and formatted_text[-1] != '\n':
                    formatted_text += '\n'
                formatted_text += '  ' + formatted_paragraph + '\n'
                indent = True
            else:
                if not indent:
                    formatted_paragraph = '  ' + formatted_paragraph
                    indent = True
                formatted_text += formatted_paragraph + '\n'
    return formatted_text


def 提取url(full_text, debug=False):
    pattern = re.compile(r'http[s]?://[\w-]+(?:\.[\w-]+)+[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-]')

    #pattern = re.compile(r'http://[^s]*\.pdf')
    result = re.findall(pattern, full_text)
    url = result[0]

    # 去除前后的标点符号
    url = url.strip('\'"<>')
    if debug: print("提取url结果=" + result[0])
    return result[0]


def extract_info_from_df(df):
    today_date = datetime.now().strftime("%Y-%m-%d")
    msg_dic = {}
    dict_list = []
    for index, row in df.iterrows():
        row_dict = {}
        for column in df.columns:
            row_dict[column] = row[column]
            row_dict['time'] = pd.to_datetime(row['time'], unit='ms').strftime('%Y-%m-%d %H:%M:%S').replace(today_date + " ", "")  #如果是今天就不需要显示日期，所以把年，同后面的空格替换成短时间。
        dict_list.append(row_dict)
    return dict_list


def lyyspeak(text="", rate=150, volume=0.8):
    pythoncom.CoInitialize()
    # 初始化语音引擎
    engine = pyttsx3.init()
    # 设置语速（可选）
    engine.setProperty('rate', rate)  # 语速范围在0-200之间，默认为200
    # 设置音量（可选）
    engine.setProperty('volume', volume)  # 音量范围在0.0-1.0之间，默认为1.0
    # 等待语音引擎初始化完成
    engine.startLoop(False)
    engine.say(text)
    # 等待语音播放完毕
    engine.iterate()


def set_volume(vol):
    pythoncom.CoInitialize()
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        最初音量 = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(float(vol), None)
        print(f"最初音量：{最初音量}， 当前音量：{volume.GetMasterVolumeLevelScalar()}")
    finally:
        pythoncom.CoUninitialize()


def set_volume2(vol):
    # 替换下面的音量值为您想设置的音量（0.0 到 1.0 之间的浮点数）
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        # 获取最初的音量
        initial_volume = volume.GetMasterVolume()
        # 设置音量
        volume.SetMasterVolume(vol, None)
        # 打印音量信息
        print(f"最初音量：{initial_volume}，当前音量：{volume.GetMasterVolume()}")


def adjust_volume_based_on_time(night_vol=0.1, daytime_vol=0.4):
    # 获取当前的时间
    now = datetime.now()
    # 判断时间是否早于8点30或者晚于9点
    if now.hour < 8 or (now.hour == 8 and now.minute < 30) or now.hour > 21:
        # 调整音量为10%
        set_volume2(night_vol)
    else:
        set_volume2(daytime_vol)


from ctypes import windll


def 关闭显示器():
    HWND_BROADCAST = 0xffff
    WM_SYSCOMMAND = 0x0112
    SC_MONITORPOWER = 0xF170
    MonitorPowerOff = 2
    SW_SHOW = 5
    windll.user32.PostMessageW(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, MonitorPowerOff)
    shell32 = windll.LoadLibrary("shell32.dll")
    shell32.ShellExecuteW(None, 'open', 'rundll32.exe', 'USER32', '', SW_SHOW)


def lnk2exe(fullpath, debug=False):
    #用来在服务里面获取快捷方式目标
    import os, win32com
    from lyylog import log
    debug = True
    lnk = fullpath
    flname = os.path.basename(fullpath)
    if debug:
        log("find link file=" + lnk)
    pythoncom.CoInitialize()
    if debug:
        log("# 获取WScript.Shell COM对象")
    shell = win32com.client.Dispatch("WScript.Shell")
    if debug:
        log("# 获取快捷方式")
    shortcut = shell.CreateShortcut(fullpath)
    if debug:
        log("# 获取快捷方式指向的目标 ")
    target = shortcut.Targetpath
    if debug:
        log("TARGET=" + target)
    return target


if __name__ == '__main__':
    from datetime import datetime
    import sys

    if len(sys.argv) == 1:
        adjust_volume_based_on_time(0.1, 0.4)

    elif len(sys.argv) == 2:
        vol = sys.argv[1]
        # 检查输入的音量是否是一个介于0和1之间的浮点数
        if not 0 <= float(vol) <= 1:
            print("错误：音量必须是一个介于0和1之间的浮点数。")
            sys.exit()
        else:
            set_volume2(vol)
    elif len(sys.argv) == 3:
        adjust_volume_based_on_time(sys.argv[1], sys.argv[2])
        # 调整音量
    else:
        print("错误：参数数量不正确。")
        print("用法：adjust_volume [当前需要调节的音量数值]")
        print("用法：adjust_volume [夜间音量] [白天音量]")
        print("例如：adjust_volume 0.1 0.4")
        sys.exit()
