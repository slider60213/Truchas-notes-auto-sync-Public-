## 3. 如何繞過「古早編譯器」的限制？

你提到的 Linux 環境限制（例如只能用 gfortran 4.8 之類的），可以透過 **Container (容器化)** 技術完美解決：

1. **Docker / Singularity**：在容器裡安裝最新版的編譯器和 GPU 驅動。這不會弄亂你 Linux 主機的系統環境。
    
2. **Conda 環境管理**：在 Python 端，你可以輕鬆安裝最新版的庫，而不需要 root 權限。



這是一個非常棒的實驗！這能讓你親自體會「Python 的便利」如何與「Fortran 的效能」無縫接合。

`f2py` 的核心邏輯是：它會讀取你的 Fortran 程式碼，自動產生一個 C 語言的「中間橋樑」，最後編譯成一個 Python 可以直接 `import` 的 **.so** (Linux) 或 **.pyd** (Windows) 檔案。

以下是你的 **「三分鐘快速測試指南」**：

---

### 第一步：撰寫一個簡單的 Fortran 矩陣相加 (matrix_add.f90)

我們寫一個最基礎的運算，模擬 VFIFE 裡常見的矩陣操作。

Fortran

```
! matrix_add.f90
subroutine add_matrices(A, B, C, n, m)
    implicit none
    integer, intent(in) :: n, m
    real(8), intent(in) :: A(n,m), B(n,m)
    real(8), intent(out) :: C(n,m)
    
    ! Fortran 的矩陣運算非常直觀且快速
    C = A + B
end subroutine add_matrices
```

---

### 第二步：使用 f2py 編譯它

在你的終端機（Terminal）輸入以下指令：

Bash

```
python -m numpy.f2py -c matrix_add.f90 -m my_fortran_lib
```

- `-c`: 代表編譯（Compile）。
    
- `-m my_fortran_lib`: 這是你之後在 Python 裡要 `import` 的模組名稱。
    

編譯成功後，你會在資料夾看到一個像 `my_fortran_lib.cpython-3xx...so` 的檔案。

---

### 第三步：在 Python 裡呼叫它

現在，打開你的 Python 環境（或是寫一個 `.py` 檔）：

Python

```
import numpy as np
import my_fortran_lib  # 這裡就是你剛編譯好的 Fortran 模組

# 1. 建立兩個 1000x1000 的隨機矩陣
n, m = 1000, 1000
A = np.random.rand(n, m).astype(np.float64)
B = np.random.rand(n, m).astype(np.float64)

# 2. 直接呼叫 Fortran 的次程序
# 注意：f2py 非常聰明，它會自動處理陣列的傳遞
C = my_fortran_lib.add_matrices(A, B)

# 3. 驗證結果
print(f"矩陣 C 的形狀: {C.shape}")
print(f"前三個元素: {C[0, :3]}")
print("結果是否正確:", np.allclose(C, A + B))
```

---

### 為什麼這對你的 Truchas 改造計畫很重要？

1. **資料共享 (Zero Copy)**：`f2py` 傳遞的是記憶體位址。這意味著你的海嘯大網格數據不需要在 Python 和 Fortran 之間「複製」來「複製」去，速度極快。
    
2. **逐步替換**：你可以先保留 VFIFE 90% 的物理運算在 Fortran，只把 $Ax=b$ 的矩陣 $A$ 與向量 $b$ 傳回 Python，然後在 Python 端用 **GPU (CuPy)** 來求解。
    
3. **現代化開發**：你可以利用 Python 的繪圖庫 (Matplotlib) 或是 AI 庫 (PyTorch)，直接對 Fortran 算出來的數據進行即時監控或加速。
    

---

### **遇到的常見坑（Shane 筆記）：**

- **矩陣儲存順序**：Fortran 是 **Column-major** (直列優先)，而 NumPy 預設是 **Row-major** (橫列優先)。當矩陣很大時，如果沒有注意這一點，性能會下降。
    
- **編譯器版本**：`f2py` 通常會抓你系統預設的 `gfortran`。如果你的環境真的太老，記得在編譯時指定路徑。