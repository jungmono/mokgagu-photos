import json,os,io,urllib.request
from PIL import Image
L=json.load(open('ov-list.json'))
os.makedirs('photos/overseas',exist_ok=True);os.makedirs('thumbs_ov',exist_ok=True)
fail=[]
for i,u in L:
    try:
        rq=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36','Referer':'https://www.christies.com/' if 'christies' in u else 'https://www.sothebys.com/','Accept':'image/*'})
        b=urllib.request.urlopen(rq,timeout=40).read()
        im=Image.open(io.BytesIO(b)).convert('RGB')
        a=im.copy();a.thumbnail((1000,1000));a.save(f'photos/overseas/{i}.jpg',quality=85)
        t=im.copy();t.thumbnail((300,300));c=Image.new('RGB',(300,300),'white');c.paste(t,((300-t.width)//2,(300-t.height)//2));c.save(f'thumbs_ov/{i}.jpg',quality=82)
    except Exception as e: fail.append((i,str(e)[:80]))
print('FAIL',fail)
open('ov-fail.txt','w').write(json.dumps(fail))
