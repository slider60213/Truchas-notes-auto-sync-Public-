---
type: 📝 Research
created: 2026-06-19 04:28
modified: 2026-06-30 19:53
tags:
  - "#Truchas"
  - 電腦/WINDOWS/WSL
---
## 📂 本文關聯檔案索引
```dataview
LIST
WHERE contains(this.file.outlinks, file.link)
AND !icontains(file.name, ".png")
AND !icontains(file.name, ".jpg") 
AND !icontains(file.name, ".pdf")
AND !icontains(file.name, "excalidraw")
```

---
# 📌 摘要


## 1. 創建捷徑

- 執行 `MakeShortcut.bat` 來生成捷徑 `Truchas_WSL_GUI`，未來只需要執行這個捷徑即可。
- 以下內容可自由替換：
	icon.ico 捷徑的圖示
	LoadingPic.png 操作面板的讀取畫面
![|475](pics/Pasted%20image%2020260626201010.png)


## 2. 匯入 WSL
- 點開捷徑後，若尚未安裝 WSL，會出現匯入視窗。
- 選擇下載好的 Truchas-WSL 壓縮檔後變會自動匯入。
![|475](pics/Pasted%20image%2020260626183825.png)
![|475](pics/Pasted%20image%2020260626184206.png)

##3. 啟用 WSL+執行模擬
- 點開捷徑後，若已安裝過 Truchas-WSL，會偵測出可啟用的環境。
![|474](pics/Pasted%20image%2020260625153031.png)

- 選擇環境後，會出現操作面板跟 Loading 畫面 (LoadingPic.png)。
- 可點選右下角的按鈕來切換顯示語言。
![|475](pics/Pasted%20image%2020260626202005.png)
![|475](pics/Pasted%20image%2020260626203206.png)
- 讀取完成會自動跳轉到 `problems/tests` 資料夾，若跳轉失敗則需手動執行跳轉。
- 手動跳轉方式：1. 瀏覽選擇資料夾路徑  2. 切換模擬目標環境（LXD）
- 在 `problems/tests` 下選擇已存在的.inp 檔
- 完成後點選 `run_sim` 來執行模擬
![|475](pics/Pasted%20image%2020260622151331.png)
## 3. AI 聊天界面
- 可以透過輸入 API KEY 來連結 GEMINI / CHATGPT。
- 可拖曳檔案到對話框進行詢問。
- 支援 Ctrl+滾輪縮放字體。
![|475](pics/Pasted%20image%2020260620041719.png)
![|475](pics/Pasted%20image%2020260620041753.png)

![|475](pics/Pasted%20image%2020260622151521.png)

---
# 📝 內容紀錄

## 未來完成：

- LXD +/- 功能
- LXD 清單修正
- 互動式創建新.inp
- AI AGENT
- 部分文字翻譯
- 自動更新通知


---
# 🔗 參考資料


---