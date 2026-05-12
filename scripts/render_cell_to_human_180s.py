#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""180-second safe conceptual renderer for 《从单细胞到人类》.

This is a scientific visualization script, not a wet-lab protocol. It uses
abstract particles, translucent membranes, lineage fields, organ-like networks
and a glowing non-realistic human outline. It contains no gene sequence, vector,
culture condition, cloning workflow, embryo manipulation, or actionable biology.
"""
from __future__ import annotations
import argparse, math, subprocess, wave
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "videos" / "cell_to_human_180s.mp4"
POSTER = ROOT / "assets" / "posters" / "cell_to_human_poster.png"
FONT_REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
C = dict(blue=(255,198,122), blue2=(255,155,78), gold=(120,235,255), purple=(255,155,190),
         red=(34,120,255), ivory=(238,245,255), warm=(82,104,250), cyan=(235,235,103), white=(248,250,252))
STAGES = [
    (0,20,"单细胞：生命的起点","边界、信息、能量与响应能力在一个动态系统中聚合"),
    (20,40,"分裂：从一到多","数量增加只是表象，细胞之间的关系开始出现"),
    (40,65,"分化：细胞获得身份","相同起点的细胞在不同时间、位置与环境中走向不同命运"),
    (65,90,"形态发生：身体蓝图浮现","迁移、折叠、分层与反馈推动整体形态生成"),
    (90,120,"器官形成：局部功能模块生成","器官不是零件，而是细胞群自然涌现出的功能秩序"),
    (120,145,"系统耦合：生命体成为整体","神经、循环、代谢、免疫和内分泌系统开始协同"),
    (145,165,"涌现：从细胞到人","微观细胞行为跨越尺度，汇聚成完整生命轮廓"),
    (165,180,"边界：理解生命，而非制造生命","科学理解必须伴随敬畏、边界与责任"),
]
NARR = [(0,"生命的起点，可以简单到一个细胞。"),(22,"当它开始分裂，真正重要的是细胞之间开始建立关系。"),
        (43,"随后，相同起点的细胞走向不同命运。"),(68,"身体并不是被外部拼装出来的。"),
        (94,"每一个器官，都不是单独制造出来的部件。"),(122,"多个系统开始耦合，多细胞集合体才真正成为生命体。"),
        (148,"从细胞到人，是一次跨越尺度的涌现。"),(167,"理解生命，不等于任意制造生命。")]
rng=np.random.default_rng(42)
cell=rng.normal(size=(160,3)); cell/=np.linalg.norm(cell,axis=1,keepdims=True); cell*=rng.random((160,1))**(1/3)
body_y=np.linspace(-2.2,2.55,240); th=rng.random(240)*2*np.pi
br=.18+.72*np.exp(-((body_y-.2)/1.18)**2)+.42*np.exp(-((body_y-2.12)/.40)**2)
body=np.c_[np.cos(th)*br*rng.uniform(.3,1,240), body_y, np.sin(th)*br*.36]
line_a=np.linspace(0,10*np.pi,80); lineage=np.c_[np.cos(line_a)*np.linspace(.25,2.35,80),np.sin(line_a)*np.linspace(.25,2.35,80),np.sin(line_a*.37)*.85]
org={"brain":np.array([0,2.25,.05]),"heart":np.array([-.22,.83,.18]),"lung_l":np.array([-.47,1.05,.05]),"lung_r":np.array([.47,1.05,.05]),"liver":np.array([.25,-.15,.05]),"gut":np.array([0,-.62,0])}

def ss(a,b,x):
    x=max(0,min(1,(x-a)/max(1e-6,b-a))); return x*x*(3-2*x)
def rot(p, ay):
    s,c=math.sin(ay),math.cos(ay); R=np.array([[c,0,s],[0,1,0],[-s,0,c]]); return p@R.T
def proj(p,w,h,scale=460,cz=5.8,center=(0,0)):
    z=np.maximum(.4,p[:,2]+cz); return (w/2+center[0]+p[:,0]*scale/z).astype(int),(h/2+center[1]-p[:,1]*scale/z).astype(int),z
def stage(t):
    for a,b,x,y in STAGES:
        if a<=t<b: return x,y
    return STAGES[-1][2],STAGES[-1][3]
def narr(t):
    s=NARR[0][1]
    for a,b in NARR:
        if t>=a: s=b
    return s

def bg(w,h,t):
    y,x=np.ogrid[:h,:w]; cx=w*(.5+.06*math.sin(t*.012)); cy=h*(.45+.04*math.cos(t*.017))
    r=np.sqrt((x-cx)**2+(y-cy)**2); rr=np.clip(r/(.78*max(w,h)),0,1)[...,None]
    early=np.array([8,14,32.]); mid=np.array([12,32,74.]); late=np.array([58,68,91.]); q=ss(80,150,t)
    arr=early*rr+(mid*(1-q)+late*q)*(1-rr); return np.clip(arr,0,255).astype(np.uint8)[:,:,::-1].copy()
def circ(im,x,y,r,col,a=.5,th=-1):
    ov=np.zeros_like(im); cv2.circle(ov,(int(x),int(y)),int(r),col,th,lineType=cv2.LINE_AA); cv2.addWeighted(ov,a,im,1,0,im)
def pts(im,p,col,w,h,scale=460,center=(0,0),rad=2,a=.7,ay=0):
    x,y,z=proj(rot(p,ay),w,h,scale,center=center); ov=np.zeros_like(im)
    for i in np.argsort(z)[::-1]:
        if 0<=x[i]<w and 0<=y[i]<h: cv2.circle(ov,(x[i],y[i]),max(1,int(rad*6/z[i])),col,-1,lineType=cv2.LINE_AA)
    cv2.addWeighted(ov,a,im,1,0,im)
def body_system(im,t,w,h,q=1):
    pts(im,body*q,C['blue'],w,h,470,(90,10),2,.55,t*.16)
    def one(p): x,y,_=proj(rot(np.array([p])*q,t*.16),w,h,470,center=(90,10)); return int(x[0]),int(y[0])
    ov=np.zeros_like(im)
    for name,axes,col,a in [('brain',(42,30),C['purple'],.42),('heart',(24,28),C['red'],.72),('lung_l',(30,54),C['blue'],.28),('lung_r',(30,54),C['blue'],.28),('liver',(42,26),C['gold'],.34),('gut',(46,38),C['cyan'],.25)]:
        cv2.ellipse(ov,one(org[name]),axes,0,0,360,col,-1,lineType=cv2.LINE_AA)
    for i in range(26):
        src=org['heart'] if i%2 else org['brain']; dst=body[(i*17)%len(body)]
        p=rot(np.vstack([src,dst])*q,t*.16); x,y,_=proj(p,w,h,470,center=(90,10)); cv2.line(ov,(x[0],y[0]),(x[1],y[1]),C['red'] if i%2 else C['blue2'],1,lineType=cv2.LINE_AA)
    cv2.addWeighted(ov,.78,im,1,0,im)

def draw_frame(t,dur,w,h):
    im=bg(w,h,t)
    for i in range(32): cv2.circle(im,(int((i*97+t*10*(1+i%3))%w),int((i*53+80*math.sin(t*.04+i))%h)),1,(120,150,200),-1)
    p=ss(0,20,t); cx=int(w*(.5-.06*ss(15,40,t))); cy=int(h*.5); r=50+70*p
    circ(im,cx,cy,r+24,C['blue'],.18,3); circ(im,cx,cy,r,C['blue'],.16,2); circ(im,cx,cy,r*.32,C['gold'],.55,-1)
    for i in range(34):
        a=i/33*math.pi*4+t*.7; cv2.circle(im,(int(cx+math.cos(a)*r*.24),int(cy-r*.35+i/33*r*.7)),2,C['gold'],-1,lineType=cv2.LINE_AA)
    pts(im,cell*(.75+.35*p),C['blue'],w,h,r*4.6,(cx-w/2,cy-h/2),2,.42,t*.18)
    if t>=20:
        q=ss(20,40,t); centers=[]
        for i in range(int(2+70*q)):
            phi=math.acos(1-2*(i+.5)/96); theta=math.pi*(1+5**.5)*i; centers.append([math.sin(phi)*math.cos(theta),math.cos(phi),math.sin(phi)*math.sin(theta)])
        pts(im,np.array(centers)*( .18+1.25*q),C['gold'],w,h,420,(0,0),8,.55,t*.22)
    if t>=40:
        q=ss(40,65,t); x,y,z=proj(rot(lineage*q*1.3,t*.2),w,h,430,center=(-90,0)); cols=[C['purple'],C['red'],C['ivory'],C['warm'],C['cyan']]
        ov=np.zeros_like(im)
        for i in range(len(x)-1): cv2.line(ov,(x[i],y[i]),(x[i+1],y[i+1]),cols[i%5],2,lineType=cv2.LINE_AA)
        cv2.addWeighted(ov,.72,im,1,0,im)
    if t>=65:
        q=ss(65,90,t); ov=np.zeros_like(im); cx2,cy2=w//2,h//2+20
        for layer,col in enumerate([C['blue'],C['purple'],C['cyan'],C['gold']]):
            old=None
            for i in range(160):
                u=(i/159-.5)*2; pt=(int(cx2+u*280*q),int(cy2+(math.sin(u*math.pi*2+t*.65+layer)*55+layer*20-40)*q))
                if old: cv2.line(ov,old,pt,col,2,lineType=cv2.LINE_AA)
                old=pt
        cv2.addWeighted(ov,.65,im,1,0,im)
    if t>=90: body_system(im,t,w,h,ss(90,120,t))
    if t>=120:
        body_system(im,t,w,h,1); ov=np.zeros_like(im); cx3,cy3=int(w*.58),int(h*.52)
        for k,col in enumerate([C['blue2'],C['red'],C['purple'],C['cyan'],C['gold']]): cv2.ellipse(ov,(cx3,cy3),(80+38*k,int((80+38*k)*.56)),k*18+t*4,0,360,col,1,lineType=cv2.LINE_AA)
        cv2.addWeighted(ov,.38,im,1,0,im)
    if t>=145: body_system(im,t,w,h,1)
    if t>=165:
        ov=np.zeros_like(im); cx4,cy4=int(w*.58),int(h*.31)
        for i in range(24):
            a=i/24*2*math.pi+t*.04; x=int(cx4+math.cos(a)*180); y=int(cy4+math.sin(a)*105); cv2.line(ov,(cx4,cy4),(x,y),C['purple'],1,lineType=cv2.LINE_AA); cv2.circle(ov,(x,y),3,C['gold'],-1)
        cv2.addWeighted(ov,.45,im,1,0,im)
    return text(im,t,dur,w,h)

def text(im,t,dur,w,h):
    pil=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)); d=ImageDraw.Draw(pil)
    fb=ImageFont.truetype(FONT_BOLD,max(20,int(w*.03))); fr=ImageFont.truetype(FONT_REG,max(12,int(w*.014)))
    fs=ImageFont.truetype(FONT_BOLD,max(17,int(w*.022))); fc=ImageFont.truetype(FONT_REG,max(13,int(w*.015)))
    title,cap=stage(t)
    def sh(pos,s,font,fill): d.text((pos[0]+2,pos[1]+2),s,font=font,fill=(0,0,0)); d.text(pos,s,font=font,fill=fill)
    sh((42,32),'从单细胞到人类',fb,(248,250,252)); sh((44,78),'From a Single Cell to a Human · Biological Self-Organization',fr,(199,210,254))
    y=h-150; d.rounded_rectangle((42,y,min(w-42,760),h-36),radius=18,fill=(4,12,28),outline=(148,197,253))
    sh((64,y+16),title,fs,(254,243,199)); sh((64,y+52),cap,fc,(226,232,240)); sh((64,y+82),narr(t),fr,(203,213,225))
    d.rounded_rectangle((42,h-26,w-42,h-20),radius=3,fill=(51,65,85)); d.rounded_rectangle((42,h-26,42+int((w-84)*t/dur),h-20),radius=3,fill=(254,243,199))
    return cv2.cvtColor(np.array(pil),cv2.COLOR_RGB2BGR)

def audio(path,dur,sr=44100):
    ts=np.arange(int(dur*sr))/sr; ramp=np.minimum(1,ts/16)*np.minimum(1,(dur-ts)/10)
    sig=(.035*np.sin(2*np.pi*55*ts)+.02*np.sin(2*np.pi*110*ts+.6*np.sin(2*np.pi*.03*ts))+.012*np.sin(2*np.pi*330*ts)*(ts>120)*(ts<166))*ramp
    pcm=(np.clip(sig,-.12,.12)*32767).astype(np.int16)
    with wave.open(str(path),'wb') as wf: wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(pcm.tobytes())

def render(output,dur,fps,w,h,poster):
    output.parent.mkdir(parents=True,exist_ok=True); poster.parent.mkdir(parents=True,exist_ok=True)
    tmp=output.with_name(output.stem+'_silent_tmp.mp4'); wav=output.with_name(output.stem+'_ambient_tmp.wav')
    vw=cv2.VideoWriter(str(tmp),cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h)); total=int(dur*fps); pf=None
    for i in range(total):
        t=i/fps; frame=draw_frame(t,dur,w,h); vw.write(frame); pf=frame if abs(t-150)<.5 else pf
        if i%max(1,fps*10)==0: print(f'rendered {i}/{total} frames ({t:.1f}s)',flush=True)
    vw.release(); cv2.imwrite(str(poster),pf if pf is not None else draw_frame(150,dur,w,h)); audio(wav,dur)
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(tmp),'-i',str(wav),'-c:v','libx264','-pix_fmt','yuv420p','-preset','veryfast','-crf','23','-c:a','aac','-b:a','96k','-shortest',str(output)],check=True)
    tmp.unlink(missing_ok=True); wav.unlink(missing_ok=True); print('Wrote',output)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=OUT); ap.add_argument('--duration',type=float,default=180); ap.add_argument('--fps',type=int,default=8); ap.add_argument('--width',type=int,default=1280); ap.add_argument('--height',type=int,default=720); ap.add_argument('--poster',type=Path,default=POSTER)
    a=ap.parse_args(); render(a.output,a.duration,a.fps,a.width,a.height,a.poster)
if __name__=='__main__': main()
