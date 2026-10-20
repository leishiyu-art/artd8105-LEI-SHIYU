# SphereTubeNet — C · 大窗

选型 **C**：Icosphere Subdivisions **1** → 20 个三角窗，30 根圆管。紫球只当管网这一类结构；没有花瓣编织、没有另加杆、没有填窗、没有 Voronoi。

规则：Icosphere 的边变成圆管；顶点先 `v' = v + Noise(v×scale)×amplitude×normal`；噪声再只调制管半径。窗来自二十面体面。

`TraceShell` 与 `NoiseDisplacedSolid` 仍在文件里（视口里藏了，方便看这一件）。没有动 `triangles_trace_shell.*` / `noise_displaced_solid.*`。没有导出 STL。

## Group Input

| 名字 | 这次用的值 | 说明 |
|---|---|---|
| Radius | 30 mm | 笼子半径 |
| Subdivisions | **1** | C · 大窗。改 2 就是 D |
| CageScale | 0.5 | 与实心球同一套 4D FBM；这里频率 0.5 |
| CageAmplitude | 4 mm | 人设的底。信号会改写它 |
| Seed | 0 | 进噪声 W |
| TubeRadius | 2.0 mm | 底线 1.2，这条不交给信号 |
| RadiusAmp | 0.4 mm | 人设的底。信号会改写它 |
| Signal | 0 | 0–1，现在是假的非人通道 |
| Influence | 0.7 | 跟 `co_constraint.html` 里那只滑块一样 |
| Correlation | 0.35 | 半径里，顺序占多少。开口值来自三角形那件 |
| Reverse | on | 边数走到一半，半径的坡折返 |
| AlongSwell | **0.8 mm** | 正弦的振幅。开口值是管半径 2.0 减 1.2 的那一截 |
| AlongCycles | **1** | 一根管子上放几个波。1 是一整个正弦，不是造型选择 |
| AlongPhase | **0** | 手拧。波沿管子挪。不接时间轴，改帧不会动 |
| AlongSamples | **8** | 每根管子上的点数。点多，波更顺，布尔更重 |

每根管子用同一个式子：

`半径 = max(1.2, 边半径 + AlongSwell × sin(2π × (AlongCycles × 沿边位置 + AlongPhase + 边序号/边数)))`

边序号那一项让管子彼此错开。你拖的是 `AlongPhase`。


顺序只走在**管半径**上，不走在顶点位移上。边的顺序是二十面体自己的边序号。走到一半，坡从升变成降。和噪声的混合是：

`offset = liveRadiusAmp × (Correlation × 顺序 + (1 − Correlation) × 噪声)`

`半径 = max(1.2, TubeRadius + offset)`

Signal = 0 时，这条顺序把管半径拉开到 **1.94–2.06 mm**（live radius amp 只有 0.12 mm）。顺序系数本身从 −1 到 0.93。


位移用的振幅、半径噪声的幅度，在节点里是：

`live = humanBase + (signalShaped − humanBase) × Influence`

`CageAmplitude` 的 signalShaped = Signal × 8 mm。`RadiusAmp` 的 signalShaped = Signal × (TubeRadius − 1.2)。`CageScale` 不在这条映射里。

现在 Signal = 0、Influence = 0.7，进噪声的仍是 **live amp 1.20 mm**、**live radius amp 0.12 mm**。

## 节点在做什么

Group Input 的 Signal / Influence 用 Math 做成 live，再送进 Set Position。半径先按边序号走，再加上沿管子的正弦。`AlongPhase` 是手拧的相位，不接帧。后面：Curve Circle → Curve to Mesh → Merge by Distance → Mesh Boolean Union → 把 min Z 抬到 1.2 mm。

## 检查数字

你当前的界面值：Subdivisions **1**（从 2 拧回），Radius 32.44，AlongSwell 0.8，Signal 0。

| | |
|---|---|
| 连通体 | 1 |
| 带符号体积 | +2950 mm³ |
| 非流形边 / 边界边 | 0 / 0 |
| Min Z | 1.20 mm |
| 管半径 | 1.20–2.82 mm |
| 管子自交 | **0** |

Subdivisions 2 时求值网格约 1 万个顶点，并有 1 对相交。拧回 1 之后相交没有了。

没有导出 STL。
