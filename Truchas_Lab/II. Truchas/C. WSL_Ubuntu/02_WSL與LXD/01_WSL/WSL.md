---
topic:
project: Truchas-Lab
status: 🟢 Active
type: 📝 Research
created: 2026-05-13 00:23
modified: 2026-06-09 16:29
tags:
  - WSL
  - Linux
  - LXD
---
# 📂 本文關聯檔案索引
```dataview
LIST
WHERE contains(this.file.outlinks, file.link)
AND !icontains(file.name, ".png")
AND !icontains(file.name, ".jpg") 
AND !icontains(file.name, ".pdf")
AND !icontains(file.name, "excalidraw")
```
# 📌 摘要與目標


# 📝 內容紀錄
## WSL 是什麼?

WSL（Windows Subsystem for Linux，適用於 Linux 的 Windows 子系統）是微軟開發的一項 Windows 內建功能，讓使用者能在 Windows 電腦上直接執行 Linux 環境。它省去了過去需要安裝個別虛擬機（如 VMware、VirtualBox）或設定雙系統的麻煩，讓開發人員可以同時享受 Windows 的日常便利與 Linux 的強大開發工具。 [[1](https://learn.microsoft.com/zh-tw/windows/wsl/about)]

### 💡 核心優點與特色

- **無縫整合**：Windows 與 Linux 的檔案系統相互打通，可以直接在 Windows 讀取 Linux 檔案。
- **資源消耗極低**：比傳統虛擬機更輕量，啟動通常只需幾秒鐘。
- **支援主流發行版**：可直接透過 [Microsoft Store](https://learn.microsoft.com/zh-tw/windows/wsl/about) 安裝 Ubuntu、Debian、Kali Linux 等多種系統。
- **GPU 加速**：支援顯卡直通，可直接在 WSL 裡跑深度學習或機器訓練。

### 🛠️ 可以用來做什麼？

- 執行常用的 Linux 終端機指令（如 `grep`、`sed`、`awk`）。
- 執行 Bash 腳本與各類程式語言環境（如 Python、Node.js、Rust、Go、C++）。
- 流暢運行 [Docker](https://www.reddit.com/r/webdev/comments/1eo6wdn/what_does_wsl_actually_do_and_why_is_it_needed/?tl=zh-hant) 容器化開發環境。
- 亦可以針對不同研究主題設置 [(LXD vs Docker ?)](../../01_116版_2.0.2/pics/LXD_Docker_.venv.md)
- 使用 Linux 套件管理工具（如 `apt`）一鍵下載安裝各式軟體。 

### 🔄 WSL 1 與 WSL 2 的差別

微軟目前主要推薦使用 **WSL 2**，兩者架構有顯著不同： [[1](https://learn.microsoft.com/zh-tw/windows/wsl/compare-versions)]

| 比較項目 [[1](https://zh.wikipedia.org/zh-tw/%E9%80%82%E7%94%A8%E4%BA%8ELinux%E7%9A%84Windows%E5%AD%90%E7%B3%BB%E7%BB%9F), [2](https://ithelp.ithome.com.tw/m/articles/10368740), [3](https://learn.microsoft.com/zh-tw/windows/wsl/compare-versions)] | WSL 1                         | WSL 2 (目前主流)              |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | ------------------------- |
| **運作原理**                                                                                                                                                                                                                                           | 轉譯層（將 Linux 指令轉換為 Windows 指令） | 微型虛擬機（內含微軟優化的真正 Linux 核心） |
| **執行效能**                                                                                                                                                                                                                                           | 檔案系統存取效能較慢                    | 檔案系統存取極快，提升數倍             |
| **相容性**                                                                                                                                                                                                                                            | 無法執行需要完整內核的軟體（如 Docker）       | 100% 完整 Linux 系統相容性       |

### 🚀 如何快速安裝？

在 Windows 10 (2004 以上) 或 Windows 11 中，只需**以系統管理員身分**開啟 PowerShell 或命令提示字元（CMD），輸入以下指令即可一鍵完成安裝：


```
wsl --install
```



安裝完成後依提示重啟電腦，系統預設會自動幫你裝好最新版的 [Ubuntu](https://learn.microsoft.com/zh-tw/windows/wsl/install) 環境。 [[1](https://learn.microsoft.com/zh-tw/windows/wsl/install)]


### 💼 匯出/匯入整個 WSL
```
# 先關閉 WSL 確保資料完整
wsl --shutdown

# 匯出打包 (可用 wsl -l -v 查看想打包的 WSL 名稱，假設是 Ubuntu-20260407)
wsl --export Ubuntu-20260407 D:\Truchas_Parallel_Full_20260407.tar

# 匯入打包好的WSL (WSL名稱取為Truchas-Lab，位置設在 D:\WSL_Truchas)
wsl --import Truchas-Lab D:\WSL_Truchas D:\Truchas_Parallel_Full_20260407.tar

# 登入 WSL
wsl -d Truchas-Lab
```
---
# 🔗 參考資料
