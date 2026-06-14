import json, asyncio, urllib.request, websockets

async def get_page():
    with urllib.request.urlopen('http://127.0.0.1:9222/json/list') as r:
        tabs = json.loads(r.read())
    for t in tabs:
        if t['type'] == 'page':
            return t['webSocketDebuggerUrl']
    return None

async def inspect(url):
    ws_url = await get_page()
    async with websockets.connect(ws_url) as ws:
        mid = [0]
        async def send(m, p=None):
            mid[0] += 1
            await ws.send(json.dumps({'id':mid[0],'method':m,'params':p or {}}))
            while True:
                r = json.loads(await ws.recv())
                if r.get('id')==mid[0]: return r
        
        await send('Page.enable')
        await send('Runtime.enable')
        
        print(f"Navigating to {url}...")
        await send('Page.navigate', {'url': url})
        await asyncio.sleep(6) # Give it some time
        
        # Let's get all img tags outerHTML
        result = await send('Runtime.evaluate', {
            'expression': """
                JSON.stringify(
                    Array.from(document.querySelectorAll('img')).map(img => img.outerHTML).slice(0, 40)
                )
            """,
            'returnByValue': True
        })
        
        val = result.get('result', {}).get('result', {}).get('value', '[]')
        imgs = json.loads(val)
        print(f"Found {len(imgs)} images:")
        for idx, html in enumerate(imgs):
            print(f"{idx}: {html}")

asyncio.run(inspect("https://www.webfx.com/blog/web-design/salon-website-design/"))
