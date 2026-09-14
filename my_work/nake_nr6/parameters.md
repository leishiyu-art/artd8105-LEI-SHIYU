# Parameters — Felder mit Rechteckschraffuren Nr. 6

*Reconstruction of Frieder Nake, 02/09/1965. Random elements from Nake et al., Programm-Information PI-21 (1966), p. 10. Everything else is marked 补全 / supplemented — needed to execute, not claimed as his numbers.*

*14 September 2026. 七项各有开关：开 = 交给伪随机；关 = 你手定。伪随机本身不是第八项，是引擎。*

---

## Nake 的七项随机 / The seven random elements

| 参数<br>Parameter | 来源<br>From | 范围<br>Range | 打开时<br>Opens at | 为什么是这个范围<br>Why this range |
|---|---|---|---|---|
| 填几个 field<br>*Amount of fields to be filled* | PI-21 p.10 | 1–全部格子 | 随机：6–12 / 16 | *(待你定)* |
| 选哪些 field<br>*Selection of these fields* | PI-21 p.10 | 格子的一个子集 | 随机抽 | *(待你定)* |
| 每个 field 里几个 square<br>*Amount of squares in each field* | PI-21 p.10 | 1–12 | 随机：3–7 | *(待你定)* |
| square 的大小<br>*Size of the squares* | PI-21 p.10 | field 边长的 0.20–1.00 | 随机：0.35–0.85 | *(待你定)* |
| 影线密度<br>*Density of the hatching* | PI-21 p.10 | 线距 0.6–8.0 mm | 随机：1.2–4.0 mm | *(待你定)* |
| 影线方向<br>*Direction of the hatching* | PI-21 p.10 | 横 或 竖 | 随机：各半 | *(待你定)* |
| 用哪支笔<br>*Choice of drawing pen* | 你的变体（原 PI-21：bi-colored） | 黑 / 荧光绿 / 紫 / 荧光粉，各有 portion | 随机：四色均等 5·5·5·5 | *(待你定)* |

**最后一栏是你的。** 说不出为什么，就是还没做这个决定。

---

## 开关（14 Sep · 你的决定）

每一项都可以从系统手里收回。

- **开 · 交给随机** — Nake 的写法：他框范围，这一次的值由伪随机抽。
- **关 · 你来定** — 该项目在所有格子/方块上用同一个你给的值。

七项全开 = 原 protocol。关掉一项 = 你开始改他的作者权边界。

---

## 符号库 · 你的变体（14 Sep）

*不是 PI-21。七项骨架不动；格子里能画的东西扩成一套符号。*

| 符号 | 默认 | 说明 |
|---|---|---|
| 横影线 | 开 | PI-21 方向 = 水平 |
| 竖影线 | 开 | PI-21 方向 = 竖直 |
| 实心 | 关 | 填充方块 |
| 空框 | 关 | 只有边线的方块 |
| 爱心 | 关 | 笔触轮廓心形 |
| ∞ infinity | 关 | 双纽线 / lemniscate |

- **手定用哪几种** — 勾选。至少保留一种；全关掉会退回横+竖。
- 每个 square 再从勾选里用 seed 抽一个。
- 影线密度（第 05 项）只作用于横/竖影线；实心、空框、爱心、∞ 不受密度影响。
- 第 06 项关掉并锁方向时：会从有效库里拿掉另一种影线（例如锁「只要横」则竖影线不出现）。
- 「只要影线 · 原作」= 只开横+竖；「六种全开」= 你的细节变体。
- 「七项全开 · Nake mode」会同时把符号库重置为只要影线。

**Breaking point 提示：** 爱心和 ∞ 一进画面，还算不算 Nr. 6 这一类——这条边界是你的，不是 Nake 的。

---

## 伪随机 / Seed — 引擎，不是第八项

| 参数 | 来源 | 范围 | 打开时 | 为什么 |
|---|---|---|---|---|
| Seed | 执行机制 | 0–∞ | 20965（日期 2/09/1965） | 同一 seed + 同一开关状态 = 同一张图 |

换 seed：同一规则下的另一次执行。改七项或开关：改规则。

---

## 补全 — 文献没写死、不补就无法执行

| 参数 | 来源 | 打开时 | 备注 |
|---|---|---|---|
| 画面 | 原作 40 × 40 cm | 400 × 400 mm（1:1 毫米） | 正方形 |
| Field 网格 | 补全。「Felder」需要先分区 | 4 × 4 = 16 | PI-21 没写几行几列。这是结构，不是七项之一。 |
| Square 在 field 里的位置 | 补全。同系列别的作品写过 Position，Nr. 6 没写 | 始终由 seed 抽，留在 field 内 | 没有单独开关 |
| 方块可否重叠 | 补全。同系列常见重叠影线 | 可重叠，裁在本 field 内 | |
| 两支笔的颜色 | ~~原作 bi-colored~~ → 你的四色变体 | 见下表 | 纸仍为白 |
| 线宽 | 补全 | 0.35 mm | Graphomat 笔宽的一个可用值 |
| Field 边界线 | 工具，不是原作 | 默认关 | 用来看分区，不是图画的一部分 |

### 笔色（14 Sep · EVA-01 变体）

纸：**白** `#ffffff`（不用色板里的浅灰）。

| 笔 | Hex | 来源 |
|---|---|---|
| 黑 / 深炭 | `#242834` | 色板最下块（取样） |
| 荧光绿 | `#b6fe02` | 色板主色（取样） |
| 紫 | `#8053fc` | 色板（取样） |
| 荧光粉 | `#ff3dbe` | **你加的**；不在原色板四块里 |

参考图：`my_work/nake_nr6/palette_eva01.jpg`

**Portion：** 第 07 项「交给随机」时，四支笔各有 0–20 的相对权重；为 0 则不出现；全 0 则四色均等。关掉随机则锁成单一笔色。

---

## 三块区域

**Boring** — 拧了也不在乎。

**Surprising** — 不再像你记忆里的 Nr. 6，但仍是这七项的合法执行。

**Breaking point** — 不再是 Nr. 6 这类作品。

---

## What I rejected, and why
