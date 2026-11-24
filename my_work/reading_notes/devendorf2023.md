---
title: "AdaCAD: Parametric Design as a New Form of Notation for Complex Weaving"
authors: "Laura Devendorf, Kathryn Walters, Marianne Fairbanks, Etta Sandry, Emma Goodwill"
year: 2023
venue: "CHI 2023, Hamburg"
venue_type: "conference"
doi_or_url: "https://doi.org/10.1145/3544548.3581571"
verified: true
stream: "personal"
topic_tags: []         # 你来填，例如 weaving / parametric-design / notation / craft-hci
subconversation: ""
relevance: ""          # core | adjacent | background | rejected — 你来选
date_read: 2026-11-22
---

# AdaCAD: Parametric Design as a New Form of Notation for Complex Weaving

对照 Downloads 里的 PDF（18 页，CHI ’23）。开源工具论文，不是 more-than-human 物种研究。PDF 在 `my_work/_local/readings/devendorf_2023_adacad.pdf`（git 忽略）。第 1、3、4、6、7 节仍须你写。

## 1 · Why this paper

（你的话。一两句：为什么现在读这篇。它和你已有的 more-than-human 笔记不是同一条线；它谈的是工艺知识怎么被记下来、怎么在织工和 HCI 之间流通。）

## 2 · Summary

（用你自己的话重写。下面是对照 PDF 的核对骨架，写完后删掉这整段提示。）

- **在谈什么：** AdaCAD，一个开源的参数化织造设计工具。织造草稿（draft）是给人和机器的指令。参数化是把操作连成数据流：改参数，结构就变。论文主张：这种数据流可以当作一种新的记谱（notation），记下复杂织物结构是怎么来的，而不只是最后那张图。
- **贡献：** (1) 软件本身（界面操作 + 代码库两条入口）；(2) 把参数化设计放进织造记谱史（小样、draft、穿孔卡、位图）；(3) 用 Star 与 Griesemer 的 boundary object / methods standardization 说明它如何让织工和 HCI 共事，又不把工艺收成一种标准流程。
- **问题：** HCI 越来越用织物做软电路、传感器、可变形结构，但有效使用需要多年默会知识。工程侧常把工艺标准化、减少材料变化。作者认为工具应让人「和材料一起想」，并记下涌现出来的过程。Pouta 等要求公开 draft；作者说只公开成品 draft 不够，因为看不出结构背后的逻辑，织工自己也常记不住。
- **做法：** first-person：Devendorf 从 2016 年起为自己的电子织物实践做工具（AdaCAD 1.0–2.0 偏直接画像素，3.0 改成参数化入口）。再和三位 complex weavers 合作，她们也是共同作者：Kathryn Walters、Etta Sandry、Marianne Fairbanks。公开演讲、视频、文档之后，按兴趣招募；大约每月见面，看软件、改操作。没有付费（文中写明）。发现写进软件功能，而不是单独的访谈语料库。
- **三条发现：**
  - **织工的 alchemy：** 做法绑在织机、地区术语和草稿方向上。Etta 的 direct-tie loom 和「先结构、再自动生成综框」冲突，空白画布让她无从下手，底层代码因此重写。Kathryn 的北欧传统是左到右、下到上，和软件默认方向相反，不信任画面，直到加了方向设置。
  - **打开新实验：** Marianne 要「N×N draft 的每一种结构」（对照历史上只有 tabby / twill / satin）。做出 all-possible-drafts。她写信把这比作 Sol LeWitt。
  - **过程记谱：** 参数化让人从微到宏，和 Photoshop / Pointcarré 的自上而下相反，Marianne 说 disorienting。Kathryn 的多层「Dragon Scales / 折成盒子」有一套手写区域记号；他们把它做成文字输入操作，由她织样确认能用。
- **讨论里他们收的一句：** 有的困难是有生产性的谜题；不支持不同织机和草稿方向则是阻碍，不是有用的约束。参数化提供一套共同词汇（操作说的是「做什么」，不是「叫什么」），个人差异在这套词汇里展开。和织工一起做软件，不是替他们总结然后自动化。

## 3 · Critical thinking

（必须是你的判断。作者已经承认：三人不能代表所有织工；first-person 一开始特权了自己的织机；有些困难只是障碍；协作者没有付费。你的批评要超过这些。）

可读时自问、答案你写：「记谱」是把默会知识说清楚，还是把织造收成计算机能读的操作？boundary object 在文中有没有被合作者自己这样用，还是作者事后贴上的理论？三位合作者同时是共同作者，发现和宣传工具的边界在哪里？

## 4 · Creative thinking

（你的话。参数化记谱、和材料实践者一起改工具，能不能用到你关心的多方 agency？）

## 5 · Form — read it as a genre, not just as content

对照 2026-11-22 这份 PDF。CHI 长文，系统 + 合作评估。

- **Length**, excluding references: PDF 18 页。正文到 Conclusion 止于 PDF 第 16 页；Acknowledgments 与 References 从第 17 页起。不含参考文献约 16 页。
- **Section proportions** (按版面粗估，含图): §1 Introduction ~8% · §2 Background ~12% · §3 AdaCAD 与方法 ~22% · §4 Findings ~28% · §5 Discussion ~18% · §6–7 Future work 与 Conclusion ~4% · 图占其余版面。重心在合作过程与三则发现，不在算法。
- **Where does the contribution claim first appear?** 摘要后半（PDF 第 1 页）；§1 末段把贡献写成书面论证加软件功能。
- **The contribution sentence, verbatim:** “Our study revealed that parametric design offers a promising option for notating the rationales by which complex structures emerge.” (Figure 1 说明，PDF 第 1 页)
- **Artifact description vs. analysis** — §3 讲界面、操作和版本时间线；§4 用三个合作故事做分析。分析（发现 + 讨论）多于界面说明书。布样照片证明工具被用过。
- **What does related work do** — §2 先界定 woven / warp / weft，再把织造放进 HCI 与工艺工具。引言用 Pouta 等的「要公开 pattern」**搭 gap**：公开成品不够，缺的是结构逻辑。
- **How is process evidenced?** 第一人称织造与展览、功能时间线（Figure 6，标出本研究直接加上的功能）、合作者草图、邮件、以及由手写记号做成的操作。会议大约每月一次。作者写明没有系统日志。
- **Figures:** 11。Fig.1 工具与布样；Fig.2 结构操作；Fig.3 工作流；Fig.4–5 参数化界面；Fig.6 版本时间线；Fig.7–11 合作者项目与操作（传感器、Song 的双层布、Etta/Kathryn 的两种设计、全结构生成、Kathryn 的层记号）。图既展示界面，也展示记谱前后。
- **First person or passive? Present or past tense?** 第一人称 **we**，Devendorf 的设计决定用 **I**。方法与合作用过去时；记谱主张用现在时。
- **Limitations — present? How much space?** 无独立 Limitations。§5 开头区分「有生产性的困难」和「阻碍」。§5.2 承认小组不能代表所有织法。§3.3 写明协作者未付费，以及 first-person 的效度靠 genuine use。

## 6 · Venue signal

（你的判断。CHI 收这篇，说明它奖励什么样的工具论文、第一人称方法和工艺合作？）

## 7 · Take-home

（你的话：学到什么、对你的研究能用什么、要不要当 CHI 系统论文的写作样本。）

## 8 · Quotable

页码按 PDF。对着文件再看一眼。不需要的删掉。

> Our study revealed that parametric design offers a promising option for notating the rationales by which complex structures emerge. (PDF p. 1, Figure 1)

> These findings led us to understand AdaCAD as a notational system for describing the processes and rationales through which a particular woven structure came about. (PDF p. 2)

> We believe that AdaCAD offers a middle ground between the draft and woven cloth that can serve to advance textile innovation by providing a new means of notation for weaving. (PDF p. 15)

> We see AdaCAD as a possible boundary object in its role as a collaborative and shared digital space accessible to both communities. (PDF p. 16)

> Our final discussion point is to call attention and reflect upon our process of developing open-source software in collaboration with weavers (in contrast to for weavers). (PDF p. 16)
