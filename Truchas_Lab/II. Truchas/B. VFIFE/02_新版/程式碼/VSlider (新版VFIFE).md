---
topic:
project: Truchas-Lab
status: 🟢 Active
type: 📝 Research
created: 2026-07-27 23:21
modified: 2026-07-30 02:20
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



## 📌 摘要與目標

```

目前關於新版 SOLID VOF 的計算，打算調整成這樣，你覺得如何？

[步驟 1] 建立外露三角形面的 SoA 列表 
└── 遍歷所有固體單元，僅提取 face_judge == 1 的三角形面頂點座標，建立極小型的外露面快取陣列。

[步驟 2] 計算固體外露面 / 總體的 AABB 包夾盒 
└── 計算固體結構的 [Xmin, Xmax], [Ymin, Ymax], [Zmin, Zmax]。 
└── 利用二分搜尋法（Direct Indexing），將背景流體網格搜尋範圍鎖定在 [i_start, i_end], [j_start, j_end], [k_start, k_end]。

[步驟 3] 雙重平行化 (OpenMP) 掃描受影響的流體 Cell 
└── 對於鎖定區域內的每個流體 Cell (i, j, k)： 
1. 根據 x_bound(i-1..i), y_bound(j-1..j), z_bound(k-1..k) 生成 64 個子網格 sampling 點。 
2. 計算子點到近鄰固體外露面的 SDF 距離與正負號判定（In/Out Check）。 
3. 累加落在固體內部的子點數量。

[步驟 4] 正規化輸出 └── solid_vof(i,j,k) = solid_sub_points / total_sub_points (64.0)
```

## 🧪 模擬參數 (若適用)
- **Case ID**: 
- **Solver**: 
- **Mesh Size**: 

## 📝 內容紀錄

1. 材料編號：現在會自動創建材料編號 V5_mat_id，數值是 inp 檔中的材料數量再+1，因此 inp 檔材料設定不可跳號。
2. 固體參數：現在會讀取與 .inp 檔同名的 .V5 檔。 （ABC.inp  $\Rightarrow$ ABC.V5）


3. 固-流位置對照：
	透過 AABB 篩選出 V5固體所在的位置，並且轉換成流體座標的網格編號
	方便調整 VOF、速度或未來其他操作
	![](pics/Pasted%20image%2020260730020933.png)








---
## 🔗 參考資料
-