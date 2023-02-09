import nonebot
from nonebot import get_driver
from .config import Config

import json
import mcstatus

with open("data/FWNP_MinecraftServerStatus/command.json", "r+", encoding="utf-8") as f:
    commands = json.loads(f.read())

global_config = get_driver().config
config = Config.parse_obj(global_config)

status_matcher = nonebot.on_command(commands["status"])
@status_matcher.handle()
async def status():
    def safe_replace(text, old, new):
        try:
            output = text.replace(old, new)
            return output
        except:
            return text
    def textinstead(middletext, server_status, name, Bedrock):
        tags = ["<server_name>", "<server_status>", "<server_online>", "<server_delay>", "<server_motd>"]
        values = [name, "正常", str(server_status.players.online), str(round(server_status.latency, 2)), server_status.description]
        if Bedrock:
            del tags[-1]
            del values[-1]
        for z in range(len(tags)):
            middletext = safe_replace(middletext, tags[z], values[z])
        return middletext

    # 获取服务器列表
    with open("data/FWNP_MinecraftServerStatus/info.json", "r+", encoding="utf-8") as f:
        try:
            text = json.loads(f.read())
            servername = text["server"]
            address = text["address"]
            result = text["message"]["header"]
            footer = text["message"]["footer"]
            for i in range(len(address)):
                if "[B]" in address[i]:
                    server = mcstatus.BedrockServer.lookup(address[i].strip("[B]"))
                    Bedrock = True
                else:
                    server = mcstatus.JavaServer.lookup(address[i])
                    Bedrock = False
                try:
                    server_status = server.status()
                    middletext = str(text["message"]["body"])
                    result += textinstead(middletext, server_status, servername[i], Bedrock)
                except:
                    result += "[{}]\n状态: 维护中\n".format(servername[i])
            result += footer
            await status_matcher.send(result)
        except:
            await status_matcher.send("[Error]\n执行失败\n请联系机器人所有者检查配置文件\n如无结果,请联系插件作者")
