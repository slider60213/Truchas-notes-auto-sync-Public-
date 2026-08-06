---
type: 📝 Research
created: 2026-08-06 14:21
modified: 2026-08-06 23:49
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


---
# 🦖 以前


---
# 👨‍💻 以後


---
# 📝 內容紀錄

# 剛體/自由落體/真空

- **V 5 佔整體模擬預算**：總耗時 **105.54 秒**，僅佔整體模擬總預算（7,849.6 秒）的 **1.34%**。
    
- **V 5 內部運算階段（105.52 秒）**：
    
    - **V 5 Solid Mapping**：耗時 **104.84 秒**（獨佔 V 5 內部的 **99.36%**，佔整體 **1.34%**）。
        
    - **V 5 Setup**：耗時 0.61 秒（佔 V 5 的 0.58%）。
        
    - **物理與力學計算**（Ext Force、Get Fluid、Kinematics、Int Force）：合計僅耗時 **0.04 秒**（佔 V 5 的 0.04%）。
        
- **V 5 初始化階段（0.024 秒）**：
    
    - **V 5 Init Mapping**：耗時 **0.023 秒**（佔初始化的 **97.26%**）。
        
    - **V 5 Init Comm 及其他**：耗時 0.001 秒（佔初始化的 2.74%）。
        
- **分析結論**：V 5 的物理與力學運算極快，但「Mapping（網格映射/搜尋）」吃掉了 V 5 模組 **99% 以上**的資源，是內部唯一的效能瓶頸。


# 剛體/自由落體/空氣密度 1.2

- **流體壓力與方程求解 (Projection)**：耗時 **1,528.30 秒**，占整體 **71.7%**（為主要運算開銷，包含 Mac_Projection 816.35 秒、Solver 696.43 秒 與 Precondition 453.91 秒 等）。
    
- **質量與體積對流 (Mass Advection)**：耗時 **368.88 秒**，占整體 **17.3%**（包含 Volume Tracking 343.29 秒、Reconstruct/Advec 223.80 秒 與 Locate Plane 1.25 秒）。
    
- **速度預測與修正 (Predictor & Corrector)**：耗時 **264.59 秒**，占整體 **12.4%**（Predictor 162.88 秒，Corrector 101.71 秒）。
    
- **黏性力計算 (Viscous)**：耗時 **47.01 秒**，占 Predictor 的 **28.9%**（占整體約 2.2%）。
    
- **固體/介面耦合 (V 5 Simulation)**：耗時 **23.50 秒**，占整體 **1.1%**（主要瓶頸為 V 5 Solid Mapping 23.37 秒）。
    
- **時間步長與動量對流 (Time Step & Momentum)**：耗時 **47.40 秒**，占整體約 **2.2%**（Time Step 21.90 秒，Momentum Advection 25.50 秒）。
    
- **幾何定位與前後處理 (Initialization & Output 等)**：耗時 **5.42 秒**，占整體 **0.3%**（Initialization 3.15 秒，Output 2.27 秒）。
    
- **總計 (Main Cycle / Total)**：耗時 **2,134.30 秒** (100.0%)，流體壓力求解與質量對流合計佔據整體約 **89.0%** 的計算時間。

---
# 🔗 參考資料


---