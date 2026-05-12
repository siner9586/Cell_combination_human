# 视频资产说明

本目录用于存放《从单细胞到人类：生命体自组织的三维演化》的视频输出。

## 当前脚本输出

运行新版 180 秒渲染脚本后会生成：

```text
assets/videos/cell_to_human_180s.mp4
assets/posters/cell_to_human_poster.png
```

推荐命令：

```bash
python scripts/render_cell_to_human_180s.py --duration 180 --fps 8 --width 1280 --height 720
```

快速预览命令：

```bash
python scripts/render_cell_to_human_180s.py --duration 180 --fps 2 --width 960 --height 540
```

## 旧版轻量预览

- `cell_combination_human_concept.svg`：轻量级动画 SVG，可直接在浏览器中预览。
- `render_concept_video.py`：早期概念 MP4/GIF 生成脚本。

## 安全说明

视频采用抽象粒子、半透明膜、形态场、分化色带、器官网络和非写实人形轮廓表达生命系统的自组织过程，不包含真实实验参数、基因编辑、克隆流程、胚胎操作或可操作生物工程信息。
