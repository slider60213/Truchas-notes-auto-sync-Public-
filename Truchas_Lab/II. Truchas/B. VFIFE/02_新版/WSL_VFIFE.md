---
type: 📝 Research
created: 2026-04-29 03:51
modified: 2026-05-14 02:56
tags:
  - Truchas
  - 電腦/WINDOWS/WSL
  - Truchas/VFIFE
  - Truchas/VFIFE/Gmsh
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


## 🔍 動機

### **舊版 VFIFE 內容：**
- [Data_save_module_F90](../01_舊版/程式碼/Data_save_module_F90.md)
- [SOLID_module_F90](../01_舊版/程式碼/SOLID_module_F90.md)
- [moving_rigid_module_F90](../01_舊版/程式碼/moving_rigid_module_F90.md)

 ### **問題：**
- 語法過舊：不易識讀，且 gfortran 無法編譯。
- 計算緩慢：受限時代技術，充斥大量低效陣列與迴圈，無法平行處理。
- 使用性低：目前除了實驗室機台外沒辦法在任何地方執行。
<font color="#ff0000"><center>與其硬啃沿用過往寫法，不如解析程式碼過程再重寫，包括變數名稱與宣告。</center> </font><font color="#ff0000"><center>即使在 161 完成改版，受限於編譯器還是只適用於實驗室機台 = 沒人會用，會了也沒用</center></font>
<center><font color="#ffff00">目標：在 WSL 上以移植完成的 116 (2.0.2) 為基礎增加 VFIFE 相關功能</font></center>

---
## 📌目標：基於 116 版 Truchas （2.0.2） 完成 WSL 版本 VFIFE 

這份重構工作將原本基於 Fortran 77 風格的舊式程式碼，轉型為具備**動態記憶體管理**、**標籤驅動解析**以及**高維度語義化**的現代 Fortran 程式架構。以下是本次修改過程的貢獻總結、遇到的問題與優化對策：

### **1. LXD 容器設置**
優化 WSL 操作，可以快速複製 LXD 容器來區分不同研究環境（116, VFIFE）。
- 新增複製容器與刪除容器指令，讓各研究計劃對應到專屬容器
- 容器與模擬資料夾名稱都可自由命名後重新編譯
- 指令優化 `run_compile, run_sim, re`：自動偵測提供選單來決定編譯/模擬的容器
![594](pics/Pasted%20image%2020260504043026.png)
![595](pics/Pasted%20image%2020260504043927.png)

### **2. dat 檔讀取**
- 原版參數宣告：[Data_save_module_F90](../01_舊版/程式碼/Data_save_module_F90.md)  
- 原版參數讀取：[SOLID_module_F90](../01_舊版/程式碼/SOLID_module_F90.md)  
[Data_save_module_F90](../01_舊版/程式碼/Data_save_module_F90.md) + [SOLID_module_F90](../01_舊版/程式碼/SOLID_module_F90.md)  :LiArrowRight:  [VFIFE_FSI_module.F90](VFIFE_FSI_module.F90.md)  

| **項目**    | **原版 (F 77 風格)**            | **重構後 (現代化 Fortran)**                         |
| --------- | --------------------------- | --------------------------------------------- |
| **記憶體管理** | 預先宣告巨型陣列 `ar()`，手動切割位址      | 依照輸入檔數值動態 `ALLOCATE`                          |
| **變數結構**  | 大多為一維陣列，索引混亂（如 `i*3-2`）     | 語義化多維陣列（如 `d(node, dir)`）                     |
| **輸入檔格式** | 純數字、無註解，必須嚴格遵守行號            | 標籤驅動（Tag-driven），支援行內註解                       |
| **擴充性**   | 修改陣列大小需重新編譯整個程式             | <font color="#ffff00">自動適應算例大小，不需更動程式碼</font> |
| **維護性**   | 充斥魔術數字與 `GOTO` 跳轉 (ERR=998) | 模組化封裝，使用 `IOSTAT` 錯誤處理                        |
| **座標存取**  | `nxc`, `nyc`, `nzc` 分散存取    | 整合為 `x_coord(nnd, 3)` 統一管理                    |

- 設計了「自帶註解（Self-documented）」的 `.dat` 格式，參照 inp 檔格式，引入 `&CARD` 與 `/` 標籤索引機制，取代原本死板的行號讀取；另外，可以像 inp 檔一樣調整 `&` 與 `/` 間的變數順序。
- 實作「自動計數」功能，程式會自動統計節點與單元數量，避免漏填或誤填。
- 廢除 `ar(2000000)` 巨型陣列與手動位址計算（Pool Management），改用 `ALLOCATABLE` 動態配置。這讓模擬規模不再受限於寫死的常數，只需視硬體記憶體大小而定。
- 將硬編碼的陣列如 `sigma3D(6, 10000)` 改為動態 `(nel, 6)`，移除單元數量的硬性限制。
- 將原本隱藏在一維陣列中的變數恢復其物理維度，例如將位移、速度從一維向量改為 `(nnd, 3)` 矩陣，並遵循「Row: 動態數量 / Column: 固定分量」的原則，優化記憶體存取效率。

![](pics/Pasted%20image%2020260504034205.png)
![](pics/Pasted%20image%2020260504034740.png)


### **3. 3D 建模**
針對不同模擬案例需要配置對應的 dat 檔（<font color="#ffff00">節點座標</font>、<font color="#ffff00">四面體節點構成</font>），[可使用的軟體](../00_聊天紀錄/Gemini/Gemini_免費建模軟體比較與建議/chat_免費建模軟體比較與建議.md) 中以 [Gmsh](Gmsh.md) 最為適配，原因主要有：
- 2026/03 仍持續更新
- 兼具 Windows 版與 Linux 版
- 腳本操作適配 AI 工具
過往最大的難點在於 UI 選項龐雜操作難用，但如今透過 AI 工具可輕鬆完成建模腳本，大幅提升建模速度與精細度，UI 則作為檢視器來預覽成果，雙版本也完美適配 [WSL](../../C.%20WSL_Ubuntu/02_WSL與LXD/01_WSL/WSL.md) 的工作環境。
### **4. 物理計算**
<mark style="background:#ff4d4f">待完成 </mark>

### **5. 模擬**
<mark style="background:#ff4d4f">待完成</mark>

---
## 📝 個人紀錄

### **1. 舊編譯器相容性 (Lahey vs. gfortran)**

- **狀況**：舊編譯器不支援 `NEWUNIT` 等新語法，且對隱含型別（Implicit Typing）有不同預設。

- **優化**：定義全域 Unit 常數（如 `DAT_IO = 100`）代替寫死數字，並強制使用 `IMPLICIT NONE` 消除型別陷阱。

### **2. 輸入檔解析失敗 (EOF 或標籤找不到)**

- **狀況**：由於 Tab 鍵、Windows/Linux 換行符號（BOM）或開錯檔案（.inp vs .dat）導致程式抓不到 `&CARD`。

- **優化**：撰寫 `FIND_CARD` 子程序，結合 `ADJUSTL` 與自定義 `compressed_line` 邏輯，排除所有不可見字元（Tab/Space）的干擾。

### **3. 數值讀取精度與格式衝突**

- **狀況**：原本讀取 `Project_Title` 等字串時會夾雜冒號後的數值，或是在 `WRITE` 時格式描述符與變數數量不符。

- **優化**：改進 `GET_VALUE` 函數，使用 `BACK=.TRUE.` 從行尾往回搜尋冒號，確保精確提取數值並過濾單位字串。

### **4. 輸出檔案異常 (噴出 fort.xxxxx 檔案)**

- **狀況**：呼叫 `getlun()` 取得 Unit 後未執行 `OPEN` 即進行 `WRITE`。

- **優化**：手動補上 `OPEN` 指令，或徹底模仿物件導向的串流語法（`.OUT.`），確保輸出路徑與檔名正確。


### **5. 初始迴圈從 0 開始**
![](pics/Pasted%20image%2020260429035229.png)

### **6. 參數讀取確認**
![](pics/Pasted%20image%2020260504023133.png)



---
## 🔗 其他參考資料
-