from bzutech import BzuTech
import asyncio

bzu = BzuTech("admin@email.com", "bzutech123")
print(asyncio.run(bzu.start()))