---
type: 📝 Research
created: 2026-05-14 01:39
modified: 2026-06-12 19:02
tags:
  - "#Truchas"
  - Truchas/VFIFE
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

- 被使用於 [SOLID_module_F90](SOLID_module_F90.md)
---
# 👨‍💻 以後

<mark style="background:#fff88f">記得改名</mark>
<mark style="background:#fff88f">之所以命名為 `rnode`，是因為它是記錄「**R**elation of **Node**s」（節點關聯）的地圖</mark>

---
## 📝 內容紀錄
```fortran
MODULE Datasave_module
real*8,save,dimension(2000000)			::ar
real*8,save						::maxq
integer,save						::nnd,nel,nummat,numout,ifbody,iacc,ndof,iforce2,iforce3,iforce4
integer,save						::iprob,isee,iplane,iprobA
real*8,save						::delta,alpha,toler,gravity,thick
real*8,save,dimension(6,10000)			::sigma3D
end MODULE Datasave_module
```



- 陣列 ar 預先開啟了大量的儲存空間，後續多組變數須依次從 ar 陣列中劃分領地，導致計算速度變慢，且程式可讀性大幅降低。

- 重新撰寫相關變數，並更改後續的分地盤步驟。

	1. 核心記憶體管理變數
	
	- **<font color="#ffff00">ar(2000000)</font>** **(Storage Pool)**：這是舊版最核心的「資料池」。在 `subroutine dynamic` 中，程式會根據 `nnd` (節點數) 與 `nel` (單元數) 計算出數十個偏移量（如 `nxct`、`npint`），並將所有幾何座標、力向量、位移等數據全部塞進這個陣列的不同區段。
	- **<font color="#ffff00">maxq</font>** **(Pool Size)**：定義 `ar` 陣列的總長度（預設 2,000,000），用於在 `dynamic` 中檢查模型規模是否超過預設負擔。
	
	2. 模型規模與基礎參數 (來自 CARD 2)
	
	- **<font color="#ffff00">nnd</font>** **(NumNodes)**：總節點數，決定了座標（`xc`）、位移（`d`）、受力（`force`）等陣列的大小。
	- **<font color="#ffff00">nel</font>** **(NumElements)**：總單元數（四面體），決定了拓撲連結陣列（`rnode`）與單元內力（`feli`）的大小。
	- **<font color="#ffff00">nummat</font>** **(NumMaterials)**：材料種類總數，決定材料參數陣列（`nem`）的大小。
	- **<font color="#ffff00">ndof</font>** **(DOF)**：節點自由度，固定為 3 (X, Y, Z)，用於計算總方程式數 `meq = nnd * ndof`。
	
	- **決定變數**：`meq` (Total Equations)，計算公式為 `nnd * 3`。,
	- **對應陣列**：
	    - **<font color="#ffff00">xc, yc, zc</font>** **/** **<font color="#ffff00">xct, yct, zct</font>**：中心初始與當前座標，每個座標分量長度為 `nnd`。,
	    - **<font color="#ffff00">force</font>** **(外力)**：包含流體壓力與重力，大小為 `meq` (nnd×3)。,
	    - **<font color="#ffff00">pint</font>** **(內力)**：結構變形產生的抗力，大小為 `meq` (nnd×3)。,
	    - **<font color="#ffff00">vt</font>** **(速度) /** **<font color="#ffff00">at</font>** **(加速度)**：運動學向量，大小均為 `meq` (nnd×3)。,
	    - **<font color="#ffff00">xmass</font>** **(節點質量)**：用於動力積分，大小為 `meq` (nnd×3)。
	
	3. 時間積分控制參數 (來自 CARD 2)
	
	- **<font color="#ffff00">delta</font>** **(TimeStep)**：結構動力的時間步長 Δt，在 `esolv` 中用於顯式中心差分積分。
	- **<font color="#ffff00">alpha</font>** **(Damping)**：質量阻尼係數，用於計算積分係數 `a1, a2` 以穩定結構震盪。
	- **<font color="#ffff00">toler</font>** **(Tolerance)**：位移收斂容許值，當單步最大位移增量小於此值時，程式判定達到平衡並結束當前時步。
	
	4. 外部負載與歷史控制 (來自 CARD 3)
	
	- **<font color="#ffff00">ifbody</font>** **(Gravity Flag)**：控制是否計算重力負載。
	- **<font color="#ffff00">iacc</font>** **(Accel Flag)**：控制是否計算地面加速度（地震力）。
	- **<font color="#ffff00">iforce 2, 3, 4</font>** **(Load Flags)**：分別控制「任意形狀力」、「正弦力」與「攪動環向力」的計算開關。
	
	5. 輸出與物理模型控制 (來自 CARD 4)
	
	- **<font color="#ffff00">numout</font>** **(NumOutputRequests)**：讀取的輸出請求點數量，決定 `rkout` 陣列大小。
	- **<font color="#ffff00">iprob</font>** **/** **iprobA** **(Output Interval)**：控制在 DMP 與 OUT 檔案中輸出結果的步數頻率。
	- **<font color="#ffff00">isee</font>** **(Monitor Index)**：控制是否在螢幕（Monitor）上顯示計算進度。
	- **<font color="#ffff00">iplane</font>** **(Stress/Strain Mode)**：平面應力或平面應變模式切換。
	- **<font color="#ffff00">thick</font>** **(Thickness)**：分析對象的物理厚度。
	
	6. 特殊物理場
	
	- **<font color="#ffff00">sigma 3D</font>(6, 10000)** **(Static Stress Array)**：儲存每個單元的 6 個應力分量。**1~3 欄**：正向應力（Normal Stresses），分別對應 $σ _{xx}$ ​, $σ_{yy}$ ​, $σ_{zz}$ ​。**4~6 欄**：剪應力（Shear Stresses），分別對應  $σ _{xy}$ ​, $σ_{xz}$ ​, $σ_{yz}$ ​。這是舊版中少數沒有進入 `ar` 陣列的變數，其靜態宣告限制了模型單元數不能超過 10,000。
	- **<font color="#ffff00">gravity</font>** **(Gravity Acceleration)**：目前的重力加速度值，由 `fextl` 根據歷史曲線插值計算得出。



---
## 🔗 參考資料
-