---
type: 📝 Research
created: 2026-07-18 04:03
modified: 2026-07-22 00:15
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

持續開發中，請期待正式版上架。

---
# 🦖 以前

1. 機台版每次運行 DBM 都需要重新編譯。
2. 只存在在 NCU 的 S-311 機房。

---
# 👨‍💻 以後

## 1. WSL 可運行 2.5.3: 
   - 測試了平行版賓漢流的速度分布測試，**以這個案例而言** ，機台版（左）與 WSL 版（右） 99.99% 一致，唯獨推算出的 Z_SCOUR 會因為精度跟記憶體分配而有微妙差別，但不影響模擬本身。
   - 操作方式調整為與之前 116 版的 Truchas-WSL 相同 (輸入 `run_sim` 即會顯示使用說明與範例)。

  ![](pics/Pasted%20image%2020260718040910.png)
  ![](pics/Pasted%20image%2020260718041136.png)
![](pics/Pasted%20image%2020260718041310.png)
  
  
## 2. 專屬區段 &DBM: 
   現在可以在 inp 檔的&DBM 設定流變參數，大幅減少編譯的依賴性。  
![](pics/Pasted%20image%2020260718040651.png)

### **- LOAD_BATHYMETRY** 
	Code Path:
	  src/drivers/drivers.F90
	  src/drivers/load_bathymetry_module.F90
	  src/input/Load_Topo_input.F90
  
### **- INTERNAL_SOURCE_SETTINGS**
	Code Path:
	  src/input/Internal_Source_input.F90
	  src/physics/fluid_flow/internal_source_nodule.F90
	  check NBLM for others

### **- DBM **
	Code Path
	  src/input/DBM_input.F90
	  src/physics/fluid_flow/viscous/viscous_module.F90
	  check NBLM for others

### **- Sponge_Layer**
	sp_Left : Face -X
	sp_Right: Face +X
	decay from start (s) to end (e)
	Code Path: 
	  src/input/Sponge_Layer_input.F90
	  src/physics/fluid_flow/Sponge_Layer_module.F90


### **- SET_BC_SETTINGS**
	Code Path:
	  src/input/Set_BC_input.F90
	  src/physics/fluid_flow/set_bc_module.F90
	  check NBLM for others


## 3. inp 檔順序調整
   - 由於 `inp` 檔讀取是認 `&` 與 `/`，外部空間可作為註解。  
   - 整體排版邏輯遵循 **「邏輯優先順序 (Logical Workflow)」**：
	1. **網格與時空 (Mesh & Time)**：決定計算邊界與時間長度。
	    
	2. **物理機制與流體物性 (Physics & Materials)**：定義算什麼、用什麼材料。
	    
	3. **幾何區域 (Body)**：把材料填入哪些空間。
	    
	4. **邊界與源項 (BC, Source, Sponge Layer)**：邊界條件與波浪/源項設置。
	    
	5. **數值解法與求解器 (Numerics & Linear Solver)**：時間步長、庫朗數與矩陣求解。
	    
	6. **輸出與平行計算 (Outputs & Parallel)**：計算結果輸出設定。

---
# 📝 內容紀錄

## 1. 平行版賓漢流速度分布測試：&BODY 僅設置兩種材料
  - 案例 A：材料 1 賓漢流、材料 2 空氣（背景）：與解析解吻合
  - 案例 B：材料 1 賓漢流、材料 2 空氣（背景）、材料 3 （同材料 1但未使用）：與解析解吻合
  - 案例 C：材料 1（同材料 3 但未使用）、材料 2 空氣（背景）、材料 3 （賓漢流）：與解析解不合
  - 即使修改 material priority，案例 C 也與解析解不合且相去甚遠。
  - 可能原因：INT_NORMAL 對多材料（>2 種）的梯度處理疑慮
	在 volume_track_module.F 90 的介面法向量計算副程式 INT_NORMAL 中，開發者留下了明確的警告註釋：維護者警告：原始碼標註「對於超過兩種材料的情況，這套系統是否能產生有意義的結果令人懷疑（grave doubts）」。程式碼使用 Mat_Normal(1,:,:) 作為暫存陣列來重新排列 VOF 順序。當材料 3 參與計算時（即便 VOF 為 0），它在 Matpri（優先權陣列）中的位置會改變梯度算子的操作順序，這可能在涉及複雜界面重構時引入非對稱的數值誤差。


## 2. 轉檔跟編譯功能
  - 持續開發中，請期待正式版上架。

---
# 🔗 參考資料


---