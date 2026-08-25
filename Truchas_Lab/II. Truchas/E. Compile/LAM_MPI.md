---
type: 📝 Research
created: 2026-08-25 03:40
modified: 2026-08-25 15:08
tags:
  - "#Truchas"
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


---
# 🦖 以前


---
# 👨‍💻 以後


---
# 📝 內容紀錄



[聊天紀錄_編譯功能 # TURN 17](../C.%20Truchsa-WSL/02_Truchas-2.0.2/00_聊天紀錄/Gemini/移植-Truchas-編譯器版本確認/聊天紀錄_編譯功能.md#TURN%2017)
### 1. LAM/MPI 不允許 root 執行

您剛剛執行的 `lamboot` 警告已經說明了一切：LAM/MPI 拒絕在 `root` 權限下啟動。雖然 `make` 只是編譯，但有些舊版專案在編譯 `partition_constants.o` 這類 MPI 相關檔案時，會試圖呼叫 MPI 環境進行檢查。 **修正方法：** 請回到 `user_student` 身份執行編譯，但要確保權限正確。





---
# 🔗 參考資料


---