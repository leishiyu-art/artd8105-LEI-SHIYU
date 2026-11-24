---
title: "Plantbot: Integrating Plant and Robot through LLM Modular Agent Networks"
authors: "Atsushi Masumori, Norihiro Maruyama, Itsuki Doi, johnsmith, Hiroki Sato, Takashi Ikegami"
year: 2025
venue: "arXiv preprint, cs.RO"
venue_type: "web"
doi_or_url: "https://doi.org/10.48550/arXiv.2509.05338"
verified: false
stream: "personal"
topic_tags: []         # 你来填
subconversation: ""
relevance: ""          # core | adjacent | background | rejected — 你来选
date_read:
---

# Plantbot: Integrating Plant and Robot through LLM Modular Agent Networks

对照 Downloads 里的 `2509.05338v1.pdf`（8 页，arXiv:2509.05338v1，2025-09-01，许可 CC BY 4.0）。这是 **预印本**，不是某次会议的录用论文。PDF 已放在 `my_work/_local/readings/masumori_2025_plantbot.pdf`（git 忽略，不上传）。第 1、3、4、6、7 节仍须你写。

作者栏第四人在 v1 的 PDF 和元数据里印的就是 **johnsmith**。文末他们自己引用 Maruyama et al. 2025 时，同一位置写成 Johnsmith。没有改成别的名字。

## 1 · Why this paper

（你的话。一两句：为什么现在读这篇。它谈植物、机器人和语言模型怎么接成一个系统，和你已有的 more-than-human / 织造笔记不是同一条线。）

## 2 · Summary

（用你自己的话重写。下面是对照 PDF 的核对骨架，写完后删掉这整段提示。）

- **在谈什么：** Plantbot。一株活的植物、带传感器的土壤、履带移动底盘，中间用一组异步的 LLM 模块用自然语言互相传话。展览：Ginza Skywalk，2024 年 5 月 4–6 日；CCBT，2025 年 1 月 30 日–2 月 2 日（Fig. 1）。
- **贡献（他们自己的说法）：** 把 LLM 当作生物系统和人工系统之间的协议层，而不是只做人机对话界面。植物的生理规范（土干了就要水）被放进感知–运动回路，用来给这个混合体安装规范性。
- **模块：** Vision（GPT-4V，摄像头）；Sensor（GPT-3.5 Turbo，土壤湿度、温度、pH、电导率、钾磷氮，转成短句，例如 “I am thirsty.”）；Chat（GPT-3.5 Turbo，汇总视觉、传感、人的对话）；Action 1（决定 Move 或 Stop）；Action 2（写成具体电机指令；近处有障碍且决定移动时，避障是反射）。模块之间用 OSC。chat / sensor / action 各有长度 10 的历史；vision 无状态。LiDAR 用于避障。麦克风是按键说话。
- **实验看什么：** 不是用户研究。把各模块的话用 text-embedding-ada-002 嵌成向量，再用 UMAP 看聚类（Fig. 4）。词云按模块分开（Fig. 5）。Action 的 Stop 显著多于 Move（Fig. 6）。进入 Stop / Move 之前，Chat 的用词不同（Fig. 7）。文中给了三段从 Stop 转到 Move 的英文日志；原输出是日文，分析时译成英文。
- **讨论里他们收的一句：** 土干了之后去找水，是结构里出来的，不是人直接下的指令。他们把现在的身体叫做 minimal embodiment。模块之间的连线目前是固定的；让连线自己改，写成下一步。也提到将来放到更大的生态系统时要考虑伦理和环境影响。没有单独的 Limitations 节。

## 3 · Critical thinking

（必须是你的判断。作者已经承认：现在只是最小的身体；模块连线是固定的；没有做 GWT 那种全局广播；下一步才谈伦理。你的批评要超过这些。）

可读时自问、答案你写：土壤读数经过语言模型说成 “thirsty”，这还是植物的规范，还是模型替植物说话？Stop 多于 Move、词云里 “stable” 对上 Stop，能不能说明有整合的 agency，还是只说明提示词把角色分开了？两次展览的日志，有没有和现场行为对上的记录？

## 4 · Creative thinking

（你的话。）

## 5 · Form — read it as a genre, not just as content

对照 2025-09-01 这份 v1。体裁是 **arXiv 预印本**（cs.RO），8 页，不是会议长文。

- **Length**, excluding references: 正文到 Acknowledgment，PDF 第 7 页上半。References 从第 7 页下半到第 8 页。
- **Section proportions** (按版面粗估): Introduction ~2 页 · System（硬件 + 五个模块）~2 页 · Experiments（图 4–7 和三段日志）~2 页 · Discussion ~1.5 页。
- **Where does the contribution claim first appear?** 摘要，PDF 第 1 页。
- **The contribution sentence, verbatim:** “We introduce Plantbot, a hybrid lifeform that connects a living plant with a mobile robot through a network of large language model (LLM) modules.” (PDF p. 1)
- **Artifact description vs. analysis** — System 和 Experiments 占大部分。Discussion 短，主要在重述“自然语言协议”和“植物安装规范性”，并写下一步。
- **What does related work do** — 引言按三条摆：植物–机器人混合、LLM agent、语言控制的机器人。用来指出别人多停在低层信号或人机界面，不是逐篇做 gap 表。
- **How is process evidenced?** 两次展览的日期和地点；模块型号；历史长度 n = 10；三段译成英文的日志。没有访谈、没有人数、没有统计检验的报告正文（Fig. 6 说 Stop “significantly” 更多，正文没给检验）。
- **Figures:** 7 张。Fig. 1 展览现场，Fig. 2 系统，Fig. 3 硬件，Fig. 4 UMAP，Fig. 5–7 词云和 Stop/Move。图在承担结果，不只是外观。
- **First person or passive? Present or past tense?** 第一人称 **we**。系统描述现在时；展览和日志过去时。
- **Limitations — present? How much space?** 无独立 Limitations。Discussion 用约一段承认身体是最小的、连线是固定的、伦理留到以后。

## 6 · Venue signal

（你的判断。这是预印本，还没有“被哪个会收下”这件事。若你要把它当 cs.RO / 人工生命的写作样本，写你看到它奖励什么。）

## 7 · Take-home

（你的话。）

## 8 · Quotable

页码是这份 PDF 的页码。对着 PDF 再看一眼。不需要的删掉。

> We introduce Plantbot, a hybrid lifeform that connects a living plant with a mobile robot through a network of large language model (LLM) modules. (p. 1)

> The significance of this system lies in demonstrating that LLMs can serve as a natural-language-based protocol layer capable of binding together different sub systems (e.g., biological and artificial) into a single agent. (p. 6)

> The plant in this architecture does not simply exist; it plays a role in naturally installing this norm into the LLM-driven agent. (p. 6)

> While our current prototype achieves just a minimal embodiment, future iterations could incorporate richer internal sensing modalities like a bioelectric potential (i.e., interoception), and enhanced memory mechanisms. (p. 6)
