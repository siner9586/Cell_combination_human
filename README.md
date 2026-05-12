# 从单细胞到人类：生命体自组织的三维演化

本仓库保存一套安全、抽象、教育性的 3D 科学可视化视频工程与可复用 skill 包，用于生成 3 分钟概念视频：

**《从单细胞到人类：生命体自组织的三维演化》**  
**From a Single Cell to a Human: A 3D Visualization of Biological Self-Organization**

> 本项目不包含任何真实湿实验配方、基因序列、载体构建、培养条件、克隆流程、胚胎操作或可复现实验参数。所有画面均为抽象粒子、半透明膜、形态场、系统网络和概念人形轮廓。

## 新增内容

```text
scripts/render_cell_to_human_180s.py          # 180 秒 MP4 生成脚本
skills/cell_combination_human/SKILL.md        # 新 skill 包说明
docs/production_guide.md                      # 3 分钟视频制作说明
docs/safety.md                                # 安全边界说明
assets/videos/README.md                       # 视频资产与生成说明
```

## 一键生成 3 分钟视频

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy opencv-python pillow
python scripts/render_cell_to_human_180s.py --duration 180 --fps 8 --width 1280 --height 720
```

快速预览版：

```bash
python scripts/render_cell_to_human_180s.py --duration 180 --fps 2 --width 960 --height 540
```

输出路径：

```text
assets/videos/cell_to_human_180s.mp4
assets/posters/cell_to_human_poster.png
```

## 8 幕结构

1. 单细胞：生命的起点
2. 分裂：从一到多
3. 分化：细胞获得身份
4. 形态发生：身体蓝图浮现
5. 器官形成：局部功能模块生成
6. 系统耦合：生命体成为整体
7. 涌现：从细胞到人
8. 边界：理解生命，而非制造生命

## 安全边界

本工程只用于表达“生命自组织与复杂系统涌现”的宏观逻辑，不提供真实生物构建、克隆、胚胎培养、基因编辑或人体制造方法。
