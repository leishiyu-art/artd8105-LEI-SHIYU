# TraceShell — Geometry Nodes（螺旋三角管）

物体：`TraceShell`。修改器：`TraceShell` → 节点组 `TraceShellGN`。  
1 Blender 单位 = 1 mm。场景单位：公制，长度缩放 0.001。

当前图 **没有 Repeat Zone**。棱柱循环留在 `build_trace_shell.py` 的 `fill_group` 里，不接到输出。

## 节点在做什么

| 区块 | 节点 | 做什么 |
|---|---|---|
| 输入 | Group Input | 她转的参数。Count 变成螺旋上的取样密度（×16 重采样）。 |
| 痕迹 | Curve Spiral | 等半径螺旋。圈数 = Helix Turns。高 28 mm，放到盒心 (40, 40, 8)。 |
| 扭矩 | Set Curve Tilt | `Torque Deg × (0.6+Overlap) × factor × sign`。Reverse 开：在 0.42–0.58 把 sign 从 +1 滑到 −1（硬切会折管）。Max Turn Deg 是按 Count 段加的噪声，不是每点乱拧。 |
| 粗细 | Set Curve Radius | Size Min–Max、Beat（每第 N 段 × Beat Scale）、可选 Fade。半径 = draw / Size Min，剖面本身按毫米建。 |
| 三角形 | 3 Points → Poly 闭合曲线 | 底 ≥ Size Min，高 ≥ max(Wall×1.3, Size Min×0.85)，顶点侧移 0.18×底。不是圆、不是正三角。 |
| 扫掠 | Curve to Mesh + Fill Caps | 三角剖面沿螺旋走。Merge by Distance 0.25 mm。 |
| 输出 | Group Output | 一根流形壳。 |

## Group Input

| 名字 | 这次用的值 | 范围 |
|---|---|---|
| Count | 8 | 3–40（控制沿曲线分段，不是颗数） |
| Overlap | 0.70 | 0.20–0.92；现在加扭矩，不加圈 |
| Size Min / Max | 6 / 12 mm | B 抬过 |
| Prism Thickness | 2.5 mm | 螺旋路径不用它挤出 |
| Wall Thickness | 2.5 mm | 剖面高的下限 |
| Correlation | 0.35 | 0–1 |
| Max Turn Deg | 35 | 度；tilt 噪声幅度 |
| Reverse | on | 半程扭矩反号 |
| Beat N | 4 | 0=关 |
| Beat Scale | 1.45 | 1.2–2.0 |
| Seed | 1 | 整数 |
| Fade Affects Size | off | 渐隐不减壁厚 |
| Helix Turns | **1.0** | 0.25–6；圈数受螺距约束 |
| Helix Radius | 16 mm | 6–32 |
| Torque Deg | 240 | 0–720 |

改 Helix Turns / Radius / Torque 时在修改器面板转。Count 先留 8。
