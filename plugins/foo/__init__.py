from pathlib import Path
from nonebot.adapters import Message
from nonebot.rule import to_me
from typing import Union
from nonebot.adapters.onebot.v11 import PokeNotifyEvent
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot import on_notice
from nonebot.params import EventPlainText
from nonebot import on_keyword
from nonebot import on_message
from nonebot.plugin.on import on_keyword, on_message
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
)
import json
import random
import subprocess
import sys
import asyncio
import time
#from yuanchu.adapters.qq_aotumouse.adapter import QQAutoMouseAdapter as QQAutoMouseAdapter
#from yuanchu.adapters.qq_aotumouse.adapter import QQAutoMouseBot as QQAutoMouseBot
#from yuanchu.adapters.qq_aotumouse.adapter import QQAutoMouseEvent as QQAutoMouseEvent
#from yuanchu.adapters.qq_aotumouse.adapter import QQAutoMouseMessage as QQAutoMouseMessage
#from yuanchu.adapters.qq_aotumouse.adapter import QQAutoMouseMessageSegment as QQAutoMouseMessageSegment
#from yuanchu.adapters.qq_aotumouse.adapter import QQWindowController as QQWindowController

#from .qq_aotumouse import QQAutoMouseAdapter as QQAutoMouseAdapter
#from .qq_aotumouse import QQAutoMouseBot as QQAutoMouseBot
#from .qq_aotumouse import QQAutoMouseEvent as QQAutoMouseEvent
#from .qq_aotumouse import QQAutoMouseMessage as QQAutoMouseMessage
#from .qq_aotumouse import QQAutoMouseMessageSegment as QQAutoMouseMessageSegment
#from .qq_aotumouse import QQWindowController as QQWindowController

# 冷却时间配置（单位：秒）
COOLDOWN_MIN = 0.53  # 500毫秒
COOLDOWN_MAX = 1.21  # 2秒

# 全局状态记录
last_send_time = 0  # 最后发送时间戳
cooldown_lock = asyncio.Lock()  # 异步锁防止并发冲突

graph_path = Path(r"D:\QQbot\QQbot3\yuanchu\yuanchu\plugins\latency_graph.png")
sever=[
        "服务器状态",
        "mc服务器",
        "服务器信息",
        "sever message",
        "服务器在线人数",
        "服务器延迟",
        "服务器地址"
    ]

#打开关键词词库
path='D:\QQbot\QQbot3\yuanchu\yuanchu\plugins\device.json'
with open(path,'r', encoding='utf-8') as f:
    dic=json.load(f)#json文件转换为字典

def _checker(event:GroupMessageEvent) -> bool:
    return not(event.to_me)
def get_message_text(data: Union[str, Message]) -> str:
    # 获取on_message的纯文本消息
    result = ""
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "text":
                result += msg["data"]["text"].strip() + " "
        return result.strip()
    else:
        for seg in data["text"]:
            result += seg.data["text"] + " "
    return result
#引用关键词组，但是艾特。
list1=list(dic.get("Subdict1").keys())#字典key值转换为列表，列：["再见","你好"]
musiclist=list(dic.get("musiclist").keys())
#用append会莫名报错
list2=list1+list(dic.get("Extralist").keys())
command1 = on_message(rule=to_me(), block=True,priority=1)
@command1.handle()
async def Command1(event: MessageEvent):
    num1=0
    msg = get_message_text(event.json())
    
    seconds=random.randint(148,760)/1000
    time.sleep(seconds)
    if not msg in sever + [
        "尖叫",
        "嚎叫",
        "恶臭",
        "叫喊",
        "啊啊啊啊啊",
        "野兽先辈",
        "114514"
    ]:
        if (not msg) or msg in [
            "你好啊",
            "你好",
            "在吗",
            "在不在",
            "您好",
            "您好啊",
            "你好",              
            "在",
            "出来"
        ]:
            await command1.send(random.choice(dic.get("Subdict1").get("你好")))
            num1=3
        else:
            for str1 in list2:
                bool=msg.count(str1)
                if bool:
                    num1+=1
                    if num1==1:
                        value1=dic.get("Subdict1").get(str1)#命令转换为对应的消息列
                        if not value1:
                            value1=dic.get("Extralist").get(str1)
                    elif num1==2:
                        value1x2=dic.get("Subdict1").get(str1)#命令转换为对应的消息列
                        if not value1x2:
                            value1x2=dic.get("Extralist").get(str1)
            text=random.choice(value1)
            if num1==2:
                text2=random.choice(value1x2)
            else:
                text2=""

            if text or text2 :
                if num1==1:
                    await command1.send(text) #消息列表中随机输出一条消息
                    num1=3
                elif text and text2 and num1==2:
                    await command1.send(text+","+text2) #消息列表中随机输出一条消息
                    num1=3
                elif text or text and num1==2:
                    await command1.send(text+text2)
                    num1=3
                elif num1==0:
                    await command1.send(random.choice(dic.get("Subdict1").get("command")))
                    
#引用关键词组。
command2 = on_keyword(list1,rule=_checker,priority=1)
@command2.handle()
async def Command2(foo: str = EventPlainText()):
    
    seconds=random.randint(679,3689)/1000
    time.sleep(seconds)

    num1=0
    if len(foo)<10:
        for str1 in list1:
            bool=foo.count(str1)
            if bool:
                num1+=1
                if num1==1:
                    value1=dic.get("Subdict1").get(str1)#命令转换为对应的消息列
                elif num1==2:
                    value1x2=dic.get("Subdict1").get(str1)#命令转换为对应的消息列
        text=random.choice(value1)
        if num1==2:
            text2=random.choice(value1x2)
        else:
            text2=""

        if text or text2 :
            if num1==1:
                await command1.send(text) #消息列表中随机输出一条消息
            elif text and text2 and num1==2:
                await command1.send(text+","+text2) #消息列表中随机输出一条消息
            elif text or text and num1==2:
                await command1.send(text+text2)
                
#戳一戳回复
list3=list(dic.get("Subdict2"))#字典key值转换为列表，列：["再见","你好"]
def _check(event:PokeNotifyEvent):
    return event.target_id==event.self_id
poke=on_notice(rule=_check)
@poke.handle()
async def _(event: PokeNotifyEvent):

    seconds=random.randint(283,978)/1000
    time.sleep(seconds)

    await poke.send(random.choice(list3))
#表情包回复
command3 = on_message(priority=1)
@command3.handle()
async def Command3(foo: str = EventPlainText()):

    seconds=random.randint(463,1821)/1000
    time.sleep(seconds)

    if random.randint(0,99)==0:
        p = Path(r'D:\QQbot\QQbot3\yuanchu\yuanchu\plugins\FileRecv\MobileFile')
        p1=p/(str(random.randint(0,18))+'.jpg')
        await command3.send(MessageSegment.image(p1))
#语音播放
music = on_message(block=True,priority=1)
@music.handle()
async def Music(event: MessageEvent):
    msg = get_message_text(event.json())

    seconds=random.randint(62,438)/1000
    time.sleep(seconds)

    if msg in [
        "尖叫",
        "嚎叫",
        "恶臭",
        "叫喊",
        "啊啊啊啊啊",
        "野兽先辈",
        "114514"         
    ]:
        p = Path(r'D:\QQbot\QQbot3\yuanchu\yuanchu\plugins\FileRecv\QQ语音')
        p1=p/(str(random.randint(0,1))+'.mp3')
        await command3.send(MessageSegment.record(p1))
#音乐分享
music1 = on_keyword(musiclist,priority=1)
@music1.handle()
async def Music1(foo: str = EventPlainText()):
    if len(foo)<10:
        for str1 in musiclist:
            bool=foo.count(str1)
            if bool:
                num=dic.get("musiclist").get(str1)
                await command3.send(MessageSegment.music(type_=163,id_=num))

# 获取当前插件所在目录（假设此代码文件在 D:\QQbot 目录下）
plugin_dir = Path(__file__).parent

handle_mc_status = on_message(rule=to_me(), block=True,priority=1)
@handle_mc_status.handle()
async def Handle_mc_status(event: MessageEvent):
    msg = get_message_text(event.json())
    if msg in sever:
        global last_send_time

        # 获取当前时间
        current_time = time.time()
        
        async with cooldown_lock:  # 加锁保证原子操作
            # 计算剩余冷却时间
            remaining = last_send_time - current_time
            if remaining > 0:
                # 如果仍在最大冷却期内，直接拦截
                await handle_mc_status.finish(f"冷却中，剩余 {remaining:.1f} 秒")
                return
            else :
                # 使用系统Python解释器执行脚本
                await handle_mc_status.send("查询中")
            
handle_mc_status = on_message(rule=to_me(), block=True,priority=1)
@handle_mc_status.handle()
async def Handle_mc_status(event: MessageEvent):
    msg = get_message_text(event.json())
    if msg in sever:
        base_dir = Path(r"D:\QQbot\QQbot3\yuanchu\yuanchu\plugins\foo")
        png_gain_path = base_dir / "png_gain.py"
        output_image_path = base_dir / "latency_graph.png"
        try:
            # 使用系统Python解释器执行脚本
            result = subprocess.run(
                [sys.executable, "mc_query.py"],
                cwd=str(plugin_dir),  # 设置工作目录
                capture_output=True,
                text=True,
                encoding="gbk",
                timeout=20  # 设置超时时间
            )

            subprocess.run(["python", str(png_gain_path)], check=True)
            
            # 组合输出结果
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += "\n错误信息:\n" + result.stderr

            # 发送结果（截断过长内容）
            await handle_mc_status.send(output.strip()[:1000] +             # 限制消息长度
                                        MessageSegment.image(f"file:///{output_image_path}"))   # 附加延迟波动图
        except subprocess.TimeoutExpired:
            await handle_mc_status.send("服务器状态查询超时，请稍后再试")
        except FileNotFoundError:
            await handle_mc_status.send("未找到服务器状态查询程序")
        except Exception as e:
            await handle_mc_status.send(f"查询出错：{str(e)}")

from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.typing import T_State
import re

# 创建一个消息响应器，用于处理群聊消息
poke_back = on_message(priority=5)

@poke_back.handle()
async def handle_poke_back(bot: Bot, event: GroupMessageEvent, state: T_State):
    # 获取发送消息的用户昵称和QQ号
    user_nickname = event.sender.card or event.sender.nickname
    user_id = event.get_user_id()
    
    # 获取消息内容
    msg_text = event.get_plaintext()
    
    # 判断是否是"笨有引力"用户发送了"戳回去"消息
    if user_nickname == "笨有引力" and msg_text in "戳":
        # 使用戳一戳功能回复该用户
        poke_action = MessageSegment.poke(user_id)
        await bot.send_group_msg(
            group_id=event.group_id,
            message=poke_action
        )