# Cell to Human Body Biomedical 3DGS Skill

## Title

《从细胞到人体：生命系统自组织的三维演化》

From Cell to Human Body: A 3D Visualization of Biological Self-Organization

## Purpose

Generate a 180-second biomedical-documentary-style 3DGS-like visualization. The video uses abstract particles, translucent membranes, tissue layers, anatomical-like organ systems, and system-coupling networks to express a multi-scale self-organizing life system.

## Visual Requirements

- biomedical visualization
- developmental biology aesthetic
- medical documentary style
- translucent anatomical rendering
- organ system emergence
- microscopic-to-anatomical scale transition
- systems biology illustration
- Gaussian-splatting-like rendering
- semi-transparent tissue layers
- cellular self-organization

## Default Command

```bash
python scripts/render_cell_to_human_biomedical_3dgs.py --duration 180 --fps 4 --width 960 --height 540
```

## macOS Compatibility

The renderer writes a temporary AVI/MJPG stream before FFmpeg encodes the final H.264 MP4. This avoids common macOS OpenCV `mp4v` output failures.

## Output

```text
assets/videos/cell_to_human_body_biomedical_3dgs_180s.mp4
assets/posters/cell_to_human_body_biomedical_3dgs_poster.png
```

## Boundary

Keep the video abstract, educational, non-operational, non-mechanical, non-gory, and documentary-like.
