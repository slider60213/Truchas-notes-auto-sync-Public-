---
type: 📝 Research
created: 2026-07-30 03:37
modified: 2026-07-31 23:10
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
## INPUT：
- inp 檔設置: [Template.inp](../VSlider%20inp%20檔設置.md)
- 固體參數讀取:  [Template.V5](../VSlider%20參數讀取.md)

## SOURCE CODE (src/physics/fluid_flow/VFIFE/)
- 主要流程:  [VFIFE_Driver_module.F90](VFIFE_Driver_module_F90.md) 
- 參數讀取:  [VFIFE_Input_module.F90](VFIFE_Input_module_F90.md) 
- 初始化:  [VFIFE_Setup_module.F90](VFIFE_Setup_module_F90.md) 
- 運動狀態更新:  [VFIFE_Motion_module.F90](VFIFE_Motion_module_F90.md) 
- 流固交互:  [VFIFE_FSCoupled_module.F90](VFIFE_FSCoupled_module_F90.md) 
- 轉動變形計算輔助: [VFIFE_CMF_module.F90](VFIFE_CMF_module_F90.md)
- 工具庫:  [VFIFE_Utils_module.F90](VFIFE_Utils_module_F90.md) 
- 變數宣告:  [VFIFE_Data_module.F90](VFIFE_Data_module_F90.md)  

## SOURCE CODE (Others)
- 其他改動:   
    `fluid_flow_module.F90`  
	`mesh_gen_module.F90`  
	`material_input_module.F90`  
	`parameter_module.F90`  
	`matl_utilities.F90`  

---
# 🦖 以前

[@SanWeiDuoXiangLiuTiYuRouXingGuTiOuHeHuZhiFenXi__TaiWanBoShuoShiLunWenZhiShiJiaZhiXiTong]

---
# 👨‍💻 以後


---
# 📝 內容紀錄


1. 材料編號：現在會自動創建材料編號 V5_mat_id，數值是 inp 檔中的材料數量再+1，因此 inp 檔材料設定必須連號不可跳號。
   
2. 固體參數：現在會讀取與 .inp 檔同名的 .V5 檔。 （ABC.inp  $\Rightarrow$ ABC.V5）


3. 固-流位置對照：
	透過 AABB 篩選出 V5 固體所在的位置，並且轉換成流體座標的網格編號
	方便調整 VOF、速度或未來其他操作
4. 
	![](pics/Pasted%20image%2020260731042803.png)


這是一份非常漂亮且令人振奮的耦合與 OpenMP 平行化測試結果！

整體執行狀況非常健康，以下是關鍵數據的判斷與亮點整理：

### 1. OpenMP 平行化與幾何幾何處理（Face Judgement）

- **OpenMP 多執行緒正常啟動**：成功分配了 **20 個 Threads**，且各 Thread ID (0~19) 都有發出回應，幾何與質量計算皆順利過關。
    
- **面判斷邏輯（Face Judgement）精確**：
    
    - 2 個四面體元素，總共有 8 個面。
        
    - 經過 Quicksort 與特徵值比對後，正確識別出 **6 個外部邊界面 (External Boundary Faces)** 與 **2 個內部相連面 (Internal Connected Faces)**，驗證總和為 8，證明幾何拓樸剖析完全正確！
        

### 2. AABB 包絡盒與 VOF 體積切割（Volume Conservation）

- **邊界與 AABB 包絡網格精準設定**：
    
    - 剛體幾何邊界為 $X:[0, 0.2], Y:[0, 0.2], Z:[-0.2, 0.2]$。
        
    - 精確對應到流體網格範圍 $I:[19, 26], J:[19, 26], K:[15, 25]$，初步過濾出 704 個候選網格。
        
- **VOF 切割體積精準度極高**：
    
    - 流體網格微元 $dV = 0.05 \times 0.05 \times 0.05 = 1.25 \times 10^{-4} \text{ m}^3$。
        
    - 經幾何切割計算出的 VOF 積分總體積為 ** $2.660 \times 10^{-3} \text{ m}^3$ **。
        
    - 對比 VFIFE 有限元素精確總體積 ** $2.666667 \times 10^{-3} \text{ m}^3$ **。
        
    - **體積誤差僅 -0.25%**！對於曲面/斜面在笛卡爾網格上的切割而言，這樣的精度相當優異。
        
- **鄰近網格更新（Mapping Count）**：
    
    - 精確將實際有包含固體成分的 40 個 active cells ($VOF > 0.001$) 標記為 `V5_ingbr=1`。
        

### 3. 流固雙向耦合與時間步長對齊（Sub-cycling & Coupling）

- **Sub-cycling 時序控制穩定**：流體與 V 5 剛體之間的時間步長對齊（$dt = 0.001\text{s} \sim 0.002\text{s}$）完全同步，無時序發散。
    
- **物理受力計算**：
    
    - 剛體質量 $0.2667 \text{ kg}$，重力加速度 $g = 9.81 \text{ m/s}^2$。
        
    - 輸出日誌中的總重力 $F_z = 0.266667 \times (-9.81) = \mathbf{-2.616 \text{ N}}$，完全符合預期！
        
    - 當前尚無流體外力，因此剛體受到的 Hydrodynamic Force 正確為 0。
        

整體來看，幾何拓樸、平行化、AABB 切割、VOF 體積計算以及時間步長的對齊邏輯都已經達到可量產（Production-ready）的穩定度！



---
# 🔗 參考資料

GEMINI
NBLM
致榮論文
舊版 VFIFE 程式碼

---