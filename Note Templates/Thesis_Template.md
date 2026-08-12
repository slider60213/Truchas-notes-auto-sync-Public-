# 第三章 研究方法與數值模型

## 3.1 控制方程式 (Governing Equations)

本研究採用三維非壓縮性流體之統御方程式，其動量守恆方程式如下所示：

$$
\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla) \mathbf{u} = -\frac{1}{\rho} \nabla p + \nu \nabla^2 \mathbf{u} + \mathbf{g}
$$

其中 $\mathbf{u}$ 為流速向量，$\rho$ 為流體密度，$p$ 為壓力，$\nu$ 為動黏性係數，$\mathbf{g}$ 為重力加速度。

---

## 3.2 Truchas 邊界條件設定

數值模擬採用 Truchas 進行配置，其關鍵流體物理參數設定如下表所示：

| 參數名稱 (Parameter) | 數值 (Value) | 單位 (Unit) | 說明 (Description) |
| :--- | :---: | :---: | :--- |
| **Fluid Density ($\rho$)** | $998.2$ | $\text{kg/m}^3$ | 水之工作密度 |
| **Dynamic Viscosity ($\mu$)** | $1.002 \times 10^{-3}$ | $\text{Pa}\cdot\text{s}$ | 20°C 下水之動黏度 |
| **Gravity ($\mathbf{g}$)** | $(0, 0, -9.81)$ | $\text{m/s}^2$ | 垂直向重力加速度 |

---

## 3.3 算例邊界網格配置

模擬之流場網格劃分與流場邊界如圖 3.1 所示：

![圖 3.1：Truchas 算例之三維網格劃分與流場邊界示意圖](attachments/mesh_boundary_config.png)

> **圖 3.1 說明**：上圖顯示入口邊界（Inflow）、自由液面（Free Surface）以及底床邊界之網格細化配置。

---

## 3.4 物理參數與關鍵程式碼設定

以下為 Truchas 模擬輸入檔中關於流體相（Phase）設定之關鍵片段：

```json
{
  "PHYSICAL_CONSTANTS": {
    "stefan_boltzmann": 5.67e-8,
    "absolute_zero": -273.15
  },
  "MATERIAL": {
    "name": "Water",
    "density": 998.2
  }
}