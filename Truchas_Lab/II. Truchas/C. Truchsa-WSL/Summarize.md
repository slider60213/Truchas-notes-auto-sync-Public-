---
type: 📝 Research
created: 2026-08-25 02:14
modified: 2026-08-25 02:16
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
以下是您的實驗室機台現況整理：

### 1. 編譯器環境：GCC 4.6.3

- **版本：** `4.6.3 (2012年發佈)`
- **特性：** 這是 14 年前的編譯器。它支援的是較早期的 Fortran 標準（如 F95/F2003 的部分功能）以及 C++98。
- **重點：** 現代 Ubuntu 預設的 `gcc` 通常是 11 或 12 版，這對於舊版 TRUCHAS 來說可能太新了，會導致許多語法檢查不通過。

### 2. MPI 實作：LAM/MPI（極為罕見）

- **情況：** 您的機台使用的不是現代主流的 OpenMPI 或 MPICH，而是 **LAM/MPI**。
- **關鍵點：** LAM/MPI 早在 2000 年代中後期就已經停止開發，並併入了 OpenMPI 計畫。這是一個非常大的「坑」，因為 LAM/MPI 的指令（如 `lamboot`）與現代 MPI 完全不同。這也是為什麼您執行 `ompi_info` 會找不到指令。

### 3. 建置工具：CMake 2.8.8

- **版本：** `2.8.8`
- **重點：** 這是非常舊的 CMake。如果 TRUCHAS 的 `CMakeLists.txt` 是針對這個版本寫的，用現代的 CMake 3.x 去跑可能會出現一堆 Deprecation Warnings 甚至錯誤。

---

### 我們的移植策略建議：

您的實驗室環境是 **「2012 年左右的技術棧」**，而您的 LXD 容器（如果是 Ubuntu 20.04 或 22.04）則是 **「2020 年以後的技術棧」**。 **要在容器內成功編譯，我們有兩個選擇：**

1. **降級安裝（推薦）：** 在容器內安裝 `gcc-4.8` 或 `gcc-5` 等較舊的版本（Ubuntu PPA 還有機會找到），並嘗試用 OpenMPI 的相容模式來取代 LAM/MPI。
2. **暴力對齊：** 如果 TRUCHAS 程式碼真的太舊，我們可能要在容器內「手動編譯」一份 GCC 4.6.3 和 LAM/MPI，但這工程非常浩大且容易失敗。

---
# 👨‍💻 以後


---
# 📝 內容紀錄


---
# 🔗 參考資料


---