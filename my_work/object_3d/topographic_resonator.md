# TopographicResonator

物体 `TopographicResonator`。修改器：`Topographic` → `Smooth by Angle`（30°）。1 单位 = 1 mm。

钟口在下，向上收。每一级等高线只向内收。底是一圈平的环。最上面大约 11 mm 台阶淡出，收成圆口。

## 函数

台阶取的是高度的 floor，不是噪声。

`z_step = floor(z / Step Height) × Step Height`

半径在这一档高度上保持不变，顶点仍停在真实的 z 上，所以每一档是一圈竖壁。

轮廓仍是两端斜率为 0 的余弦。波用原来的整数倍，权重 1、1/2、1/3：

`r = R(z_step) + Tectonic Amplitude × env × wave + Core Offset × env × cos(θ)`

`env` 在底和顶是 0。Core Offset 是单独的一瓣，用来拆开 7 次对称。内壁是同一条半径再收进 Wall Thickness。

## 面板

| 名字 | 值 | |
|---|---|---|
| Step Height | 0.6 mm | 三层 0.2 mm。可改 0.4 或 0.8 |
| Tectonic Amplitude | 1.6 mm | 2.5 mm 时最薄处 0.89 mm |
| Helix Twist | 36° | 整段高度转过的角 |
| Base Radius | 30 mm | |
| Harmonic Frequency | 7 | |
| Core Offset | 0.8 mm | 那一瓣不对称。0 就是正对称 |
| Height | 80 mm | |
| Wall Thickness | 2.0 mm | 沿半径 |

## 检查

| | |
|---|---|
| 连通体 | 1 |
| 非流形 / 边界 | 0 / 0 |
| 自交 | 0 |
| 体积 | +16145 mm³ |
| 尺寸 | 60 × 60 × 80 mm |
| 最低点 | 0 mm |
| 底环半径 | 28–30 mm |
| 竖壁厚度 | 最薄 1.34 mm，中位 2.00 mm |
| 外侧悬垂 | 0° |

中段每一档高度是 0.6 mm，半径在这一档里不变，下一档大约收进 0.28 mm。

STL：`topographic_resonator.stl`（约 13 MB）。
