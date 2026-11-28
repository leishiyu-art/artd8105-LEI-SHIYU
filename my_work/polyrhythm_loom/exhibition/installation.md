# 布展要求

Installation requirements

整理日期：2026-11-28。事实只来自 `project_document.md`、`exhibition/wall_label.md` 和已经在仓库里的文件。方括号是那些文件里没有写上的事实，没有补造。

## 作品

與多重節律共織 / Weaving With：Polyrhythm Loom

雷詩語 / Lei Shiyu

一片濕地是由生態、物質與技術系統交織而成的環境。從地下的土壤與水分、地表的潮汐與生物，到空氣中的光照與無線網絡信號，不同的非人類行動者各有節律，卻又彼此牽連。我們如何感知這些跨越時空尺度的關係？

作品以澳門的路氹城生態保護區,為取樣與探索場域，借鑑地球關鍵帶（Critical Zone）的分層視角，透過環境感測裝置與互動網頁，將環境數據轉譯為交織的視覺節律，邀請觀眾探索不同時間尺度的交錯與共存。

作品提出「數據作為關係」，數據不僅記錄環境，也在感測、轉譯與體驗中生成，參與塑造人與非人類行動者的關係。從閱讀數值到親身經歷，邀請我們與環境的多重節律共同編織。

A wetland is an entanglement of ecological, material, and technological systems. From soil and water underground to tides, organisms, sunlight, and wireless signals, more-than-human agents follow distinct yet interconnected rhythms. How might we perceive these relationships across space and time?

Taking Macao’s Cotai Ecological Zones as a site for sampling and exploration, the work draws on the layered perspective of the Critical Zone. Through environmental sensors and an interactive web experience, it translates environmental data into interwoven visual rhythms, inviting visitors to explore how different temporalities intersect and coexist.

The work proposes Data as Relation, data does not merely record the environment, but takes shape through sensing, translation, and experience, actively shaping relationships between humans and more-than-human agents. Moving beyond reading numbers, it invites us to experience and weave with the rhythms of our shared environment.

## 现场已经能对上的设备

来自 2026-11-22 的项目文档和两张展位照片：

- 一张桌子。桌上从左到右是说明页。
- 一台显示器。画面是织布界面。显示器顶上有一个摄像头，给网页里的手势用。下面接脚踏板作为输入。
- 左侧立架上的主视觉。
- 桌上的说明页：场地、时间尺度、方法、系统，以及《怎么参与》。
- 播放页是 `polyrhythm_loom/tablet.html`。手势需要浏览器允许摄像头，并且用 https 打开。本机带走图的服务写在 `serve_takeaway.py`，端口 8770。带走的文件在 `my_work/_local/takeaway/`，git 不跟踪。

## 接上传感板

`project_document.md` 写的接线，两份程序相同，板子是 Arduino UNO R4 WiFi。程序不写 SD 卡。串口 115200，输出 CSV。

- DS18B20 信号 → D2
- 光线模拟 → A2
- 按钮 → D7 和 GND

带屏幕的那一份另接 SH1106 OLED，SDA A4，SCL A5。进仓库的户外记录只有 2026-11-17 的几行。不能写成一次完整的泥滩采样。



