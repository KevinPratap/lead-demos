"""
Deeper design analysis - visit the best live sites and extract full CSS tokens.
"""
import json, asyncio, urllib.request, websockets

CDP = "http://127.0.0.1:9222"

def get_page():
    with urllib.request.urlopen(f"{CDP}/json/list") as r:
        tabs = json.loads(r.read())
    for t in tabs:
        if t['type'] == 'page':
            return t['id'], t['webSocketDebuggerUrl']
    return None, None

async def analyze_site(ws_url, url):
    async with websockets.connect(ws_url) as ws:
        msg_id = [0]
        async def send(method, params=None):
            msg_id[0] += 1
            await ws.send(json.dumps({"id": msg_id[0], "method": method, "params": params or {}}))
            while True:
                resp = json.loads(await ws.recv())
                if resp.get("id") == msg_id[0]:
                    return resp
        
        await send("Page.enable")
        await send("Runtime.enable")
        await send("Page.navigate", {"url": url})
        await asyncio.sleep(5)
        
        # Extract comprehensive design tokens
        script = """
        (() => {
            const body = getComputedStyle(document.body);
            const h1 = document.querySelector('h1');
            const h1s = h1 ? getComputedStyle(h1) : {};
            const h2 = document.querySelector('h2');
            const h2s = h2 ? getComputedStyle(h2) : {};
            
            // Get nav
            const nav = document.querySelector('nav, header, .nav, .header');
            const navS = nav ? getComputedStyle(nav) : {};
            
            // Get real CTA buttons (not nav links)
            const ctas = Array.from(document.querySelectorAll('a[href*="book"], a[href*="contact"], a[href*="appoint"], a[href*="call"], .cta, [class*="cta"], [class*="CTA"]')).slice(0,5).map(b => {
                const s = getComputedStyle(b);
                return {text: b.textContent.trim().slice(0,40), bg: s.backgroundColor, color: s.color, radius: s.borderRadius, padding: s.padding, fontSize: s.fontSize, fontWeight: s.fontWeight, border: s.border};
            });
            
            // Get all unique background colors from major sections
            const sections = document.querySelectorAll('section, .section, [class*="section"], [class*="hero"], [class*="about"], [class*="service"], [class*="contact"], [class*="footer"]');
            const bgColors = new Set();
            const textColors = new Set();
            sections.forEach(el => {
                const s = getComputedStyle(el);
                const bg = s.backgroundColor;
                const tc = s.color;
                if (bg && bg !== 'rgba(0, 0, 0, 0)') bgColors.add(bg);
                if (tc && tc !== 'rgba(0, 0, 0, 0)') textColors.add(tc);
            });
            
            // Get images
            const heroImg = document.querySelector('.hero img, [class*="hero"] img, section:first-of-type img');
            const allImgs = document.querySelectorAll('img[src*=".jpg"], img[src*=".png"], img[src*=".webp"]');
            
            return JSON.stringify({
                title: document.title,
                url: window.location.href,
                font: body.fontFamily,
                bg: body.backgroundColor,
                textColor: body.color,
                h1Text: h1?.textContent.trim().slice(0,100),
                h1Size: h1s.fontSize,
                h1Weight: h1s.fontWeight,
                h1Color: h1s.color,
                h1Spacing: h1s.letterSpacing,
                h2Text: h2?.textContent.trim().slice(0,80),
                h2Size: h2s.fontSize,
                h2Weight: h2s.fontWeight,
                navBg: navS.backgroundColor,
                navText: navS.color,
                ctas: ctas,
                bgColors: [...bgColors].slice(0,10),
                textColors: [...textColors].slice(0,10),
                heroImg: heroImg?.src?.slice(0,100) || null,
                imageCount: allImgs.length,
                sectionCount: sections.length
            });
        })()
        """
        
        result = await send("Runtime.evaluate", {"expression": script, "returnByValue": True})
        value = result.get("result", {}).get("result", {}).get("value")
        return json.loads(value) if value else None

async def main():
    _, ws_url = get_page()
    if not ws_url:
        print("No page")
        return
    
    sites = [
        ("dental", "https://www.tenddental.com"),
        ("dental", "https://www.bitestudio.co"),
        ("spa", "https://www.scandinave.com"),
        ("spa", "https://www.bloomingmoonspa.com"),
        ("spa", "https://www.mamounia.com"),
        ("salon", "https://www.visagesalonspa.com"),
        ("salon", "https://www.oasisaveda.com"),
    ]
    
    results = {}
    for niche, url in sites:
        print(f"\n[{niche}] {url}")
        try:
            tokens = await asyncio.wait_for(analyze_site(ws_url, url), timeout=15)
            if tokens:
                results[f"{niche}:{url}"] = tokens
                print(f"  {tokens.get('title','?')[:60]}")
                print(f"  Font: {tokens.get('font','?')[:60]}")
                print(f"  H1: {tokens.get('h1Size','?')} / {tokens.get('h1Weight','?')} / spacing: {tokens.get('h1Spacing','?')}")
                print(f"  Nav: bg={tokens.get('navBg','?')} text={tokens.get('navText','?')}")
                print(f"  BG colors: {len(tokens.get('bgColors',[]))}")
                for c in tokens.get('bgColors',[])[:5]:
                    print(f"    {c}")
                print(f"  Text colors: {len(tokens.get('textColors',[]))}")
                for c in tokens.get('textColors',[])[:5]:
                    print(f"    {c}")
                if tokens.get('ctas'):
                    cta = tokens['ctas'][0]
                    print(f"  CTA: \"{cta['text'][:30]}\" | bg:{cta['bg']} | text:{cta['color']} | border:{cta['border']} | radius:{cta['radius']} | size:{cta['fontSize']}")
        except Exception as e:
            print(f"  Error: {e}")
    
    with open('/home/prata/leads/design-inspiration/design_tokens.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {len(results)} sites to design_tokens.json")

asyncio.run(main())
