# encoding: utf-8
""" 
@version: v1.0 
@author: autumner 
@license: Apache Licence  
@contact: 18322313385@163.com 
@site: https://github.com/nzj1981/mywebapp_py36.git 
@software: PyCharm 
@file: test_table_user.py 
@time: 2018/4/23 17:06
"""

__author__ = 'autumner'

'''
test table user
'''

import orm, asyncio
from config import configs
from models import Blog, Comment

# print(configs.get('db'), type(configs.get('db')))

'''
blogs = Blog(user_id='00152462211971819c66403a2dd461fa1c5fa55cded2951000',
             user_name='Test2',
             user_image='about:blank',
             name=r'沁园春·雪',
             summary=r"""北国风光，千里冰封，万里雪飘。
望长城内外，惟余莽莽；大河上下，顿失滔滔。
""",
             content=r"""北国风光，千里冰封，万里雪飘。

望长城内外，惟余莽莽；大河上下，顿失滔滔。

山舞银蛇，原驰蜡象，欲与天公试比高。

须晴日，看红装素裹，分外妖娆。

江山如此多娇，引无数英雄竞折腰。

惜秦皇汉武，略输文采；唐宗宋祖，稍逊风骚。

一代天骄，成吉思汗，只识弯弓射大雕。

俱往矣，数风流人物，还看今朝。"""
             )

'''

comments = Comment(blog_id='0015246275670282790f1d86ce04c768501391fd6f1acc7000',
                   user_id='00152462211971819c66403a2dd461fa1c5fa55cded2951000',
                   user_name='Test2',
                   user_image='about:blank',
                   content=r"""雪：这首词作于红一方面军一九三六年二月由陕北准备东渡黄河进入山西省西部的时候。作者在一九四五年十月七日给柳亚子信中说，这首词作于“初到陕北看见大雪时”。
惟：只。
馀：剩下。此字一作“余”，但目前刊出的书法作品中写作“馀”，以此为准。
莽莽：无边无际。
大河上下：大河，指黄河。大河上下，犹言整条黄河。
顿失滔滔：（黄河）立刻失去了波涛滚滚的气势。描写黄河水结冰的景象。
山舞银蛇，原驰蜡象：群山好像（一条条）银蛇在舞动。高原（上的丘陵）好像（许多）白象在奔跑。“原”指高原，即秦晋高原。蜡象，白色的象。
天公：指天，即命运。
须：等到；需要。
红装素裹：形容雪后天晴，红日和白雪交相辉映的壮丽景色。红装，原指妇女的艳装，这里指红日为大地披上了红装。素裹，原指妇女的淡装，这里指皑皑白雪覆盖着大地。
分外妖娆：格外婀娜多姿。
竞折腰：折腰，倾倒，躬着腰侍候。这里是说争着为江山奔走操劳。
秦皇：秦始皇嬴政（前259~前210），秦朝的创业皇帝。
汉武：汉武帝刘彻（前156~前87），汉朝功业最盛的皇帝。
略输文采：文采本指辞藻、才华。“略输文采”，是说秦皇汉武，武功甚盛，对比之下，文治方面的成就略有逊色。
唐宗：唐太宗李世民（599~649），唐朝的建立统一大业的皇帝。
宋祖：宋太祖赵匡胤（927~976），宋朝的创业皇帝。
稍逊风骚：意近“略输文采”。风骚，本指《诗经》里的《国风》和《楚辞》里的《离骚》，后来泛指文章辞藻。
一代天骄：指可以称雄一世的英雄人物，泛指非常著名，有才能的人物。天骄，“天之骄子”的省略语。意思是上天所骄纵宠爱的人，成吉思汗即是。汉时匈奴自称。后来也泛称强盛的少数名族或其首领。
成吉思汗（hán）：元太祖铁木真（1162~1227）在1206年统一蒙古后的尊称，意为“强者之汗”（汗是可汗的省称，即王）。后蒙古于1271年改国号为元，成吉思汗被尊为建立元朝的始祖。成吉思汗除占领中国黄河以北地区外，还曾向西远征，占领中亚和南俄，建立了庞大的蒙古帝国。
只识弯弓射大雕：雕，一种属于鹰类的大型猛禽，善飞难射，古代因用“射雕手”比喻高强的射手。“只识弯弓射大雕”，是说只以武功见长。
俱往矣：都已经过去了。 俱，都。
数风流人物：称得上能建功立业的英雄人物。数，数得着、称得上的意思。"""
                   )

loop = asyncio.get_event_loop()
loop.run_until_complete(orm.create_pool(loop=loop, **configs.db))

# blog conntent add
# rs = loop.run_until_complete(blogs.save())
# # rs = loop.run_until_complete(u2.update())
# print('save ok', rs)
# rs1 = loop.run_until_complete(orm.select('select * from blogs', None))
# print("list: %s" % rs1)

# comment conntent add
rs = loop.run_until_complete(comments.save())
print('comments save ok', rs)
rs1 = loop.run_until_complete(orm.select('select * from blogs', None))
print("list: %s" % rs1)
loop.run_until_complete(orm.close_pool())
# loop.run_forever()
