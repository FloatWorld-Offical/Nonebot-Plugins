import nonebot
from nonebot import get_driver
from nonebot.params import CommandArg
from nonebot.adapters import Message
from .config import Config

import json
import mcstatus

with open("data/FWNP_MinecraftServerStatus/command.json", "r+", encoding="utf-8") as f:
    commands = json.loads(f.read())

global_config = get_driver().config
config = Config.parse_obj(global_config)


def safe_replace(text, old, new):
    try:
        output = text.replace(old, new)
        return output
    except:
        return text


def textinstead(middletext, server_status, name, Bedrock):
    tags = ["<server_name>", "<server_status>", "<server_online>", "<server_delay>", "<server_motd>"]
    values = [name, "正常", str(server_status.players.online), str(round(server_status.latency, 2)),
              server_status.description]
    if Bedrock:
        del tags[-1]
        del values[-1]
    for z in range(len(tags)):
        middletext = safe_replace(middletext, tags[z], values[z])
    return middletext

if commands["list"]["enable"]:
    list_matcher = nonebot.on_command(commands["list"]["command"])
    @list_matcher.handle()
    async def list():
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
                await list_matcher.send(result)
            except:
                await list_matcher.send("[Error]\n执行失败\n请联系机器人所有者检查配置文件\n如无结果,请联系插件作者")
                
if commands["single_JE"]["enable"]:
    single_matcher = nonebot.on_command(commands["single_JE"]["command"])
    @single_matcher.handle()
    async def single(key: Message = CommandArg()):
        with open("data/FWNP_MinecraftServerStatus/info.json", "r+", encoding="utf-8") as f:
            try:
                text = json.loads(f.read())
                result = text["message"]["header"]
                footer = text["message"]["footer"]
                address = key.extract_plain_text()
                server = mcstatus.JavaServer.lookup(address)
                Bedrock = False
                try:
                    server_status = server.status()
                    middletext = str(text["message"]["body"])
                    result += textinstead(middletext, server_status, "", Bedrock)
                except:
                    result += "状态: 维护中\n".format()
                result += footer
                await list_matcher.send(result)
            except:
                await list_matcher.send("[Error]\n无法正常获取数据\n一般是地址错误(不支持无端口)\n如无结果,请联系插件作者")

if commands["single_BE"]["enable"]:
    single_matcher = nonebot.on_command(commands["single_BE"]["command"])
    @single_matcher.handle()
    async def single(key: Message = CommandArg()):
        with open("data/FWNP_MinecraftServerStatus/info.json", "r+", encoding="utf-8") as f:
            try:
                text = json.loads(f.read())
                result = text["message"]["header"]
                footer = text["message"]["footer"]
                address = key.extract_plain_text()
                server = mcstatus.BedrockServer.lookup(address)
                Bedrock = True
                try:
                    server_status = server.status()
                    middletext = str(text["message"]["body"])
                    result += textinstead(middletext, server_status, "", Bedrock)
                except:
                    result += "状态: 维护中\n".format()
                result += footer
                await list_matcher.send(result)
            except:
                await list_matcher.send("[Error]\n无法正常获取数据\n一般是地址错误(不支持无端口)\n如无结果,请联系插件作者")