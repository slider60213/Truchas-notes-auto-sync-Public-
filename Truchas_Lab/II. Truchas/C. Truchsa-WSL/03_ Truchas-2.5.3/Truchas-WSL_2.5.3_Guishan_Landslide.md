---
type: 📝 Research
created: 2026-08-16 02:06
modified: 2026-08-17 00:46
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
|                          |                                                                        |                                                                           |                                                                           |                                                                  |





---
# 🔗 參考資料


---