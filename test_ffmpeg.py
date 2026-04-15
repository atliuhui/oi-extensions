import os
from tools.FFmpeg import Tools

tools = Tools()
path = os.getenv("USERPROFILE")

result = tools.convert_audio(
    rf"{path}\Downloads\白鸽乌鸦相爱的戏码-伴奏-音频.mp4"
)
print(result)

result = tools.replace_audio(
    rf"{path}\Downloads\白鸽乌鸦相爱的戏码-伴奏-视频.mp4",
    rf"{path}\Downloads\白鸽乌鸦相爱的戏码-伴奏-音频.mp4",
)
print(result)
