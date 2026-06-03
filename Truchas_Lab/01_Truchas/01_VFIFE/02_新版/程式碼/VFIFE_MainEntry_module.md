---
type: 📝 Research
created: 2026-05-27 13:23
modified: 2026-06-04 01:32
tags:
  - "#Truchas"
  - WSL
  - VFIFE
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
[SOLID_module_F90](../../01_舊版/程式碼/SOLID_module_F90.md)
`esolv` 的流程確實採用了顯式動力學常見的「時空交錯（Staggered）」步進，這意味著你在當前迴圈看到的「幾何形態」是基於上一時步的位移結果，而新算出的位移則是為了下一個迴圈的幾何更新做準備,。

身為流體數值模式專家，我根據 `SOLID_module.f90` 的原始碼邏輯，為您精確梳理 `do 2222` 動力循環內部的變數演進時序：

1. 核心流程的時序拆解（以第 n 步循環為例）

2. **幾何形態構建（Form State** n**）**：
    - 迴圈一開始，利用**上一時步**算好的基準座標 `xct` 與相對位移 `d` 組合出當前的瞬時座標 `xc = xct + d`。此時的 `xc` 代表物體在第 n 步開始時的精確空間位置。
3. **內力與應力計算（Internal Forces & Stress）**：
    - **計算內力**：呼叫 `fintiso3`。它利用 `xc` 算出單元的純變形，進而得到節點內力 `feli`。
    - **應力更新**：在 `fintiso3` 內層會呼叫 `tliel`，將應變增量轉化為應力並更新 `sigma3D`。這就是在當前時步 n 更新應力的時機。
4. **流固耦合受力（Pressure & VOF 2）**：
    - **取得壓力**：透過 `face_judge` 索引從流體端獲取 `IGPRESSURE`，並積分為節點力 `pforce`。
    - **更新 VOF 2**：若本步為流體週期的結尾（`nstep == maxstp`），則計算固體佔據網格的體積分率 `solid_vof2`，供流體端下一步使用。
5. **外力與運動積分（External Forces &** F=ma**）**：
    - **計算外力**：呼叫 `fextl` 取得重力或地震力。
    - **求解運動**：執行 `c4 = fsum/xmass`。這裡算出的加速度與新位移增量 `dp`，實質上是為了決定物體**在第** n+1 **步**該去哪裡。
6. **狀態更新（The Staggered Update）**：
    - **更新座標**：執行 `xct = xct + d`。注意，這裡加的是**舊的** **d**。目的是將已經完成的運動「固化」到基準座標中。
    - **準備下一步位移**：執行 `d = dt1 - db`。這將剛算好的總位移 `dt1` 轉化為新的相對位移，留給**下一個迴圈（第 n+1 步）**一開始的 `xc` 組合使用。

7. 為什麼變數會在 n 與 n+1 之間交錯？

這種設計並非效率低下的「蠢寫法」，而是 VFIFE **途徑單元（Path Element）** 理論的要求：

- **物理一致性**：為了保證內力計算時「移動參考構架（CMF）」的一致性，在一個完整的力學平衡計算（從 `fintiso3` 到 `fsum`）過程中，參考基準 `xct` 絕對不能變動。
- **顯式解法的特徵**：顯式演算法（Explicit Method）本質上就是「用現在的受力推測未來的位移」。因此，你在步驟 4 算出的位移結果，本來就應該在步驟 5 之後（即下一個循環）才反映在幾何位置上。

---
# 👨‍💻 以後

新的架構將改為「現時計算、即時更新」，確保進入迴圈時 `xc` 就是 t=n 的位置，結束時 `xc` 更新至 t=n+1：
**讓程式碼流程符合「當前狀態** → **計算受力** → **更新位置」的直觀邏輯。**
```
subroutine esolv_refactored(...)
  ! 1. 初始化：xc 已在進入迴圈前更新至起始狀態
  do 2222 nstep = 1, maxstp
    ! --- 物理分析階段 (Physics at t=n) ---
    
    ! (A) 計算內力 (直接使用當前步已就緒的 xc)
    ! 不再需要在迴圈開頭執行 xc = xct + d 的組合
    call fintiso3(..., xc, ...)

    ! (B) 流固耦合受力與外力計算
    ! 直接以當前 xc 計算 pforce 與 fextl
    call fextl(..., xc, ...)
    ! 執行壓力積分...

    ! --- 運動積分階段 (Solve for t=n+1) ---

    ! (C) 求解 F=ma
    ! 根據當前合力計算加速度，並求得位移增量 dp (從 t 到 t+1)
    ! dp = ... 

    ! --- 狀態更新階段 (Update to t=n+1) ---

    ! (D) 更新總位移與瞬時座標
    dt1 = dt1 + dp
    xc = xc_initial + dt1  ! 立即更新 xc 到下一步的位置

    ! (E) 重置途徑單元基準 (Path Element Reset)
    ! 為了維持 VFIFE 途徑單元理論，將 xc 固化為新的參考基準
    xct = xc
    d = 0  ! 在此架構下相對增量重置為0，因為 xc 已即時更新

    ! (F) 數據輸出 (此時輸出的是 t=n+1 的最終狀態)
    if (mod(nstep, iprob) == 0) call plot_Tecplot(...)
  end do
end subroutine
```

---
# 📝 內容紀錄

``` fortran
MODULE VFIFE_MainEntry_module
   USE VFIFE_Core_module  ! �ޥΤj���`�Greadata1, dynamic, compute_internal
   !SHANE 記得把 input_file 開回來
   !USE output_module,             ONLY: input_file

   IMPLICIT NONE          ! ��� Module �g�@���Y�i�A�j��n�D�Ҳդ��Ҧ����l�{�ǳ��������T�ŧi�ܼ�


   PRIVATE
   PUBLIC :: EXECUTE_VFIFE_SIMULATION
   character(LEN = 256),  public :: input_file

CONTAINS

   ! ==========================================================
   !  VFIFE �D����{�� (�����x�ŧO)
   ! ==========================================================
   SUBROUTINE EXECUTE_VFIFE_SIMULATION()
      CHARACTER(LEN=256)           :: V5_dat_name
      INTEGER                      :: i_err, u_inp

      WRITE(*,*) ">>> [VFIFE] Starting Simulation Workflow..."
      !input_file='V5_New_Dat_Format.inp'
      input_file='Code_devlope_test.inp'

      ! 1. ���� input_file �O�_�w�Q��� (�w�����ˬd)
      IF (LEN_TRIM(input_file) == 0) THEN
         WRITE(*,*) "Fatal: No input file specified in output_module."
         STOP
      END IF

      ! 2. �ϥ� NEWUNIT �}�ҭ�l .inp (�۰ʨ��o�t�ƽs���A�O�Ҥ��P Truchas �Ĭ�)
      OPEN(NEWUNIT=u_inp, FILE=TRIM(input_file), STATUS='OLD', IOSTAT=i_err)
      IF (i_err /= 0) THEN
         WRITE(*, '("Fatal: Cannot open [", A, "].")') TRIM(input_file)
         STOP
      END IF

      ! 3. �ʺA�ഫ�ɦW (�d�ҡGcase1.inp -> case1.dat)
      ! input_file(1:LEN_TRIM(input_file)-4) �|�I���̫�|�Ӧr�� ".inp"
      V5_dat_name = input_file(1:LEN_TRIM(input_file)-4) // '.dat'
      WRITE(*,*) " [DEBUG] V5 Solid logic will read from: ", TRIM(V5_dat_name)

      ! 4. ����֤�Ū���P�p��y�{
      WRITE(*,*) ' Shane: readata1 start'
      CALL readata1(V5_dat_name) ! �ǤJ�ഫ�᪺ .dat �ɦW
      WRITE(*,*) ' Shane: readata1 finish'

      WRITE(*,*) ' Shane: bmass start'
      CALL bmass()
      WRITE(*,*) ' Shane: bmass finish'

      WRITE(*,*) ' Shane: dynamic start'
      CALL dynamic()
      WRITE(*,*) ' Shane: dynamic finish'


      ! 5. �����ɮרòM�z
      CLOSE(u_inp)

      WRITE(*,*) ">>> [VFIFE] Simulation Completed."
   END SUBROUTINE EXECUTE_VFIFE_SIMULATION

END MODULE VFIFE_MainEntry_module

```
---
# 🔗 參考資料


---