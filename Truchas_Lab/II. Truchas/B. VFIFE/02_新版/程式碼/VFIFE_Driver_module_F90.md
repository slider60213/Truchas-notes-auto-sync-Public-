---
type: 📝 Research
created: 2026-05-27 13:23
modified: 2026-07-31 04:38
tags:
  - "#Truchas"
  - 電腦/WINDOWS/WSL
  - Truchas/VFIFE
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



---
# 📝 內容紀錄

``` fortran
MODULE VFIFE_Driver_module

   USE VFIFE_Input_module,     only: read_data, check_data
   USE VFIFE_Setup_module,     only: V5Setup
   USE VFIFE_Motion_module
   USE VFIFE_FSCoupled_module

   ! Basic Modules of VFIFE
   USE VFIFE_Data_module
   USE VFIFE_Utils_module


   ! Truchas
   use mesh_module,            only: Cell
   use parameter_module,       only: ncells, nfc, ndim
   use output_module,          only: getlun, freelun, input_file
   use time_step_module,       only: cycle_number, t2




   IMPLICIT NONE

   PRIVATE
   PUBLIC :: V5_Initialize
   PUBLIC :: EXECUTE_V5_SIMULATION



CONTAINS

   ! =========================================================
   ! VFIFE 初始化: 讀取輸入資料與檢查、計算幾何、質量與表面判定
   ! =========================================================
   SUBROUTINE V5_Initialize()
      IMPLICIT NONE

      WRITE(*,*) ">>> [VFIFE] Starting Simulation Workflow..."
      IF (.NOT. is_V5_initialized) THEN

         ! 衍生 .V5 檔名
         V5_dat_name = input_file(1:LEN_TRIM(input_file)-4) // '.V5'
         WRITE(*,*) " [V5] V5 Solid logic will read from: ", TRIM(V5_dat_name)

         ! 讀取輸入資料與檢查
         CALL read_data(V5_dat_name)
         WRITE(*,*) ' [V5] read_data finish'

         CALL check_data()
         WRITE(*,*) ' [V5] check_data finish'

         ! 指針容器初始化
         ! 未來 SOUBROUTINE 調用變數就不用逐一引入
         ! 而是可直接傳入 Nodes, Elements 來作為INPUT
         call Link_VFIFE_Containers()
         WRITE(*,*) " [V5] VFIFE_containers init finish"

         ! 剛體模式：不會變形，靜態初始化質量、面判定與 AABB 包夾盒 (只需算一次)
         IF (.NOT. is_V5_deformable) THEN
            ! 計算幾何、質量與表面判定
            CALL V5Setup()
            WRITE(*,*) ' [V5] (Rigid)V5Setup finish at V5_time:', V5_time
         END IF

         ! 計算 V5solid_vof_t0 當作初始值
         ! Check allocated or not
         WRITE(*,*) ' [V5] Checking V5solid_vof allocation state...'
         IF (.NOT. ALLOCATED(V5solid_vof_t0)) THEN
            WRITE(*,*) ' [V5] Allocating V5solid_vof_t0 memory...'
            ALLOCATE(V5solid_vof_t0(ncells))
            V5solid_vof_t0 = 0.0_real_kind
         END IF

         CALL compute_V5solid_vof(V5solid_vof_t0)
         CALL Update_Fluid_Solid_VOF(V5solid_vof_t0)
         WRITE(*,*) " [V5] compute and update V5solid_vof_t0 finish"

         ! 驗證程式碼：計算 VOF 換算體積與 VFIFE 精確體積的比對
         BLOCK
            REAL(real_kind) :: vof_cell_vol, total_vof_vol
            vof_cell_vol = 0.05_real_kind * 0.05_real_kind * 0.05_real_kind
            total_vof_vol = SUM(V5solid_vof_t0) * vof_cell_vol

            WRITE(*,*) "=========================================="
            WRITE(*,*) " [V5 VOF Volume Verification]"
            WRITE(*,*) "  Sum of VOF Ratio (Sum VOF) :", SUM(V5solid_vof_t0)
            WRITE(*,*) "  Single Cell Volume (dV)    :", vof_cell_vol
            WRITE(*,*) "  Calculated VOF Volume      :", total_vof_vol
            WRITE(*,*) "  VFIFE Exact Solid Volume   :", sum(elem_vol)
            WRITE(*,*) "  Volume Error Ratio (%)     :", (total_vof_vol - sum(elem_vol)) / sum(elem_vol) * 100.0_real_kind
            WRITE(*,*) "=========================================="
         END BLOCK

         ! 標記初始化完成
         is_V5_initialized = .TRUE.
      END IF
   END SUBROUTINE


   ! ==================================================================
   ! VFIFE 主控制工作流
   ! ==================================================================
   SUBROUTINE EXECUTE_V5_SIMULATION()

      IMPLICIT NONE
      INTEGER               :: step_count = 0
      REAL(8), SAVE         :: V5_DeltaT=0.0d0

      if (cycle_number > 1 .and. is_V5_initialized) then


         ! 在達到流體新時間步 t2 之前，持續迭代進行計算
         step_count = 0  ! 請確認開頭宣告統一使用 step_count


         ! 在達到流體新時間步 t2 ���前，持續迭代進行計算 (動態微調最後一步 dt)
         DO WHILE (V5_time < t2 - 1.0e-12_real_kind)

            ! 0. 動態微調固體計算的 dt，防止最後一步 dt 過大
            V5_DeltaT = MIN(V5_dt, t2 - V5_time)
            V5_time    = V5_time + V5_DeltaT
            step_count = step_count + 1

            ! 1. 彈性體：會變形，每個時間步皆需更新幾何與 AABB 包夾盒
            IF (is_V5_deformable) THEN
               CALL V5Setup()
               WRITE(*,*) ' [V5] (Deformable) V5Setup finish at V5_time:', V5_time
            END IF



            ! 3. 獲取流體壓力 (映射至固體節點 Nodes%fsum)
            CALL Get_Fluid_Info()
            WRITE(*,*) ' [V5] Get_Fluid_Info finish at V5_time:', V5_time


            ! 4. 彙整外力 (重力、流體耦合力等)
            CALL calculate_external_forces()

            ! 5. 計算單元內力與阻尼力
            CALL calculate_internal_forces()

            ! 6. 顯式時間積分，更新運動學變數 (加速度、速度、位移、座標)
            CALL update_kinematics(V5_DeltaT)

            ! 7. 模組執行完成驗證訊息
            WRITE(*, '(A, F10.6, A)') '[VFIFE_MOTION] V5 executed successfully for dt = ', V5_DeltaT, ' s'
            WRITE(*, '(A, 3F12.6)')   '[VFIFE_VERIFY] Current CoM Pos (m)  : ', Rigid_CoM
            WRITE(*, '(A, 3F12.6)')   '[VFIFE_VERIFY] Current CoM Vel (m/s): ', Rigid_vel
            WRITE(*, '(A, F12.8)')    '[VFIFE_VERIFY] Quaternion Norm     : ', SQRT(SUM(Rigid_quat**2))

         END DO


         WRITE(*,*) ' [V5] V5_time:', V5_time, 'fluid time:',t2
         WRITE(*,*) ' [V5] V5 catch up to fluid time step'
         WRITE(*,*) ' [V5] Start Fluid-Solid coupling:'

         ! 將固體的VOF與速度投影到流體網格���為流固資訊對接����準備
         CALL update_fluid_mapping()
         WRITE(*,*) ' [V5] update_fluid_mapping finish'

         ! 依照最新 VOF 與固體速度，將速度反饋給流���
         CALL V5Solid_Feedback()
         WRITE(*,*) ' [V5] V5Solid_Feedback finish'

      end if
      ! DEALLOCATE


      WRITE(*,*) " [V5] Simulation Completed"

   END SUBROUTINE EXECUTE_V5_SIMULATION


END MODULE VFIFE_Driver_module




```
---
# 🔗 參考資料


---