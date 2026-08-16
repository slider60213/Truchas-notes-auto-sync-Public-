---
type: 📝 Research
created: 2026-08-16 02:06
modified: 2026-08-17 04:01
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
160     4CPU      第25個 Output 檔案: 14hr 6min
160   10CPU      第25個 Output 檔案:   5hr 37min
WSL  10CPU      第25個 Output 檔案:   4hr 27min

- WSL 多核心數模擬展現出與機台160媲美的成果，並且速度上略勝一籌。
- 繪圖上 DBM-Landslide 模擬分布與軌跡基本一致。
- 數據差異主要來自 CPU 數量以及計算精度的迭代累積。
- 使用不同的CPU 數量時，水位資料數據約有 O(3) 的差異。
- WSL 與機台160所使用的CPU 數量相同時，水位資料數據約有 O(6) 的差異。
- 平行運算（MPI 核心數不同）搭配浮點數精度累積誤差造成的正常現象

|                          | 160-報告<br>(4 CPU)                                                      | 160 <br>(4 CPU)                                                           | 160<br>(10 CPU)                                                           | WSL<br>(10 CPU)                                                  |
| ------------------------ | ---------------------------------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Runtime                  | N/A                                                                    | 14hr 6min                                                                 | 5hr 37min                                                                 | 4hr 27min                                                        |
| Top<br>view              | ![\|200](pics/Guishan_d2000_1e-3_new_VOFs_TopView_MTD3_000025%201.png) | ![\|200](pics/Guishan_d2000_1e-3_new_VOFs_TopView_MTD3_000025%202.png)    | ![\|200](pics/Guishan_d2000_1e-3_new_VOFs_TopView_MTD3_000025%203.png)    | ![\|200](pics/Guishan_Landslide_VOFs_TopView_MTD3_000025.png)    |
| Side<br>view             | ![\|200](pics/Guishan_d2000_1e-3_new_VOFs_SideView_000025%201.png)     | ![\|200](pics/Guishan_d2000_1e-3_new_VOFs_SideView_000025%202.png)        | ![\|200](pics/Guishan_d2000_1e-3_new_VOFs_SideView_000025%203.png)        | ![\|200](pics/Guishan_Landslide_VOFs_SideView_000025.png)        |
| Water<br>surface         | ![\|200](pics/Guishan_d2000_1e-3_new_WaterSurface_TopView_000025.png)  | ![\|200](pics/Guishan_d2000_1e-3_new_WaterSurface_TopView_000025%201.png) | ![\|200](pics/Guishan_d2000_1e-3_new_WaterSurface_TopView_000025%202.png) | ![\|200](pics/Guishan_Landslide_WaterSurface_TopView_000025.png) |
| Water<br>surface<br>data | ![\|200](pics/Pasted%20image%2020260816233211.png)                     | ![\|200](pics/Pasted%20image%2020260816233229.png)                        | ![\|200](pics/Pasted%20image%2020260816233412.png)                        | ![\|200](pics/Pasted%20image%2020260816233545.png)               |
| Scatter<br>correlation   |                                                                        | ![\|200](pics/Scatter_Correlation_160_4_CPU.png)                          | ![\|200](pics/Scatter_Correlation_160_10_CPU.png)                         | ![\|200](pics/Scatter_Correlation_WSL_LXD_10_CPU.png)            |
| Spatial<br>error         |                                                                        | ![\|200](pics/Spatial_Error_160_4_CPU.png)                                | ![\|200](pics/Spatial_Error_160_10_CPU.png)                               | ![\|200](pics/Spatial_Error_WSL_LXD_10_CPU.png)                  |


### **算力升級與環境移轉效益驗證 (HPC & Environment Migration Benchmark)**


本分析以過往報告之機台 160 (4 CPU) 為基準 (Baseline)，評估擴充核心至 10 CPU 以及轉移至 WSL-LXD 虛擬化環境對自由水面模擬（Truchas）之精確度與算力效益。結果顯示，轉移至 WSL-LXD (10 CPU) 可將運算時間從 **14 小時 6 分鐘大幅縮短至 4 小時 27 分鐘**（計算效率提升約 3.16 倍），且全場域平均絕對誤差 (MAE) 僅為 **0.0204 m**，整體判定係數 ($R^2$) 高達 **0.9953**。超過 **99.00%** 的空間網格點位誤差低於 0.1 m，證實環境變更與平行劃分並未造成顯著的數值耗散或非物理偏置。局部最大誤差（15.0 m）集中於乾濕邊界 $(1025, -875)$，主因為自由液面捕捉機制之邊界判定差異，不影響總體水位波形場域的一致性。


This benchmark evaluates the precision and computational efficiency of migrating Truchas free-surface wave simulations from the baseline platform (Machine 160, 4 CPUs) to an expanded 10-CPU configuration and a WSL-LXD containerized environment. Results demonstrate that the WSL-LXD (10 CPU) setup dramatically reduces execution time from **14 hr 06 min to 4 hr 27 min** (achieving a 3.16x speedup). Across the 8,000 grid points, the WSL-LXD model yields a Mean Absolute Error (MAE) of merely **0.0204 m** and a coefficient of determination ($R^2$) of **0.9953**, with **99.00%** of nodes exhibiting errors under 0.1 m. The benchmark confirms that domain decomposition and OS containerization introduce negligible numerical dissipation. The isolated peak local deviation (15.0 m at grid $(1025, -875)$) stems from subtle wetting-and-drying boundary interface reconstructions rather than global physical discrepancies.


![](pics/VOF_SPLASH_V2.png)

---
# 🔗 參考資料


---