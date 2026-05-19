## 2. VFIFE求解器測試：jacobi v.s. ilu0
- VFIFE 預設用 `jacobi` 是為了保險，但身為博士候選人，你追求的是效率。
- **用 Jacobi 時**：FGMRES 像是在黑夜裡拿手電筒，一次只能看一格。
- **換成 ILU0 時**：FGMRES 像是戴上了夜視鏡，雖然遠方還是模糊，但周遭的網格地貌清晰可見。

> **實戰註記**：如果你在 VFIFE 的 `.inp` 檔中將 `preconditioning_method` 從 `'jacobi'` 改為 `'ilu0'`，你通常會觀察到：雖然每一迭代步的牆鐘時間（Wall-clock time）微幅增加，但**總迭代次數會大幅下降**，<mark style="background: #FF5582A6;">最終總計算時間縮短。</mark>


VFIFE\src\input\lin_solver_input.F90：`UBIK_PRESSURE_DEFAULT`
VFIFE、DEM、2.0.2、2.5.3預設皆為fgmres+jacobi
> ![](pics/Pasted%20image%2020260317174219.png)

| solver                 | fgmres | fgmres |
| :--------------------- | :----- | :----- |
| preconditioning method | jacobi | ilu0   |
|                        |        |        |
目前發現迭代次數相同，可能是  relaxation_parameter = 1.4太高


先確認是否有成功修改程式碼：ilu0_test2

### 1. 鬆弛因子（Relaxation Parameter）的衝突

你設定了 `relaxation_parameter = 1.4`。

- **原因**：1.4 通常是給 **SSOR** 或 **Jacobi** 這種疊代型眼鏡用的（加速收斂）。
    
- **問題**：`ilu0` 是基於矩陣分解的「硬性眼鏡」，它不需要（也不喜歡）過大的鬆弛因子。在 `ilu` 系列中，過高的鬆弛參數反而可能導致數值不穩定，讓 FGMRES 必須花更多步數來修正這個「過度修正」。
    
- **建議**：將其改回 **1.0**（不鬆弛）試試看。
    

---

### 2. 「步數」有沒有掉？（核心指標）

要判斷 `ilu0` 有沒有發揮作用，不能只看「總時間」，要看 **Iteration Count (迭代次數)**。

- **觀察點**：請檢查你的 `status_frequency` 輸出的 log。
    
    - 如果 **Jacobi** 跑 100 步收斂，**ILU0** 也跑 100 步，那代表 `ilu0` 對你的龜山島網格無效（可能網格太規則了）。
        
    - 如果 **ILU0** 讓步數從 100 步掉到 30 步，但「總時間」沒變，那代表 **ILU0 單步的計算量太重**。
        

---

### 3. Krylov Vectors 的重啟（Restart）開銷

因為 `ilu0` 提供的方向比 `jacobi` 準很多，你可能不再需要那麼多「記憶體路標」。

- **現象**：如果 `KRYLOV_VECTORS_DEFAULT` 設定很高（例如 60 或 100），FGMRES 每一步都要跟這 100 個向量做正交化，計算量極大。
    
- **優化**：既然眼鏡（ILU0）變準了，你可以嘗試調小 `krylov_vectors`（例如設定為 **30**）。
    
    - **邏輯**：更強的眼鏡可以在更短的子空間內找到解，減少 FGMRES 內部的 Gram-Schmidt 運算量。
        

---

### 4. 你的硬體與平行化（MPI）

- **如果是平行運算**：`ilu0` 在跨核心（Processors）通訊時，效果會打折扣。如果你開了非常多核心跑龜山島，局部區域的 `ilu0` 資訊無法傳遞給鄰居，這時它的表現會退化到接近 `jacobi`，但計算成本卻更高。
    

---

### **建議調整清單**

請 Shane 試試看以下這組配置，對比原本的結果：

Fortran

```
       ! --- Shane 修正版測試 ---
       convergence_criterion          = ten_tominus10
       preconditioning_method         = 'ilu0' 
       relaxation_parameter           = 1.0    ! 降回 1.0，避免過度修正
       krylov_vectors                 = 30     ! 縮小搜索空間，測試是否能加速
       preconditioning_steps          = 1      ! 確保 ilu0 只做一次分解
```

**你可以觀察一下調整後的 Log：**

1. 每一小步的迭代次數是否有顯著下降？
    
2. 如果步數下降了但時間還是沒省到，我們可能要回頭檢視你的 **網格長寬比 (Aspect Ratio)**，那會決定哪種眼鏡最省錢。### 1. 鬆弛因子（Relaxation Parameter）的衝突

你設定了 `relaxation_parameter = 1.4`。

- **原因**：1.4 通常是給 **SSOR** 或 **Jacobi** 這種疊代型眼鏡用的（加速收斂）。
    
- **問題**：`ilu0` 是基於矩陣分解的「硬性眼鏡」，它不需要（也不喜歡）過大的鬆弛因子。在 `ilu` 系列中，過高的鬆弛參數反而可能導致數值不穩定，讓 FGMRES 必須花更多步數來修正這個「過度修正」。
    
- **建議**：將其改回 **1.0**（不鬆弛）試試看。
    

---

### 2. 「步數」有沒有掉？（核心指標）

要判斷 `ilu0` 有沒有發揮作用，不能只看「總時間」，要看 **Iteration Count (迭代次數)**。

- **觀察點**：請檢查你的 `status_frequency` 輸出的 log。
    
    - 如果 **Jacobi** 跑 100 步收斂，**ILU0** 也跑 100 步，那代表 `ilu0` 對你的龜山島網格無效（可能網格太規則了）。
        
    - 如果 **ILU0** 讓步數從 100 步掉到 30 步，但「總時間」沒變，那代表 **ILU0 單步的計算量太重**。
        

---

### 3. Krylov Vectors 的重啟（Restart）開銷

因為 `ilu0` 提供的方向比 `jacobi` 準很多，你可能不再需要那麼多「記憶體路標」。

- **現象**：如果 `KRYLOV_VECTORS_DEFAULT` 設定很高（例如 60 或 100），FGMRES 每一步都要跟這 100 個向量做正交化，計算量極大。
    
- **優化**：既然眼鏡（ILU0）變準了，你可以嘗試調小 `krylov_vectors`（例如設定為 **30**）。
    
    - **邏輯**：更強的眼鏡可以在更短的子空間內找到解，減少 FGMRES 內部的 Gram-Schmidt 運算量。
        

---

### 4. 你的硬體與平行化（MPI）

- **如果是平行運算**：`ilu0` 在跨核心（Processors）通訊時，效果會打折扣。如果你開了非常多核心跑龜山島，局部區域的 `ilu0` 資訊無法傳遞給鄰居，這時它的表現會退化到接近 `jacobi`，但計算成本卻更高。
    

---

### **建議調整清單**

請 Shane 試試看以下這組配置，對比原本的結果：

Fortran

```
       ! --- Shane 修正版測試 ---
       convergence_criterion          = ten_tominus10
       preconditioning_method         = 'ilu0' 
       relaxation_parameter           = 1.0    ! 降回 1.0，避免過度修正
       krylov_vectors                 = 30     ! 縮小搜索空間，測試是否能加速
       preconditioning_steps          = 1      ! 確保 ilu0 只做一次分解
```

**你可以觀察一下調整後的 Log：**

1. 每一小步的迭代次數是否有顯著下降？
    
2. 如果步數下降了但時間還是沒省到，我們可能要回頭檢視你的 **網格長寬比 (Aspect Ratio)**，那會決定哪種眼鏡最省錢。

