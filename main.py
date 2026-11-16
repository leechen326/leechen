import json,os
from urllib.request import Request,urlopen as O
U=os.environ["MAKEFUN_ENV_URL"]
def P(p,b):return json.load(O(Request(U+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})))
V={"p":8,"n":26,"b":27,"r":42,"q":78,"k":900}
D={"n":((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)),"b":((1,1),(1,-1),(-1,-1),(-1,1)),"r":((1,0),(0,1),(-1,0),(0,-1)),"q":((1,1),(1,-1),(-1,-1),(-1,1),(1,0),(0,1),(-1,0),(0,-1)),"k":((1,1),(1,-1),(-1,-1),(-1,1),(1,0),(0,1),(-1,0),(0,-1))}
def fen(f):
 b=["."]*64
 for r,row in enumerate(f.split()[0].split("/")):
  c=0
  for x in row:
   if x.isdigit():c+=int(x)
   else:b[r*8+c]=x;c+=1
 return b
def sq(s):return(8-int(s[1]))*8+"abcdefgh".index(s[0])
def u(i,j,p):return"abcdefgh"[i&7]+str(8-(i>>3))+"abcdefgh"[j&7]+str(8-(j>>3))+p
def gen(b,w):
 m=[]
 for i,c in enumerate(b):
  if c=="."or c.isupper()!=w:continue
  t=c.lower();r=i>>3;f=i&7
  if t=="p":
   d=-8 if w else 8;j=i+d
   if 0<=j<64 and b[j]==".":
    m.append((i,j,"q" if j>>3 in(0,7)else""))
    j+=d
    if r==(6 if w else 1)and b[j]==".":m.append((i,j,""))
   for df in(-1,1):
    rr=r+(-1 if w else 1);ff=f+df
    if 0<=rr<8 and 0<=ff<8:
     j=rr*8+ff;x=b[j]
     if x!="."and x.isupper()!=w:m.append((i,j,"q" if rr in(0,7)else""))
  else:
   for df,dr in D[t]:
    rr=r+dr;ff=f+df
    while 0<=rr<8 and 0<=ff<8:
     j=rr*8+ff;x=b[j]
     if x==".":m.append((i,j,""))
     else:
      if x.isupper()!=w:m.append((i,j,""))
      break
     if t in"nk":break
     rr+=dr;ff+=df
 return m
def mv(b,m):
 i,j,p=m;b=b[:];c=b[i];x=b[j]
 if c.lower()=="p"and(i&7)!=(j&7)and x==".":b[j+(8 if c.isupper()else -8)]="."
 b[i]=".";b[j]=(p.upper()if c.isupper()else p.lower())if p else c
 if c.lower()=="k"and abs((j&7)-(i&7))==2:
  a,z=(i+3,i+1)if j>i else(i-4,i-1);b[z]=b[a];b[a]="."
 return b
def EV(b):
 s=0
 for i,c in enumerate(b):
  if c==".":continue
  t=c.lower();r=i>>3;f=i&7
  m=V[t]
  if t=="p":m+=(5-r if c.isupper()else r-2)*2
  elif t in"nb":m+=16-abs(2*r-7)-abs(2*f-7)
  elif t=="k":m+=(abs(2*r-7)+abs(2*f-7))>>1
  s+=m if c.isupper()else -m
 return s
n=0;CAP=180000
def Q(b,w,a,f):
 global n
 n+=1
 s=EV(b)*(1 if w else -1)
 if s>=f or n>CAP:return s
 if s>a:a=s
 for m in gen(b,w):
  if b[m[1]]==".":continue
  v=-Q(mv(b,m),not w,-f,-a)
  if v>s:
   s=v
   if s>a:a=s
   if a>=f:break
 return s
def S(b,w,d,a,f):
 global n
 n+=1
 if n>CAP:return 0
 if d<1:return Q(b,w,a,f)
 ms=gen(b,w)
 if not ms:return -9000
 ms.sort(key=lambda m:-(V[b[m[1]].lower()]if b[m[1]]!="."else 0))
 best=-99999
 for m in ms:
  x=b[m[1]]
  if x!="."and x.lower()=="k":return 9000-d
  v=-S(mv(b,m),not w,d-1,-f,-a)
  if v>best:
   best=v
   if v>a:a=v
   if a>=f:break
 return best
def pick(g,dep):
 global n
 b=fen(g["fen"]);w=" w "in" "+g["fen"].split(" ")[1]+" "
 best=g["legal_moves"][0];bs=-99999
 for s in g["legal_moves"]:
  n=0
  v=-S(mv(b,(sq(s[:2]),sq(s[2:4]),s[4:])),not w,dep-1,-99999,99999)
  if v>bs:bs=v;best=s
 return best
while 1:
 g=P("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  g=P("/move",{"game":g["game"],"move":pick(g,4)})
