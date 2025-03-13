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
        if "https://v.douyin.com/" in message_str:
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
                    yield event.file_video(video_url)
                    # 发送视频描述和作者昵称
                    yield event.plain_result(f"视频描述：{desc}\n作者昵称：{nickname}")
                else:
                    yield event.plain_result("解析抖音视频失败")
            else:
                yield event.plain_result("解析抖音视频失败")
