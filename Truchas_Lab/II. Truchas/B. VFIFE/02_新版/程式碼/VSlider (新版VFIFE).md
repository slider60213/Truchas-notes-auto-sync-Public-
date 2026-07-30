---
type: 📝 Research
created: 2026-07-30 03:37
modified: 2026-07-31 03:02
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
	![](pics/Pasted%20image%2020260730020933.png)






---
# 🔗 參考資料

GEMINI
NBLM
致榮論文
舊版 VFIFE 程式碼

---