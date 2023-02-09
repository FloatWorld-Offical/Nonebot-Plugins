from nonebot import get_driver
from .config import Config

import json

global_config = get_driver().config
config = Config.parse_obj(global_config)

with open("data/FWNP_BaseQABot/QA.json", "r+", encoding="utf-8") as f:
    text = json.loads(f.read())
f = open("./src/plugins/FWNP_BaseQABot/run.py", "w", encoding='utf-8')
key = list(text.keys())
final = "import nonebot\n\n"

for i in range(len(key)):
    final += "{a}_matcher = nonebot.on_command('{command}')\n@{a}_matcher.handle()\nasync def {a}():\n\tawait {a}_matcher.send('{answer}')\n".format(a=key[i], command=text[key[i]]["Command"], answer=text[key[i]]["Answer"])

f.write(final)
f.close()
from . import run
