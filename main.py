from astrbot.api.all import *
import requests
import re

@register("douyin_video", "Your Name", "解析抖音视频链接并发送视频及信息", "1.0.0")
class DouyinVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent):
        message_str = event.message_str
        # 检测消息中是否包含抖音视频链接
        if '<url id="cv994u9g6i8ttaifj4og" type="url" status="parsed" title="抖音-记录美好生活" wc="442"><url id="temp" type="url" status="" title="" wc="">https://v.douyin.com/</url></url>' in message_str:
            # 提取抖音视频链接
            douyin_url = re.search(r"https://v\.douyin\.com/\S+", message_str).group()
            # 调用 API 解析抖音视频
            api_url = f"https://api.xinyew.cn/api/douyinjx?url={douyin_url}"
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if data["code"] == 200:
                    video_url = data["data"]["video_url"]
                    desc = data["data"]["additional_data"][0]["desc"]
                    nickname = data["data"]["additional_data"][0]["nickname"]
                    # 发送视频文件
                    # 根据平台适配器发送视频
                    if event.get_platform_name() == "aiocqhttp":
                        from astrbot.api.message_components import Video
                        # 发送视频时不引用消息且不@发送者
                        await event.send(message=Video.fromURL(video_url), reply=False, at_sender=False)
                    else:
                        # 对于其他平台，可以尝试发送视频链接
                        await event.send(message=f"视频链接：{video_url}", reply=False, at_sender=False)
                    # 发送视频描述和作者昵称时不引用消息且不@发送者
                    await event.send(message=f"视频描述：{desc}\n作者昵称：{nickname}", reply=False, at_sender=False)
                else:
                    await event.send(message="解析抖音视频失败", reply=False, at_sender=False)
            else:
                await event.send(message="解析抖音视频失败", reply=False, at_sender=False)
