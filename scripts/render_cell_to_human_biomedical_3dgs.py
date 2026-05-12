#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render 《从细胞到人体：生命系统自组织的三维演化》.

A safe abstract biomedical-documentary style 3DGS-like visualization.
"""
from __future__ import annotations
import argparse, math, subprocess, wave
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/videos/cell_to_human_body_biomedical_3dgs_180s.mp4"
POSTER = ROOT / "assets/posters/cell_to_human_body_biomedical_3dgs_poster.png"
TITLE_CN = "从细胞到人体：生命系统自组织的三维演化"
SUBTITLE_EN = "From Cell to Human Body: A 3D Visualization of Biological Self-Organization"

STAGES = [
    (0,20,"单细胞：生命的起点","细胞膜、细胞核、胞质流动与显微微环境"),
    (20,40,"分裂：从一到多","细胞间信号脉冲与空间秩序逐渐出现"),
    (40,65,"分化：细胞获得身份","神经、循环、骨骼、肌肉、上皮与代谢方向形成"),
    (65,90,"形态发生：身体蓝图浮现","组织片层折叠、卷曲、分层与身体轴线建立"),
    (90,120,"器官形成：局部功能模块生成","透明器官结构、神经网络、循环系统、骨骼支架与肌纤维束显现"),
    (120,145,"系统耦合：生命体成为整体","神经、循环、代谢、免疫与内分泌网络同步运行"),
    (145,165,"涌现：从细胞到人体","细胞点云、组织层、器官与系统网络汇聚成人体轮廓"),
    (165,180,"边界：理解生命，而非制造生命","科学理解伴随敬畏、边界与责任"),
]
NARR = [(0,"生命的起点，可以简单到一个细胞。"),(22,"分裂并不只是数量增加，更意味着细胞关系开始形成。"),(43,"相同起点的细胞，在空间和时间中走向不同命运。"),(68,"身体不是外部拼装的产物，而是在组织重排中逐渐生成。"),(94,"器官是局部细胞群与整体需求之间形成的功能秩序。"),(122,"多个系统相互耦合，多细胞集合体才成为动态生命体。"),(148,"从细胞到人体，是一次跨尺度的生命系统涌现。"),(167,"理解生命，不等于任意制造生命。")]

# BGR biomedical palette for OpenCV.
COL = dict(bg0=np.array([30,18,8.],np.float32), bg1=np.array([72,38,16.],np.float32), bg2=np.array([126,105,82.],np.float32),
           white=np.array([252,250,248.],np.float32), membrane=np.array([250,210,130.],np.float32), cell=np.array([255,190,112.],np.float32),
           nucleus=np.array([150,232,255.],np.float32), info=np.array([248,175,230.],np.float32), neural=np.array([255,160,205.],np.float32),
           vascular=np.array([76,126,255.],np.float32), skeletal=np.array([226,240,242.],np.float32), muscle=np.array([94,115,222.],np.float32),
           epithelial=np.array([230,238,152.],np.float32), metabolic=np.array([150,225,255.],np.float32), immune=np.array([180,255,170.],np.float32), endocrine=np.array([246,178,228.],np.float32))
rng=np.random.default_rng(13); cache={}

def font(bold=False):
    paths=["/System/Library/Fonts/PingFang.ttc","/System/Library/Fonts/Supplemental/Songti.ttc","/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]
    return next((p for p in paths if Path(p).exists()), "DejaVuSans.ttf")
FONT_REG, FONT_BOLD = font(False), font(True)
def norm(x): return x/np.maximum(1e-8,np.linalg.norm(x,axis=1,keepdims=True))
def ss(a,b,x):
    if x<=a: return 0.0
    if x>=b: return 1.0
    t=(x-a)/(b-a); return t*t*(3-2*t)
def stamp(n):
    n=max(4,int(n)); n+=n%2
    if n not in cache:
        y,x=np.mgrid[-1:1:complex(0,n),-1:1:complex(0,n)]; a=np.exp(-(x*x+y*y)/(2*.34*.34)).astype(np.float32); cache[n]=a/a.max()
    return cache[n]
def blend(img,x,y,n,col,a):
    st=stamp(n); h=st.shape[0]//2; x0,x1=max(0,x-h),min(img.shape[1],x+h); y0,y1=max(0,y-h),min(img.shape[0],y+h)
    if x0>=x1 or y0>=y1: return
    sx0,sx1=h-(x-x0),h+(x1-x); sy0,sy1=h-(y-y0),h+(y1-y); aa=st[sy0:sy1,sx0:sx1][...,None]*a
    img[y0:y1,x0:x1]=img[y0:y1,x0:x1]*(1-aa)+col*aa
def ry(p,a):
    s,c=math.sin(a),math.cos(a); return p@np.array([[c,0,s],[0,1,0],[-s,0,c]],np.float32).T
def proj(p,w,h,scale,center=(0,0),cz=6.1):
    z=np.maximum(.35,p[:,2]+cz); return (w/2+center[0]+p[:,0]*scale/z).astype(int),(h/2+center[1]-p[:,1]*scale/z).astype(int),z

def pts(img,p,col,w,h,scale=470,center=(0,0),alpha=.7,size=16,ang=0):
    pp=ry(p.astype(np.float32),ang); x,y,z=proj(pp,w,h,scale,center); c=COL[col]
    for i in np.argsort(z)[::-1]:
        if 0<=x[i]<w and 0<=y[i]<h: blend(img,int(x[i]),int(y[i]),max(5,int(size*4.8/z[i])),c,float(alpha*np.clip(1.7/z[i],.25,1)))

def now_stage(t):
    for a,b,c,d in STAGES:
        if a<=t<b: return c,d
    return STAGES[-1][2],STAGES[-1][3]
def now_narr(t):
    v=NARR[0][1]
    for a,b in NARR:
        if t>=a: v=b
    return v

CELL=norm(rng.normal(size=(180,3)))*(rng.random((180,1))**(1/3)); VES=norm(rng.normal(size=(90,3)))*(rng.random((90,1))**(1/3))*.78
la=np.linspace(0,10*np.pi,108); LINE=np.c_[np.cos(la)*np.linspace(.2,2.6,108),np.sin(la)*np.linspace(.2,2.6,108),np.sin(la*.37)*.9]
by=np.linspace(-2.35,2.62,400); th=rng.random(400)*2*np.pi; br=.16+.74*np.exp(-((by-.15)/1.22)**2)+.48*np.exp(-((by-2.13)/.42)**2)
BODY=np.c_[np.cos(th)*br*rng.uniform(.25,1,400),by,np.sin(th)*br*.42]
for s in (-1,1):
    ay=np.linspace(1.48,-.45,78); ly=np.linspace(-.45,-2.55,88)
    BODY=np.vstack([BODY,np.c_[np.full_like(ay,s*1.06)+rng.normal(scale=.07,size=ay.shape),ay,rng.normal(scale=.09,size=ay.shape)],np.c_[np.full_like(ly,s*.42)+rng.normal(scale=.06,size=ly.shape),ly,rng.normal(scale=.07,size=ly.shape)]])
ORG={"brain":(np.array([0,2.18,.02]),70,np.array([.33,.24,.18]),"neural"),"heart":(np.array([-.22,.85,.13]),44,np.array([.12,.14,.10]),"vascular"),"lung_l":(np.array([-.46,1.1,.03]),62,np.array([.24,.42,.16]),"cell"),"lung_r":(np.array([.46,1.1,.03]),62,np.array([.24,.42,.16]),"cell"),"liver":(np.array([.28,-.05,.05]),50,np.array([.30,.16,.12]),"metabolic"),"gut":(np.array([0,-.72,0]),66,np.array([.33,.27,.14]),"epithelial")}
OP={k:rng.normal(size=(n,3))*sc+c for k,(c,n,sc,co) in ORG.items()}; TARGETS=BODY[rng.choice(len(BODY),56,replace=False)]

def bg(w,h,t):
    y,x=np.mgrid[0:h,0:w]; cx=w*(.51+.035*math.sin(t*.011)); cy=h*(.46+.025*math.cos(t*.017)); r=np.sqrt((x-cx)**2+(y-cy)**2)/(.84*max(w,h)); r=np.clip(r,0,1)[...,None]
    q=ss(92,160,t); im=COL['bg0']*r+((1-q)*COL['bg1']+q*COL['bg2'])*(1-r); ov=np.zeros_like(im)
    for k in range(30):
        yy=int((k*31+20*math.sin(t*.02+k))%h); x0=int((k*73+t*2)%w); x1=int((x0+180+40*math.sin(k))%w); cv2.line(ov,(x0,yy),(x1,int(yy+22*math.sin(k+t*.02))),COL['membrane'].tolist(),1,lineType=cv2.LINE_AA)
    im=np.clip(im+ov*.10,0,255)
    for i in range(72): blend(im,int((i*97+t*(2+i%3))%w),int((i*43+70*math.sin(i+t*.035))%h),5,COL['cell'],.20)
    return im.astype(np.float32)

def tissue(img,w,h,t,a):
    ov=np.zeros_like(img); cx,cy=w//2,h//2+12
    for layer,col in enumerate(['cell','neural','epithelial','metabolic']):
        last=None
        for i in range(190):
            u=(i/189-.5)*2; x=int(cx+u*305*a); y=int(cy+(math.sin(u*math.pi*2+t*.52+layer)*50+layer*20-38)*a)
            if last: cv2.line(ov,last,(x,y),COL[col].tolist(),2,lineType=cv2.LINE_AA)
            if i%18==0: blend(ov,x,y,10,COL[col],.65)
            last=(x,y)
    img[:]=np.clip(img+ov*.48,0,255)

def systems(img,w,h,t,q):
    a=t*.155; center=(95,12); scale=478; pts(img,BODY*q,'cell',w,h,scale,center,.45,13,a); pts(img,BODY*q,'skeletal',w,h,scale,center,.16,10,a)
    for name,(c,n,sc,co) in ORG.items(): pts(img,OP[name]*q*(1+.08*math.sin(t*2.6) if name=='heart' else 1),co,w,h,scale,center,(.92 if name=='heart' else .62)*q,16,a)
    ov=np.zeros_like(img); spine=np.c_[np.zeros(22),np.linspace(2.05,-2.25,22),np.zeros(22)]*q; x,y,_=proj(ry(spine.astype(np.float32),a),w,h,scale,center)
    for i in range(len(x)-1): cv2.line(ov,(x[i],y[i]),(x[i+1],y[i+1]),COL['skeletal'].tolist(),1,lineType=cv2.LINE_AA)
    for k in range(22):
        side=-1 if k%2 else 1; fib=np.array([[side*.25,1.1-k*.10,.08],[side*.55,.8-k*.09,.06],[side*.35,.45-k*.08,.08]])*q; x,y,_=proj(ry(fib.astype(np.float32),a),w,h,scale,center); cv2.polylines(ov,[np.c_[x,y].astype(np.int32)],False,COL['muscle'].tolist(),1,lineType=cv2.LINE_AA)
    img[:]=np.clip(img+ov*.72,0,255)

def feedback(img,w,h,t):
    ov=np.zeros_like(img); center=(95,12); scale=478; a=t*.155; src=[ORG['brain'][0],ORG['heart'][0],ORG['liver'][0]]; cols=[COL['neural'],COL['vascular'],COL['metabolic']]
    for idx,target in enumerate(TARGETS[:42]):
        u=np.linspace(0,1,18); path=np.outer(1-u,src[idx%3])+np.outer(u,target); path[:,0]+=.10*np.sin(u*np.pi*2+t*.08+idx); path[:,2]+=.10*np.cos(u*np.pi*2+t*.07+idx); x,y,_=proj(ry(path.astype(np.float32),a),w,h,scale,center)
        for i in range(len(x)-1): cv2.line(ov,(x[i],y[i]),(x[i+1],y[i+1]),cols[idx%3].tolist(),1,lineType=cv2.LINE_AA)
        if idx%5==0: blend(ov,x[(idx*3)%len(x)],y[(idx*3)%len(y)],9,COL['immune'],.75)
    cx,cy=int(w*.58),int(h*.52)
    for k,col in enumerate(['neural','vascular','endocrine','immune','metabolic']): cv2.ellipse(ov,(cx,cy),(82+35*k,int((82+35*k)*.56)),int(t*3+k*15),0,360,COL[col].tolist(),1,lineType=cv2.LINE_AA)
    img[:]=np.clip(img+ov*.45,0,255)

def hud(img,t,dur,w,h):
    pil=Image.fromarray(cv2.cvtColor(np.clip(img,0,255).astype(np.uint8),cv2.COLOR_BGR2RGB)); d=ImageDraw.Draw(pil); ft=ImageFont.truetype(FONT_BOLD,max(18,int(w*.026))); fs=ImageFont.truetype(FONT_REG,max(13,int(w*.014))); fh=ImageFont.truetype(FONT_BOLD,max(17,int(w*.020)))
    title,desc=now_stage(t)
    def tx(xy,s,font,fill): x,y=xy; d.text((x+2,y+2),s,font=font,fill=(0,0,0)); d.text((x,y),s,font=font,fill=fill)
    tx((40,26),TITLE_CN,ft,(248,250,252)); tx((42,66),SUBTITLE_EN,fs,(199,210,254)); py=h-150; d.rounded_rectangle((34,py,min(w-34,850),h-34),radius=18,fill=(7,15,32),outline=(130,196,245),width=1); tx((56,py+14),title,fh,(254,243,199)); tx((56,py+46),desc,fs,(228,232,240)); tx((56,py+76),now_narr(t),fs,(204,214,225)); d.rounded_rectangle((42,h-22,w-42,h-16),radius=3,fill=(44,60,80)); d.rounded_rectangle((42,h-22,42+int((w-84)*t/dur),h-16),radius=3,fill=(254,243,199)); return cv2.cvtColor(np.array(pil),cv2.COLOR_RGB2BGR).astype(np.float32)

def draw_frame(t,dur,w,h):
    img=bg(w,h,t); p=ss(0,18,t); fade=1-ss(50,72,t); cx=int(w*(.50-.08*ss(16,40,t))); cy=int(h*.49); rr=48+70*p
    if fade>.02:
        ov=np.zeros_like(img); cv2.circle(ov,(cx,cy),int(rr+20),COL['membrane'].tolist(),2,lineType=cv2.LINE_AA); cv2.circle(ov,(cx,cy),int(rr),COL['cell'].tolist(),1,lineType=cv2.LINE_AA); img=np.clip(img+ov*.32*fade,0,255); pts(img,CELL*(.72+.36*p),'cell',w,h,rr*4.8,(cx-w/2,cy-h/2),.42*fade,14,t*.12); pts(img,VES*(.66+.30*p),'metabolic',w,h,rr*4.8,(cx-w/2,cy-h/2),.32*fade,9,-t*.15); blend(img,cx,cy,int(rr*.42),COL['nucleus'],.45*fade)
        for i in range(32): a=i/32*math.pi*4+t*.7; blend(img,int(cx+math.cos(a)*rr*.22),int(cy-rr*.35+i/32*rr*.7),7,COL['info'],.55*fade)
    div=ss(20,38,t)*(1-ss(44,58,t))
    if div>.02:
        n=int(3+36*ss(20,40,t)); ids=np.arange(n); ph=np.arccos(1-2*(ids+.5)/n); th=np.pi*(1+5**.5)*ids; cl=np.c_[np.sin(ph)*np.cos(th),np.cos(ph),np.sin(ph)*np.sin(th)]*(.2+1.25*ss(20,40,t)); pts(img,cl,'nucleus',w,h,420,(0,0),.55*div,20,t*.22); x,y,_=proj(ry(cl.astype(np.float32),t*.22),w,h,420); ov=np.zeros_like(img)
        for i in range(n):
            if i%3==0: cv2.line(ov,(x[i],y[i]),(x[(i+5)%n],y[(i+5)%n]),COL['cell'].tolist(),1,lineType=cv2.LINE_AA)
        img=np.clip(img+ov*.32*div,0,255)
    lin=ss(40,55,t)*(1-ss(72,92,t))
    if lin>.02:
        colors=['neural','vascular','skeletal','muscle','epithelial','metabolic']; ov=np.zeros_like(img)
        for j,col in enumerate(colors):
            p2=LINE[j*18:(j+1)*18]*(.8+.75*ss(40,65,t)); p2[:,0]+=(j-2.5)*.35; pts(img,p2,col,w,h,400,(-90,0),.62*lin,16,t*.19); x,y,_=proj(ry(p2.astype(np.float32),t*.19),w,h,400,center=(-90,0))
            for i in range(len(x)-1): cv2.line(ov,(x[i],y[i]),(x[i+1],y[i+1]),COL[col].tolist(),1,lineType=cv2.LINE_AA)
        img=np.clip(img+ov*.32*lin,0,255)
    morph=ss(65,82,t)*(1-ss(94,108,t))
    if morph>.02: tissue(img,w,h,t,morph); pts(img,BODY*morph,'skeletal',w,h,458,(92,15),.18*morph,10,t*.14)
    bodyq=ss(88,112,t)
    if bodyq>.02: systems(img,w,h,t,max(.1,bodyq))
    if t>=118: feedback(img,w,h,t)
    if t>=145: pts(img,BODY*1.08,'white',w,h,505,(95,10),.09*ss(145,160,t),16,t*.18)
    if t>=165:
        e=ss(165,174,t); ov=np.zeros_like(img); bx,by=int(w*.58),int(h*.31)
        for i in range(24): a=i/24*2*math.pi+t*.04; x2=int(bx+math.cos(a)*180); y2=int(by+math.sin(a)*105); cv2.line(ov,(bx,by),(x2,y2),COL['neural'].tolist(),1,lineType=cv2.LINE_AA); blend(ov,x2,y2,7,COL['metabolic'],.65)
        img=np.clip(img+ov*.38*e,0,255); blend(img,int(w*.18),int(h*.35),42,COL['cell'],.30*e); blend(img,int(w*.18),int(h*.35),18,COL['nucleus'],.42*e)
    return np.clip(hud(img,t,dur,w,h),0,255).astype(np.uint8)

def audio(path,dur,sr=44100):
    t=np.arange(int(sr*dur))/sr; ramp=np.minimum(1,t/12)*np.minimum(1,(dur-t)/10); sig=(.032*np.sin(2*np.pi*55*t)+.018*np.sin(2*np.pi*110*t+.4*np.sin(2*np.pi*.04*t))+.006*np.sin(2*np.pi*330*t)*((t>118)&(t<170)))*ramp; pcm=(np.clip(sig,-.12,.12)*32767).astype(np.int16)
    with wave.open(str(path),'wb') as wf: wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(pcm.tobytes())

def open_writer(stem,fps,size):
    for suffix,codec in [('.avi','MJPG'),('.mp4','mp4v')]:
        path=stem.with_suffix(suffix); vw=cv2.VideoWriter(str(path),cv2.VideoWriter_fourcc(*codec),fps,size)
        if vw.isOpened(): return vw,path
    raise RuntimeError('OpenCV VideoWriter failed to open any supported temporary format')

def render(output,dur,fps,w,h,poster):
    output.parent.mkdir(parents=True,exist_ok=True); poster.parent.mkdir(parents=True,exist_ok=True); vw,tmp=open_writer(output.with_name(output.stem+'_silent_tmp'),fps,(w,h)); wav=output.with_name(output.stem+'_ambient_tmp.wav'); total=int(dur*fps); pf=None
    for i in range(total):
        t=i/fps; fr=draw_frame(t,dur,w,h); vw.write(fr); pf=(abs(t-152),fr.copy()) if pf is None or abs(t-152)<pf[0] else pf
        if i%max(1,fps*10)==0: print(f'rendered {i}/{total} frames ({t:.1f}s)',flush=True)
    vw.release()
    if not tmp.exists() or tmp.stat().st_size==0: raise RuntimeError(f'temporary video not created: {tmp}')
    cv2.imwrite(str(poster),pf[1] if pf else draw_frame(152,dur,w,h)); audio(wav,dur)
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(tmp),'-i',str(wav),'-c:v','libx264','-pix_fmt','yuv420p','-preset','veryfast','-crf','22','-c:a','aac','-b:a','96k','-shortest',str(output)],check=True)
    tmp.unlink(missing_ok=True); wav.unlink(missing_ok=True); print('Wrote',output)

def main():
    ap=argparse.ArgumentParser(description='Render a safe biomedical 3DGS-style 180-second visualization video.'); ap.add_argument('--output',type=Path,default=OUT); ap.add_argument('--duration',type=float,default=180); ap.add_argument('--fps',type=int,default=4); ap.add_argument('--width',type=int,default=960); ap.add_argument('--height',type=int,default=540); ap.add_argument('--poster',type=Path,default=POSTER)
    a=ap.parse_args(); render(a.output,a.duration,a.fps,a.width,a.height,a.poster)
if __name__=='__main__': main()
