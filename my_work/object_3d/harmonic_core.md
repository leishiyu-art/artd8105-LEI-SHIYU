# HarmonicCore

物体 `HarmonicCore`。修改器：`HarmonicCore` → `Smooth by Angle`（60°）。1 单位 = 1 mm。

底是平的环。30% 高度是束腰，70% 高度是鼓起，顶是平口。面板上的半径以你现在拖过的数为准。

领口台阶和斜向细纹已拿掉，回到圆角那一版。

## 函数

轮廓是三段 smoothstep。扭转角是同一段，从 30% 的 0 走到 70% 的滑杆角度。两端转速为 0。

肋深被 **Crest Radius**（1.5 mm）卡住的是上下两段。扭转段（高度约 30%–70%）另有一圈沟，深度大约 `0.80 · R / 肋数`，所以肋会跟着扭转走。这一段外侧面会超过 45°，壁也会薄于 1.5 mm。

`Set Shade Smooth` 开着。Smooth by Angle 夹角 60°。外圈高度 960 层。

内壁是外壁半径减去 Wall Thickness。

播放用同一个时间 `t = Frame / Time Scale`。

滑杆上的数是静止值。播放时整颗一起乘上 `1 + Shape Amount · sin(t)`。口径再乘一层，增益是 1.80，所以口比身体张得更大。**Shape Amount** 默认 0.12。

| | 增益 |
|---|---|
| 底口、顶口 | 1.80 |
| 腰、核心、高度 | 1.00 |
| 扭转 / 翼深 / 圆角 / 壁厚 | 0.35 / 0.40 / 0.20 / 0.12 |

腰和鼓起另有一拍：

`BreathFactor = sin(t · 0.5) · 0.7 + abs(cos(t · 1.5)) · 0.3`

再乘 **Breath Amplitude**（默认 4 mm），只加在大约 14%–90% 的高度上。中间扭转是 `BaseTwist + t · 0.1`，两端仍是 0。`t = Frame / Time Scale`，示例除数是 30。

底口和顶口是花瓣。`cos(Petal Count · (θ + 曲轴))`。瓣深 `min(4.2 mm, 0.15 · R)`。**Petal Count** 默认 5。底面仍在 z = 0。

课堂演示页：`harmonic_core_talk.html`。用浏览器打开。主界面是按同一套式子算的壳体，可拖可播放。圈数少于 Blender。概念那一格要你自己写。

## 检查

| | |
|---|---|
| 连通体 | 1 |
| 非流形 / 边界 | 0 / 0 |
| 体积 | +25701 mm³ |
| 尺寸 | 67.4 × 67.4 × 80 mm |
| 顶点 | 553536 |
| 外侧面离竖直的最大角 | 75° |
| 超过 45° 的外侧面 | 38460，在扭转段 |

自交和壁厚没有逐面重测。没有写新的 STL。

先前的 TraceShell、NoiseDisplacedSolid、SphereTubeNet、SchumannResonator、TopographicResonator 还在文件里，只是视口里藏了。
