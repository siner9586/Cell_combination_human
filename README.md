# 从单细胞到人类：生命体自组织的三维演化

这是一个安全、抽象、教育性的 3D 科学可视化项目，用于展示“单细胞 → 多细胞团 → 分化 → 形态发生 → 器官系统 → 多尺度人体轮廓”的概念演化过程。

> 项目不包含任何真实湿实验配方、基因序列、载体构建、培养条件、克隆流程或可操作的人体/胚胎制造步骤。所有内容均为概念动画、抽象粒子和系统生物学可视化表达。

## 项目结构

```text
.
├── index.html                         # Three.js 交互式 3D 演示入口
├── package.json                       # 本地开发脚本
├── src/
│   ├── main.js                        # 3D 场景、分镜、粒子和系统耦合动画
│   └── style.css                      # 页面视觉样式
├── scripts/
│   └── render_concept_video.py        # Python 离线生成概念 MP4/GIF 的脚本
├── assets/
│   └── videos/
│       ├── cell_combination_human_concept.svg # 可直接预览的动画 SVG
│       └── README.md                  # 视频资产说明与生成方式
└── docs/
    ├── storyboard.md                  # 8 幕分镜、旁白与视觉设计
    └── safety.md                      # 安全边界与非湿实验声明
```

## 本地运行 Three.js 交互式演示

```bash
npm install
npm run dev
```

然后打开终端提示的本地地址。

## 离线渲染 MP4/GIF

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install numpy matplotlib imageio imageio-ffmpeg pillow
python scripts/render_concept_video.py
```

输出文件：

```text
assets/videos/cell_combination_human_concept.mp4
assets/videos/cell_combination_human_concept.gif
```

## 核心叙事

1. 单细胞：边界、信息、能量与响应能力。
2. 分裂：从一到多，关系开始出现。
3. 分化：相同起点产生不同命运。
4. 形态发生：身体轴线与组织层浮现。
5. 器官形成：局部细胞群形成神经、循环、骨骼、肌肉等功能秩序。
6. 系统耦合：神经、循环、代谢、免疫、内分泌相互反馈。
7. 尺度跃迁：由细胞点阵、组织层、器官网络构成半透明人形。
8. 伦理边界：理解生命，而非制造生命。

## 安全声明

本项目只表达“生命体自组织与涌现”的宏观逻辑，不提供真实生物构建流程、克隆流程、胚胎操作、基因编辑、培养条件或可复现实验参数。
