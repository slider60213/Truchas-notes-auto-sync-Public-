---
topic:
project: Truchas-Lab
status: 🟢 Active
type: 📝 Research
created: 2026-05-13 00:23
modified: 2026-07-20 05:09
tags:
  - 電腦/WINDOWS/WSL
  - 電腦/Linux
  - 電腦/WINDOWS/LXD
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

### 🎨 個人化設定
透過 power shell 輸入 `notepad $env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json`
會跳出 `setting.json` 可於其中設定 WSL 的個人配置，以下內容僅供參考，複製貼上無用必須針對個人電腦調整。
```
{
    "$help": "https://aka.ms/terminal-documentation",
    "$schema": "https://aka.ms/terminal-profiles-schema",
    "actions": 
    [
        {
            "command": 
            {
                "action": "splitPane",
                "split": "auto",
                "splitMode": "duplicate"
            },
            "id": "User.splitPane.A6751878"
        },
        {
            "command": "find",
            "id": "User.find"
        },
        {
            "command": "paste",
            "id": "User.paste"
        },
        {
            "command": 
            {
                "action": "copy",
                "singleLine": false
            },
            "id": "User.copy.644BA8F2"
        }
    ],
    "copyFormatting": "none",
    "copyOnSelect": false,
    "defaultProfile": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
    "keybindings": 
    [
        {
            "id": "User.paste",
            "keys": "ctrl+v"
        },
        {
            "id": "User.find",
            "keys": "ctrl+shift+f"
        },
        {
            "id": "User.copy.644BA8F2",
            "keys": "ctrl+c"
        },
        {
            "id": "User.splitPane.A6751878",
            "keys": "alt+shift+d"
        }
    ],
    "newTabMenu": 
    [
        {
            "type": "remainingProfiles"
        }
    ],
    "profiles": 
    {
        // 所有終端機環境（WSL、PowerShell、CMD）皆會自動繼承此處的視覺預設值
        "defaults": 
        {
            // [變數 1] 圖片路徑：請確保路徑中的斜線為雙反斜線 \\
            "backgroundImage": "C:\\Users\\user\\Desktop\\Truchas_App_Project\\theme\\loading\\Truchas Slider.png",
            
            // [變數 2] 透明度：數值範圍為 0.0 (完全透明) 到 1.0 (完全不透明)
            "backgroundImageOpacity": 0.15, 
            
            // [變數 3] 圖片大小縮放模式：
            // "uniformToFill" -> 等比例拉伸填滿視窗 (目前設定，適合當大背景)
            // "uniform"       -> 保持原圖比例縮放，直到碰到視窗邊緣
            // "none"          -> 保持圖片原本的原始大小，不進行縮放
            "backgroundImageStretchMode": "uniform",
            
            // [變數 4] 圖片對齊位置：可選 "center", "left", "right", "top", "bottom"
            "backgroundImageAlignment": "center",

            // 💡 提示：如果將 StretchMode 改為 "none" 或 "uniform"，
            // 這裡已經取消註解，可以自由自訂圖片的具體像素寬高：
            "backgroundImageHeight": "1600px",
            "backgroundImageWidth": "1600px"
        },
        "list": 
        [
            {
                "commandline": "%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
                "guid": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
                "hidden": false,
                "name": "Windows PowerShell"
            },
            {
                "commandline": "%SystemRoot%\\System32\\cmd.exe",
                "guid": "{0caa0dad-35be-5f56-a8ff-afceeeaa6101}",
                "hidden": false,
                "name": "\u547d\u4ee4\u63d0\u793a\u5b57\u5143"
            },
            {
                "guid": "{b453ae62-4e3d-5e58-b989-0a998ec441b8}",
                "hidden": false,
                "name": "Azure Cloud Shell",
                "source": "Windows.Terminal.Azure"
            },
            {
                "guid": "{4af6b532-e771-585d-9d6c-a046937ee234}",
                "hidden": false,
                "name": "Ubuntu-24.04",
                "source": "Microsoft.WSL"
            },
            {
                "guid": "{8eaa6b02-91c4-56d4-9211-cad6ec54f96e}",
                "hidden": false,
                "name": "Ubuntu-Legacy",
                "source": "Microsoft.WSL"
            },
            {
                "guid": "{60de18b7-9498-5800-a4a0-7a6f9ac32a4b}",
                "hidden": false,
                "name": "Truchas_Lab_20260422",
                "source": "Microsoft.WSL"
            },
            {
                "guid": "{41afc21a-4062-511e-90fa-ed31a2d48929}",
                "hidden": false,
                "name": "Truchas-Lab_20260609",
                "source": "Microsoft.WSL"
            },
            {
                "guid": "{9431cfd9-cb5f-5436-8813-17bf5719831c}",
                "hidden": false,
                "name": "Truchas-Lab-ENG",
                "source": "Microsoft.WSL"
            },
            {
                "guid": "{e2ffec3e-52b7-55b5-8db4-0df48f9bca75}",
                "hidden": false,
                "name": "Truchas-Lab-CHI",
                "source": "Microsoft.WSL"
            },
            {
                "guid": "{47c07f62-b6fa-5f1e-9ce4-3580a6b21ae4}",
                "hidden": false,
                "name": "Truchas-Lab-CHI",
                "source": "Microsoft.WSL"
            },
            {
                "guid": "{6e2da920-8006-5b14-9aca-802210ad63a4}",
                "hidden": false,
                "name": "Truchas-Lab-ENG",
                "source": "Microsoft.WSL"
            }
        ]
    },
    "schemes": [],
    "themes": []
}
```


### 👨‍💻 若為 MAC 用戶

#### 方案 A：使用 Docker 匯入（最快、最直覺）

Mac 上的 Docker 可以直接把 WSL 導出的 `.tar` 檔匯入成一個 Docker 映像檔（Image），並直接啟動。

1. **在 Mac 安裝 Docker Desktop**。
2. **匯入您的 TAR 檔**：打開 Mac 的終端機（Terminal），切換到該檔案所在資料夾，執行：
    
    bash
    
    ```
    docker import Truchas_Parallel_Full_20260407.tar truchas_backup:v1
    ```
    
    請謹慎使用程式碼。
    
3. **啟動並進入環境**：
    
    bash
    
    ```
    docker run -it truchas_backup:v1 /bin/bash
    ```
    
    請謹慎使用程式碼。
    
    _注意：因為 WSL 本身就是一個完整的系統，裡面可能帶有一些不必要的 init 服務，但這種方式能讓您最快在 Mac 裡面看到原本的檔案與軟體。_

#### 方案 B：使用 Lima 虛擬機還原（最接近原本 WSL 的體驗）

如果您希望像原本 WSL 一樣，擁有一個獨立的 Linux 虛擬機，而且能在裡面繼續操作 LXD，可以用 **Lima** 來載入這個根檔案系統：

1. **安裝 Lima**（透過 Homebrew）：
    
    bash
    
    ```
    brew install lima
    ```
    
    請謹慎使用程式碼。
    
2. **解壓並轉換**：您可以利用 Lima 的規格檔案（YAML），將這個 `.tar` 檔指定為虛擬機的磁碟映像來源，Lima 就會直接把這個備份還原成 Mac 上的 Linux 虛擬機環境。
---
# 🔗 參考資料
