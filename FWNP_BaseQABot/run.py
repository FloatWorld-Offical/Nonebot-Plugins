import nonebot

Example_matcher = nonebot.on_command('test')
@Example_matcher.handle()
async def Example():
	await Example_matcher.send('1')
Example2_matcher = nonebot.on_command('test2')
@Example2_matcher.handle()
async def Example2():
	await Example2_matcher.send('2')
