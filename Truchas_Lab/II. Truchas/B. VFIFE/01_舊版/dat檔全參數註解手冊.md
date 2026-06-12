---
type: 📝 Research
created: 2026-05-14 01:49
modified: 2026-05-14 01:50
tags:
  - "#Truchas"
  - Truchas/VFIFE
---
2026-04-12 17:55  
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

# 註解範例：cylinder.dat

<font color="#ffff00">Cylinder Case: Floating Column in Waves</font> ! Title Card  
<font color="#ffff00">356 1276 2 1 1000 1.0e-6 1.0 -1.0e-6</font> ! nnd, nel, nummat, minstp, maxstp, delta, alpha, toler  

<font color="#ffff00">1 0 1 0 0 0</font> ! ifbody, iacc, iforce2, iforce3, iforce4, isequel  

<font color="#ffff00">1000 1000000 1 0 2 1. 0</font> ! part_skip, full_skip, numout, isee, iplane, thick, icontact  

<font color="#ffff00">1 0.2024 0.2028 0.0438 0 0 0</font> ! ID, X, Y, Z, ifixX, ifixY, ifixZ  
... (其餘節點)  

<font color="#ffff00">1 1 2 3 4 1 10 1 1 1</font> ! ID, Node1-4, mat-typ, mat-mdl, row, col, layer  
... (其餘單元)  

<font color="#ffff00">1 1 256.34 1e10 0.35 0.0</font> ! Group, Type, Density, Youngs, Poisson, Relaxation  
<font color="#ffff00">10. 10. 0. 0. </font>! Tensile, Fracture, Tangent, Hardening  
<font color="#ffff00">2 1 256.34 1e10 0.35 0.0 </font>! (若有第二種材料)  
...  

<font color="#ffff00">3</font> ! ng (Gravity pair number)  
<font color="#ffff00">0.0 9.81 0.1 9.81 50.0 9.81</font> ! Time, Gravity-Z

<font color="#ffff00">1 2</font> ! numif (Force History count), nnaf2 (Total nodes applied)  
<font color="#ffff00">11</font> ! kfpnts (Points in History #1)  
<font color="#ffff00">0.0 0.0</font> ! Time, Force-X  
<font color="#ffff00">0.1 0.0 </font> 
... (其餘歷時點) 

<font color="#ffff00">1 1 1</font> ! nodeID, direction(1:X), historyID  
<font color="#ffff00">2 1 1</font> ! nodeID, direction(1:X), historyID  
<font color="#ffff00">13 0 1</font> ! nodeID, type(0:disp), direction(1:X) - Card 25

---

# **第一部分：全域與控制區 (始終存在)**

## **CARD 1: 標題卡 (Title Card)**

<center><font color="#ffff00">a cantilever beam under pure bending</font>  </center>

- **head**：長度為 80 個字元的字串，用於定義模擬案例的名稱（如範例中的 Cylinder Case）,。

## **CARD 2: 全域控制參數 (General Control)**
  
  
<center><font color="#ffff00">356  1276 2   1	1000	1.0e-6  1.0  -1.0e-6 </font>	</center>	  

- **nnd** **(Number of Nodes) <font color="#ffff00">356</font>**：總節點數。定義固體結構中座標點的總量。
- **nel** **(Number of Elements) <font color="#ffff00">1276</font>**：總單元數。定義結構由多少個四面體（Tetrahedron）組成。
- **nummat <font color="#ffff00">2</font>**：材料群組總數。指定模擬中使用的不同材料特性種類數量。
- **minstp**  <font color="#ffff00">1</font>**/** **maxstp <font color="#ffff00">1000</font>**：固體求解器運算的起始與最大時步。`maxstp` 決定了在單個流體時步內固體迭代的最大次數。
- **delta <font color="#ffff00">1.0e-6</font>**：固體運算的時步長度 (Δt)。
- **alpha <font color="#ffff00">1.0</font>**：質量阻尼係數。用於數值穩定，壓制固體運動的震盪。
- **toler <font color="#ffff00">-1.0e-6</font>**：收斂容許誤差。判斷固體位移計算是否達成數值平衡。

## **CARD 3: 力/位移控制卡 (Force/Displacement Control)**
  
<center><font color="#ffff00">1  0  1  0  0	0</font></center>  

- **ifbody <font color="#ffff00">1</font>**：重力載重指標。1 代表考慮重力，0 代表不考慮。
	**[聯動]** 若為 1，則程式後續會讀取 **CARD 10-11**。
		 
- **iacc<font color="#ffff00"> 0</font>**：地面加速度指標。用於地震力或基底震動模擬,。
	**[聯動]** 若為 1，則程式後續會讀取 **CARD 12-14**。
		 
- **iforce2 <font color="#ffff00">1</font>**：任意形狀載重指標。決定是否啟用手動定義的時間載重曲線,。
	**[聯動]** 若為 1，則程式後續會讀取 **CARD 15-18**。
		  
- **iforce3 <font color="#ffff00">0</font>**：簡諧載重指標。用於模擬正弦或餘弦形式的週期力,。
	**[聯動]** 若為 1 或 2，則程式後續會讀取 **CARD 19-20**。
		  
- **iforce4 <font color="#ffff00">0</font>**：攪拌力指標。特定的工業攪拌受力模擬,。
	**[聯動]** 若為 1，則程式後續會讀取 **CARD 21-24**。
		  
- **isequel <font color="#ffff00">0</font>**：續算指標。1 代表從上一個工作檔案（DMP 檔）讀取位移與塑性數據進行續算,。

## **CARD 4: 輸出控制卡 (Output Control)**
  
<center><font color="#ffff00">1000  1000000  1  0  2  1.  0</font></center>  

- **part_skip** **(iprob) <font color="#ffff00">1000</font>**：輸出至 DMP 檔（重啟用）的跳步數。
- **full_skip** **(iprobA) <font color="#ffff00">1000000</font>**：輸出至 OUT 檔（文字報告）的跳步數。
- **numout <font color="#ffff00">1</font>**：特定輸出請求數量。
	**[聯動]** 決定最後 **CARD 25** 的讀取行數（若為 0 則不讀取 25）,。
- **isee <font color="#ffff00">0</font>**：螢幕顯示模式。控制模擬時終端機輸出的詳細程度。
- **iplane <font color="#ffff00">2</font>**：平面分析指標。1 為平面應力（Plane Stress），2 為平面應變（Plane Strain）。
- **thick <font color="#ffff00">1.</font>**：分析厚度。定義二維結構在第三維度的名目厚度。
- **icontact <font color="#ffff00">0</font>**：接觸條件指標。決定是否啟用塊體間的邊界接觸演算法。

## **CARD 5: (遺失/跳過)**
  
- 在 `SOLID_module.F90` 的 `readata1` 中，程式碼從 1800 格式讀完後直接標記 `CARD 6` 註解並開始讀取節點。
  
---
# **第二部分：幾何與材料定義區 (始終存在)**

## **CARD 6: 節點數據 (Node Data)**
  
<center><font color="#ffff00">1 0.2024 0.2028 0.0438 0 0 0</font></center>  

- **ID <font color="#ffff00">1</font>**：節點編號。
- **X, Y, Z <font color="#ffff00">0.2024 0.2028 0.0438</font>**：節點在三維空間的初始座標值。
- **ifixX, ifixY, ifixZ <font color="#ffff00">0 0 0</font>**：位移約束旗標。1 為固定（Fixed），0 為自由（Free）。

## **CARD 7: 單元幾何數據 (Element Data)**
  
<center><font color="#ffff00">1 1 2 3 4 1 10 1 1 1</font></center>  

- **ID <font color="#ffff00">1</font>**：單元編號。
- **Node1-4 <font color="#ffff00">1 2 3 4</font>**：組成該四面體單元的 4 個節點 ID。
- **mat-typ <font color="#ffff00">1</font>**：材料類型編號。對應後方材料屬性卡的組別。
- **mat-mdl <font color="#ffff00">10</font>**：材料模型編號。例如 10 代表線性彈性模型,。
	-  `mat-mdl` 選項是決定「應力計算公式」的開關。目前代碼中明確定義了 **10（線性彈性）** 與 **20（黏彈性）**，其餘數值則預留給**彈塑性（Non-linear Plasticity）**計算，並要求使用者補全對應的強度常數
- **row, col, layer <font color="#ffff00">1 1 1</font>**：幾何排列索引。用於描述單元在結構中的拓樸方位。

## **CARD 8: 材料特性 (Material Property)**
  
<center><font color="#ffff00">1 1 256.34 1e10 0.35 0.0</font></center>

- **Group <font color="#ffff00">1</font>**： 材料群組編號
- **Type <font color="#ffff00">1</font>**：材料物理特性類型，同時讀取CARD 9。
	- 若 **mtyp2 = 1** **(彈塑性金屬)**：隨後讀取 4 個參數（抗拉強度、斷裂應力、切線模數、硬化係數）。
	- 若 **mtyp2 = 2** **(土壤泥沙)**：則讀取 5 個參數（包含內摩擦角 `Phi` 與黏聚力 `Cohesion`）。
	- 若此處讀取的個數與 `mtyp2` 定義不符，讀取指標就會錯位，導致後續數據全部毀損。
- **Density <font color="#ffff00">256.34</font>**：質量密度 (ρ)。
- **Youngs <font color="#ffff00">1e10</font>**：楊氏模數 (E)。反映材料的抵抗彈性變形能力。
- **Poisson <font color="#ffff00">0.35</font>**：帕松比 (ν)。
- **Relaxation <font color="#ffff00">0.0</font>**：鬆弛時間 (τ)。用於黏彈性模型計算。

## CARD 9: 進階屬性

 <center><font color="#ffff00">10. 10. 0. 0.</font></center>


- **Tensile <font color="#ffff00">10.</font>**：抗拉強度 (Tensile Strenth)
- **Fracture <font color="#ffff00">10.</font>**：斷裂/破壞應力門檻 (Fracture Stress)。
- **Tangent <font color="#ffff00">0.</font>** ：切線模數(Tangent Modulus)，用於塑性段斜率計算。
- **Hardening <font color="#ffff00">0.</font>**：硬化參數 $\beta$。

---
# **第三部分：受力歷史區 (取決於 CARD 3 的設定)**
## **CARD 10 & 11: Body force (依照 ifbody)**
  
<center><font color="#ffff00">3</font></center>
<center><font color="#ffff00">0.0 9.81 0.1 9.81 50.0 9.81</font></center>

- **ng <font color="#ffff00">3</font>**：重力數據對的數量。  

	- `ng` 的數量直接決定了重力隨時間變化的精細度，而其內部的 `finter` 程序採用的是**線性插值（Linear Interpolation）**，因此非線性變化必須透過增加數據對數量來進行「分段線性」逼近。
	- 當模擬演進的時間 `t` 超出您定義的數據範圍（例如小於 `tg(1)` 或大於 `tg(ng)`）時，`finter` 程序會發出警告，並將該時間點的重力值設為 **0**。這在漂浮圓柱模擬中是非常危險的，因為固體會突然失去重力而導致計算發散。當模擬演進的時間 `t` 超出您定義的數據範圍（例如小於 `tg(1)` 或大於 `tg(ng)`）時，`finter` 程序會發出警告，並將該時間點的重力值設為 **0**。這在漂浮圓柱模擬中是非常危險的，因為固體會突然失去重力而導致計算發散。  

- **Time, Gravity-Z <font color="#ffff00">0.0 9.81</font>**：定義重力值隨時間變動的數值對。


## CARD 12~14: Ground Acceleration (iacc)

- `nptsX`, `nptsY`, `g`: X/Y 向點數、重力倍率。隨後讀取對應的加速度歷時。
- 目前 iacc = 0，因此dat檔中沒有對應的區段。

## **CARD 15-18: 任意力載重 (依照 iforce2)**
  
<center><font color="#ffff00">1 2</font></center>
<center><font color="#ffff00">11</font></center> 
<center><font color="#ffff00">0.0 0.0</font></center>
<center><font color="#ffff00">0.1 0.0</font></center>
<center><font color="#ffff00">10.0 0.0</font></center>

<center><font color="#ffff00">1 1 1</font></center>
<center><font color="#ffff00">2 1 1</font></center>

- **numif <font color="#ffff00">1**</font>/ **nnaf2 <font color="#ffff00">2</font>**：力歷時總數與受力總點數。  
- **kfpnts <font color="#ffff00">11</font>**：特定載重曲線中的數據點數量。  
- **Time, Force-X <font color="#ffff00">0.0 0.0</font>**：定義外力值隨時間變動的數值對。  
- **外力輸入 (Card 18)：** **<font color="#ffff00">1 1 1</font> 與 <font color="#ffff00">2 1 1</font>**
    - **所屬區塊**：任意形狀外力 (FORCE TYPE #2 -- ARBITRARY SHAPE FORCE)。
    - **欄位意義**：`節點ID (jnode2) / 作用方向 (jdir2) / 歷時曲線ID (jaf2)`。
    - **物理行為**：這是在模擬中「主動」對結構施加能量。這兩行告訴電腦：在節點 1 和節點 2 的 **X 方向**（代碼 1），掛載你剛才定義的那組 **第 1 號力歷時曲線**。


## CARD 19～20 (依照 iforce3)
- `nnaf3`: 點數。隨後讀取 `ID`, `Dir`, `Amp`, `Freq`。
- 目前 iforce3 = 0，因此dat檔中沒有對應的區段。

## CARD 21～24 (依照 iforce4)
- `kf4`, `nnaf4`: 歷時點數、受力點數。隨後讀取攪拌力歷時與中心定義。
- 目前 iforce4 = 0，因此dat檔中沒有對應的區段。

---
# **第四部分：數據請求區 (取決於 CARD 4 的 numout)**
## **CARD 25: 輸出請求 (Output Request)**

<center><font color="#ffff00">13 0 1</font></center>

- **nodeID <font color="#ffff00">13</font>**：欲監測的特定節點編號。
- **type <font color="#ffff00">0</font>**：輸出物理量類型。0: 位移, 1: 速度, 2: 加速度, 3: 應力,。    
- **direction <font color="#ffff00">1</font>**：分量方向。1: X, 2: Y, 3: Z/XY 剪力,。  


---
# 🔗 參考資料


---
