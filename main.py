import asyncio
import aiohttp

from exceptions import InvalidProxy


async def check_format(proxy:str):
	if 'http' not in proxy:
		proxy=f'http://{proxy}'
	return proxy

async def check_ip(proxy: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('http://eth0.me/', proxy=proxy) as r:
                your_ip = (await r.text()).strip()
                if your_ip not in proxy:
                    raise InvalidProxy(f"Proxy {proxy} doesn't work! Your IP is {your_ip}.")
                else:
                    print(f'Proxy {proxy} is good')
        except Exception as e:
            raise InvalidProxy(f"Proxy {proxy} doesn't work! Error: {e}")


async def main():
	proxies = []
	try:
		with open('proxies.txt', 'r') as file:
			proxies = [line.strip() for line in file if line.strip()]
	except FileNotFoundError:
		print("Proxies file not found!")
		return

	tasks = []
	for proxy in proxies:
		formatted_proxy = await check_format(proxy)
		tasks.append(check_ip(formatted_proxy))

	results = await asyncio.gather(*tasks, return_exceptions=True)

	for result in results:
		if isinstance(result, Exception):
			print(result)



if __name__=='__main__':
	asyncio.run(main())