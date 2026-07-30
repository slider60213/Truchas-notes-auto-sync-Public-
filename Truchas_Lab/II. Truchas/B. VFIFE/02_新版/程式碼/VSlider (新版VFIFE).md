---
type: 📝 Research
created: 2026-07-30 03:37
modified: 2026-07-31 04:44
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


我們已經成功完成了初始化的驗證（`V5_Initialize`），接下來要驗證的是**時間跨步（Time-stepping）與動態計算**的邏輯。

進入 `EXECUTE_V5_SIMULATION()` 後，涉及**時間子步（Sub-cycling）、外力/內力計算、顯式積分（VFIFE Motion）、以及流固耦合（Feedback）**。為了維持程式碼的架構品質與維護性，建議將驗證分為兩個階梯來進行。

### 第一階段：驗證架構方向與驗證設計（請確認）

為了驗證 `EXECUTE_V5_SIMULATION` 是否正確運作，我建議採用**無干擾的 Log 診斷點（Diagnostic Markers）**，透過印出關鍵物理量來檢查以下 4 個核心機制：

1. **時間子步對齊（Sub-cycling & Time Alignment）**：
    
    - **概念**：驗證 `V5_time` 是否能精確追上流體時間 `t2`，且動態微調 `V5_DeltaT = MIN(V5_dt, t2 - V5_time)` 時沒有產生浮點數累積誤差或死迴圈。
        
    - **驗證方式**：印出每次 `DO WHILE` 的 `step_count`、目前 `V5_DeltaT` 與剩餘時間差距 `(t2 - V5_time)`。
        
2. **剛體/變形體運動學與動量守恆（Kinematics & Conservation）**：
    
    - **概念**：檢查在受力狀態下，顯式時間積分（`update_kinematics`）計算出的質心位置（CoM）、速度（Vel）、加速度，以及四元數範數（`Quaternion Norm` 是否恆等於 $1.0$）。
        
    - **驗證方式**：若是自由落體測試（僅受重力），$Z$ 軸速度應滿足 $v_z(t) = -g \cdot t$，位移應滿足 $z(t) = -\frac{1}{2}g t^2$。
        
3. **雙向耦合映射數據流（FS-Coupling Data Flow）**：
    
    - **概念**：確認流體壓力映射至固體節點（`Get_Fluid_Info`）以及固體 VOF/速度反饋給流體（`update_fluid_mapping` & `V5Solid_Feedback`）的數據傳遞順序。
        
    - **驗證方式**：在 `V5Solid_Feedback` 執行後，印出固體涵蓋區域內流體網格的最大反饋速度（`MAXVAL(fluid_u)`），確認流體確實收到固體的邊界速度。
        
4. **記憶體安全性與週期轉換（Lifecycle & Cleanup）**：
    
    - **概念**：確認在跨越多個流體時間步（`cycle_number` 增加）時，區域變數沒有發生 Leak，且 `SAVE` 變數在跨步間保持連續性。
        

### 第二階段：驗證步驟規劃

建議我們先透過一個簡單的測試情境（例如：**純重力自由落體** 或 **固定剛體受流場作用**）進行 1~2 個 `cycle_number` 的試算。

按此規劃，我們會執行以下步驟：

1. **確認驗證方向**：請確認上述 4 個核心驗證點是否符合你目前的測試目標。
    
2. **小範圍插樁（Diagnostic Insertion）**：同意後，我們僅在關鍵位置（如子步迴圈結束處、`V5Solid_Feedback` 之後）插入幾行 `WRITE(*,*)` 的診斷程式碼，**完全不改動任何核心物理計算邏輯**。
    
3. **執行並對照**：運行程式並觀測 Log 輸出，確認動態物理量與時間步對齊無誤。



---
# 🔗 參考資料

GEMINI
NBLM
致榮論文
舊版 VFIFE 程式碼

---