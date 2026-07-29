---
type: 📝 Research
created: 2026-05-27 13:25
modified: 2026-07-30 03:22
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


---
# 👨‍💻 以後


---
# 📝 內容紀錄

``` fortran
MODULE VFIFE_Utils_module

   !Truchas
   USE kind_module,      ONLY: int_kind, real_kind, log_kind
   USE parameter_module, ONLY: Nx_tot, nmat, ncells
   USE mesh_gen_module,  ONLY: x_axis, y_axis, z_axis, MAKE_LOCAL
   use matl_utilities,   ONLY: Update_matl






   ! Basic Modules of VFIFE
   USE VFIFE_Data_module

   IMPLICIT NONE

   ! �u���}����u��A�O���������b
   PRIVATE

   PUBLIC :: GET_VALUE_AFTER_COLON
   PUBLIC :: compute_triangle_solid_angle
   PUBLIC :: is_point_inside_solid
   PUBLIC :: find_cell_index
   PUBLIC :: compute_solid_aabb
   PUBLIC :: build_surface_cache






CONTAINS


   !=======================================================================
   ! Function : GET_VALUE_AFTER_COLON
   ! Purpose  : 解析文字行，自動尋找冒號 (:) 的位置，並讀取冒號後方的雙精度浮點數值。
   !            常用於讀取 key: value 格式的純文字參數設定檔。
   !
   ! [呼叫方式]
   !   param_val = GET_VALUE_AFTER_COLON(line_str)
   !
   ! [輸入參數]
   !   line (CHARACTER(LEN=*), INTENT(IN)) : 包含設定項名稱與數值的文字行字串。
   !
   ! [傳回值]
   !   val (REAL(8))                       : 解析出的雙精度數值。
   !                                         若無冒號或解析失敗，預設傳回 0.0d0。
   !
   ! [使用範例 (讀取參數檔)]
   !   CHARACTER(LEN=256) :: line
   !   REAL(8)            :: dt, youngs_modulus
   !   INTEGER            :: io_unit, ios
   !
   !   OPEN(NEWUNIT=io_unit, FILE='input_parameters.txt', STATUS='OLD')
   !
   !   DO
   !      READ(io_unit, '(A)', IOSTAT=ios) line
   !      IF (ios /= 0) EXIT
   !
   !      !例如 "Time Step: 1.0e-3" -> dt = 0.001d0
   !      !例如 "Young's Modulus: 2.1e11" -> youngs_modulus = 2.1d11
   !
   !      IF (INDEX(line, "Time Step:") > 0) THEN
   !         dt = GET_VALUE_AFTER_COLON(line)
   !      ELSE IF (INDEX(line, "Young's Modulus:") > 0) THEN
   !         youngs_modulus = GET_VALUE_AFTER_COLON(line)
   !      END IF
   !   END DO
   !
   !   CLOSE(io_unit)
   !=======================================================================
   FUNCTION GET_VALUE_AFTER_COLON(line) RESULT(val)
      CHARACTER(LEN=*), INTENT(IN) :: line
      REAL(8) :: val
      INTEGER :: pos, ios
      val = 0.0d0
      pos = INDEX(line, ":")
      IF (pos > 0) THEN
         READ(line(pos+1:), *, IOSTAT=ios) val
      END IF
   END FUNCTION GET_VALUE_AFTER_COLON


   !=======================================================================
   ! Function : compute_triangle_solid_angle
   ! Purpose  : 計算一個 3D 三角形相對於觀察點 (原點) 所張開的帶符號立體角 (Solid Angle)。
   !            採用 Oosterom & Strackee (1983) 數值穩定公式。
   !
   ! [呼叫方式]
   !   omega = compute_triangle_solid_angle(a, b, c)
   !
   ! [輸入參數]
   !   a(3), b(3), c(3) : REAL(real_kind), INTENT(IN)
   !                      從觀察點 p 指向三角形三個頂點 (v1, v2, v3) 的相對位置向量。
   !                      即 a = v1 - p, b = v2 - p, c = v3 - p。
   !
   ! [傳回值]
   !   omega            : REAL(real_kind)
   !                      帶符號之立體角大小，範圍為 [-4*PI, 4*PI]。
   !                      符號由 (a x b) . c 之繞行方向與法向量決定。
   !=======================================================================
   PURE FUNCTION compute_triangle_solid_angle(a, b, c) RESULT(omega)
      IMPLICIT NONE

      ! --- Input Arguments ---
      REAL(real_kind), INTENT(IN) :: a(3), b(3), c(3)

      ! --- Function Result ---
      REAL(real_kind) :: omega

      ! --- Local Variables ---
      REAL(real_kind) :: la, lb, lc
      REAL(real_kind) :: det_abc, denom
      REAL(real_kind) :: dot_ab, dot_bc, dot_ca
      REAL(real_kind), PARAMETER :: EPSILON = 1.0e-12_real_kind

      la = SQRT(a(1)*a(1) + a(2)*a(2) + a(3)*a(3))
      lb = SQRT(b(1)*b(1) + b(2)*b(2) + b(3)*b(3))
      lc = SQRT(c(1)*c(1) + c(2)*c(2) + c(3)*c(3))

      IF (la < EPSILON .OR. lb < EPSILON .OR. lc < EPSILON) THEN
         omega = 0.0_real_kind
         RETURN
      END IF

      det_abc = a(1)*(b(2)*c(3) - b(3)*c(2)) - &
         a(2)*(b(1)*c(3) - b(3)*c(1)) + &
         a(3)*(b(1)*c(2) - b(2)*c(1))

      dot_ab = a(1)*b(1) + a(2)*b(2) + a(3)*b(3)
      dot_bc = b(1)*c(1) + b(2)*c(2) + b(3)*c(3)
      dot_ca = c(1)*a(1) + c(2)*a(2) + c(3)*a(3)

      denom = la*lb*lc + dot_ab*lc + dot_bc*la + dot_ca*lb

      omega = 2.0_real_kind * ATAN2(det_abc, denom)

   END FUNCTION compute_triangle_solid_angle





   !=======================================================================
   ! Function : is_point_inside_solid
   ! Purpose  : 使用廣義繞數法 (Generalized Winding Number / 邊界面立體角積分)
   !            判定任意 3D 空間點 p_pt 是否位於封閉固體內部。
   !
   ! [前置條件]
   !   呼叫前必須確保已被 build_surface_cache() 建立 (或更新) 邊界面快取。
   !
   ! [呼叫方式]
   !   inside_flag = is_point_inside_solid(p_pt)
   !
   ! [輸入參數]
   !   p_pt(3)     : REAL(real_kind), INTENT(IN)
   !                 欲判定的 3D 空間點座標 (x, y, z)。
   !
   ! [傳回值]
   !   is_inside   : LOGICAL
   !                 .TRUE.  -> 該點地位於固體內部
   !                 .FALSE. -> 該點地位於固體外部
   !
   ! [使用範例 (流體網格體積率 VOF / Sub-grid 採樣)]
   !   CALL build_surface_cache()  ! 先建立/更新快取
   !
   !   ! 對第 icell 個流體網格中的微採樣點進行判定
   !   sub_pt = (/ x_sub, y_sub, z_sub /)
   !   IF (is_point_inside_solid(sub_pt)) THEN
   !      solid_count = solid_count + 1
   !   END IF
   !=======================================================================
   PURE FUNCTION is_point_inside_solid(p_pt) RESULT(is_inside)

      IMPLICIT NONE

      ! --- Input Arguments ---
      REAL(real_kind), INTENT(IN) :: p_pt(3)

      ! --- Function Result ---
      LOGICAL :: is_inside

      ! --- Local Variables ---
      INTEGER(int_kind) :: f
      REAL(real_kind)   :: total_solid_angle, omega
      REAL(real_kind)   :: pa(3), pb(3), pc(3)
      REAL(real_kind), PARAMETER :: PI = 3.14159265358979323846_real_kind
      REAL(real_kind), PARAMETER :: FOUR_PI = 4.0_real_kind * PI

      IF (num_surf_faces == 0) THEN
         is_inside = .FALSE.
         RETURN
      END IF

      total_solid_angle = 0.0_real_kind

      DO f = 1, num_surf_faces
         pa = surf_node1(:, f) - p_pt
         pb = surf_node2(:, f) - p_pt
         pc = surf_node3(:, f) - p_pt

         omega = compute_triangle_solid_angle(pa, pb, pc)
         total_solid_angle = total_solid_angle + omega
      END DO

      IF (ABS(total_solid_angle) / FOUR_PI >= 0.5_real_kind) THEN
         is_inside = .TRUE.
      ELSE
         is_inside = .FALSE.
      END IF

   END FUNCTION is_point_inside_solid



   !=======================================================================
   ! Function: find_cell_index
   ! Purpose : Locates which fluid cell index a physical coordinate 'val'
   !           falls into along a non-uniform rectilinear axis.
   !
   ! Example (VFIFE Solid-Fluid Mapping):
   !   Given fluid mesh axis: x_axis = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0] (5 cells)
   !   If solid minimum boundary x = 1.2 m:
   !     idx = find_cell_index(1.2_real_kind, x_axis, 5)
   !     --> Returns idx = 2 (Cell 2 covers range [1.0, 2.0])
   !=======================================================================
   INTEGER(int_kind) FUNCTION find_cell_index(val, axis, N) RESULT(idx)
      REAL(real_kind), INTENT(IN) :: val
      REAL(real_kind), INTENT(IN) :: axis(:)
      INTEGER(int_kind), INTENT(IN) :: N
      INTEGER(int_kind) :: low, high, mid

      IF (val <= axis(1)) THEN
         idx = 1
         RETURN
      END IF
      IF (val >= axis(N)) THEN
         idx = N
         RETURN
      END IF

      low = 1
      high = N
      DO WHILE (low <= high)
         mid = (low + high) / 2
         IF (val >= axis(mid) .AND. val < axis(mid+1)) THEN
            idx = mid
            RETURN
         ELSE IF (val < axis(mid)) THEN
            high = mid - 1
         ELSE
            low = mid + 1
         END IF
      END DO
      idx = low
   END FUNCTION find_cell_index

   !=======================================================================
   ! Subroutine: compute_solid_aabb_and_vof
   ! Purpose   : Maps VFIFE solid node bounding box (AABB) to fluid grid range,
   !             and computes solid VOF to update fluidVof array.
   !
   ! Usage Scenario in VFIFE Solver Loop:
   !   1. Compute VFIFE solid node min/max bounds:
   !      solid_x_min = 1.2 m, solid_x_max = 3.8 m
   !   2. Map bounds to fluid cell indices via find_cell_index:
   !      istart = 2, iend = 4
   !   3. Perform sub-voxel sampling only on cells [2..4] to update fluidVof:
   !      fluidVof(icell) = 1.0 - V5solid_vof(icell)
   !=======================================================================
   SUBROUTINE compute_solid_aabb()

      IMPLICIT NONE

      ! ---------------------------------------------------
      ! 局部變數 (Local Variables)
      ! ---------------------------------------------------
      INTEGER :: i, v, count_boundary_faces
      INTEGER :: Nx, Ny, Nz
      INTEGER :: gi, gj, gk, global_id, local_id
      INTEGER :: local_active_count

      Nx = Nx_tot(1)
      Ny = Nx_tot(2)
      Nz = Nx_tot(3)

      ! 1. 安全性檢查
      IF (.NOT. ALLOCATED(face_judge) .OR. .NOT. ALLOCATED(elem_vertices)) THEN
         WRITE(*,*) "Fatal: [compute_solid_aabb] Required arrays are not allocated."
         STOP
      END IF

      ! 2. 初始化 AABB 極值
      V5_minX =  1.0d30
      V5_maxX = -1.0d30
      count_boundary_faces = COUNT(face_judge == 1)

      ! 安全性防護：若完全無外露面，避免後續反��崩潰
      IF (count_boundary_faces == 0) THEN
         WRITE(*,*) "Warning: [compute_solid_aabb] No boundary faces (face_judge == 1) found."
         V5_minX = 0.0d0; V5_maxX = 0.0d0
         V5_fluid_istart = 1; V5_fluid_iend = 1
         V5_fluid_jstart = 1; V5_fluid_jend = 1
         V5_fluid_kstart = 1; V5_fluid_kend = 1
         RETURN
      END IF

      ! 3. 遍歷所有單元：以 elem_vertices 快速更新 AABB 包夾盒
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, v) &
      !$OMP SHARED(nel, face_judge, elem_vertices) &
      !$OMP REDUCTION(min: V5_minX) REDUCTION(max: V5_maxX)
      DO i = 1, nel
         IF (ANY(face_judge(:, i) == 1)) THEN
            DO v = 1, 4
               V5_minX = MIN(V5_minX, elem_vertices(:, v, i))
               V5_maxX = MAX(V5_maxX, elem_vertices(:, v, i))
            END DO
         END IF
      END DO
      !$OMP END PARALLEL DO

      ! 4. 利用網格軸陣列定位索引 (加上 1 格 Safety Margin 確保切角邊界涵蓋)
      V5_fluid_istart = MAX(1, find_cell_index(V5_minX(1), x_axis, Nx) - 1)
      V5_fluid_iend   = MIN(Nx, find_cell_index(V5_maxX(1), x_axis, Nx) + 1)

      V5_fluid_jstart = MAX(1, find_cell_index(V5_minX(2), y_axis, Ny) - 1)
      V5_fluid_jend   = MIN(Ny, find_cell_index(V5_maxX(2), y_axis, Ny) + 1)

      V5_fluid_kstart = MAX(1, find_cell_index(V5_minX(3), z_axis, Nz) - 1)
      V5_fluid_kend   = MIN(Nz, find_cell_index(V5_maxX(3), z_axis, Nz) + 1)

      ! 5. 驗證輸出
      WRITE(*,*) "=========================================="
      WRITE(*,*) " [AABB & MAPPING VERIFICATION]"
      WRITE(*,*) "=========================================="
      WRITE(*,*) " Processed Boundary Faces :", count_boundary_faces
      WRITE(*, '(A,3F12.4)') " Solid Bounding Min (X,Y,Z):", V5_minX
      WRITE(*, '(A,3F12.4)') " Solid Bounding Max (X,Y,Z):", V5_maxX
      WRITE(*,*) "------------------------------------------"
      WRITE(*, '(A,2I6)') " Fluid Index Range X [istart:iend]:", V5_fluid_istart, V5_fluid_iend
      WRITE(*, '(A,2I6)') " Fluid Index Range Y [jstart:jend]:", V5_fluid_jstart, V5_fluid_jend
      WRITE(*, '(A,2I6)') " Fluid Index Range Z [kstart:kend]:", V5_fluid_kstart, V5_fluid_kend
      WRITE(*, '(A,I10)') " Target Active Grid Cells         :", &
         (V5_fluid_iend - V5_fluid_istart + 1) * &
         (V5_fluid_jend - V5_fluid_jstart + 1) * &
         (V5_fluid_kend - V5_fluid_kstart + 1)
      WRITE(*,*) "=========================================="

      ! 6. 收集與標記受影響的本地一維網格 (Global to Local Mapping)
      IF (.NOT. ALLOCATED(V5_ingbr)) ALLOCATE(V5_ingbr(ncells))
      V5_ingbr = 0
      local_active_count = 0

      DO gk = V5_fluid_kstart, V5_fluid_kend
         DO gj = V5_fluid_jstart, V5_fluid_jend
            DO gi = V5_fluid_istart, V5_fluid_iend

               ! 計算 Truchas 結構化網格全域一維索引 (Row-major / Flat Index)
               global_id = (gk - 1) * Nx * Ny + (gj - 1) * Nx + gi

               ! 關鍵：將全域索引轉換為目前處理器的本地索引
               local_id = MAKE_LOCAL(global_id, ncells)

               ! ! 若網格屬於本處理器，則標記 V5_ingbr 旗標供後續 MSA/det44 篩選使用
               ! IF (local_id /= -1) THEN
               !    V5_ingbr(local_id) = 1
               !    local_active_count = local_active_count + 1

               !    ! 僅印出 i, j, k 三個方向的前 3 格與後 3 格，避免日誌洗版
               !    IF ((gi <= V5_fluid_istart + 1 .OR. gi >= V5_fluid_iend - 1) .AND. &
               !       (gj <= V5_fluid_jstart + 1 .OR. gj >= V5_fluid_jend - 1) .AND. &
               !       (gk <= V5_fluid_kstart + 1 .OR. gk >= V5_fluid_kend - 1)) THEN

               !       WRITE(*, '(A,I8,A,I8,A,3I5,A,2F10.4,A,2F10.4,A,2F10.4)') &
               !          "  [Candidate Cell] Local ID:", local_id, " | Global ID:", global_id, &
               !          " | (i,j,k):", gi, gj, gk, &
               !          " | X:[", x_axis(gi), x_axis(gi+1), &
               !          "] Y:[", y_axis(gj), y_axis(gj+1), &
               !          "] Z:[", z_axis(gk), z_axis(gk+1), "]"
               !    END IF
               ! END IF

            END DO
         END DO
      END DO

      WRITE(*, '(A,I8)') " [AABB Mapping] Total Local Candidate Cells (V5_ingbr=1) :", local_active_count
      WRITE(*,*) "=========================================="

   END SUBROUTINE compute_solid_aabb

   !=======================================================================
   ! Subroutine: build_surface_cache
   ! Purpose   : 掃描 VFIFE 固體網格，將所有位於邊界面 (face_judge == 1) 的
   !             三角形頂點座標抽取至 SoA (Structure of Arrays) 格式快取中。
   !
   ! [使用時機]
   !   1. 模擬初始化階段 (初始化體積率/IBM 採樣前)。
   !   2. 若固體發生幾何大變形、網格更新節點座標後，需重新呼叫以更新快取。
   !
   ! [呼叫方式]
   !   CALL build_surface_cache()
   !
   ! [更新的全域變數 (VFIFE_Data_module)]
   !   - num_surf_faces  : 外露邊界面總數
   !   - surf_node1(3,f) : 第 f 個外露面第一個頂點的三維座標 (x, y, z)
   !   - surf_node2(3,f) : 第 f 個外露面第二個頂點的三維座標 (x, y, z)
   !   - surf_node3(3,f) : 第 f 個外露面第三個頂點的三維座標 (x, y, z)
   !=======================================================================
   SUBROUTINE build_surface_cache()

      IMPLICIT NONE
      INTEGER :: i, j, f_idx

      num_surf_faces = COUNT(face_judge == 1)
      IF (num_surf_faces == 0) RETURN

      IF (ALLOCATED(surf_node1)) DEALLOCATE(surf_node1, surf_node2, surf_node3)
      ALLOCATE(surf_node1(3, num_surf_faces))
      ALLOCATE(surf_node2(3, num_surf_faces))
      ALLOCATE(surf_node3(3, num_surf_faces))

      f_idx = 0
      DO i = 1, nel
         DO j = 1, 4
            IF (face_judge(j, i) == 1) THEN
               f_idx = f_idx + 1
               ! 根據四面體 Local Face 拓樸提取對應 3 頂點 (elem_topo 2:5 對應 N1:N4)
               SELECT CASE (j)
                CASE (1) ! Face 1: (N2, N3, N4) -> elem_topo 欄位 (3, 4, 5)
                  surf_node1(:, f_idx) = x_coord(:, elem_topo(3, i))
                  surf_node2(:, f_idx) = x_coord(:, elem_topo(4, i))
                  surf_node3(:, f_idx) = x_coord(:, elem_topo(5, i))
                CASE (2) ! Face 2: (N1, N4, N3) -> elem_topo �����位 (2, 5, 4)
                  surf_node1(:, f_idx) = x_coord(:, elem_topo(2, i))
                  surf_node2(:, f_idx) = x_coord(:, elem_topo(5, i))
                  surf_node3(:, f_idx) = x_coord(:, elem_topo(4, i))
                CASE (3) ! Face 3: (N1, N2, N4) -> elem_topo 欄�������� (2, 3, 5)
                  surf_node1(:, f_idx) = x_coord(:, elem_topo(2, i))
                  surf_node2(:, f_idx) = x_coord(:, elem_topo(3, i))
                  surf_node3(:, f_idx) = x_coord(:, elem_topo(5, i))
                CASE (4) ! Face 4: (N1, N3, N2) -> elem_topo 欄位 (2, 4, 3)
                  surf_node1(:, f_idx) = x_coord(:, elem_topo(2, i))
                  surf_node2(:, f_idx) = x_coord(:, elem_topo(4, i))
                  surf_node3(:, f_idx) = x_coord(:, elem_topo(3, i))
               END SELECT
            END IF
         END DO
      END DO
   END SUBROUTINE build_surface_cache

END MODULE VFIFE_Utils_module


```
---
# 🔗 參考資料


---