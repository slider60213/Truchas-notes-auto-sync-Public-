##  N-S乃至PPE看起來都是建立於面速度的計算來確保答案準確,那為何2.5.3不用面速度？而且為什麼還可以準確？


## Internal Source 不會導致散度不為0嗎？怎麼知道設為多少合理？範圍呢?會不會反射？


## Pressure BC 作用在PPE之前還之後？會不會影響？


## 非正交網格如何處理？
Stage 5-1 聚焦於如何透過**最小平方法線性重建（LSLR）****非正交修正技術**，將連續物理場的梯度（Gradient）與散度（Divergence）運算精確地轉化為電腦可解算的離散矩陣算子,,。

針對 Stage 5-1 的底層離散算子架構，以下是基於原始碼的深度技術校閱：

1. 離散算子的核心方法 (Discrete Methods)

根據 `discrete_op_module.F90` 與 `discrete_derivatives.f90`，VFIFE 提供了多種離散策略以應對不同網格品質：

- **LSLR (Least-Squares Linear Reconstruction)**：這是模式在處理一般非正交網格時的首選技術,。它針對每個胞元及其鄰居建立泰勒級數展開，透過最小化誤差來求得最高精度的梯度值,。
- **Green-Gauss 法**：透過高斯散度定理，將胞元積分轉換為面通量的總和，具有良好的守恆性,。
- **Volume-Average 法**：透過 3x3 行列式解算，在胞元內進行體積平均以獲得梯度。
- **Orthogonal Stencil (正交算子)**：若網格被判定為全正交（`orthogonal_mesh = .true.`），系統會切換至高效的 7 點（3D）或 5 點（2D）正交算子以節省運算成本,。

2. 數據容器：`DO_Specifier`

為了提升運算效率並避免重複計算幾何參數，系統定義了 `DO_Specifier` 結構,：

- **功能**：它是一個「容器」，用來存放持久性的解算向量、係數矩陣及解法旗標。
- **解法旗標 (Method ID)**：包含 `DO_SOLVE_ORTHO` (1)、`DO_SOLVE_LU_LSLR` (2) 與 `DO_SOLVE_SVD_LSLR` (3),。
- **矩陣封裝**：對於 LSLR，容器會儲存 LU 分解後的矩陣 `ALU` 或奇異值分解後的 `SVD_cM` 矩陣,。

3. 非正交修正與數值穩定性

在劇烈地形（如沖刷坑邊界）下，網格往往會發生偏斜，此時算子的修正至關重要：

- **壓力梯度修正**：在投影步中，`VELOCITY_TO_FACES` 會利用 Rhie-Chow 演算法修正面壓力梯度，防止壓力場在非正交網格上產生數值震盪,。
- **雜訊消除 (Noise Elimination)**：所有的離散運算（如 `DIVERGENCE`）最後都會執行 `MERGE(zero, Value, ABS(Value) <= alittle)`，將低於機器精度（`alittle`）的微小數值強制歸零，以維持數值「純淨」,。
- **奇異性檢查**：在進行 `UpdateFaceLU` 時，系統會檢查主軸元素（Pivot），若獨立分量不足則會將該面判定為奇異，解算值設為 0 以防崩潰,。

4. 特殊處理：間隙與退化網格

- **Gap Elements**：算子模組特別考慮了厚度極薄的間隙單元（如 `GAP_ELEMENT_1`），這在模擬橋樑接縫或微小裂隙時會自動切換插值邏輯,。
- **退化面 (Degenerate Face)**：在處理三角形或四面體網格時，算子會偵測退化面並調整分量加總的權重,。

**專家校閱確認：** 確認 5-1 的技術細節完全對應 `discrete_derivatives.F90` 與 `do_base_types.F90` 的資料結構定義與邏輯分支


