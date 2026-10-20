# SchumannResonator

物体 `SchumannResonator`。修改器：`Schumann` → `Smooth by Angle`（30°）。1 单位 = 1 mm。

钟口在下，向上收。外面没有朝下的面，所以不用支撑。底是一圈平的环，不是实心圆片。顶上留一个小孔，没有要去桥接的天花板。

## 函数

没有噪声。

轮廓，两端斜率是 0，中段最斜大约 22°：

`R(z) = 4 + (Base Radius − 4) × (1 + cos(π z / Height)) / 2`

包络，底和顶都收成正圆：

`env = sin(π z / Height)²`

相位：

`φ = θ + Twist × (z / Height)`

整数倍谐波，权重 1、1/2、1/3，峰值归到 1。`n` 是 Harmonic Frequency：

`wave = [cos(nφ) + ½ cos(2nφ) + ⅓ cos(3nφ)] / (1 + ½ + ⅓)`

`r = R(z) + Amplitude × env × wave`

内壁是同一条函数再沿半径收进 Wall Thickness。沿法线加厚会在凹槽里对穿，所以不用 Solidify。

## 面板上的起点

| 名字 | 值 | |
|---|---|---|
| Base Radius | 25 mm | 底圈外半径 |
| Harmonic Frequency | 7 | 一圈主肋。8 也能闭上 |
| Resonance Amplitude | 1.5 mm | 2.5 mm 时最薄处是 0.92 mm，低于 1.2 |
| Twist Angle | 60° | 整段高度转过的角 |
| Height | 80 mm | |
| Wall Thickness | 2.0 mm | 沿半径的间隙。真实壁厚更薄 |

## 检查（Amplitude 1.5）

| | |
|---|---|
| 连通体 | 1 |
| 非流形 / 边界 | 0 / 0 |
| 自交 | 0 |
| 体积 | +13568 mm³ |
| 尺寸 | 50 × 50 × 80 mm |
| 最低点 | 0 mm |
| 底环半径 | 23–25 mm |
| 壁厚 | 最薄 1.27 mm，中位 1.89 mm |
| 外侧悬垂 | 0° |

STL：`schumann_resonator.stl`。

顶孔内半径 2 mm，直径约 4 mm。底是 2 mm 宽的环。若要实心底，那是下一步，会改成有底的容器。
