"""오늘의 역 카드 렌더러. 사용: python3 render.py YYYY-MM-DD out.png  → out.png + 캡션 JSON(stdout)"""
import sys,asyncio,json,os
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__))
LUNAR=open(os.path.join(D,'lunar.js')).read()
def chrome():
    for p in ['/usr/bin/google-chrome','/usr/bin/chromium','/usr/bin/chromium-browser']:
        if os.path.exists(p): return p
async def main(day,out):
    y,m,d=day.split('-')
    async with async_playwright() as p:
        kw={'args':['--no-sandbox']};c=chrome()
        if c: kw['executable_path']=c
        b=await p.chromium.launch(**kw)
        ctx=await b.new_context(viewport={'width':1080,'height':1500},timezone_id='Asia/Seoul')
        pg=await ctx.new_page()
        await pg.route('**/lunar.js',lambda r:r.fulfill(body=LUNAR,content_type='application/javascript'))
        await pg.route('**fonts.g*',lambda r:r.abort())
        await pg.goto(f'file://{D}/index.html#d{y}{m}{d}')
        await pg.wait_for_timeout(1200)
        await pg.locator('#card').screenshot(path=out,type='jpeg',quality=93)
        t=lambda i:pg.eval_on_selector('#'+i,'e=>e.innerText.replace(/\\s+/g," ").trim()')
        info={k:await t(k) for k in ['big','lu','yr','tn','hw','hk','zt','xn','xs','word']}
        g=await pg.eval_on_selector('#gua .n','e=>e.innerText.replace(/\\s+/g," ").trim()')
        gm=await pg.eval_on_selector('#gua .m','e=>e.innerText.trim()')
        info['gua']=g;info['gua_m']=gm
        await b.close()
    lu=info['lu'].split(' 十')[0].split(' 正')[0].split(' 冬')[0].split(' 腊')[0]
    import re
    m=re.match(r'(\S+?)([\u4e00-\u9fff]+)$',info['tn']);tn=f"{m.group(1)}({m.group(2)})" if m else info['tn']
    zh,za=(info['zt'].split(' ',1)+[''])[:2];zt=f"{za}날({zh}日)"
    cap=(f"오늘의 역 曆 · {info['big']}\n"
         f"{lu} · {info['yr'].split(' · ',1)[-1]}\n\n"
         f"🌾 절기 {tn} — {info['hw']} {info['hk']}\n"
         f"🐾 일진 {zt}\n"
         f"✦ 별자리 {info['xn']} · {info['xs']}\n"
         f"☯ 오늘의 괘 {info['gua']} — {info['gua_m']}\n\n"
         f"“{info['word']}”\n\n"
         "#오늘의역 #동양책력 #절기 #음력 #사주 #일진 #28수 #이십팔수 #주역 #오늘의괘 #수묵화 #십이지신 #천상열차분야지도")
    print(json.dumps({'caption':cap,'info':info},ensure_ascii=False))
asyncio.run(main(sys.argv[1],sys.argv[2]))
