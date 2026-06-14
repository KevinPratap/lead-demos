import json, asyncio, urllib.request, websockets, sys

async def analyze(url):
    with urllib.request.urlopen('http://127.0.0.1:9222/json/list') as r:
        tabs = json.loads(r.read())
    ws_url = [t['webSocketDebuggerUrl'] for t in tabs if t['type']=='page'][0]
    
    async with websockets.connect(ws_url) as ws:
        mid = [0]
        async def send(m, p=None):
            mid[0] += 1
            await ws.send(json.dumps({'id':mid[0],'method':m,'params':p or {}}))
            while True:
                r = json.loads(await ws.recv())
                if r.get('id')==mid[0]: return r
        
        await send('Page.enable')
        await send('Page.navigate', {'url': url})
        await asyncio.sleep(4)
        
        r = await send('Runtime.evaluate', {
            'expression': """JSON.stringify({title:document.title, font:getComputedStyle(document.body).fontFamily.split(',')[0].replace(/"/g,'').trim(), h1Text:document.querySelector('h1')?.textContent?.trim()?.slice(0,60)||'', h1Size:document.querySelector('h1')?getComputedStyle(document.querySelector('h1')).fontSize:'', h1Weight:document.querySelector('h1')?getComputedStyle(document.querySelector('h1')).fontWeight:'', h1Color:document.querySelector('h1')?getComputedStyle(document.querySelector('h1')).color:'', sections:Array.from(document.querySelectorAll('section,[class*=section]')).slice(0,6).map(e=>({bg:getComputedStyle(e).backgroundColor,color:getComputedStyle(e).color})), buttons:Array.from(document.querySelectorAll('a[href*=book],a[href*=contact],a[href*=appointment],.btn,[class*=cta]')).slice(0,4).map(b=>({text:b.textContent.trim().slice(0,30),bg:getComputedStyle(b).backgroundColor,color:getComputedStyle(b).color,radius:getComputedStyle(b).borderRadius,padding:getComputedStyle(b).padding,fontSize:getComputedStyle(b).fontSize}))})""",
            'returnByValue': True
        })
        return json.loads(r['result']['result']['value'])

async def main():
    sites = [
        ('dental','https://www.tenddental.com'),
        ('dental','https://www.seattledentalco.com'),
        ('spa','https://www.scandinave.com'),
        ('spa','https://www.spabelles.com'),
        ('salon','https://www.oasisaveda.com'),
    ]
    
    results = {}
    for niche, url in sites:
        print(f'\n[{niche}] {url}')
        try:
            d = await asyncio.wait_for(analyze(url), timeout=12)
            results[url] = d
            print(f'  {d["title"][:60]}')
            print(f'  Font: {d["font"]}')
            print(f'  H1: {d["h1Size"]}/{d["h1Weight"]} "{d["h1Text"][:40]}"')
            print(f'  H1 color: {d["h1Color"]}')
            for s in d.get('sections',[])[:4]:
                print(f'  Sec: bg={s["bg"]} text={s["color"]}')
            for b in d.get('buttons',[])[:2]:
                print(f'  Btn: "{b["text"][:25]}" bg={b["bg"]} color={b["color"]} radius={b["radius"]} size={b["fontSize"]}')
        except Exception as e:
            print(f'  Error: {e}')
    
    with open('/home/prata/leads/design-inspiration/design_tokens.json','w') as f:
        json.dump(results, f, indent=2)
    print(f'\nSaved {len(results)} analyses')

asyncio.run(main())
