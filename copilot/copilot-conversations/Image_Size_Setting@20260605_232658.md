---
epoch: 1780673218177
modelKey: "gemini-2.5-flash|google"
topic: "Image Size Setting"



tags:
  - copilot-conversation
---

**user**: [|587/400](../../Truchas_Lab/II.%20Truchas/D.%202.5.3版/pics/Pasted%20image%2020260605231731.png)

圖片大小的設定是這樣寫嗎
[Context: Notes: Truchas_Lab/01_Truchas/00_2.5.3版/未命名.md]
[Timestamp: 2026/06/05 23:26:58]

**ai**: 您好！您目前使用的圖片大小設定方式 `![|587/400](pics/Pasted%20image%2020260605231731.png)` 並不是 Obsidian 官方建議的內部圖片連結調整大小語法。

在 Obsidian 中，如果您要調整內部連結圖片的大小，正確的語法應該是將尺寸參數放在雙方括號 `[[...]]` 內部，並使用 `|` 分隔圖片名稱和尺寸。

以下是正確的寫法：

1.  **只設定寬度：**
    `![[圖片路徑/圖片名稱.png|寬度]]`
    例如：`![[pics/Pasted image 20260605231731.png|587]]`

2.  **同時設定寬度和高度：**
    `![[圖片路徑/圖片名稱.png|寬度x高度]]`
    例如：`![[pics/Pasted image 20260605231731.png|587x400]]`

所以，您筆記中的圖片連結應該修改為：

```markdown
| ![[pics/Pasted image 20260605231731.png|587x400]] | ![[pics/Pasted image 20260605231619.png|325x400]] |
| ------------------------------------------------------ | ------------------------------------------------------- |
| ![[pics/Pasted image 20260605232403.png|587x400]] | ![[pics/Pasted image 20260605232500.png|587x400]] |
|                                                        |                                                         |
```

這樣 Obsidian 就能正確解析並顯示您設定的圖片大小了。
[Timestamp: 2026/06/05 23:27:07]