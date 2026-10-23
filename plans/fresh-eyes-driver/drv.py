# Phone-sized browser kept open; commands via HTTP: /cmd?c=...
import asyncio, re, json, sys, urllib.parse
from aiohttp import web
from playwright.async_api import async_playwright
THREE=open('/tmp/cadet-work/three/package/build/three.min.js').read()
GAME=sys.argv[1]
state={}
async def main():
    pw=await async_playwright().start()
    ctx=await pw.chromium.launch_persistent_context((sys.argv[2] if len(sys.argv)>2 else '/tmp/cadet-work/profile'),executable_path='/opt/pw-browsers/chromium',
        viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True,
        args=['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    await ctx.route(re.compile(r'.*three\.min\.js'),lambda r: r.fulfill(body=THREE,content_type='application/javascript'))
    page=ctx.pages[0] if ctx.pages else await ctx.new_page()
    logs=[]
    page.on('console',lambda m: logs.append(m.type+': '+m.text) if m.type in('error','warning') else None)
    page.on('pageerror',lambda e: logs.append('PAGEERROR: '+str(e)))
    async def h(req):
        q=req.query; c=q.get('c','')
        try:
            if c=='goto': await page.goto(q['url']); r='ok'
            elif c=='shot':
                await page.screenshot(path=q['p']); r=q['p']
            elif c=='tap':
                await page.touchscreen.tap(float(q['x']),float(q['y'])); r='tapped'
            elif c=='click':
                await page.mouse.click(float(q['x']),float(q['y'])); r='clicked'
            elif c=='wait':
                await page.wait_for_timeout(float(q['s'])*1000); r='waited'
            elif c=='text':
                r=await page.evaluate("""()=>{const out=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_ELEMENT);let n;
                 while(n=w.nextNode()){if(n.children.length&&[...n.childNodes].every(x=>x.nodeType!==3||!x.textContent.trim()))continue;
                 const s=getComputedStyle(n);if(s.display=='none'||s.visibility=='hidden'||+s.opacity==0)continue;
                 const b=n.getBoundingClientRect();if(b.width<1||b.height<1||b.bottom<0||b.top>innerHeight||b.right<0||b.left>innerWidth)continue;
                 const t=[...n.childNodes].filter(x=>x.nodeType===3).map(x=>x.textContent.trim()).join(' ').trim()||(n.tagName=='BUTTON'?n.innerText.trim():'');
                 if(!t)continue;out.push(`[${Math.round(b.left)},${Math.round(b.top)} ${Math.round(b.width)}x${Math.round(b.height)} ${s.fontSize}${n.tagName=='BUTTON'?' BTN':''}] ${t.slice(0,160)}`)}return out.join('\\n')}""")
            elif c=='fps':
                r=await page.evaluate("()=>new Promise(res=>{let n=0;const t0=performance.now();function f(){n++;if(performance.now()-t0<3000)requestAnimationFrame(f);else res(n/3)}requestAnimationFrame(f)})")
            elif c=='vp':
                await page.set_viewport_size({'width':int(q['w']),'height':int(q['h'])}); r='vp'
            elif c=='js':
                r=await page.evaluate(q['e'])
            elif c=='logs': r='\n'.join(logs[-30:]); logs.clear()
            elif c=='key': await page.keyboard.press(q['k']); r='key'
            elif c=='type': await page.keyboard.type(q['t']); r='typed'
            elif c=='drag':
                # touch drag via CDP
                cdp=await ctx.new_cdp_session(page)
                x1,y1,x2,y2=[float(q[k]) for k in('x1','y1','x2','y2')]
                await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x1,'y':y1}]})
                n=10
                for i in range(1,n+1):
                    await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x1+(x2-x1)*i/n,'y':y1+(y2-y1)*i/n}]})
                    await page.wait_for_timeout(30)
                if q.get('hold'): await page.wait_for_timeout(float(q['hold'])*1000)
                await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]}); r='dragged'
            else: r='?'
        except Exception as e: r='ERR '+repr(e)
        return web.Response(text=str(r))
    app=web.Application(); app.router.add_get('/cmd',h)
    runner=web.AppRunner(app); await runner.setup(); await web.TCPSite(runner,'127.0.0.1',8765).start()
    await page.goto(GAME)
    print('ready',flush=True)
    while True: await asyncio.sleep(3600)
asyncio.run(main())
