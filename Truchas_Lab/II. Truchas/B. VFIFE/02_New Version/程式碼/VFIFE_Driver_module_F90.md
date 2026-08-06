---
type: 📝 Research
created: 2026-05-27 13:23
modified: 2026-08-06 03:48
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
[SOLID_module_F90](../../01_Old%20Version/程式碼/SOLID_module_F90.md)
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
   USE VFIFE_Parallel_module


   ! Truchas
   use mesh_module,            only: Cell
   use parameter_module,       only: ncells, nfc, ndim
   use output_module,          only: getlun, freelun, input_file
   use time_step_module,       only: cycle_number, t2, dt
   ! Parallel
   use parallel_info_module,   only: p_info
   use pgslib_module,          only: PGSLib_GLOBAL_SUM





   IMPLICIT NONE

   PUBLIC :: V5_Initialize
   PUBLIC :: EXECUTE_V5_SIMULATION

   PRIVATE :: compute_v5_cfl_dt

CONTAINS

   ! =========================================================
   ! VFIFE 初始化: 讀取輸入資料與檢查、計算幾何、質量與表面判定
   ! =========================================================
   SUBROUTINE V5_Initialize()
      USE timing_module, ONLY: TIMER_START, TIMER_STOP, &
         TIMER_V5_INIT, TIMER_V5_INIT_COMM, TIMER_V5_INIT_MAP
      IMPLICIT NONE

      IF (p_info%IOP) WRITE(*,*) ">>> [V5] Starting Simulation Workflow..."

      ! 檢查是否已經初始化
      IF (.NOT. is_V5_initialized) THEN

         ! 開始記錄 V5 總初始化時間
         CALL TIMER_START(TIMER_V5_INIT)

         ! 衍生 .V5 檔名
         V5_dat_name = input_file(1:LEN_TRIM(input_file)-4) // '.V5'
         !WRITE(*,*) " [V5_Initialize] V5 Solid logic will read from: ", TRIM(V5_dat_name)

         ! 讀取輸入資料與檢查
         CALL read_data(V5_dat_name)
         !WRITE(*,*) ' [V5_Initialize] read_data finish'

         !CALL check_data()
         !WRITE(*,*) ' [V5_Initialize] check_data finish'

         ! ===== [位置：在 CALL read_data(V5_dat_name) 之後] =====

         ! --- 動態計算與調整 OpenMP 線程數 ---
         ! --- 動態計算與調整 OpenMP 線程數 ---
         BLOCK
            INTEGER, EXTERNAL :: omp_get_max_threads
            INTEGER :: max_env_threads, calc_threads
            INTEGER, PARAMETER :: min_nel_per_thread = 1000

            max_env_threads = omp_get_max_threads()

            IF (nel < min_nel_per_thread) THEN
               calc_threads = 1
            ELSE
               calc_threads = nel / min_nel_per_thread
               IF (calc_threads > max_env_threads) calc_threads = max_env_threads
            END IF

            CALL omp_set_num_threads(calc_threads)

            IF (p_info%IOP) THEN
               WRITE(*, '(A,I0,A,I0,A,I0)') " [OpenMP Dynamic Tuning] nel = ", nel, &
                  " | Max Env Threads = ", max_env_threads, &
                  " -> Set Active Threads = ", calc_threads
               FLUSH(6)
            END IF
         END BLOCK

         ! ===================================================


         ! 指針容器初始化
         ! 未來 SOUBROUTINE 調用變數就不用逐一引入
         ! 而是可直接傳入 Nodes, Elements 來作為INPUT
         call Link_VFIFE_Containers()
         !WRITE(*,*) " [V5_Initialize] VFIFE_containers init finish"

         ! ------------------------------------------------------------------
         ! 【新增】建立 PGSLib 跨 CPU 邊界通訊地圖 (V5_Trace)
         ! 必須在 read_data 載入 nel, nnd, rnode 之後立刻執行
         ! ------------------------------------------------------------------
         CALL TIMER_START(TIMER_V5_INIT_COMM)
         CALL V5_Setup_Communication(nel, nnd, rnode)
         CALL TIMER_STOP(TIMER_V5_INIT_COMM)
         IF (p_info%IOP) WRITE(*,*) " [V5_Initialize] V5_Setup_Communication finish"


         ! 靜態初始化質量、面判定與 AABB 包夾盒 (只需算一次)
         ! 計算幾何、質量與表面判定
         CALL V5Setup()
         !WRITE(*,*) ' [V5_Initialize] V5Setup finish at cycle:', cycle_number


         ! ------------------------------------------------------------------
         ! 直接呼叫 update_fluid_mapping：
         ! 內部�������自動完成 compute_solid_aabb, build_surface_cache,
         ! compute_V5solid_vof, Update_Fluid_Solid_VOF 以及速度插值
         ! ------------------------------------------------------------------
         CALL TIMER_START(TIMER_V5_INIT_MAP)
         CALL update_fluid_mapping()
         !WRITE(*,*) " [V5_Initialize] update_fluid_mapping finish"

         ! 驗證程式碼：計算 VOF 換算體積與 VFIFE 精確體積的比對 (平行全域加總版)
         BLOCK
            REAL(real_kind) :: vof_cell_vol, total_vof_vol
            REAL(real_kind) :: local_vof_sum, global_vof_sum
            REAL(real_kind) :: local_elem_vol, global_elem_vol

            ! 1. 計算 CPU 本地的局部累加量
            vof_cell_vol   = 0.05_real_kind * 0.05_real_kind * 0.05_real_kind
            local_vof_sum  = SUM(V5solid_vof)
            local_elem_vol = SUM(elem_vol)

            ! 2. 透過 PGSLib 進行跨 CPU 全域加總
            ! 修正後的全域加總邏輯
            IF (p_info%IsParallel) THEN
               ! PGSLib_GLOBAL_SUM 是函數，直接回傳所有 CPU 加總後的結果
               global_vof_sum  = PGSLib_GLOBAL_SUM(local_vof_sum)
               global_elem_vol = PGSLib_GLOBAL_SUM(local_elem_vol)
            ELSE
               global_vof_sum  = local_vof_sum
               global_elem_vol = local_elem_vol
            END IF

            total_vof_vol = global_vof_sum * vof_cell_vol

            ! 3. 僅由主 CPU (Rank 0) 印出全域驗證結果
            IF (p_info%IOP) THEN
               WRITE(*,*) "=========================================="
               WRITE(*,*) " [V5_Initialize] VOF Volume Verification"
               WRITE(*,*) "   Sum of VOF Ratio (Sum VOF) :", global_vof_sum
               WRITE(*,*) "   Single Cell Volume (dV)    :", vof_cell_vol
               WRITE(*,*) "   Calculated VOF Volume      :", total_vof_vol
               WRITE(*,*) "   VFIFE Exact Solid Volume   :", global_elem_vol
               WRITE(*,*) "   Volume Error Ratio (%)     :", (total_vof_vol - global_elem_vol) / global_elem_vol * 100.0_real_kind
               WRITE(*,*) "=========================================="

               WRITE(*,*) "=========================================="
               WRITE(*,*) " [V5_Initialize] Coord Verification"
               WRITE(*,*) "   Node 1 Coord (initial)     :", Nodes%xc(:, 1)
               WRITE(*,*) "   Time                       :", V5_time
               WRITE(*,*) "=========================================="
            END IF
         END BLOCK
         CALL TIMER_STOP(TIMER_V5_INIT_MAP)

         V5solid_vof_t0 = V5solid_vof  ! 儲存初始 VOF 以便後續比對

         ! 結束記錄 V5 總初始化時間
         CALL TIMER_STOP(TIMER_V5_INIT)

         ! 標記初始化完成
         is_V5_initialized = .TRUE.
         IF (p_info%IOP) THEN
            WRITE(*,*) " [V5_Initialize] is_V5_initialized =", is_V5_initialized
         END IF
      END IF


   END SUBROUTINE V5_Initialize


   ! ==================================================================
   ! VFIFE 主控制工作流
   ! ==================================================================
   SUBROUTINE EXECUTE_V5_SIMULATION()

      USE timing_module, ONLY: TIMER_START, TIMER_STOP, &
         TIMER_V5_EXECUTE, TIMER_V5_SETUP, TIMER_V5_GET_FLUID, &
         TIMER_V5_EXT_FORCE, TIMER_V5_INT_FORCE, TIMER_V5_KINEMATICS, &
         TIMER_V5_MAPPING

      IMPLICIT NONE

      REAL(8), SAVE         :: V5_DeltaT=0.0d0
      REAL(8)               :: dt_fluid, dt_physics
      INTEGER               :: step_count = 0
      INTEGER               :: n_sub_steps

      if (cycle_number >= 1 .and. is_V5_initialized) then

         ! 開始記錄 V5 總模擬執行時間
         CALL TIMER_START(TIMER_V5_EXECUTE)

         ! 初始化子循環計數器與流體步長
         step_count = 0
         dt_fluid   = dt

         ! 如果使用者有設定自訂 dt，優先使用者設定的 V5_User_dt
         ! 否則，動態計算 CFL 臨界步長，並將流體步�� dt_fluid 均分給固體子循環
         IF (V5_User_dt > 0.0d0) then
            V5_User_dt = V5_User_dt
         else
            ! 在進入子循環前更新當前的物理 CFL 臨界步長
            dt_physics = 0.0d0
            CALL compute_v5_cfl_dt(dt_physics)

            ! 動態計算所需的最小子步數 N_sub_steps (無條件進位，且最少 1 步)
            !    確保每一小步都滿足 CFL 條件 <= dt_physics
            IF (dt_physics > 1.0e-12_real_kind) THEN
               n_sub_steps = MAX(1, CEILING(dt_fluid / dt_physics))
            ELSE
               n_sub_steps = 1
            END IF

            ! 將流體時間步長均勻等分給固體子循環
            V5_User_dt = dt_fluid / REAL(n_sub_steps, 8)
         endif

         ! 在達到流體當前時間步 t2 前，迭代進行計算 (動態微調最後一步 dt)
         DO WHILE (V5_time < t2 - 1.0e-12_real_kind)

            ! 0. 動態微調固體計算的 dt，防止最後一步 dt 過大
            V5_DeltaT = MIN(V5_User_dt, t2 - V5_time)
            V5_time    = V5_time + V5_DeltaT
            step_count = step_count + 1

            ! 判斷是否為整個模擬的第一個 Sub-step (用於蛙躍法 v^{1/2} 啟動)
            is_first_step = (cycle_number == 1 .AND. step_count == 1)

            ! =========================================================
            ! [驗證程式碼] Sub-cycling 時間跨步追逐監控
            ! =========================================================
            !WRITE(*,*) '  [EXECUTE_V5_SIMULATION] Step: ', step_count, &
            !   ' | dt: ', V5_DeltaT, ' | V5_time: ', V5_time, &
            !   ' | Target t2: ', t2, ' | Is First Step: ', is_first_step

            ! 每個時間步皆需更新幾何與 AABB 包夾盒
            ! 剛體模式時可跳過部分計算 face_judgement、compute_body_mass_properties 與 nodemass
            ! 但目前選擇保留作為驗證程式碼，確保 Sub-cycling 時間跨步追逐的正確性
            CALL TIMER_START(TIMER_V5_SETUP)
            CALL V5Setup()
            CALL TIMER_STOP(TIMER_V5_SETUP)
            !WRITE(*,*) ' [EXECUTE_V5_SIMULATION] V5Setup finish at V5_time:', V5_time


            Nodes%force = 0.0d0
            Nodes%fsum = 0.0d0

            ! 3. 獲取流體壓力 (映射至固體節點 Nodes%fsum)
            CALL TIMER_START(TIMER_V5_GET_FLUID)
            CALL Get_Fluid_Info()
            CALL TIMER_STOP(TIMER_V5_GET_FLUID)
            !WRITE(*,*) ' [EXECUTE_V5_SIMULATION] Get_Fluid_Info finish at V5_time:', V5_time


            ! 4. 彙整外力 (重力、流體耦合力等)
            CALL TIMER_START(TIMER_V5_EXT_FORCE)
            CALL calculate_external_forces()
            CALL TIMER_STOP(TIMER_V5_EXT_FORCE)

            ! 5. 計算單元內力與阻尼力
            CALL TIMER_START(TIMER_V5_INT_FORCE)
            CALL calculate_internal_forces()
            CALL TIMER_STOP(TIMER_V5_INT_FORCE)

            ! 6. 顯式時間積分，更新運動學變數 (加速度、速度、位移、座標)
            ! 6. 顯式時間積分 (修正點 2: 傳入 is_first_step 進行蛙躍法半步啟動)
            CALL TIMER_START(TIMER_V5_KINEMATICS)
            CALL update_kinematics(V5_DeltaT, is_first_step)
            CALL TIMER_STOP(TIMER_V5_KINEMATICS)

            ! 7. 模組執行完成驗證訊息
            ! WRITE(*,*) '[EXECUTE_V5_SIMULATION] V5 executed successfully for dt = ', V5_DeltaT, ' s'
            ! WRITE(*,*) '[EXECUTE_V5_SIMULATION] Current CoM Pos (m)  : ', V5_Rigid_CoM
            ! WRITE(*,*) '[EXECUTE_V5_SIMULATION] Current CoM Vel (m/s): ', V5_Rigid_vel
            ! WRITE(*,*) "=========================================="
            ! WRITE(*,*) '[EXECUTE_V5_SIMULATION] Quaternion Norm     : ', SQRT(SUM(V5_Rigid_quat**2))
            ! WRITE(*,*) "=========================================="
            ! WRITE(*,*) " [EXECUTE_V5_SIMULATION] Coord Verification]"
            ! WRITE(*,*) "  Node 1 Coord (initial)     :", Nodes%xc(:, 1)
            ! WRITE(*,*) "  Time                       :", V5_time
            ! WRITE(*,*) "=========================================="

         END DO

         ! 將固體的VOF與速度投影到流體網格為流固資訊對接準備
         CALL TIMER_START(TIMER_V5_MAPPING)
         CALL update_fluid_mapping()

         ! 依照最新 VOF 與固體速度，將速度反饋給流體
         CALL V5Solid_Feedback()
         CALL TIMER_STOP(TIMER_V5_MAPPING)
         !WRITE(*,*) ' [EXECUTE_V5_SIMULATION] V5Solid_Feedback finish'

         ! 結束記錄 V5 總模擬執行時間
         CALL TIMER_STOP(TIMER_V5_EXECUTE)

      end if
      ! DEALLOCATE

      ! =========================================================
      ! [驗證程式碼] 固體時間步完全追上流體時間步 (Alignment Complete)
      ! =========================================================
      WRITE(*,*) "=========================================="
      WRITE(*,*) &
         ' [EXECUTE_V5_SIMULATION] Total Sub-steps: ', step_count, &
         ' | Final V5_time: ', V5_time, &
         ' | Target Fluid t2: ', t2

      WRITE(*,*) '--------------------------------------------------'

      WRITE(*,*) '[EXECUTE_V5_SIMULATION] Current CoM Pos (m)  : ', V5_Rigid_CoM
      WRITE(*,*) '[EXECUTE_V5_SIMULATION] Current CoM Vel (m/s): ', V5_Rigid_vel
      WRITE(*,*) " [EXECUTE_V5_SIMULATION] Coord Verification]"
      WRITE(*,*) "  Node 1 Coord (initial)     :", Nodes%xc(:, 1)
      WRITE(*,*) "=========================================="

      WRITE(*,*) " [EXECUTE_V5_SIMULATION] Simulation Completed"

   END SUBROUTINE EXECUTE_V5_SIMULATION



   SUBROUTINE compute_v5_cfl_dt(dt_cfl)
      !============================================================================
      ! SUBROUTINE: compute_v5_cfl_dt
      !
      ! [物理原理說明]
      ! 本副程式依據 Courant-Friedrichs-Lewy (CFL) 穩定性條件，評估 3D 四面體網格
      ! 在顯式時間積分 (Explicit Time Integration) 下的臨界時間步長 (dt_cfl)。
      !
      ! 1. 縱波聲速 (P-wave Speed, Cs):
      !    Cs = sqrt( (E * (1 - v)) / (rho * (1 + v) * (1 - 2*v)) )
      !    彈性體中應力波傳遞速度最快者為縱波 (P-wave)，代表資訊傳播的極限物理速度。
      !
      ! 2. 四面體特徵長度 (Characteristic Length, h_elem):
      !    h_elem = 3 * Volume / Max_Face_Area
      !    取四面體單元之最小幾何高度，代表應力波穿過該單元的最短距離。
      !
      ! 3. 臨界時間步長 (dt_cfl):
      !    dt_elem = safety_factor * (h_elem / Cs)
      !    取全網格單元之最小值 MIN(dt_elem)。確保數值傳播速度不超過物理波速，
      !    防止顯式動力學 (如 VFIFE) 產生數值發散與非物理震盪。
      !============================================================================
      IMPLICIT NONE
      REAL(8), INTENT(OUT) :: dt_cfl

      INTEGER :: i, mat_id
      REAL(8) :: E_mod, nu_val, rho_val, Cs
      REAL(8) :: max_f_area, h_elem, dt_elem
      REAL(8) :: safety_factor

      safety_factor = 0.8d0 ! 顯式積分安全係數 (建議取 0.8 ~ 0.9)
      dt_cfl = 1.0d30       ! 初始化為極大值

      !$OMP PARALLEL DO PRIVATE(i, mat_id, E_mod, nu_val, rho_val, Cs, max_f_area, h_elem, dt_elem) &
      !$OMP SHARED(nel, Elements, e, safety_factor) &
      !$OMP REDUCTION(min:dt_cfl)
      DO i = 1, nel
         ! 1. 依據 elem_mat(1, i) 取得材料 ID 與對應參數
         mat_id  = Elements%mat(1, i)
         rho_val = e(3, mat_id) ! 密度 Density
         E_mod   = e(4, mat_id) ! 彈性模數 Young's Modulus (Pa)
         nu_val  = e(5, mat_id) ! 泊松比 Poisson's Ratio

         ! 2. 計算縱波 (P-wave) 聲速 Cs
         IF (E_mod <= 0.0d0 .OR. rho_val <= 0.0d0) THEN
            ! 剛度或密度為零時防呆（例如剛性體或無抗拉材料），給予極大聲速避免 dt 被拉長，或跳過
            Cs = 0.0d0
         ELSE IF (nu_val >= 0.5d0 .OR. nu_val < 0.0d0) THEN
            ! 防呆：不可壓縮或異常泊松���
            Cs = SQRT(E_mod / rho_val)
         ELSE
            Cs = SQRT((E_mod * (1.0d0 - nu_val)) / &
               (rho_val * (1.0d0 + nu_val) * (1.0d0 - 2.0d0 * nu_val)))
         END IF

         ! 3. 取 4 個面的最大面積，計算四面體最小特徵高度 h = 3 * Vol / A_max
         max_f_area = MAXVAL(Elements%area(:, i))
         IF (max_f_area > 1.0e-12_real_kind) THEN
            h_elem = (3.0d0 * Elements%vol(i)) / max_f_area
         ELSE
            h_elem = 0.0d0
         END IF

         ! 4. 單元���界時間步長評估
         IF (Cs > 1.0e-12_real_kind .AND. h_elem > 0.0d0) THEN
            dt_elem = safety_factor * (h_elem / Cs)
            IF (dt_elem < dt_cfl) dt_cfl = dt_elem
         END IF
      END DO
      !$OMP END PARALLEL DO

      WRITE(*, '(A, ES15.7)') " [V5 CFL Check] Calculated Critical Time Step (dt_cfl): ", dt_cfl

   END SUBROUTINE compute_v5_cfl_dt

END MODULE VFIFE_Driver_module



```
---
# 🔗 參考資料


---