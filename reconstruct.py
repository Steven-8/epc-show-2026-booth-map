import json, re, math, urllib.request

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
def fetch(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=30).read().decode("utf-8","ignore")

ex=json.load(open('exhibitors_list.json'))

# ---- logo map: scrape pages, map slug -> logo url ----
logos={}
for page in (1,2,3):
    try: html=fetch(f"https://www.epcshow.com/exhibition-floorplan?page={page}")
    except Exception: break
    for blk in html.split('m-exhibitors-list__list__items__item__wrapper')[1:]:
        b=blk[:2500]
        ms=re.search(r"openRemoteModal\('exhibitors/([a-z0-9\-]+)'",b)
        mi=re.search(r'src="(https://cdn\.asp\.events/[^"]+?(?:logo|exhibitors)[^"]+?\.(?:png|jpg|jpeg))',b,re.I)
        if not mi: mi=re.search(r'src="(https://cdn\.asp\.events/[^"]+?\.(?:png|jpg|jpeg))',b,re.I)
        if ms and mi and ms.group(1) not in logos:
            logos[ms.group(1)]=mi.group(1)
print("logos found:",len(logos))

# ---- parse stand -> (zone, number, span) ----
def parse_stand(s):
    s=s.strip().upper()
    parts=[p.strip() for p in s.split(',') if p.strip()]
    if not parts: return None
    m=re.match(r'^([A-Z]+)\s*0*([0-9]+)$',parts[0])
    if not m: return None
    zone=m.group(1); num=int(m.group(2))
    span=len(parts) if len(parts)>1 else 1
    return zone,num,span

placed=[]; tbd=[]
for x in ex:
    p=parse_stand(x['stand'])
    rec={"slug":x['slug'],"name":x['name'],"stand":x['stand'],"logo":logos.get(x['slug'],"")}
    if p:
        rec["zone"],rec["num"],rec["span"]=p
        placed.append(rec)
    else:
        tbd.append(rec)

# group by zone
from collections import defaultdict, OrderedDict
zmap=defaultdict(list)
for r in placed: zmap[r['zone']].append(r)
ZONES=sorted(zmap.keys())
for z in ZONES: zmap[z].sort(key=lambda r:r['num'])

# ---- layout (feet) ----
BOOTH=10.0           # standard 10x10 ft
AISLE_IN=0.0         # booths back-to-back within a block (real expos)
BLOCK_GAP=22.0       # cross-aisle between zone blocks
TARGET_W=360.0       # interior target width (ft) ~ approaches Hall A width 327
MARGIN=24.0

def block_dims(items):
    # count booth cells accounting for spans
    cells=sum(it['span'] for it in items)
    bcols=max(1,int(round(math.sqrt(cells*1.25))))
    return bcols

zone_blocks=[]
for z in ZONES:
    items=zmap[z]
    bcols=block_dims(items)
    # place booths within block grid, row-major by number, honoring span widths
    cells=[]
    cx=0; cy=0; rowmax_h=BOOTH
    col=0
    layout=[]
    x=0.0;y=0.0
    # simple row packer inside block
    cur_w=0.0; row_booths=[]; rows=[]
    for it in items:
        w=BOOTH*it['span']
        if col>0 and col+it['span']>bcols:
            rows.append(row_booths); row_booths=[]; col=0
        row_booths.append((it,w)); col+=it['span']
    if row_booths: rows.append(row_booths)
    # assign coords
    bw=0.0
    yy=0.0
    placed_local=[]
    for row in rows:
        xx=0.0
        for it,w in row:
            placed_local.append((it,xx,yy,w,BOOTH))
            xx+=w
        bw=max(bw,xx); yy+=BOOTH
    bh=yy
    zone_blocks.append({"zone":z,"w":bw,"h":bh,"booths":placed_local})

# shelf-pack blocks into TARGET_W
shelves=[]; cur=[]; cur_w=0.0
for blk in zone_blocks:
    if cur and cur_w+BLOCK_GAP+blk['w']>TARGET_W:
        shelves.append(cur); cur=[]; cur_w=0.0
    if cur: cur_w+=BLOCK_GAP
    cur.append(blk); cur_w+=blk['w']
if cur: shelves.append(cur)

booths=[]
oy=MARGIN
maxx=0.0
for shelf in shelves:
    sh_h=max(b['h'] for b in shelf)
    ox=MARGIN
    for blk in shelf:
        for it,lx,ly,w,h in blk['booths']:
            booths.append({
                "stand":it['stand'],"zone":blk['zone'],"num":it['num'],"span":it['span'],
                "slug":it['slug'],"name":it['name'],"logo":it['logo'],
                "x":round(ox+lx,2),"y":round(oy+ly,2),"w":w,"h":h
            })
        # zone label anchor stored via block origin -> compute later in JS; keep here
        ox+=blk['w']+BLOCK_GAP
        maxx=max(maxx,ox)
    oy+=sh_h+BLOCK_GAP
extent_w=maxx-BLOCK_GAP+MARGIN
extent_h=oy-BLOCK_GAP+MARGIN

# hall outline to scale: use Hall A (327x429) if fits else bounding
hall_w=max(327.0, math.ceil(extent_w/10)*10)
hall_h=max(extent_h, 0)
meta={
  "venue":"George R. Brown Convention Center · Houston",
  "show":"EPC Show 2026 — Energy Projects Conference & Expo",
  "level":"Level 1 · Exhibit Hall (to-scale reconstruction)",
  "unit":"feet","booth_standard":"10×10 ft","ceiling_ft":35,
  "hall_real_dims":"GRB Hall A 327×429 ft (Level 1, 35 ft clear)",
  "extent_w":round(extent_w,1),"extent_h":round(extent_h,1),
  "hall_w":round(hall_w,1),"hall_h":round(extent_h+ MARGIN,1),
  "n_booths":len(booths),"n_tbd":len(tbd),"zones":ZONES,
  "approximate":True
}
# zone block bounds for labels/coloring
zb=[]
for blk_shelf in []:
    pass
out={"meta":meta,"booths":booths,"tbd":tbd}
json.dump(out,open('booths.json','w'),ensure_ascii=False,indent=1)
print("placed booths:",len(booths),"| tbd:",len(tbd))
print("extent ft:",round(extent_w,1),"x",round(extent_h,1),"| zones:",len(ZONES))
