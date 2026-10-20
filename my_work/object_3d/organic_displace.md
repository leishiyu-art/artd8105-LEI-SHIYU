# OrganicDisplace — FDM 可打的一版

物体 `SphereTubeNet`。修改器顺序：`OrganicDisplace` → `Wall`（Solidify 2.0 mm）→ `Smooth by Angle`。1 单位 = 1 mm。

上一版 Frequency 6、Amplitude 12、Noise Scale 3.22 时，瓣互相穿过，非流形边 956。普通喷头打不了。这一版把规则收回到还能打的范围。

## 这一版留着的规则

- 外形只跟高度上的余弦走：`偏移 = Normal × Amplitude × cos(π × Frequency × Z / Radius)`。主噪声不再加进偏移。
- 域畸变还在，但 Warp Amount 收到 4 mm。Voronoi 的 Randomness 固定为 0，细胞更齐。
- 孔仍是 Distance to Edge 挖穿，再 Solidify 2 mm 封边。

## 打印用的数

| 名字 | 值 | 为什么是这个数 |
|---|---|---|
| Base Radius | 30 mm | 原来的尺度 |
| Warp Amount | 4 mm | 再大，壳会自己折进去 |
| Noise Scale | 0.4 | 只影响畸变的粗细 |
| Breathing Frequency | 1 | 一次收–胀–收。6 会让瓣穿在一起 |
| Amplitude | 4 mm | 12 mm 在这个半径上会自交 |
| Cell Scale | 0.18 | 孔的周长大约 9–11 mm |
| Wall Band | 0.35 | 再低，加厚之后出现非流形边 |
| Wall thickness | 2.0 mm | 高于 1.2 mm 的底线 |

## 检查

| | |
|---|---|
| 连通体 | 1 |
| 非流形边 / 边界边 | 0 / 0 |
| 自交 | 0 |
| 体积 | +22917 mm³ |
| Min Z | 2.20 mm |
| 包围盒 | 70 × 70 × 54 mm |
| 面（加厚后） | 10308 |

STL：`organic_fdm.stl`。

底面仍是拱起的，切片时底部孔的边缘可能要支撑。这不是树脂才能打的细网格，是一层 2 mm 的带孔壳。
