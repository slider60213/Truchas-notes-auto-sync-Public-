---
topic:
project: Truchas-Lab
status: 🟢 Active
type: 📝 Research
created: 2026-05-11 20:09
modified: 2026-08-21 15:56
tags:
  - "#Truchas"
---



## 📌 核心問題：為什麼是 LXD？

### 💡 Why LXD over Docker?

Legacy scientific software like Truchas requires an integrated toolchain (Gmsh for meshing, GMV for visualization). **LXD (System Containers)** was chosen over Docker for four engineering reasons:

* **Monolithic Toolchain Support**: Unlike Docker's single-process design, LXD provides a full `systemd` environment, allowing multiple heavy simulation packages to co-exist and interact natively without bloating a Dockerfile.
* **Seamless GPU/X11 Pipeline**: LXD's system-level hardware mapping allows Truchas, Gmsh, and GMV to share a single configured graphical pipeline back to WSL2 automatically, eliminating Docker's complex runtime flags for X11.
* **Stateful Research Environment**: Scientific workflows are highly dynamic. LXD is stateful by design, meaning students can modify `.bashrc` and save simulation states permanently without dealing with Docker’s volume permission traps (root ownership issues).
* **Linux Mastery for Students**: LXD acts exactly like a regular Ubuntu server. It serves as a persistent playground for students to practice sysadmin tasks and customize their engineering workstations.
* **Identical Kernel Limits (No Double Testing)**: Both Docker and LXD share the same WSL2 Linux kernel. If a legacy dependency crashes due to modern kernel system calls, it fails identically in both. Since the core compatibility limits were already verified and patched via compiler re-configuration in LXD, testing in Docker is redundant.


### 💡 為什麼選擇 LXD 而不是 Docker？

科學模擬（Truchas）需要一整套完整的工具鏈（包含前處理 Gmsh、後處理 GMV）。我們選擇 LXD（系統容器）而非 Docker 的核心原因如下：

* **完整的科學運算環境**：LXD 提供具備 `systemd` 的完整作業系統，允許 Truchas、Gmsh、GMV 多個重型軟體原生共存、互相呼叫，避免 Docker 容易遇到的相依性地獄。
* **完美的圖形畫面（X11）共享**：LXD 擁有成熟的系統級硬體映射。只要設定一次 GPU 通道，裡面所有圖形化軟體都能直接把模擬畫面傳回 WSL，不需要為每個工具單獨修改複雜的 Docker 啟動指令。
* **檔案永久保存，無權限問題**：LXD 具備持久性（Stateful）。學生今天微調的 `.bashrc`、編譯到一半的檔案都會永久保存。這避開了 Docker 自動化掛載時，極易產生的「路徑限制」與「檔案變成 root 權限地獄」。
* **擬真的 Linux 練習場**：LXD 的操作體驗跟真正的獨立伺服器一模一樣，能讓學生在做研究的同時，真正累積個人化的環境設定，並學會如何當一個 Linux Power User。
* **核心共用，免去 Docker 無謂測試**：Docker 與 LXD 都共用 WSL2 的 Linux 核心。當舊套件與現代核心發生底層相容性衝突時，兩者表現完全一致。本專案已在 LXD 中摸清核心邊界並修正編譯器，因此完全不需浪費時間去 Docker 重複測試。



---

## 📝 內容紀錄

### 1.  LXD 跟 Docker 差異？
![](pics/Pasted%20image%2020260511201551.png)

這是一個非常經典的問題。雖然兩者都使用 Linux 核心技術（如 Namespaces 和 Cgroups），但它們的**設計哲學**與**使用目的**完全不同。

簡單來說：**Docker 是為了跑「程式」，LXD 是為了跑「作業系統」。**

1. 本質上的差別：應用程式 vs. 系統

- **Docker (應用程式容器 - Application Containers)**：
    - **目標**：把一個特定的應用程式（例如：一個網站程式、一個資料庫）及其所需的環境打包。
    - **邏輯**：通常一個容器只跑**一個進程 (Process)**。如果你關掉那個程式，容器就會自動結束。
    - **特點**：它不包含完整的作業系統，只包含跑那個程式必要的檔案。它非常強調「拋棄式」，壞了就重開一個。
- **LXD (系統容器 - System Containers)**：
    - **目標**：提供一個跟「虛擬機 (VM)」用起來一模一樣，但更輕量的**完整作業系統環境**。
    - **邏輯**：它會跑整套系統服務（如 systemd、ssh、syslog）。你可以在裡面開帳號、裝各種軟體，它會像一台獨立的電腦一樣一直跑著。
    - **特點**：它適合拿來當作「輕量級的開發主機」，你可以隨意進入裡面進行各種操作，且它的狀態是可以長久保存的。

---

2. 為什麼有了 Docker 還需要 LXD？（使用場景）

雖然 Docker 很紅，但在以下情境，LXD 是更好的選擇：

- **需要「多個應用程式」協作時**：  
    在 Docker 裡，你通常要寫 `docker-compose` 把網頁、資料庫、快取分成三個容器。但在 LXD 裡，你可以直接把它們全部裝在同一個容器內，就像在一台實體伺服器上操作一樣簡單。
- **需要執行「非雲端原生」的舊程式**：  
    有些舊軟體啟動時需要依賴很多系統服務，Docker 很難跑起來，但 LXD 就像一台電腦，裝上去就能跑。
- **作實驗、搞壞系統也不怕**：  
    如果你想練習 Linux 指令（例如改網路設定、安裝核心模組），在 Docker 裡很難操作（因為它被閹割了很多功能），但在 LXD 裡你可以像管理實體機一樣隨便玩，玩壞了就秒速重置。
- **在裡面跑 Docker (Docker in LXD)**：  
    這是高手常用的招數。因為 LXD 提供了一個完整的系統環境，你可以在 LXD 裡面安裝 Docker。這樣你的主機環境會非常乾淨，所有的 Docker 鏡像跟設定都鎖在 LXD 容器裡。

總結比喻

- **Docker** 像是一個**「外送餐盒」**：打開來就是一份炒飯（程式），吃完餐盒就丟了。
- **LXD** 像是一個**「行動小套房」**：裡面有床、廁所、廚房（完整系統）。你可以在裡面煮飯、睡覺、生活，它是一個完整的空間。

你可以想像成：如果你只想跑一個 Python 網站，用 **Docker**；如果你想要一台練習 Linux 操作的實驗電腦，用 **LXD**。

### 2. 為什麼用.venv

在科學運算和模擬的領域中（例如你的 Truchas 專案），這是一種非常經典且高明的**組合拳搭配（Hybrid Architecture）**：

- **LXD（大盒子）**：負責承載**系統級的重型依賴**（如舊版 GCC 編譯器、Mesa 3D 繪圖庫、Gmsh 底層套件）。
- **venv（小盒子）**：在 LXD 內部負責**精準切換不同的 Python 版本與套件**（如有些模擬腳本要 Python 2.7，有些自動化分析要 Python 3.7）。

以下為你詳細拆解為什麼在 LXD 裡面搭配 `venv` 是一個完美的科研環境架構：

---

🎨 用你的脈絡來還原這個「組合拳」場景

假設你在 LXD 容器（Ubuntu）裡面做研究，遇到了這個嚴苛的相容性問題：

1. **Truchas 核心**：需要舊版的 Linux 繪圖庫，你已經在 LXD 系統裡裝好了。
2. **網格分析腳本 A**：是 10 年前的老學長寫的，必須在 **Python 2.7** 下跑 `numpy==1.10`。
3. **數據視覺化腳本 B**：是現代開源社群寫的，必須在 **Python 3.7** 下跑 `matplotlib==3.x`。

❌ 錯誤的做法（不用 venv，直接污染 LXD 系統）：

如果你不用 `venv`，直接在 LXD 系統裡用 `pip install` 盲目安裝，新版的套件會直接覆蓋掉舊版的套件，導致「執行腳本 B 時，腳本 A 就崩潰；修好腳本 A 時，腳本 B 又動不了」。這就是典型的 **Python 套件地獄**。

⭕ 正確的做法（LXD 內建 venv 臨時開關）：

你在這個 LXD 系統裡面同時保留 Python 2.7 與 Python 3.7（Linux 系統允許安裝多個 Python 版本，彼此不衝突）。

- **當你需要跑老學長的網格分析（開啟開源開關 A）**：
- **當你需要跑現代的數據視覺化（開啟開源開關 B）**：

### 3. 要怎麼退出.venv

退出 `.venv` 虛擬環境非常簡單，不論你使用的是 Windows、macOS 還是 Linux，指令都是同一個：
```
deactivate
```

因為太難記了，我把登入跟退出的指令改成
```
登入：venv
退出：venv_exit
```
![](pics/Pasted%20image%2020260513025542.png)

---

## 🔗 參考資料
-