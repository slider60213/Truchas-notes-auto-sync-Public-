---
type: 📝 Research
created: 2026-07-30 03:24
modified: 2026-07-30 03:35
tags:
  - "#Truchas"
  - Truchas/VFIFE
  - 電腦/WINDOWS/WSL
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

- 充滿格式凌亂的數字，比摩斯密碼還難懂。
- 可讀性過低：即使用 AI 查出了各個參數意義，下次看還是要重找。
- 大量花式參數：為了以讀取參數的方式來實現很多自訂功能，導致冷門參數大量增加。
- 寫死參數讀取：不能任意添加行間註解、增減參數困難。

---
# 👨‍💻 以後

- 改為與 inp 檔相似的讀取方式。
- 只保留常用跟必要的參數。
- 可以任意添加註解。
- 未來增減參數更為簡單。

---
# 📝 內容紀錄

```fortran
! --- 第 1 區塊 (CARD 1): 專案標題 ---
! 對應原始程式：head
&CARD 1
Project_Title: V5 Core Unit Benchmark Test - Single Tetrahedron Pure Tension
Deformable_Body: 0
Check_V5_Loading: 1
/
------------------------------------------------------------------------------------

! --- 第 2 區塊 (CARD 2): 全域物理與時間控制 ---
! 對應原始參數：minstp, maxstp, delta, alpha, toler
&CARD 2
Start_Step: 1
Max_Step: 10
Time_Step_Delta (s): 5.0e-1
Damping_Alpha: 0.0
Convergence_Toler: -1.0e-6
/
------------------------------------------------------------------------------------

! --- 第 3 區塊 (CARD 3): 模擬功能開關 ---

------------------------------------------------------------------------------------

! --- 第 4 區塊 (CARD 4): 輸出與幾何控制 ---

------------------------------------------------------------------------------------

! ==========================================================
! 幾何定義章節
! ==========================================================

! --- 第 6 區塊 (CARD 6): 節點數據 ---
! 格式：編號  X軸 (m)  Y軸 (m)  Z軸 (m)  固定_X  固定_Y  固定_Z (0 為固定, 1 為自由)
&CARD 6
1   0.0   0.0   0.0   1   1   1
2   0.2   0.0   0.0   1   1   1
3   0.0   0.2   0.0   1   1   1
4   0.0   0.0  -0.2   1   1   1
5   0.0   0.0   0.2   1   1   1
/

&CARD-- 6
1   0.0   0.0   0.0   0   0   0
2   0.2   0.0   0.0   0   0   0
3   0.0   0.2   0.0   0   0   0
4   0.0   0.0  -0.2   0   0   0
5   0.0   0.0   0.2   0   0   0
/
------------------------------------------------------------------------------------

! --- 第 7 區塊 (CARD 7): 單元連接數據 ---
! 格式：單元編號  節點_1  節點_2  節點_3  節點_4  材料編號
&CARD 7
1   1   2   3   5   1   10  1   1   1
2   1   3   2   4   1   10  1   1   1
/
------------------------------------------------------------------------------------

! ==========================================================
! 材料性質章節 (可重複多次)
! ==========================================================

! --- 第 8 區塊: 材料性質定義 (自動掃描 Material_Group 數量) ---
&CARD 8

Material_Group: 1
Physical_Type (mtyp1): 1
Model_Type (mtyp2): 1
Density (rho): 100.0
Youngs_Modulus (e) (Pa): 0.0
Poisson_Ratio (v): 0.3
Relaxation_Time (tau): 0.0
Tensile_Strength (s_tens) (Pa): 1.0e10
Fracture_Stress (s_frac) (Pa): 1.0e9
Tangent_Modulus (Et): 0.0
Hardening_Beta (beta): 0.0

Material_Group: 2
Physical_Type (mtyp1): 1
Model_Type (mtyp2): 1
Density (rho): 3690.211
Youngs_Modulus (e) (Pa): 1.0e8
Poisson_Ratio (v): 0.35
Relaxation_Time (tau): 0.0
Tensile_Strength (s_tens) (Pa): 10.0
Fracture_Stress (s_frac) (Pa): 10.0
Tangent_Modulus (Et): 0.0
Hardening_Beta (beta): 0.0

Material_Group: 3
Physical_Type (mtyp1): 1
Model_Type (mtyp2): 2
Density (rho): 1800.0
Youngs_Modulus (e) (Pa): 1.0e7
Poisson_Ratio (v): 0.3
Relaxation_Time (tau): 0.0
Internal_Friction_Angle (Phi): 30.0
Cohesion (c) (Pa): 5.0
Tangent_Modulus (Et): 0.0
Hardening_Beta (beta): 0.0

/
```
---
# 🔗 參考資料

GEMINI
NBLM
致榮論文
舊版 VFIFE 程式碼

---