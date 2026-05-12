# 生物医学纪录片风格 3DGS 重渲染说明

## 标题

《从细胞到人体：生命系统自组织的三维演化》

From Cell to Human Body: A 3D Visualization of Biological Self-Organization

## 渲染定位

本版本将视频整体从“抽象科技感”升级为“生物医学纪录片感”。画面更接近高端医学纪录片、发育生物学概念动画、系统生物学动态图谱和透明解剖可视化影片。

## 视觉增强

- 背景从深蓝黑显微微环境过渡到蓝白医学空间；
- 细胞膜采用半透明青蓝边缘高光，内部加入胞质微粒和信息光带；
- 中段强调组织片层、折叠、卷曲、分层与身体轴线；
- 后段强化透明器官结构、神经网络、循环脉冲、骨骼支架、肌纤维束、代谢流、免疫巡逻和内分泌波纹；
- 镜头保持显微推进、剖面穿透、透明器官透视、多尺度连续过渡与缓慢解剖式旋转。

## 运行命令

```bash
python scripts/render_cell_to_human_biomedical_3dgs.py --duration 180 --fps 4 --width 960 --height 540
```

更高清版本：

```bash
python scripts/render_cell_to_human_biomedical_3dgs.py --duration 180 --fps 6 --width 1280 --height 720
```

## 输出

```text
assets/videos/cell_to_human_body_biomedical_3dgs_180s.mp4
assets/posters/cell_to_human_body_biomedical_3dgs_poster.png
```

## 技术更新

脚本已改用跨平台更稳定的临时 AVI/MJPG 写入，再交给 FFmpeg 转为 H.264 MP4，可避免 macOS 环境下 OpenCV `mp4v` 临时文件未生成的问题。

## 边界

本视频只表达生命系统的自组织与多尺度涌现，不呈现任何真实实验操作或人体工业化构造场景。
