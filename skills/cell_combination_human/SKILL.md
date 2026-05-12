# Cell Combination Human 3D Visualization Skill

## Purpose

Generate a safe, abstract, education-oriented 3D scientific visualization video titled:

**《从单细胞到人类：生命体自组织的三维演化》**

The skill creates a 180-second conceptual video that visualizes the transition from a single cell to a complex human-like multi-system outline through division, differentiation, morphogenesis, organ-system formation, and multi-scale coupling.

## Safety Boundary

This skill must never output or generate:

- wet-lab protocols;
- cell culture conditions;
- gene sequences, gRNA, vectors, plasmids, or construct maps;
- cloning, embryo manipulation, or human manufacturing workflows;
- actionable biological engineering parameters;
- images implying a human factory, cloning facility, embryo lab, or mechanical assembly line.

All visual elements must remain abstract: particles, translucent membranes, fields, gradients, networks, organ-like light modules, and a non-realistic glowing human outline.

## Recommended Workflow

1. Confirm the video is conceptual and non-operational.
2. Use `scripts/render_cell_to_human_180s.py` to generate the video.
3. Keep the eight-act structure:
   - Single cell
   - Division
   - Differentiation
   - Morphogenesis
   - Organ formation
   - System coupling
   - Emergence
   - Ethical boundary
4. Use restrained documentary-style language.
5. Export video assets to `assets/videos/` and poster frames to `assets/posters/`.

## Default Command

```bash
python scripts/render_cell_to_human_180s.py --duration 180 --fps 8 --width 1280 --height 720
```

## Quick Preview Command

```bash
python scripts/render_cell_to_human_180s.py --duration 180 --fps 2 --width 960 --height 540
```

## Visual Style

- deep blue-black microcosmic background;
- translucent glowing cell membrane;
- abstract helices only, never real DNA sequence;
- lineage colors: neural blue-purple, circulatory red-gold, skeletal ivory, muscle warm red, epithelial cyan;
- semi-transparent human outline built from particles, networks, and organ-like fields;
- soft, reverent, scientific, non-horror aesthetic.

## Output

- `assets/videos/cell_to_human_180s.mp4`
- `assets/posters/cell_to_human_poster.png`
- updated documentation in `docs/`
