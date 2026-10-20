# PlanetaryMonolith

物体 `PlanetaryMonolith`。修改器：`Monolith` → `Smooth by Angle`（30°）。1 单位 = 1 mm。

平顶封死，底是平的环，开口朝下，贴着打印床。截面是三叶瓣，不是圆。外面是一层层向内收的台阶。

两条里面选了三叶瓣：`r = R(z) · (1 + Lobe · cos(3θ))`。Lobe 为 0 时回到圆。

## 函数

平均半径从底到顶直线变细，再按层高取 floor。台阶只向内收。

`z_step = floor(z / Step Height + 0.001) · Step Height`

`R = Base + (Top − Base) · z_step / Height`

内壁不用 floor。向内的台阶如果做在空腔里，会朝下悬出。空腔是平滑变细，到顶部用一个锥收口。锥的高度按最宽的内半径算，斜度锁在大约 37°（离竖直）。平盖横跨空腔的话，中间没有支撑。

内壁半径是外壁减去 Wall Thickness。

## 面板

| 名字 | 值 | |
|---|---|---|
| Base Radius | 32 mm | 底部平均半径。叶尖大约 39 mm，叶谷大约 25 mm |
| Top Radius | 16 mm | 平顶的平均半径。叶尖大约 19.5 mm |
| Lobe | 0.22 | 三叶深浅 |
| Step Height | 2.0 mm | 十层 0.2 mm。每一级半径大约收 0.4 mm |
| Height | 80 mm | |
| Wall Thickness | 2.5 mm | 沿半径 |

锥高大约 35 mm，从 z ≈ 43 mm 收到顶盖下面。这是算出来的，不是滑条。

## 检查

| | |
|---|---|
| 连通体 | 1 |
| 非流形 / 边界 | 0 / 0 |
| 自交 | 0 |
| 体积 | +50412 mm³ |
| 尺寸 | 66.8 × 71.7 × 80 mm |
| 底半径 | 22.4–39.0 mm |
| 顶 | 中心到 19.5 mm，平的，封死 |
| 壁厚 min / p5 / p50 | 2.02 / 2.10 / 2.42 mm |
| 外侧面离竖直 | 0° |
| 内锥离竖直 | 36.8° |
| 超过 45° 的面 | 0 |

`planetary_monolith.stl`，135360 个三角形，约 6.8 MB。`check_stl.py` 也对上：一个闭合壳。

先前的几个物体还在文件里，只是视口里藏了。
