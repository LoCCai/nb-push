## nb_push
nb2 定时推送插件 由60s-<https://github.com/bingganhe123/60s->修改

#当前插件内默认推送：
1.摸鱼日历
2.易即今日-新闻图
3.60s读世界

##缓存图片位置：
bot/data/xxx

#下载方式：
下载源码，复制到plugins文件夹内食用（缺少哪些库自行pip install）

## 配置方法 注python3.9以上版本才能正常使用

在nonebot的env配置文件中输入以下内容
```
#定时发送配置-60s读世界/易即今日/Moyu

#-60s读世界
read_qq_friends=[] #设定要发送的QQ好友
read_qq_groups=[123456,123456789] #设定要发送的群
read_inform_time=[{"HOUR":8,"MINUTE":10}] #在输入时间的时候 不要 以0开头如{"HOUR":06,"MINUTE":08}是错误的

#-Moyu
moyu_qq_friends=[]
moyu_qq_groups=[737907680,954788994,1050243516]
moyu_inform_time=[{"HOUR":7,"MINUTE":52}]

#-易即今日（建议至少每日9时以后再进行访问，该api接口一般9:30后确定更新）
yitoday_qq_friends=[]
yitoday_qq_groups=[737907680,954788994,1050243516]
yitoday_inform_time=[{"HOUR":9,"MINUTE":30}]

#可以接入历史上的今天
today_in_history_qq_friends=[]
today_in_history_qq_groups=[954788994,1050243516]
today_in_history_inform_time=[{"HOUR":8,"MINUTE":20}]

#黄历
yellow_calendar_qq_friends=[]
yellow_calendar_qq_groups=[954788994,1050243516]
yellow_calendar_inform_time=[{"HOUR":7,"MINUTE":10}]
