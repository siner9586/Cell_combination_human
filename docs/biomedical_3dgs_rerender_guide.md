# 生物医学纪录片风格 3DGS 重渲染说明

## 标题

《从细胞到人体：生命系统自组织的三维演化》

From Cell to Human Body: A 3D Visualization of Biological Self-Organization

## 渲染目标

将原先偏抽象科技感的概念视频升级为更具生物医学纪录片气质的科学可视化表达。

## 重点增强

- 显微微环境背景，不再偏太空科幻；
- 半透明细胞膜与胞质微粒流；
- 组织片层、折叠、卷曲、分层；
- 透明器官结构；
- 神经网络、循环系统、骨骼支架、肌纤维束；
- 肺部、代谢流、免疫巡逻与内分泌波纹；
- 从细胞尺度到人体尺度的连续镜头过渡。

## 默认命令

```bash
python scripts/render_cell_to_human_biomedical_3dgs.py --duration 180 --fps 4 --width 960 --height 540
```

## 输出

```text
assets/videos/cell_to_human_body_biomedical_3dgs_180s.mp4
assets/posters/cell_to_human_body_biomedical_3dgs_poster.png
```

## 安全边界

本视频只表达生命系统的自组织与多尺度涌现，不呈现实验操作、克隆、胚胎操作、真实序列或人体制造场景。
