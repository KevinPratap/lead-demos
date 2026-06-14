"""Scrape award-winning design galleries via CDP websocket."""
import json
import asyncio
import urllib.request
import urllib.parse
import websockets
import os
import time
import re
import subprocess

OUTPUT = '/home/prata/leads/design-inspiration'
INDEX_PATH = '/home/prata/leads/design-inspiration/index.html'

async def get_page():
    try:
        with urllib.request.urlopen('http://127.0.0.1:9222/json/list') as r:
            tabs = json.loads(r.read())
        for t in tabs:
            if t['type'] == 'page':
                return t['webSocketDebuggerUrl']
    except Exception as e:
        print(f"Error connecting to Chrome CDP: {e}")
    return None

def download_image(url, filepath):
    """Download image with Chrome User-Agent to prevent 403 Forbidden."""
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read()
            # If the size is less than 5KB, discard it (usually trackers or placeholders)
            if len(data) < 5120:
                return False
            with open(filepath, 'wb') as f:
                f.write(data)
        return True
    except Exception as e:
        # Silently fail for individual images
        return False

async def scrape_site(ws_url, url, niche, site_name):
    """Navigate to a design gallery, scroll to lazy-load, and extract screenshots."""
    try:
        async with websockets.connect(ws_url, max_size=10*1024*1024) as ws:
            mid = [0]
            async def send(m, p=None):
                mid[0] += 1
                await ws.send(json.dumps({'id':mid[0],'method':m,'params':p or {}}))
                while True:
                    r = json.loads(await ws.recv())
                    if r.get('id')==mid[0]: return r
            
            await send('Page.enable')
            await send('Runtime.enable')
            
            print(f'  Navigating to {url}...')
            await send('Page.navigate', {'url': url})
            
            # Wait for initial load
            await asyncio.sleep(5)
            
            # Scroll down the page a few times to trigger lazy-loaded images
            print('  Scrolling page to trigger lazy loading...')
            scroll_expr = """
                (async () => {
                    for (let i = 0; i < 4; i++) {
                        window.scrollBy(0, window.innerHeight * 1.2);
                        await new Promise(r => setTimeout(r, 1000));
                    }
                    window.scrollTo(0, 0);
                })()
            """
            await send('Runtime.evaluate', {'expression': scroll_expr, 'awaitPromise': True})
            await asyncio.sleep(2)
            
            # Extract all image URLs from the page with smart checks
            js_extract = """
                (() => {
                    let imgs = Array.from(document.querySelectorAll('img'));
                    let results = [];
                    for (let img of imgs) {
                        let src = '';
                        
                        // Check common lazy-loading attributes
                        for (let attr of ['data-src', 'data-lazy-src', 'nitro-lazy-src', 'data-original', 'lazy-src', 'data-lazyload', 'data-hi-res']) {
                            let val = img.getAttribute(attr);
                            if (val) { src = val; break; }
                        }
                        if (!src) {
                            src = img.src || '';
                        }
                        
                        // If src is empty/data URI, try srcset attributes
                        if (!src || src.startsWith('data:image')) {
                            let srcset = img.getAttribute('srcset') || img.getAttribute('nitro-lazy-srcset') || img.getAttribute('data-srcset') || img.getAttribute('data-lazy-srcset');
                            if (srcset) {
                                let parts = srcset.trim().split(/\\s*,\\s*/);
                                if (parts.length > 0) {
                                    let urlPart = parts[parts.length - 1].trim().split(/\\s+/)[0];
                                    if (urlPart) src = urlPart;
                                }
                            }
                        }
                        
                        if (!src || src.startsWith('data:image')) continue;
                        
                        // Filter out small sizes based on attributes
                        let width = parseInt(img.getAttribute('width') || img.style.width || '999');
                        let height = parseInt(img.getAttribute('height') || img.style.height || '999');
                        if (width < 150 || height < 150) continue;
                        
                        // Filter out obvious layout icons, avatars, logo patterns
                        let s = src.toLowerCase();
                        if (s.includes('logo') || s.includes('avatar') || s.includes('icon') || s.includes('tracker') || s.includes('pixel') || s.includes('spacer') || s.includes('spinner') || s.includes('social') || s.includes('button') || s.includes('badge') || s.includes('profile')) continue;
                        
                        // Filter out small thumbnail patterns in filenames
                        if (/\\d+x\\d+/.test(s)) {
                            let match = s.match(/(\\d+)x(\\d+)/);
                            if (match) {
                                let w = parseInt(match[1]);
                                let h = parseInt(match[2]);
                                if (w < 200 || h < 200) continue;
                            }
                        }
                        
                        results.push({
                            src: src,
                            alt: img.alt || ''
                        });
                    }
                    // Deduplicate results by src
                    let unique = [];
                    let seen = new Set();
                    for (let item of results) {
                        if (!seen.has(item.src)) {
                            seen.add(item.src);
                            unique.push(item);
                        }
                    }
                    return JSON.stringify(unique.slice(0, 30));
                })()
            """
            
            result = await send('Runtime.evaluate', {
                'expression': js_extract,
                'returnByValue': True
            })
            
            val = result.get('result', {}).get('result', {}).get('value', '[]')
            imgs = json.loads(val)
            print(f'  Found {len(imgs)} candidate images')
            
            saved = 0
            for img in imgs:
                src = img['src']
                # Resolve relative paths
                src = urllib.parse.urljoin(url, src)
                
                # Extract clean filename
                parsed_url = urllib.parse.urlparse(src)
                filename = os.path.basename(parsed_url.path)
                if not filename or not (filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png') or filename.endswith('.webp') or filename.endswith('.avif')):
                    filename = f"image_{hash(src) % 100000}.jpg"
                
                # Create descriptive filename prefix based on domain/site name
                clean_name = re.sub(r'[^\w.-]', '_', f"{site_name}_{filename}")
                # Ensure it ends with an appropriate extension
                if not any(clean_name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.avif']):
                    clean_name += '.jpg'
                
                filepath = os.path.join(OUTPUT, niche, clean_name)
                
                # Skip if already exists and is valid
                if os.path.exists(filepath) and os.path.getsize(filepath) > 5000:
                    continue
                
                if download_image(src, filepath):
                    saved += 1
            
            print(f'  Saved {saved} new images')
            return saved
    except Exception as e:
        print(f'  Error in scrape_site: {e}')
        return 0

def update_gallery():
    """Scan the design-inspiration directory, update index.html filters and data."""
    if not os.path.exists(INDEX_PATH):
        print(f"Gallery file not found at {INDEX_PATH}")
        return
    
    # Scan subdirectories
    niches = []
    d_array = []
    niche_counts = {}
    
    # Niches to look for
    valid_niches = ['dental', 'gym', 'physio', 'salon', 'spa', 'yoga']
    
    for niche in os.listdir(OUTPUT):
        niche_path = os.path.join(OUTPUT, niche)
        if os.path.isdir(niche_path) and niche in valid_niches:
            files = [f for f in os.listdir(niche_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.avif'))]
            # Verify file size > 5KB to exclude corrupted/placeholder files
            valid_files = []
            for f in files:
                fpath = os.path.join(niche_path, f)
                if os.path.getsize(fpath) > 5000:
                    valid_files.append(f)
            
            niche_counts[niche] = len(valid_files)
            for f in valid_files:
                d_array.append({
                    "niche": niche,
                    "url": f"https://kevinpratap.github.io/lead-demos/design-inspiration/{niche}/{f}",
                    "file": f
                })
    
    # Sort files by name so output is stable
    d_array.sort(key=lambda x: (x['niche'], x['file']))
    
    total_count = len(d_array)
    print(f"\nGallery scan complete. Total images in index: {total_count}")
    for niche, count in sorted(niche_counts.items()):
        print(f"  {niche.capitalize()}: {count}")
    
    # Read index.html
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update subtext
    content = re.sub(
        r'<p class="sub">.*?</p>', 
        f'<p class="sub">{total_count} website design screenshots scraped from Awwwards, CSS Design Awards, and design blogs</p>', 
        content
    )
    
    # 2. Update filters div
    filters_html = '<div class="filters">\n<button class="fbtn active" data-niche="all">All</button>\n'
    for niche in sorted(valid_niches):
        count = niche_counts.get(niche, 0)
        filters_html += f'<button class="fbtn" data-niche="{niche}">{niche.capitalize()}<span class="badge">{count}</span></button>'
    filters_html += '\n</div>'
    
    content = re.sub(r'<div class="filters">.*?</div>', filters_html, content, flags=re.DOTALL)
    
    # 3. Update JSON array D
    json_d = json.dumps(d_array, separators=(',', ':'))
    content = re.sub(r'const D=\[.*?\];', f'const D={json_d};', content)
    
    # Write back to index.html
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated index.html successfully.")

def git_push():
    """Git commit and push changes to GitHub."""
    try:
        print("\nPushing changes to GitHub...")
        subprocess.run(['git', 'add', '.'], cwd='/home/prata/leads', check=True)
        # Check if there are changes to commit
        status = subprocess.run(['git', 'status', '--porcelain'], cwd='/home/prata/leads', capture_output=True, text=True)
        if not status.stdout.strip():
            print("No new changes to commit.")
            return
            
        subprocess.run(['git', 'commit', '-m', 'Scrape more award-winning design references and update gallery index'], cwd='/home/prata/leads', check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], cwd='/home/prata/leads', check=True)
        print("GitHub push completed successfully!")
    except Exception as e:
        print(f"Git operations failed: {e}")

async def main():
    ws_url = await get_page()
    if not ws_url:
        print("No Chrome tab found. Make sure Chrome CDP is running on port 9222.")
        return
    
    targets = [
        # Dental Niches
        ("dental", "https://thomasdigital.com/best-dental-websites/", "thomas"),
        ("dental", "https://www.insidea.com/blog/dental-clinic-website-design/", "insidea"),
        ("dental", "https://www.awwwards.com/websites/health/", "awwwards_health"),
        ("dental", "https://www.cssdesignawards.com/search?q=dentist+website", "cssda_dentist"),
        
        # Spa Niches
        ("spa", "https://www.awwwards.com/websites/beauty/", "awwwards_beauty"),
        ("spa", "https://www.cssdesignawards.com/search?q=spa+website", "cssda_spa"),
        
        # Salon Niches
        ("salon", "https://www.webfx.com/blog/web-design/salon-website-design/", "webfx"),
        ("salon", "https://www.cssdesignawards.com/search?q=salon+website", "cssda_salon"),
        ("salon", "https://www.webcitz.com/best-salon-websites", "webcitz_salon"),
        
        # Gym Niches
        ("gym", "https://www.awwwards.com/websites/fitness/", "awwwards_fitness"),
        ("gym", "https://www.cssdesignawards.com/search?q=gym+website", "cssda_gym"),
        
        # Yoga Niches
        ("yoga", "https://www.cssdesignawards.com/search?q=yoga+studio+website", "cssda_yoga"),
    ]
    
    niche_new_counts = {"dental": 0, "spa": 0, "salon": 0, "gym": 0, "yoga": 0}
    total = 0
    
    for niche, url, name in targets:
        os.makedirs(os.path.join(OUTPUT, niche), exist_ok=True)
        print(f'\n[{niche}] {name}')
        try:
            saved = await asyncio.wait_for(scrape_site(ws_url, url, niche, name), timeout=45)
            if niche in niche_new_counts:
                niche_new_counts[niche] += saved
            total += saved
        except Exception as e:
            print(f'  Error: {e}')
    
    print(f'\nScrape run finished. Total new images saved: {total}')
    print("New images per niche:")
    for niche, count in niche_new_counts.items():
        print(f"  {niche.capitalize()}: {count}")
    
    # Update index.html
    update_gallery()
    
    # Push to GitHub
    git_push()

if __name__ == '__main__':
    asyncio.run(main())
