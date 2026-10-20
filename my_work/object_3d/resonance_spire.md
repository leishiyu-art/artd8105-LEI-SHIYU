# ResonanceSpire

物体 `ResonanceSpire`。修改器：`Spire` → `Smooth by Angle`（30°）。1 单位 = 1 mm。

圆截面。底是平的环，贴着打印床。腰收进去，中段再鼓起，然后收到一个没有孔的尖。三叶瓣那一版留在 `PlanetaryMonolith`，视口里藏了。

## 函数

`t = z / Height`

`R = Base + (Waist − Base) · s(0.06, 0.42) + (Core − Waist) · s(0.42, 0.55)`

`t > 0.55` 之后，`R = Core · (1 − u)`，`u` 从 0 到 1，顶端是 0。

凹槽是 `A · cos(7θ)`。`A` 不超过 `min(Flute Depth, 1.40 · R / 7)`。底面以上大约 1–11 mm 才逐渐出现，所以落脚的那一圈是圆的。尖端随半径变浅，到顶点是 0。

等高线只加在半径正在变小的地方，层高 0.5 mm，台阶向内。中段鼓起如果也做成台阶，会向外悬出。

内壁是同一条半径减去 Wall Thickness，再减去同一条凹槽。空腔在尖端前大约 5 mm 收到轴上，最后那一截是实心的。再尖、或者中段再粗，内壁就会超过 45°。

## 面板

| 名字 | 值 | |
|---|---|---|
| Base Radius | 36 mm | 底 |
| Waist Radius | 20 mm | 大约 z = 34 mm |
| Core Radius | 26 mm | 大约 z = 44 mm。面板上限 32，拉满会过 45° |
| Height | 80 mm | |
| Flute Count | 7 | 可改 8 |
| Flute Depth | 4.5 mm | 鼓起处大约用满。腰大约 4 mm |
| Step Height | 0.5 mm | 只在收进去的外表面 |
| Wall Thickness | 3.8 mm | 沿半径 |

## 检查

| | |
|---|---|
| 连通体 | 1 |
| 非流形 / 边界 | 0 / 0 |
| 自交 | 0 |
| 体积 | +37621 mm³ |
| 尺寸 | 75.2 × 76.7 × 80 mm |
| 底半径 | 32.2–36.0 mm，圆的 |
| 顶 | 收到 0，没有孔 |
| 壁厚 min / p5 / p50 | 1.88 / 2.05 / 2.83 mm |
| 外侧面离竖直 | 44.2° |
| 内壁离竖直 | 43.2° |
| 超过 45° 的面 | 0 |

`resonance_spire.stl`，125342 个三角形，约 6.3 MB。`check_stl.py` 也对上：一个闭合壳。
