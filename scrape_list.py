import re, json, urllib.request, time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
URL="https://www.epcshow.com/exhibition-floorplan?page=%d"
def fetch(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=30).read().decode("utf-8","ignore")

# bounded, non-greedy-free parsing:
title_re=re.compile(r"aria-label=\"Exhibitor - (.*?) - Name\"")
slug_re=re.compile(r"openRemoteModal\('exhibitors/([a-z0-9\-]+)'")
stand_re=re.compile(r"__meta__stand[^>]*>\s*Stand:\s*([^<]*)<")

seen={}
for page in range(1,16):
    try: html=fetch(URL%page)
    except Exception as e:
        print("page",page,"err",e,flush=True); break
    # split into item blocks by the wrapper-two marker
    blocks=html.split('m-exhibitors-list__list__items__item__wrapper-two')
    cnt=0
    for b in blocks[1:]:
        b=b[:4000]  # bound each block
        ms=slug_re.search(b); mt=title_re.search(b); md=stand_re.search(b)
        if not ms: continue
        slug=ms.group(1)
        name=(mt.group(1) if mt else slug).replace("&amp;","&").strip()
        stand=(md.group(1).strip() if md else "")
        if slug not in seen:
            seen[slug]={"slug":slug,"name":name,"stand":stand}; cnt+=1
    print(f"page {page}: +{cnt} (total {len(seen)})",flush=True)
    if cnt==0 and page>1: break
    time.sleep(0.3)

data=list(seen.values())
json.dump(data,open("exhibitors_list.json","w"),ensure_ascii=False,indent=1)
print("TOTAL",len(data),"| missing stand:",sum(1 for d in data if not d["stand"]),flush=True)
