---
type: 📝 Research
created: 2026-08-25 03:40
modified: 2026-08-31 13:59
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

[聊天紀錄_編譯功能 # TURN 4](../C.%20Truchsa-WSL/02_Truchas-2.0.2/00_聊天紀錄/Gemini/移植-Truchas-編譯器版本確認/聊天紀錄_編譯功能.md#TURN%204)

| 項目           | 實驗室機台 (superstorm) | LXD 容器 (truchas-student) | 狀態                          |
| ------------ | ------------------ | ------------------------ | --------------------------- |
| GCC/Gfortran | 4.6.3              | 4.6.4                    | 幾乎一致 (微版本差異不影響編譯)           |
| MPI 實作       | LAM/MPI            | LAM/MPI                  | 一致 (這非常難得，現代 Ubuntu 幾乎找不到了) |
| CMake        | 2.8.8              | 未安裝                      | 待解決                         |
|              |                    |                          |                             |
|              |                    |                          |                             |


- 由於您的工具鏈（GCC 4.6.4）非常舊，我們不能隨便安裝一個最新版的 CMake，否則它產生的編譯指令可能會讓舊編譯器無法理解。為了保證環境與實驗室機台完全一致，我們需要手動在容器內安裝 **CMake 2.8.8** 或相近版本（2.8.12 也可以）。**與實驗室對齊：** 實驗室是 2.8.8，我們安裝 2.8.12 是為了獲得更好的穩定性，這兩者在語法上是高度相容的。**不影響舊設定：** 這個操作只會增加一個 `/usr/local/bin/cmake` 指令，不會動到您 `/opt/lahey` 或 `/opt/lam-6.5.9` 的配置。[聊天紀錄_編譯功能 # TURN 7](../C.%20Truchsa-WSL/02_Truchas-2.0.2/00_聊天紀錄/Gemini/移植-Truchas-編譯器版本確認/聊天紀錄_編譯功能.md#TURN%207)
- 
- 只打包 `/usr/bin/cmake` 單一檔案**恐怕無法運作**。 從您的 `ldd` 輸出可以看到，這台機台的 `cmake` 依賴了非常龐大的系統函式庫（超過 40 個 `.so` 檔），包括 `libarchive`、`libcurl`、`libssl` 等。由於實驗室機台是 **Red Hat/CentOS** 系列（路徑含 `/lib64`），而您的容器是 **Ubuntu** 系列，這兩者的函式庫名稱與版本存在顯著差異，直接執行會噴出大量 `library not found` 錯誤。


- 從 GitHub 抓取 2.8.12 的靜態編譯版本: 下載 **cmake-2.8.12.2-Linux-i386.tar.gz**。 雖然它是 32 位元版本，但在您的 64 位元 Ubuntu 容器環境下，通常只要有相應的 32 位元相容庫，它依然可以正常運作。[聊天紀錄_編譯功能 # TURN 10](../C.%20Truchsa-WSL/02_Truchas-2.0.2/00_聊天紀錄/Gemini/移植-Truchas-編譯器版本確認/聊天紀錄_編譯功能.md#TURN%2010)

<font color="#ffc000">如果專案本身完全是用 `GNUmakefile` 打造，你**完全不需要安裝 CMake**，不論是新版還是舊版都不需要。但是 packages 內的套件（PGSLib、Ubiksolve、Chaco）需要</font>










---
# 🔗 參考資料
[實驗室機台-Truchas-移植回顧：CMake](聊天紀錄/實驗室機台-Truchas-移植回顧：CMake.md)

---