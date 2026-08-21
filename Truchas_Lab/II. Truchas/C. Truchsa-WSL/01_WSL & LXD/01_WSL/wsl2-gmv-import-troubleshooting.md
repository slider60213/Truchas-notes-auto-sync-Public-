#  WSL2 GMV 匯入畫面問題排查 01

**Date**: August 15, 2026 at 02:48 AM
**Turns**: 1
**Source**: [Gemini Chat](https://gemini.google.com/app/922f00bb0fe88a4b?android-min-version=301356232&ios-min-version=322.0&is_sa=1&campaign_id=test_autosubmit&pt=9008&mt=8)

---

### Turn 1

#### 👤 使用者

我在 WSL2移植了 GMV 軟體，並且打包整個 WSL 給其他電腦使用，為什麼有些電腦匯入後可以正常開啟 GMV，有些卻只有視窗但沒有畫面

### 🤖 助理

這主要是目標電腦的顯示卡驅動、OpenGL 硬體加速或 WSLg 相容性差異所導致的繪圖渲染問題。

### 核心原因分析
GMV (General Mesh Viewer) 高度依賴 **OpenGL** 進行 3D 網格與場域的繪圖渲染。當您打包 WSL2 匯入到不同電腦時，系統環境從「軟體層（Linux）」跨到了「硬體與宿主環境（Windows + 顯卡）」，常見導致「有視窗卻白屏/黑屏/無畫面」的原因有：

1. **宿主電腦缺少 WSL Virtual GPU (vGPU) 驅動**
  - WSL2 預設會透過 Mesa3D 將 OpenGL 指令轉譯給 Windows 的 GPU (DirectX 12)。若目標電腦的 Windows 顯示卡驅動太舊，或沒有安裝支援 WSL2 vGPU 的驅動程式，OpenGL 畫面就無法正常傳遞。
2. **硬體加速渲染失敗（Direct3D 12 映射問題）**
  - 部分整合顯示卡（例如舊款 Intel iGPU）或雙顯示卡筆電（Intel/AMD + NVIDIA）在 WSLg 的 GPU Passthrough 下，會發生繪圖 context 建立成功但無法繪製 buffer 的情況。
3. **WSLg 與傳統 X-Server (VcXsrv/XMing) 設定衝突**
  - 若無畫面的電腦使用的是較舊的 Windows 10（無原生 WSLg），或是環境變數 `$DISPLAY` 被指向了外部 X-Server，可能會因為 Direct Rendering (GLX) 被停用而無法顯示畫面。

### 建議排查步驟
您可以請發生問題的電腦執行以下測試，以確定是 GPU 驅動還是 OpenGL 渲染的問題：

### 1. 測試 OpenGL 畫面是否能正常運作
在 WSL2 中執行：

```bash
glxgears

```

- **若連齒輪畫面都沒有或同樣空白**：代表問題出在宿主電腦的 OpenGL / GPU 加速。
- **若齒輪可以正常轉動**：代表是 GMV 專屬的 OpenGL Context 或 X11 視覺元件問題。

### 2. 強制改用軟體渲染測試
在該台電腦的 WSL2 中執行：

```bash
LIBGL_ALWAYS_SOFTWARE=1 gmv

```

- 如果加上 `LIBGL_ALWAYS_SOFTWARE=1` 後 **GMV 畫面就正常顯示了**，那就可以 100% 確定是該台電腦的顯示卡驅動或 WSL GPU 支援度問題。
您可以先讓有問題的電腦嘗試上述測試，確認結果後我們再針對對應的原因調整環境設定或打包腳本！

---

*Exported from [Voyager](https://github.com/Nagi-ovo/voyager) *  
*Generated on August 15, 2026 at 02:48 AM




# WSL2 GMV 匯入畫面問題排查02

**Date**: August 21, 2026 at 02:48 PM
**Turns**: 6
**Source**: [Gemini Chat](https://gemini.google.com/app/922f00bb0fe88a4b?android-min-version=301356232&ios-min-version=322.0&is_sa=1&campaign_id=test_autosubmit&pt=9008&mt=8)

---

## Turn 1

### 👤 使用者

你可以再告訴我一次WSL開啟不了GMV跟PYVISTA的圖形視窗是為什麼嗎

### 🤖 助理

先針對您的問題一句話回答答案：
**主要原因是 WSL2 與宿主 Windows 之間的 GPU 硬體加速轉譯機制（WSLg vGPU）失效，或缺至少量的 OpenGL 動態連結庫，導致 3D 繪圖軟體無法成功建立視窗 Context。**

### 詳細原因解析與排查
GMV 與 PyVista 都極度依賴 **OpenGL** 進行 3D 網格與幾何場域的繪圖渲染。當它們在 WSL2 內部執行時，預設會透過 Mesa3D 將 OpenGL 指令轉譯給 Windows 的 GPU (DirectX 12)。
當視窗完全開啟失敗或報錯時，通常源自以下三個核心問題：

1. **宿主電腦缺乏 WSL vGPU 驅動支援**
  - 目標 Windows 電腦的顯示卡驅動程式過舊，或者沒有安裝廠商（NVIDIA / AMD / Intel）針對 WSL2 提供包含 vGPU 支援的專用驅動程式，導致 WSL2 無法取得 GPU 算力。
2. **OpenGL 雙顯示卡切換或 D3D12 轉譯失敗**
  - 部分雙顯示卡筆電（Intel/AMD 內顯 + NVIDIA 獨顯）在 WSLg 的 GPU Passthrough 下，會因為預設選擇了錯誤的顯示晶片，導致 OpenGL context 建立失敗。
3. **PyVista 的 Off-Screen (無頭模式) 或 LibGL 缺少**
  - PyVista 常常因為環境內缺乏 `libgl1-mesa-glx` 或 `libglib2.0-0` 等底層 OpenGL 庫而崩潰；若在伺服器/容器環境下執行，若未啟用 Virtual Framebuffer (如 `xvfb`) 或設定 `off_screen=True`，視窗便無法彈出。

### 快速驗證與排查命令
您可以透過以下兩個步驟，快速判定是「顯示卡驅動/硬體加速」問題還是「軟體套件缺失」問題：

#### 步驟一：測試 OpenGL 硬體加速狀態
在 WSL2 終端機執行：

```bash
glxinfo | grep -i "OpenGL renderer"

```

- **若顯示 D3D12 或您的顯卡名稱**：代表 GPU 硬體加速正常運作。
- **若顯示 llvmpipe 或 Error**：代表系統正處於純軟體渲染或繪圖驅動失效狀態。

#### 步驟二：強制切換為軟體渲染測試
在 WSL2 執行以下指令，觀察 GMV 或 PyVista 是否能打開：

- **GMV 測試：**
  ```bash
  LIBGL_ALWAYS_SOFTWARE=1 gmv
  
  ```
- **PyVista 測試 (Python)：**
  ```python
  import pyvista as pv
  pv.start_xvfb() # 若在無 GUI 容器環境
  sphere = pv.Sphere()
  sphere.plot(off_screen=False)
  
  ```
判斷結論：如果加上 LIBGL_ALWAYS_SOFTWARE=1 後視窗就能成功開啟，代表百分之百是該台電腦的 Windows 顯示卡驅動太舊 或 WSLg vGPU 相容性 的問題。

## Turn 2

### 👤 使用者

user_student@gram16W:~/student-116/116_test02/problems/tests$ glxinfo | grep -i "OpenGL renderer"
Command 'glxinfo' not found, but can be installed with:
sudo apt install mesa-utils

### 🤖 助理

先針對您的問題一句話回答答案：
**這是因為系統內尚未安裝 mesa-utils 套件，導致缺少 glxinfo 這個 OpenGL 診斷工具。**

### 原因說明與解決方式
`glxinfo` 並不是 Ubuntu / Debian 預設內建的命令，而是包含在 `mesa-utils` 顯示工具包中。
只要安裝該套件，即可成功執行該命令來查詢 OpenGL 渲染器資訊：

```bash
sudo apt update && sudo apt install -y mesa-utils

```
安裝完成後再次執行：

```bash
glxinfo | grep -i "OpenGL renderer"

```

### 開啟 GMV / PyVista 圖形視窗的補充建議
若您在執行 PyVista 或 GMV 時出現缺少底層繪圖庫的報錯，建議可順手補充安裝以下 OpenGL 與 X11 基礎依賴套件：

```bash
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libgomp1 libxrender1

```

## Turn 3

### 👤 使用者

安裝完 sudo apt update && sudo apt install -y mesa-utils 確實就可以了 不過為什麼我都是解包同樣的WSL打包檔案,有些可以出現視窗有些卻不行，反而還要安裝 sudo apt update && sudo apt install -y mesa-utils？

### 🤖 助理

先針對您的問題一句話回答答案：
**因為 mesa-utils 只是用來提供測試指令的工具包，視窗能不能開啟的核心差異在於宿主 Windows 電腦的硬體驅動與 WSLg 狀態，而非該套件本身。**

### 詳細原因解析
安裝 `mesa-utils` 只會帶來 `glxinfo` 和 `glxgears` 這類診斷工具，它本身**並不會補齊或修復**渲染相關的系統核心驅動。
您會感覺「有些電腦可以開啟視窗、有些卻不行」，主要源自以下三個硬體與宿主環境的差異：

1. **宿主 Windows 顯示卡驅動支援度不同**
  - **可開啟的電腦**：Windows 已經安裝了支援 WSL2 vGPU (Direct3D 12 轉譯) 的最新顯卡驅動。WSL2 自動接軌宿主 GPU，因此即使沒裝額外套件，GMV / PyVista 也能直接硬體加速並跳出視窗。
  - **無法開啟的電腦**：Windows 顯卡驅動過舊、或使用微軟預設基本顯示驅動（如剛重灌好的電腦），導致 WSLg 無法調用 GPU，OpenGL 視窗建立直接失敗。
2. **雙顯示卡筆電的預設渲染晶片衝突**
  - 在具備「內顯 + 獨顯」的筆電上，WSLg 有時會預設綁定到 Intel/AMD 內顯，若內顯對 D3D12 的 OpenGL 轉譯支援不佳，就會出現視窗開不出來或白屏卡住的情況。
3. **系統更新與 WSL 版本差異**
  - 不同電腦上的 Windows 10/11 版本不同，WSLg（GUI 視窗支援元件）的版本或啟動狀態也可能不同。有些電腦的 WSL2 升級到了最新版，有些則還停留在舊版無 GUI 支援的環境。

### 總結與解決方案
`mesa-utils` 只是幫助您「印出診斷資訊（`glxinfo`）」或「測試齒輪畫面（`glxgears`）」的工具。
在**無法開啟視窗**的那些電腦上，真正的解決方法是：

1. **更新該台 Windows 的顯示卡驅動**（至 NVIDIA / AMD / Intel 官網下載最新驅動）。
2. 在 Windows 終端機執行 `wsl --update`，將 WSL 及 WSLg 組件更新至最新版本。

## Turn 4

### 👤 使用者

所以我應該幫我要打包的環境都裝好 sudo apt update && sudo apt install -y mesa-utils 再匯出嗎？這樣才會每個人匯入之後都能正常使用？

### 🤖 助理

先針對您的問題一句話回答答案：
**可以預先安裝，但這只能確保每台電腦都有診斷工具，並不能保證每個人匯入後都能正常開啟視窗。**

### 詳細原因與建議
`mesa-utils` 提供的主要是 `glxinfo`（查看渲染器）與 `glxgears`（測試齒輪動畫）這類**測試診斷工具**，它並不是渲染視窗所必需的底層繪圖驅動。
若希望打包的環境匯入到任何電腦都能最大程度順利開啟視窗，建議在打包前的原始 WSL2 中補齊以下兩類設定：

#### 1. 預先安裝基礎 OpenGL / X11 繪圖依賴庫
雖然 `mesa-utils` 包含了一部分 Mesa 底層庫，但 GMV 或 PyVista 等 GUI 軟體通常還需要其他標準繪圖套件。建議在打包前執行：

```bash
sudo apt update && sudo apt install -y \
    mesa-utils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    libxrender1 \
    x11-apps

```

#### 2. 提供「自動降級為軟體渲染」的備用機制（最關鍵）
如前所述，有些電腦開啟失敗是因為**宿主 Windows 的顯示卡驅動太舊或 WSLg GPU 加速失效**。
為了讓硬體不支援的電腦也能順利開出視窗，可以在 `.bashrc` 中新增一個自動備用（Fallback）或方便開關的別名：

```bash
# 在 .bashrc 中加入：當 GPU 渲染失敗時，可直接用軟體渲染開啟 GMV
alias gmv_sw='LIBGL_ALWAYS_SOFTWARE=1 $HOME/Shane_Command/gmv'

```

### 總結給使用者的標準操作 SOP
打包好環境發給其他同學/同事後，若有人遇到「有視窗無畫面」或「開不起來」的情況，請提供以下排查指引：

1. **請對方升級 Windows 顯示卡驅動**（更新至 NVIDIA/AMD/Intel 最新版）並在 Windows 執行 `wsl --update`。
2. **測試齒輪**：執行 `glxgears`，確認該台電腦的 WSLg 能否繪製視窗。
3. **軟體渲染備用方案**：若對方的 GPU 驅動無法修復，請對方直接改用軟體渲染指令（如 `LIBGL_ALWAYS_SOFTWARE=1 gmv` 或 `gmv_sw`）來開啟視窗。

## Turn 5

### 👤 使用者

執行這段會增加多少容量？
sudo apt update && sudo apt install -y \
mesa-utils \
libgl1-mesa-glx \
libglib2.0-0 \
libgomp1 \
libxrender1 \
x11-apps

### 🤖 助理

先針對您的問題一句話回答答案：
**大約只會增加 30 MB 至 80 MB 左右的磁碟容量。**

### 容量拆解說明
這些套件基本上都是輕量級的底層動態連結庫（C/C++ 函式庫）與基礎 X11 測試小工具，本身體積非常小：

- **mesa-utils & x11-apps**：包含 `glxinfo`、`glxgears`、`xclock` 等基礎小工具，解開後約 **10~20 MB**。
- **libgl1-mesa-glx、libglib2.0-0、libgomp1、libxrender1**：大部分 Linux 發行版預設已經內建其中的一部分；若需補齊，下載與解壓後的總容量通常在 **20~50 MB** 以內。
- **APT 快取（.deb 暫存檔）**：`sudo apt update` 下載的軟體源清單與安裝包快取，約佔 **10~30 MB**。

### 打包前淨化環境建議
如果您是在建立 **WSL2 基礎環境映像檔（要打包 .tar 發給其他同學）**，安裝完這些套件後，建議執行以下指令清除 APT 快取，可以順便省下約 20~50 MB 的體積：

```bash
sudo apt clean && sudo rm -rf /var/lib/apt/lists/*

```
這樣打包出來的環境既補齊了 OpenGL/X11 繪圖依賴，又不會佔用多餘的暫存空間。

## Turn 6

### 👤 使用者

user_student@DESKTOP-KCIIFGN:~$ sudo apt install -y libgl1-mesa-glx libglib2.0-0 libgomp1 libxrender1
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Note, selecting 'libglib2.0-0t64' instead of 'libglib2.0-0'
Package libgl1-mesa-glx is not available, but is referred to by another package.
This may mean that the package is missing, has been obsoleted, or
is only available from another source
E: Package 'libgl1-mesa-glx' has no installation candidate
user_student@DESKTOP-KCIIFGN:~$

### 🤖 助理

先針對您的問題一句話回答答案：
**這是因為在較新的 Ubuntu 版本（如 24.04 LTS）中，舊的 libgl1-mesa-glx 套件已經被廢棄（Obsoleted），被拆分改名為 libgl1 與 libglx-mesa0。**

### 詳細原因說明

- **Package 'libgl1-mesa-glx' has no installation candidate**：Ubuntu 在過往的版本重構了 OpenGL 套件結構，舊名稱已不提供安裝，系統目前標準的 OpenGL 庫套件為 **libgl1** 與 **libglx-mesa0**。
- **selecting 'libglib2.0-0t64' instead of 'libglib2.0-0'**：這是 Ubuntu 24.04 (Noble Numbat) 針對 64 位元 64-bit time_t 架構轉型採用的新套件命名，系統會自動幫您轉換，不影響使用。

### 替換安裝指令
請改用以下適應新版 Ubuntu 的完整指令進行安裝：

```bash
sudo apt update && sudo apt install -y \
    mesa-utils \
    libgl1 \
    libglx-mesa0 \
    libglib2.0-0 \
    libgomp1 \
    libxrender1 \
    x11-apps

```
安裝完畢後，建議同樣執行以下清除暫存指令以維持打包體積最小化：

```bash
sudo apt clean && sudo rm -rf /var/lib/apt/lists/*

```

---

*Exported from [Voyager](https://github.com/Nagi-ovo/voyager)*  
*Generated on August 21, 2026 at 02:48 PM*