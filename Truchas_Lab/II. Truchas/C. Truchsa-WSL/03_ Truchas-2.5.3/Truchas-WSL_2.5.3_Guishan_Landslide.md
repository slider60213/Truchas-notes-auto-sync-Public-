---
type: 📝 Research
created: 2026-08-16 02:06
modified: 2026-08-18 11:11
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

Guishan Landslide
mud density: 2000 kg/m $^3$
Viscosity: 1e-3
Output_Dt = 5.0 s
比較第25個 Output 檔案 (t=125.0 s)
160     4CPU      第25個 Output 檔案(.bin) : 14hr 6min
160   10CPU      第25個 Output 檔案(.bin) :   5hr 37min
WSL    4CPU      第25個 Output 檔案(.bin) :   5hr 48min
WSL  10CPU      第25個 Output 檔案(.bin) :   4hr 27min

[Comp_160 vs WSL_Guishan_Island](../../../../Excalidraw/Comp_160%20vs%20WSL_Guishan_Island.md)

**1. Spatial Error（空間誤差分佈圖）**

- **關鍵看點**：觀察誤差在全域空間（$X, Y$ 座標）上的分佈型態與擴散狀況。
    
- **越準的趨勢**：
    
    - **底色一致性**：整張圖呈現均一的深紫色（誤差趨近於 $0$）。
        
    - **無區域性亮點**：亮點（綠/黃色）越少越好；若有亮點，應僅呈極少數的點狀分佈，而非大規模的帶狀或區域性亮斑（後者代表整片流場傳播方向或速度算錯）。
        

**2. Scatter Correlation（水面高程相關性散佈圖）**

- **關鍵看點**：評估比較組與 Baseline 的全域水位（$\eta$）線性相關程度與整體一致性。
    
- **越準的趨勢**：
    
    - **緊貼對角線**：所有藍色資料點高度集中並**緊密重合於紅色的 $1:1$ 參考虛線**上。
        
    - ** $R^2$ 趨近於 $1.0000$ **：判定係數 $R^2$ 越接近 $1$（例如 $> 0.999$），代表整體水面的空間波形相關性越高。
        
    - **無對角線偏離**：散佈點不應出現上下不對稱的飄移（若整體偏向虛線上側或下側，代表存在系統性水位偏差 Bias）。
        

**3. Error - Gradient（誤差 vs. 水面梯度 $\vert{}\nabla \eta\vert{}$）**

- **關鍵看點**：驗證數值誤差是否成功收斂在高梯度的波浪前緣（Steep Wave Front），並確定平緩水域不受影響。
    
- **越準的趨勢**：
    
    - **綠點（平緩區）貼底**：在黑色虛線左側及內部的綠點，應**全部扁平地貼在縱軸最底部（誤差接近 $0$）**。
        
    - **紅點（陡峭區）誤差可控**：縱軸較高的誤差點應 100% 被分類為紅點；且隨著梯度增加，紅點的縱軸高度（誤差值）越低代表越精準。
        
    - **趨勢符合物理**：證明「平緩區完全精準，誤差僅由波前微小相位差引起」。
        

**4. Error - Surface VOF（誤差 vs. 抽樣水面 VOF 值）**

- **關鍵看點**：評估 Volume of Fluid (VOF) 自由液面捕捉技術在數值重構水面（等值面 $0.49$）時的數值穩定度。
    
- **越準的趨勢**：
    
    - **集中於 Target VOF 兩側**：資料點應高度緊貼紅色虛線（VOF $= 0.49$），代表等值面萃取位置精確。
        
    - **縱軸誤差低**：在 VOF $= 0.49$ 附近的資料點，其縱軸（絕對誤差）越接近 $0$ 越好。
        
    - **無低梯度大誤差**：深藍色/綠色（低梯度）的點不應出現在縱軸高處，確保只有高梯度界面（黃色點）才會產生輕微過渡誤差。

- WSL 多核心數模擬展現出與機台160媲美的成果，並且速度上略勝一籌。
- 繪圖上 DBM-Landslide 的分布位置與傳播軌跡基本一致。
- 水位數據差異是平行運算（MPI 核心數不同）搭配浮點數精度累積誤差造成的正常現象。

### **算力升級與環境移轉效益驗證 (HPC & Environment Migration Benchmark)**


本分析以過往報告之機台 160 (4 CPU) 為基準 (Baseline)，評估擴充核心至 10 CPU 以及轉移至 WSL-LXD 虛擬化環境對自由水面模擬（Truchas）之精確度與算力效益。結果顯示，轉移至 WSL-LXD (10 CPU) 可將運算時間從 **14 小時 6 分鐘大幅縮短至 4 小時 27 分鐘**（計算效率提升約 3.16 倍），且全場域平均絕對誤差 (MAE) 僅為 **0.0204 m**，整體判定係數 ($R^2$) 高達 **0.9953**。超過 **99.00%** 的空間網格點位誤差低於 0.1 m，證實環境變更與平行劃分並未造成顯著的數值耗散或非物理偏置。局部最大誤差（15.0 m）集中於乾濕邊界 $(1025, -875)$，主因為自由液面捕捉機制之邊界判定差異，不影響總體水位波形場域的一致性。


This benchmark evaluates the precision and computational efficiency of migrating Truchas free-surface wave simulations from the baseline platform (Machine 160, 4 CPUs) to an expanded 10-CPU configuration and a WSL-LXD containerized environment. Results demonstrate that the WSL-LXD (10 CPU) setup dramatically reduces execution time from **14 hr 06 min to 4 hr 27 min** (achieving a 3.16x speedup). Across the 8,000 grid points, the WSL-LXD model yields a Mean Absolute Error (MAE) of merely **0.0204 m** and a coefficient of determination ($R^2$) of **0.9953**, with **99.00%** of nodes exhibiting errors under 0.1 m. The benchmark confirms that domain decomposition and OS containerization introduce negligible numerical dissipation. The isolated peak local deviation (15.0 m at grid $(1025, -875)$) stems from subtle wetting-and-drying boundary interface reconstructions rather than global physical discrepancies.


![](pics/VOF_SPLASH_V2.png)

---
# 🔗 參考資料


---