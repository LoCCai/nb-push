#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====qiqi-bot|Push====
-60S观世界/易即今日/Moyu
@API:iyk0/2xb/soyiji
@time: 2022年5月31日
@version: 1.0
技术栈：Regx|Await|Eval|PIL|os
"""
from .Moyu_Config import Moyu_Config
from .Read_Config import Read_Config
from .Yitoday_Config import Yitoday_Config

import nonebot,sys
from nonebot import on_regex, require
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11 import Message,MessageSegment
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11.event import  MessageEvent
from nonebot.typing import T_State
from nonebot.params import State,RegexGroup

from PIL import Image,ImageFilter
import re,os,json,requests
from typing import Tuple, Any

global_config = nonebot.get_driver().config
nonebot.logger.info("global_config:{}".format(global_config))
Moyu_config = Moyu_Config(**global_config.dict())
Read_config = Read_Config(**global_config.dict())
Yitoday_config = Yitoday_Config(**global_config.dict())
nonebot.logger.info("Moyu_config:{}".format(Moyu_config))
nonebot.logger.info("Read_config:{}".format(Read_config))
nonebot.logger.info("Yitoday_config:{}".format(Yitoday_config))
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler


#测试-消息拉取-部分
push = on_regex(r"^[?？](.*)$",priority=20,block=False)
@push.handle()
async def _(reg_group: Tuple[Any, ...] = RegexGroup()):
    get= reg_group[0]
    print(get)
    if get in ['今日简报', '每日简报',"简报",'易即今日','每日新闻']:
        msg=await Yitoday()
    elif get in ['read60s', 'read',"读世界",'60秒读世界','60s读世界']:
        msg=await readworld()
    elif get in ['moyu', '摸鱼',"摸鱼日历",'摸鱼简报','摸鱼推送']:
        msg=await Moyu()
    else:
        msg=""
    if msg=="":
        print("未找到的请求")
    else:
        await push.send(message=Message("\n"+msg), at_sender=True)


#辅助函数
def remove_upprintable_chars(s):
    return ''.join(x for x in s if x.isprintable())#去除imageUrl可能存在的不可见字符

def GetMiddleStr(content, startStr, endStr):
        #patternStr = r'"ip":"(.*?)","urls"'
        patternStr = r'%s(.*?)%s' %(startStr,endStr)
        p = re.compile(patternStr, re.IGNORECASE)
        m = re.findall(p, content)
        if m:
            return m[0]

#图片处理部分

def News_pic_paste(file_adress,save_adress):
    orinagial_img = Image.open(file_adress)
    #head_pic_adress-易即今日头图路径
    head_pic_adress="/root/NoneBot/ccbot/data/Yitoday/head_pic.jpg"
    head_img = Image.open(head_pic_adress)
    width, height = orinagial_img.size
    head_width, head_height = head_img.size
    print(width,height,orinagial_img.mode)
    print(head_width,head_height,head_img.mode)
    # 前两个坐标点是左上角坐标
    # 后两个坐标点是右下角坐标
    # width在前， height在后
    # 处理今日图像完毕
    orinagial_box = (0, 539, width, height)
    orinagial_om = orinagial_img.crop(orinagial_box)
    #新建图像
    target = Image.new('RGB', (width,height)) 
    #拼接头部图像
    #a =    # 图片距离左边的大小
    #b =    # 图片距离上边的大小
    #c =    # 图片距离左边的大小 + 图片自身宽度
    #d =    # 图片距离上边的大小 + 图片自身高度
    a=0
    b=0
    c=head_width
    d=head_height
    target.paste(head_img, (a, b, c, d))
    target.save('crop.jpg')
    #拼接今日图像
    a=0
    b=head_height
    c=head_width
    d=height
    target.paste(orinagial_om, (a, b, c, d))
    target.save(save_adress)

def blend_images1(background_pic_adress,news_pic_adress,save_adress,pic_blend):
    #"C:/LoCCai/bot/Yitoday/test.jpg"
    img1 = Image.open(background_pic_adress)
    img1 = img1.convert('RGBA')

    img2 = Image.open(news_pic_adress)
    img2 = img2.convert('RGBA')
    img2 = img2.resize(img1.size)
    print(img2.size)

    img = Image.blend(img1, img2, pic_blend)
    img.save(save_adress)

#获取待Push图片部分

async def Yitoday():
    #heal_url   根链
    head_url = "http://api.soyiji.com//news_jpg"
    resp = requests.get(head_url)
    resp = resp.text
    retdata = json.loads(resp)
    lst = retdata['url']
    #lst   图链 http://news.soyiji.com/256120-2022-5-19.jpg
    #headers    协议头
    headers = {
        'Referer': 'safe.soyiji.com'
    }
    re = requests.request("GET", lst, headers=headers)
    name=GetMiddleStr(lst,"-",".jpg")+".jpg"
    name2=GetMiddleStr(lst,"-",".jpg")+".png"
    file_adress="data/Yitoday/"
    os.makedirs(file_adress, exist_ok=True)
    with open(file_adress+name,'wb') as f_save:
        f_save.write(re.content)
        f_save.flush()
        f_save.close()
    News_pic_paste(file_adress+name,file_adress+name)
    blend_images1(file_adress+"背景图层.jpg",file_adress+name,file_adress+name2,0.8)
    #合成后的图片路径位置（你的bot的data文件夹内）
    file='file:///root/NoneBot/ccbot/'+file_adress+name2
    print(file)
    pic_ti = f"====qiqi-bot|易即今日Push====\nProcessed By:LoCCai\n======================\n[CQ:image,file={file}]"
    return pic_ti

async def Moyu() -> str:
    response = requests.get("https://api.j4u.ink/v1/store/other/proxy/remote/moyu.json")
    text=json.loads(response.text)
    if text["code"]==200:
        pic_url= text["data"]["moyu_url"]
        re = requests.request("GET", pic_url,)
        name=GetMiddleStr(pic_url,"calendar/",".png")+".png"
        file_adress="data/Moyu/"
        print(file_adress+name)
        os.makedirs(file_adress, exist_ok=True)
        with open(file_adress+name,'wb') as f_save:
            f_save.write(re.content)
            f_save.flush()
            f_save.close()
        #缓存的图片路径位置（你的bot的data文件夹内）
        file="file:///root/NoneBot/ccbot/"+file_adress+name
        pic_ti =f"====qiqi-bot|摸鱼日历Push====\n[CQ:image,file={file}]"
    else:
        pic_url= f"摸鱼日历获取失败，错误码："+text["code"]+text["message"]
    return pic_ti

async def readworld():
    try:
        url = "https://api.2xb.cn/zaob"  # 备用网址
        resp = requests.get(url)
        resp = resp.text
        resp = remove_upprintable_chars(resp)
        retdata = json.loads(resp)
        lst = retdata['imageUrl']
        pic_ti1 = f"====qiqi-bot|60s读世界Push====\nApi from:2xb\n[CQ:image,file={lst}]"
        return pic_ti1
        
    except:
        url = "https://api.iyk0.com/60s"
        resp = requests.get(url)
        resp = resp.text
        resp = remove_upprintable_chars(resp)
        retdata = json.loads(resp)
        lst = retdata['imageUrl']
        pic_ti = f"====qiqi-bot|60s读世界Push====\nApi from:iyk0\n[CQ:image,file={lst}]"
        return pic_ti

#Push部分

async def Moyu_Push():
    msg_Moyu = await Moyu()
    for qq in Moyu_config.moyu_qq_friends:
        await nonebot.get_bot().send_private_msg(user_id=qq, message=Message(msg_Moyu))
    for qq_group in Moyu_config.moyu_qq_groups:
        await nonebot.get_bot().send_group_msg(group_id=qq_group, message=Message(msg_Moyu))

async def Read_Push():
    msg_readworld = await readworld()
    for qq in Read_config.read_qq_friends:
        await nonebot.get_bot().send_private_msg(user_id=qq, message=Message(msg_readworld))
    for qq_group in Read_config.read_qq_groups:
        await nonebot.get_bot().send_group_msg(group_id=qq_group, message=Message(msg_readworld))# MessageEvent可以使用CQ发图片

async def Yitoday_Push():
    msg_Yitoday = await Yitoday()
    for qq in Yitoday_config.yitoday_qq_friends:
        await nonebot.get_bot().send_private_msg(user_id=qq, message=Message(msg_Yitoday))
    for qq_group in Yitoday_config.yitoday_qq_groups:
        await nonebot.get_bot().send_group_msg(group_id=qq_group, message=Message(msg_Yitoday))# MessageEvent可以使用CQ发图片

for index, time in enumerate(Moyu_config.moyu_inform_time):
    nonebot.logger.info("id:{},time:{}".format(index, time))
    scheduler.add_job(Moyu_Push, "cron", hour=time.hour, minute=time.minute, id="Moyu"+str(index))
for index, time in enumerate(Read_config.read_inform_time):
    nonebot.logger.info("id:{},time:{}".format(index, time))
    scheduler.add_job(Read_Push, "cron", hour=time.hour, minute=time.minute, id="Read"+str(index))
for index, time in enumerate(Yitoday_config.yitoday_inform_time):
    nonebot.logger.info("id:{},time:{}".format(index, time))
    scheduler.add_job(Yitoday_Push, "cron", hour=time.hour, minute=time.minute, id="Yitoday"+str(index))
