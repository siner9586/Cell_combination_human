#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Biomedical 3DGS-style renderer for
《从细胞到人体：生命系统自组织的三维演化》.

This script renders a safe, abstract, medical-documentary-style visualization.
It does not contain wet-lab protocols, gene sequences, cloning workflows,
embryo operations, or actionable biological engineering parameters.
"""
from __future__ import annotations
import argparse, math, subprocess, wave
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'videos' / 'cell_to_human_body_biomedical_3dgs_180s.mp4'
POSTER = ROOT / 'assets' / 'posters' / 'cell_to_human_body_biomedical_3dgs_poster.png'
FONT_REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

TITLE_CN = '从细胞到人体'
SUBTITLE_EN = 'From Cell to Human Body · Biological Self-Organization'

STAGES = [
    (0, 20, '单细胞：生命的起点', '细胞膜、细胞核、胞质流动与显微微环境'),
    (20, 40, '分裂：从一到多', '细胞数量增加，细胞间关系与空间秩序出现'),
    (40, 65, '分化：细胞获得身份', '谱系分化形成神经、循环、结构、肌肉、上皮与代谢方向'),
    (65, 90, '形态发生：身体蓝图浮现', '组织片层折叠、卷曲、分层，身体轴线逐渐明确'),
    (90, 120, '器官形成：局部功能模块生成', '透明器官结构、神经网络、循环系统、骨骼支架与肌纤维束显现'),
    (120, 145, '系统耦合：生命体成为整体', '神经、循环、代谢、免疫与内分泌网络同步运行'),
    (145, 165, '涌现：从细胞到人体', '细胞点云、组织层、器官与系统网络汇聚成人体轮廓'),
    (165, 180, '边界：理解生命，而非制造生命', '科学理解伴随敬畏、边界与责任'),
]
NARR = [
    (0, '生命的起点，可以简单到一个细胞。'),
    (22, '分裂并不只是数量增加，更意味着细胞关系开始形成。'),
    (43, '相同起点的细胞，在空间和时间中走向不同命运。'),
    (68, '身体不是外部拼装的产物，而是在组织重排中逐渐生成。'),
    (94, '器官是局部细胞群与整体需求之间形成的功能秩序。'),
    (122, '多个系统相互耦合，多细胞集合体才成为动态生命体。'),
    (148, '从细胞到人体，是一次跨尺度的生命系统涌现。'),
    (167, '理解生命，不等于任意制造生命。'),
]

# BGR colors for OpenCV: professional biomedical palette.
COL = {
    'bg1': np.array([30, 18, 8], np.float32),
    'bg2': np.array([76, 40, 16], np.float32),
    'bg3': np.array([112, 96, 74], np.float32),
    'white': np.array([252, 250, 248], np.float32),
    'membrane': np.array([250, 210, 130], np.float32),
    'cellblue': np.array([255, 190, 112], np.float32),
    'nucleus': np.array([150, 232, 255], np.float32),
    'neural': np.array([255, 160, 205], np.float32),
    'vascular': np.array([80, 126, 255], np.float32),
    'skeletal': np.array([225, 240, 242], np.float32),
    'muscle': np.array([96, 118, 218], np.float32),
    'epithelial': np.array([230, 236, 150], np.float32),
    'metabolic': np.array([150, 225, 255], np.float32),
    'immune': np.array([180, 255, 170], np.float32),
    'endocrine': np.array([246, 178, 228], np.float32),
}
rng = np.random.default_rng(13)

cell = rng.normal(size=(160, 3)); cell /= np.linalg.norm(cell, axis=1, keepdims=True); cell *= rng.random((160,1)) ** (1/3)
vesicles = rng.normal(size=(80, 3)); vesicles /= np.linalg.norm(vesicles, axis=1, keepdims=True); vesicles *= rng.random((80,1)) ** (1/3) * 0.8

line_a = np.linspace(0, 10*np.pi, 105)
lineage = np.c_[np.cos(line_a)*np.linspace(.2,2.55,105), np.sin(line_a)*np.linspace(.2,2.55,105), np.sin(line_a*.37)*.9]

body_y = np.linspace(-2.35, 2.62, 360)
th = rng.random(360) * 2*np.pi
body_r = .16 + .74*np.exp(-((body_y-.15)/1.22)**2) + .48*np.exp(-((body_y-2.13)/.42)**2)
body = np.c_[np.cos(th)*body_r*rng.uniform(.25,1,360), body_y, np.sin(th)*body_r*.42]
for side in (-1,1):
    arm_y = np.linspace(1.48, -.45, 70)
    arm = np.c_[np.full_like(arm_y, side*1.06)+rng.normal(scale=.07,size=arm_y.shape), arm_y, rng.normal(scale=.09,size=arm_y.shape)]
    leg_y = np.linspace(-.45, -2.55, 80)
    leg = np.c_[np.full_like(leg_y, side*.42)+rng.normal(scale=.06,size=leg_y.shape), leg_y, rng.normal(scale=.07,size=leg_y.shape)]
    body = np.vstack([body, arm, leg])

organs = {
    'brain': {'center': np.array([0.0, 2.18, 0.02]), 'n': 65, 'scale': np.array([.33,.24,.18]), 'color': 'neural'},
    'heart': {'center': np.array([-.22, .85, .13]), 'n': 42, 'scale': np.array([.12,.14,.10]), 'color': 'vascular'},
    'lung_l': {'center': np.array([-.46, 1.10, .03]), 'n': 58, 'scale': np.array([.24,.42,.16]), 'color': 'cellblue'},
    'lung_r': {'center': np.array([.46, 1.10, .03]), 'n': 58, 'scale': np.array([.24,.42,.16]), 'color': 'cellblue'},
    'liver': {'center': np.array([.28, -.05, .05]), 'n': 48, 'scale': np.array([.30,.16,.12]), 'color': 'metabolic'},
    'gut': {'center': np.array([0.0, -.72, .00]), 'n': 64, 'scale': np.array([.33,.27,.14]), 'color': 'epithelial'},
}
organ_points = {k: rng.normal(size=(v['n'],3))*v['scale'] + v['center'] for k,v in organs.items()}
sys_targets = body[rng.choice(len(body), size=52, replace=False)]

_stamp_cache = {}
def smoothstep(a,b,x):
    if x <= a: return 0.0
    if x >= b: return 1.0
    t = (x-a)/(b-a); return t*t*(3-2*t)
def stamp(size):
    size = max(4, int(size)); size += size % 2
    if size in _stamp_cache: return _stamp_cache[size]
    y,x = np.mgrid[-1:1:complex(0,size), -1:1:complex(0,size)]
    a = np.exp(-(x*x+y*y)/(2*.34*.34)).astype(np.float32); a /= a.max()
    _stamp_cache[size] = a; return a
def blend(img,x,y,size,color,alpha):
    a = stamp(size); hs=a.shape[0]//2
    x0,x1=max(0,x-hs),min(img.shape[1],x+hs); y0,y1=max(0,y-hs),min(img.shape[0],y+hs)
    if x0>=x1 or y0>=y1: return
    sx0,sx1=hs-(x-x0),hs+(x1-x); sy0,sy1=hs-(y-y0),hs+(y1-y)
    aa=a[sy0:sy1,sx0:sx1][...,None]*alpha; roi=img[y0:y1,x0:x1]
    roi[:] = roi*(1-aa) + color*aa
def rot_y(p,ang):
    s,c=math.sin(ang),math.cos(ang); return p @ np.array([[c,0,s],[0,1,0],[-s,0,c]],np.float32).T
def project(p,w,h,scale,cam_z=6.1,center=(0,0)):
    z=np.maximum(.35,p[:,2]+cam_z); x=w/2+center[0]+p[:,0]*scale/z; y=h/2+center[1]-p[:,1]*scale/z
    return x.astype(np.int32), y.astype(np.int32), z
def points(img, pts, color, w,h, scale=470, center=(0,0), alpha=.8, size=16, ay=0.0):
    p=rot_y(pts.astype(np.float32),ay); xs,ys,z=project(p,w,h,scale,center=center); col=COL[color] if isinstance(color,str) else color
    for i in np.argsort(z)[::-1]:
        if 0<=xs[i]<w and 0<=ys[i]<h:
            blend(img,int(xs[i]),int(ys[i]),max(5,int(size*4.8/z[i])),col,float(alpha*np.clip(1.7/z[i],.25,1)))
def stage(t):
    for a,b,c,d in STAGES:
        if a<=t<b: return c,d
    return STAGES[-1][2], STAGES[-1][3]
def narr(t):
    v=NARR[0][1]
    for a,b in NARR:
        if t>=a: v=b
    return v

def background(w,h,t):
    y,x=np.mgrid[0:h,0:w]
    cx=w*(.51+.035*math.sin(t*.011)); cy=h*(.46+.025*math.cos(t*.017))
    r=np.sqrt((x-cx)**2+(y-cy)**2)/(0.84*max(w,h)); r=np.clip(r,0,1)[...,None]
    q=smoothstep(92,160,t); base=COL['bg1']*r + ((1-q)*COL['bg2']+q*COL['bg3'])*(1-r)
    # microscope medium / ECM fibers
    overlay=np.zeros_like(base)
    for k in range(26):
        yy=int((k*31 + 20*math.sin(t*.02+k))%h)
        x0=int((k*73+t*2)%w); x1=int((x0+180+40*math.sin(k))%w)
        cv2.line(overlay,(x0,yy),(x1,int(yy+22*math.sin(k+t*.02))),COL['membrane'].tolist(),1,lineType=cv2.LINE_AA)
    base=np.clip(base+overlay*.10,0,255)
    for i in range(70):
        xx=int((i*97+t*(2+i%3))%w); yy=int((i*43+70*math.sin(i+t*.035))%h)
        blend(base,xx,yy,5,COL['cellblue'],.22)
    return base.astype(np.float32)

def draw_tissue_layers(img,w,h,t,alpha=1.0):
    ov=np.zeros_like(img); cx,cy=w//2,h//2+12
    for layer,col in enumerate(['cellblue','neural','epithelial','metabolic']):
        last=None
        for i in range(180):
            u=(i/179-.5)*2
            x=int(cx+u*300*alpha)
            y=int(cy+(math.sin(u*math.pi*2+t*.52+layer)*48+layer*20-38)*alpha)
            if last: cv2.line(ov,last,(x,y),COL[col].tolist(),2,lineType=cv2.LINE_AA)
            if i%18==0: blend(ov,x,y,10,COL[col],.65)
            last=(x,y)
    img[:] = np.clip(img+ov*.48,0,255)

def draw_body_systems(img,w,h,t,q=1.0):
    ay=t*.155; center=(95,12); scale=478
    points(img, body*q, 'cellblue', w,h,scale,center,.47,13,ay)
    points(img, body*q, 'skeletal', w,h,scale,center,.16,10,ay)
    # organs
    for name,cfg in organs.items():
        a=.62 if name!='heart' else .92
        pulse=1+.08*math.sin(t*2.6) if name=='heart' else 1
        points(img, organ_points[name]*q*pulse, cfg['color'], w,h,scale,center,a*q,16,ay)
    ov=np.zeros_like(img)
    # spine and ribs
    spine=np.c_[np.zeros(22),np.linspace(2.05,-2.25,22),np.zeros(22)]*q
    pp=rot_y(spine.astype(np.float32),ay); xs,ys,_=project(pp,w,h,scale,center=center)
    for i in range(len(xs)-1): cv2.line(ov,(xs[i],ys[i]),(xs[i+1],ys[i+1]),COL['skeletal'].tolist(),1,lineType=cv2.LINE_AA)
    for r_i in range(7):
        yv=1.25-r_i*.16
        for side in (-1,1):
            rib=np.array([[0,yv,0],[side*(.34+.035*r_i),yv-.05,.04],[side*(.55+.03*r_i),yv-.12,.01]])*q
            pp=rot_y(rib.astype(np.float32),ay); x,y,_=project(pp,w,h,scale,center=center)
            cv2.polylines(ov,[np.c_[x,y].astype(np.int32)],False,COL['skeletal'].tolist(),1,lineType=cv2.LINE_AA)
    # muscle fibers
    for k in range(18):
        side=-1 if k%2 else 1
        fib=np.array([[side*.25,1.1-k*.12,.08],[side*.55,.8-k*.10,.06],[side*.35,.45-k*.09,.08]])*q
        pp=rot_y(fib.astype(np.float32),ay); x,y,_=project(pp,w,h,scale,center=center)
        cv2.polylines(ov,[np.c_[x,y].astype(np.int32)],False,COL['muscle'].tolist(),1,lineType=cv2.LINE_AA)
    img[:] = np.clip(img+ov*.72,0,255)

def draw_feedback(img,w,h,t):
    ov=np.zeros_like(img); center=(95,12); scale=478; ay=t*.155
    sources=[organs['brain']['center'],organs['heart']['center'],organs['liver']['center']]
    cols=[COL['neural'],COL['vascular'],COL['metabolic']]
    for idx,target in enumerate(sys_targets[:38]):
        src=sources[idx%3]; u=np.linspace(0,1,18)
        path=np.outer(1-u,src)+np.outer(u,target)
        path[:,0]+=.10*np.sin(u*np.pi*2+t*.08+idx); path[:,2]+=.10*np.cos(u*np.pi*2+t*.07+idx)
        pp=rot_y(path.astype(np.float32),ay); xs,ys,_=project(pp,w,h,scale,center=center)
        for i in range(len(xs)-1): cv2.line(ov,(xs[i],ys[i]),(xs[i+1],ys[i+1]),cols[idx%3].tolist(),1,lineType=cv2.LINE_AA)
        if idx%5==0: blend(ov,xs[(idx*3)%len(xs)],ys[(idx*3)%len(ys)],9,COL['immune'],.75)
    cx,cy=int(w*.58),int(h*.52)
    for k,col in enumerate(['neural','vascular','endocrine','immune','metabolic']):
        cv2.ellipse(ov,(cx,cy),(82+35*k,int((82+35*k)*.56)),int(t*3+k*15),0,360,COL[col].tolist(),1,lineType=cv2.LINE_AA)
    img[:] = np.clip(img+ov*.45,0,255)

def hud(img,t,dur,w,h):
    pil=Image.fromarray(cv2.cvtColor(np.clip(img,0,255).astype(np.uint8),cv2.COLOR_BGR2RGB)); d=ImageDraw.Draw(pil)
    ft=ImageFont.truetype(FONT_BOLD,max(22,int(w*.031))); fs=ImageFont.truetype(FONT_REG,max(13,int(w*.014))); fh=ImageFont.truetype(FONT_BOLD,max(17,int(w*.020)))
    title,desc=stage(t)
    def txt(xy,s,font,fill):
        x,y=xy; d.text((x+2,y+2),s,font=font,fill=(0,0,0)); d.text((x,y),s,font=font,fill=fill)
    txt((42,28),TITLE_CN,ft,(248,250,252)); txt((44,74),SUBTITLE_EN,fs,(199,210,254))
    y=h-150; d.rounded_rectangle((34,y,min(w-34,820),h-34),radius=18,fill=(7,15,32),outline=(130,196,245),width=1)
    txt((56,y+14),title,fh,(254,243,199)); txt((56,y+46),desc,fs,(228,232,240)); txt((56,y+76),narr(t),fs,(204,214,225))
    d.rounded_rectangle((42,h-22,w-42,h-16),radius=3,fill=(44,60,80)); d.rounded_rectangle((42,h-22,42+int((w-84)*t/dur),h-16),radius=3,fill=(254,243,199))
    return cv2.cvtColor(np.array(pil),cv2.COLOR_RGB2BGR).astype(np.float32)

def frame(t,dur,w,h):
    img=background(w,h,t)
    p=smoothstep(0,18,t); cell_fade=1-smoothstep(50,72,t); cx=int(w*(.50-.08*smoothstep(16,40,t))); cy=int(h*.49); rr=48+70*p
    if cell_fade>.02:
        ov=np.zeros_like(img); cv2.circle(ov,(cx,cy),int(rr+20),COL['membrane'].tolist(),2,lineType=cv2.LINE_AA); cv2.circle(ov,(cx,cy),int(rr),COL['cellblue'].tolist(),1,lineType=cv2.LINE_AA); img=np.clip(img+ov*.32*cell_fade,0,255)
        points(img,cell*(.72+.36*p),'cellblue',w,h,rr*4.8,(cx-w/2,cy-h/2),.42*cell_fade,14,t*.12)
        points(img,vesicles*(.66+.30*p),'metabolic',w,h,rr*4.8,(cx-w/2,cy-h/2),.32*cell_fade,9,-t*.15)
        blend(img,cx,cy,int(rr*.42),COL['nucleus'],.45*cell_fade)
        for i in range(32):
            a=i/32*math.pi*4+t*.7; blend(img,int(cx+math.cos(a)*rr*.22),int(cy-rr*.35+i/32*rr*.7),7,COL['metabolic'],.55*cell_fade)
    div=smoothstep(20,38,t)*(1-smoothstep(44,58,t))
    if div>.02:
        n=int(3+35*smoothstep(20,40,t)); ids=np.arange(n); ph=np.arccos(1-2*(ids+.5)/n); th=np.pi*(1+5**.5)*ids
        cl=np.c_[np.sin(ph)*np.cos(th),np.cos(ph),np.sin(ph)*np.sin(th)]*(.2+1.25*smoothstep(20,40,t))
        points(img,cl,'nucleus',w,h,420,(0,0),.55*div,20,t*.22)
        pp=rot_y(cl.astype(np.float32),t*.22); xs,ys,_=project(pp,w,h,420); ov=np.zeros_like(img)
        for i in range(n):
            if i%3==0: cv2.line(ov,(xs[i],ys[i]),(xs[(i+5)%n],ys[(i+5)%n]),COL['cellblue'].tolist(),1,lineType=cv2.LINE_AA)
        img=np.clip(img+ov*.32*div,0,255)
    lin=smoothstep(40,55,t)*(1-smoothstep(72,92,t))
    if lin>.02:
        cols=['neural','vascular','skeletal','muscle','epithelial','metabolic']; ov=np.zeros_like(img)
        for j,col in enumerate(cols):
            pts=lineage[j*17:(j+1)*17]*(.8+.75*smoothstep(40,65,t)); pts[:,0]+=(j-2.5)*.35
            points(img,pts,col,w,h,400,(-90,0),.62*lin,16,t*.19)
            pp=rot_y(pts.astype(np.float32),t*.19); xs,ys,_=project(pp,w,h,400,center=(-90,0))
            for i in range(len(xs)-1): cv2.line(ov,(xs[i],ys[i]),(xs[i+1],ys[i+1]),COL[col].tolist(),1,lineType=cv2.LINE_AA)
        img=np.clip(img+ov*.32*lin,0,255)
    morph=smoothstep(65,82,t)*(1-smoothstep(94,108,t))
    if morph>.02:
        draw_tissue_layers(img,w,h,t,morph); points(img,body*morph,'skeletal',w,h,458,(92,15),.18*morph,10,t*.14)
    bodyq=smoothstep(88,112,t)
    if bodyq>.02:
        draw_body_systems(img,w,h,t,max(.1,bodyq))
    if t>=118:
        draw_feedback(img,w,h,t)
    if t>=145:
        points(img,body*1.08,'white',w,h,505,(95,10),.09*smoothstep(145,160,t),16,t*.18)
    if t>=165:
        eth=smoothstep(165,174,t); ov=np.zeros_like(img); bx,by=int(w*.58),int(h*.31)
        for i in range(24):
            a=i/24*2*math.pi+t*.04; x2=int(bx+math.cos(a)*180); y2=int(by+math.sin(a)*105); cv2.line(ov,(bx,by),(x2,y2),COL['neural'].tolist(),1,lineType=cv2.LINE_AA); blend(ov,x2,y2,7,COL['metabolic'],.65)
        img=np.clip(img+ov*.38*eth,0,255); blend(img,int(w*.18),int(h*.35),42,COL['cellblue'],.30*eth); blend(img,int(w*.18),int(h*.35),18,COL['nucleus'],.42*eth)
    return np.clip(hud(img,t,dur,w,h),0,255).astype(np.uint8)

def audio(path,dur,sr=44100):
    ts=np.arange(int(sr*dur))/sr; ramp=np.minimum(1,ts/12)*np.minimum(1,(dur-ts)/10)
    sig=(.032*np.sin(2*np.pi*55*ts)+.018*np.sin(2*np.pi*110*ts+.4*np.sin(2*np.pi*.04*ts))+.006*np.sin(2*np.pi*330*ts)*((ts>118)&(ts<170)))*ramp
    pcm=(np.clip(sig,-.12,.12)*32767).astype(np.int16)
    with wave.open(str(path),'wb') as wf: wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(pcm.tobytes())

def render(output,dur,fps,w,h,poster):
    output.parent.mkdir(parents=True,exist_ok=True); poster.parent.mkdir(parents=True,exist_ok=True)
    tmp=output.with_name(output.stem+'_silent_tmp.mp4'); wav=output.with_name(output.stem+'_ambient_tmp.wav')
    vw=cv2.VideoWriter(str(tmp),cv2.VideoWriter_fourcc(*'mp4v'),fps,(w,h)); total=int(dur*fps); pf=None
    for i in range(total):
        t=i/fps; fr=frame(t,dur,w,h); vw.write(fr)
        if pf is None or abs(t-152)<pf[0]: pf=(abs(t-152),fr.copy())
        if i%max(1,fps*10)==0: print(f'rendered {i}/{total} frames ({t:.1f}s)',flush=True)
    vw.release(); cv2.imwrite(str(poster),pf[1] if pf else frame(152,dur,w,h)); audio(wav,dur)
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(tmp),'-i',str(wav),'-c:v','libx264','-pix_fmt','yuv420p','-preset','veryfast','-crf','22','-c:a','aac','-b:a','96k','-shortest',str(output)],check=True)
    tmp.unlink(missing_ok=True); wav.unlink(missing_ok=True); print('Wrote',output)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=OUT); ap.add_argument('--duration',type=float,default=180); ap.add_argument('--fps',type=int,default=4); ap.add_argument('--width',type=int,default=960); ap.add_argument('--height',type=int,default=540); ap.add_argument('--poster',type=Path,default=POSTER)
    a=ap.parse_args(); render(a.output,a.duration,a.fps,a.width,a.height,a.poster)
if __name__=='__main__': main()
