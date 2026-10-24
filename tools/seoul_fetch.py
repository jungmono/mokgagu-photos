import json,os,sys,urllib.request,io
from PIL import Image
L=json.load(open('seoul-list.json'))
os.makedirs('photos/seoul',exist_ok=True); os.makedirs('thumbs-seoul',exist_ok=True)
cache={}; bad=[]
for pid,u in L:
    if u not in cache:
        try:
            rq=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0','Referer':'https://www.seoulauction.com/'})
            cache[u]=urllib.request.urlopen(rq,timeout=60).read()
        except Exception as e:
            bad.append((pid,str(e))); continue
    im=Image.open(io.BytesIO(cache[u])).convert('RGB')
    big=im.copy(); big.thumbnail((1000,1000)); big.save(f'photos/seoul/{pid}.jpg',quality=85,optimize=True)
    t=im.copy(); t.thumbnail((300,300)); bg=Image.new('RGB',(300,300),(245,242,236)); bg.paste(t,((300-t.width)//2,(300-t.height)//2)); bg.save(f'thumbs-seoul/{pid}.jpg',quality=80,optimize=True)
print('ok',len(L)-len(bad),'bad',bad)
open('seoul-report.txt','w').write(f'ok {len(L)-len(bad)} bad {bad}\n')
