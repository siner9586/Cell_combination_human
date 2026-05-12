# 180 秒 3D 科学可视化视频制作说明

## 片名

《从单细胞到人类：生命体自组织的三维演化》

英文副标题：From a Single Cell to a Human: A 3D Visualization of Biological Self-Organization

## 工程目标

使用 Python 可视化脚本生成一部约 180 秒的抽象科学可视化视频。画面以粒子、半透明膜、形态场、发光网络、器官样光团和非写实人形轮廓表达生命系统的自组织过程。

## 时间轴

| 时间 | 幕名 | 画面重点 |
|---|---|---|
| 0–20s | 单细胞 | 半透明膜、细胞核、抽象螺旋光带、能量流 |
| 20–40s | 分裂 | 从一到多，多细胞团与通信光丝 |
| 40–65s | 分化 | 蓝紫、红金、象牙白、暖红、浅青谱系分区 |
| 65–90s | 形态发生 | 拉伸、折叠、分层、身体蓝图 |
| 90–120s | 器官形成 | 神经、心脏、循环、骨骼、肌肉、代谢结构 |
| 120–145s | 系统耦合 | 神经、循环、代谢、免疫、内分泌反馈 |
| 145–165s | 尺度跃迁 | 从分子光点到人形轮廓 |
| 165–180s | 伦理边界 | 脑部柔光、社会与自然抽象连接、单细胞与人形重叠 |

## 运行命令

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

## 输出

```text
assets/videos/cell_to_human_180s.mp4
assets/posters/cell_to_human_poster.png
```

## 视觉原则

- 深蓝黑微观背景逐渐过渡到蓝白柔光空间；
- 使用半透明材质、粒子流、低饱和谱系色和发光网络；
- 人形必须保持非写实轮廓，由细胞点阵、系统网络和光流构成；
- 不表现机械拼装、人造工厂或恐怖风格；
- 结尾强调理解生命、尊重边界与责任。
