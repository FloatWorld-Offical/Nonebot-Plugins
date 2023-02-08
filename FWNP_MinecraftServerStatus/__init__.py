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
    # 获取服务器列表
    with open("data/FWNP_MinecraftServerStatus/info.json", "r+", encoding="utf-8") as f:
        try:
            text = json.loads(f.read())
            servername = text["server"]
            address = text["address"]
            result = text["message"]["header"]
            footer = text["message"]["footer"]
            for i in range(len(address)):
                if text["BedrockMODE"] == False:
                    server = mcstatus.JavaServer.lookup(address[i])
                else:
                    server = mcstatus.BedrockServer.lookup(address[i])
                try:
                    server_status = server.status()
                    middletext = str(text["message"]["body"])
                    result += middletext.replace("<server_name>", servername[i]).replace("<server_status>", "正常").replace("<server_online>", str(server_status.players.online))
                except:
                    result += "[{}]\n状态: 维护中\n".format(servername[i])
            result += footer
            await status_matcher.send(result)
        except:
            await status_matcher.send("[Error]\n执行失败\n请联系机器人所有者检查配置文件\n如无结果,请联系插件作者")