---
type: 📝 Research
created: 2026-07-30 03:10
modified: 2026-08-06 03:49
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

``` fortran
MODULE VFIFE_FSCoupled_module

   ! Basic Modules of VFIFE
   USE VFIFE_Data_module
   USE VFIFE_Utils_module

   ! Truchas
   USE kind_module,           ONLY : int_kind, real_kind
   USE mesh_module,           ONLY : Mesh, Cell
   USE mesh_gen_module,       ONLY : x_axis, y_axis, z_axis, MAKE_LOCAL
   USE parameter_module,      ONLY : ncells, nfc, Nx_tot, nmat
   USE zone_module,           ONLY : Zone
   USE fluid_data_module,     ONLY : fluidVof, fluidRho
   USE matl_module,           ONLY : Matl
   USE matl_utilities,        ONLY : MATL_GET, UPDATE_MATL

   IMPLICIT NONE

   PRIVATE
   PUBLIC :: Get_Fluid_Info
   PUBLIC :: compute_V5solid_vof
   PUBLIC :: Update_Fluid_Solid_VOF
   PUBLIC :: build_fluid_to_solid_mapping
   PUBLIC :: update_fluid_mapping
   PUBLIC :: V5Solid_Feedback




CONTAINS

   !=======================================================================
   ! Subroutine: Get_Fluid_Info
   ! Purpose   : 遍歷固體外露邊界面 (num_surf_faces)，同步採樣流體網格之壓力、
   !             速度與動態流體密度，分別存入 Elements 容器中。
   !=======================================================================
   SUBROUTINE Get_Fluid_Info()

      IMPLICIT NONE

      ! --- 區域變數 ---
      INTEGER(KIND=int_kind) :: i, j, f_idx, k, n, ngbr, counter, ic, jc, kc
      INTEGER(KIND=int_kind) :: n_pts
      INTEGER(KIND=int_kind) :: n_global
      INTEGER                :: V5_NOT_LOCAL_INDEX = -1
      REAL(KIND=real_kind), ALLOCATABLE :: w(:, :) ! 重心座標權重陣列 (3, n_pts)
      REAL(KIND=real_kind)   :: p_sample(3), v1(3), v2(3), v3(3), norm(3)
      REAL(KIND=real_kind)   :: area, P_sum, p_sample_val, P_face
      REAL(KIND=real_kind)   :: V_sum(3), v_sample_val(3), V_face(3)
      REAL(KIND=real_kind)   :: Rho_sum, rho_sample_val, Rho_face
      REAL(KIND=real_kind)   :: t
      REAL(KIND=real_kind)   :: total_force_check(3)
      LOGICAL                :: cell_found

      ! 1. 邊界條件檢查：若無外露面則直接跳過主計算
      IF (num_surf_faces > 0) THEN
         total_force_check = 0.0_real_kind

         ! 防呆與維度初始化
         n_pts = MAX(1, num_p_samples)
         IF (.NOT. ALLOCATED(w)) ALLOCATE(w(3, n_pts))

         ! 通用重心座標權重矩陣建構 w(3, n_pts)
         IF (n_pts == 1) THEN
            w(:, 1) = [1.0_real_kind/3.0_real_kind, 1.0_real_kind/3.0_real_kind, 1.0_real_kind/3.0_real_kind]
         ELSE IF (n_pts == 3) THEN
            w(:, 1) = [1.0_real_kind, 0.0_real_kind, 0.0_real_kind]
            w(:, 2) = [0.0_real_kind, 1.0_real_kind, 0.0_real_kind]
            w(:, 3) = [0.0_real_kind, 0.0_real_kind, 1.0_real_kind]
         ELSE IF (n_pts == 4) THEN
            w(:, 1) = [1.0_real_kind/3.0_real_kind, 1.0_real_kind/3.0_real_kind, 1.0_real_kind/3.0_real_kind]
            w(:, 2) = [1.0_real_kind, 0.0_real_kind, 0.0_real_kind]
            w(:, 3) = [0.0_real_kind, 1.0_real_kind, 0.0_real_kind]
            w(:, 4) = [0.0_real_kind, 0.0_real_kind, 1.0_real_kind]
         ELSE
            w(:, 1) = [1.0_real_kind/3.0_real_kind, 1.0_real_kind/3.0_real_kind, 1.0_real_kind/3.0_real_kind]
            DO k = 2, n_pts
               t = REAL(k - 2, KIND=real_kind) / REAL(n_pts - 2, KIND=real_kind)
               w(1, k) = (1.0_real_kind - t)
               w(2, k) = t * 0.5_real_kind
               w(3, k) = t * 0.5_real_kind
            END DO
         END IF

         ! =========================================================
         ! 主運算迴圈：遍歷外露面
         ! =========================================================
         f_idx = 0
         DO i = 1, nel
            DO j = 1, 4
               IF (face_judge(j, i) /= 1) CYCLE

               f_idx = f_idx + 1

               ! 頂點座標與幾何資訊
               v1 = surf_node1(:, f_idx)
               v2 = surf_node2(:, f_idx)
               v3 = surf_node3(:, f_idx)

               area    = Elements%area(j, i)
               norm(:) = Elements%normal(:, j, i)

               ! 多點採樣：壓力、速度與密度積分
               P_face   = 0.0_real_kind
               V_face   = 0.0_real_kind
               Rho_face = 0.0_real_kind

               DO k = 1, n_pts
                  p_sample(:) = w(1, k)*v1(:) + w(2, k)*v2(:) + w(3, k)*v3(:)

                  ic = find_cell_index(p_sample(1), x_axis, Nx_tot(1))
                  jc = find_cell_index(p_sample(2), y_axis, Nx_tot(2))
                  kc = find_cell_index(p_sample(3), z_axis, Nx_tot(3))

                  cell_found = .FALSE.
                  n = 0

                  ! 在 n (Global ID) 計算之後、存取流體陣列之前執行轉換
                  IF (ic >= V5_fluid_istart .AND. ic <= V5_fluid_iend .AND. &
                     jc >= V5_fluid_jstart .AND. jc <= V5_fluid_jend .AND. &
                     kc >= V5_fluid_kstart .AND. kc <= V5_fluid_kend) THEN

                     n_global = ic + (jc - 1) * Nx_tot(1) + (kc - 1) * Nx_tot(1) * Nx_tot(2)

                     ! 透過 MAKE_LOCAL 將 Global ID 轉換為 Local ID
                     n = MAKE_LOCAL(n_global, ncells)

                     ! 僅當網格屬於當前 Local PE (n /= V5_NOT_LOCAL_INDEX
                     ! 且 1 <= n <= ncells) 時才算找到
                     IF (n /= V5_NOT_LOCAL_INDEX .AND. n > 0 .AND. n <= ncells) THEN
                        cell_found = .TRUE.
                     END IF
                  END IF

                  p_sample_val   = 0.0_real_kind
                  v_sample_val   = 0.0_real_kind
                  rho_sample_val = 0.0_real_kind

                  IF (cell_found .AND. n > 0) THEN
                     counter = 0
                     P_sum   = 0.0_real_kind
                     V_sum   = 0.0_real_kind
                     Rho_sum = 0.0_real_kind

                     IF (fluidVof(n) >= 0.3_real_kind) THEN
                        counter = counter + 1
                        P_sum   = P_sum + Zone(n)%P
                        V_sum   = V_sum + Zone(n)%Vc(:)
                        Rho_sum = Rho_sum + fluidRho(n)
                     ELSE
                        DO ngbr = 1, nfc
                           IF (Mesh(n)%Ngbr_cell(ngbr) > 0) THEN
                              IF (fluidVof(Mesh(n)%Ngbr_cell(ngbr)) >= 0.3_real_kind) THEN
                                 counter = counter + 1
                                 P_sum   = P_sum + Zone(Mesh(n)%Ngbr_cell(ngbr))%P
                                 V_sum   = V_sum + Zone(Mesh(n)%Ngbr_cell(ngbr))%Vc(:)
                                 Rho_sum = Rho_sum + fluidRho(Mesh(n)%Ngbr_cell(ngbr))
                              END IF
                           END IF
                        END DO
                     END IF

                     IF (counter > 0) THEN
                        p_sample_val   = P_sum / REAL(counter, KIND=real_kind)
                        v_sample_val(:) = V_sum(:) / REAL(counter, KIND=real_kind)
                        rho_sample_val = Rho_sum / REAL(counter, KIND=real_kind)
                     ELSE
                        p_sample_val   = Zone(n)%P
                        v_sample_val(:) = Zone(n)%Vc(:)
                        rho_sample_val = fluidRho(n)
                     END IF
                  END IF

                  P_face    = P_face + p_sample_val
                  V_face(:) = V_face(:) + v_sample_val(:)
                  Rho_face  = Rho_face + rho_sample_val
               END DO

               ! 採樣點算術平均
               P_face    = P_face / REAL(n_pts, KIND=real_kind)
               V_face(:) = V_face(:) / REAL(n_pts, KIND=real_kind)
               Rho_face  = Rho_face / REAL(n_pts, KIND=real_kind)

               ! 將採樣完成的物理量儲存至元素容器
               Elements%pressure(j, i)    = P_face
               Elements%velocity(:, j, i) = V_face(:)
               Elements%density(j, i)     = Rho_face

               ! 驗證用：前 2 個面輸出採樣資訊
               ! IF (f_idx <= 2) THEN
               !    WRITE(*,*) &
               !       '    [Get_Fluid_Info] Face: ', f_idx, &
               !       ' | Cell: ', n, ' | P_face: ', P_face, &
               !       ' | V_face: ', V_face(1:3), &
               !       ' | Rho_face: ', Rho_face
               ! END IF

               total_force_check(:) = total_force_check(:) - P_face * area * norm(:)
            END DO
         END DO

         IF (ALLOCATED(w)) DEALLOCATE(w)
      END IF

      ! =========================================================
      ! [驗證程式碼] 檢查 MPI 索引轉換與採樣安全性
      ! =========================================================
      ! IF (num_surf_faces > 0) THEN
      !    WRITE(*,*) '  [Get_Fluid_Info] Total Faces Processed: ', f_idx, &
      !       ' | Sampled Density Range Check: OK (Checked against Local ncells = ', ncells, ')'
      ! END IF
      ! WRITE(*,*) " [Get_Fluid_Info] Total Samples/Face:", n_pts, &
      !    " | Total Face Pressure Force (X,Y,Z):", total_force_check

   END SUBROUTINE Get_Fluid_Info






   !=======================================================================
   ! Purpose: Compute Solid Volume Fraction (Solid VOF) on Rectilinear
   !          Fluid Mesh using Sub-voxel Sampling inside AABB range.
   !=======================================================================
   SUBROUTINE compute_V5solid_vof(V5solid_vof)

      IMPLICIT NONE

      ! --- Argument List ---
      REAL(real_kind), INTENT(OUT) :: V5solid_vof(Nx_tot(1)*Nx_tot(2)*Nx_tot(3))

      ! --- Local Variables ---
      INTEGER(int_kind) :: i, j, k, icell
      INTEGER(int_kind) :: sub_i, sub_j, sub_k
      INTEGER(int_kind), PARAMETER :: Nsub = 5 ! 單軸採樣點數 (Nsub^3 個點)
      REAL(real_kind) :: dx_local, dy_local, dz_local
      REAL(real_kind) :: dx_sub, dy_sub, dz_sub
      REAL(real_kind) :: cell_x_min, cell_y_min, cell_z_min
      REAL(real_kind) :: p_sub(3)
      INTEGER(int_kind) :: inside_count
      REAL(real_kind), PARAMETER :: total_sub_pts = REAL(Nsub * Nsub * Nsub, real_kind)

      ! 1. 全域初始化為 0.0
      V5solid_vof = 0.0_real_kind

      ! 2. 僅在 AABB 包夾盒範圍內做動態 dx, dy, dz 的 VOF 採樣計算
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, j, k, icell, cell_x_min, cell_y_min, cell_z_min) &
      !$OMP PRIVATE(dx_local, dy_local, dz_local, dx_sub, dy_sub, dz_sub) &
      !$OMP PRIVATE(sub_i, sub_j, sub_k, p_sub, inside_count) &
      !$OMP SHARED(V5_fluid_istart, V5_fluid_iend, V5_fluid_jstart, V5_fluid_jend, V5_fluid_kstart, V5_fluid_kend, Nx_tot) &
      !$OMP SHARED(x_axis, y_axis, z_axis, V5solid_vof, Cell)
      DO k = V5_fluid_kstart, V5_fluid_kend
         cell_z_min = z_axis(k)
         dz_local   = z_axis(k+1) - z_axis(k)
         dz_sub     = dz_local / REAL(Nsub, real_kind)

         DO j = V5_fluid_jstart, V5_fluid_jend
            cell_y_min = y_axis(j)
            dy_local   = y_axis(j+1) - y_axis(j)
            dy_sub     = dy_local / REAL(Nsub, real_kind)

            DO i = V5_fluid_istart, V5_fluid_iend
               cell_x_min = x_axis(i)
               dx_local   = x_axis(i+1) - x_axis(i)
               dx_sub     = dx_local / REAL(Nsub, real_kind)

               ! 計算流體 1D Cell Index
               icell = i + (j - 1) * Nx_tot(1) + (k - 1) * Nx_tot(1) * Nx_tot(2)

               inside_count = 0

               ! 子網格 (Sub-voxel) 採樣
               DO sub_k = 1, Nsub
                  p_sub(3) = cell_z_min + (REAL(sub_k, real_kind) - 0.5_real_kind) * dz_sub
                  DO sub_j = 1, Nsub
                     p_sub(2) = cell_y_min + (REAL(sub_j, real_kind) - 0.5_real_kind) * dy_sub
                     DO sub_i = 1, Nsub
                        p_sub(1) = cell_x_min + (REAL(sub_i, real_kind) - 0.5_real_kind) * dx_sub

                        IF (is_point_inside_solid(p_sub)) THEN
                           inside_count = inside_count + 1
                        END IF

                     END DO
                  END DO
               END DO

               V5solid_vof(icell) = REAL(inside_count, real_kind) / total_sub_pts


               !    ! 驗證����式碼：僅印出 i, j, k 三個方向最��間區域 (中心點前��������各 1 格) 的資訊��� VOF 數值
               !    IF (ABS(i - (V5_fluid_istart + V5_fluid_iend)/2) <= 1 .AND. &
               !       ABS(j - (V5_fluid_jstart + V5_fluid_jend)/2) <= 1 .AND. &
               !       ABS(k - (V5_fluid_kstart + V5_fluid_kend)/2) <= 1) THEN

               !       !$OMP CRITICAL(vof_write_lock)
               !       WRITE(*, '(A,I8,A,3I5,A,F8.4,A,3F8.3,A,2F8.3,A,2F8.3,A,2F8.3,A)') &
               !          "  [AABB VOF] Cell ID:", icell, &
               !          " | (i,j,k):", i, j, k, &
               !          " | VOF:", V5solid_vof(icell), &
               !          " | Centroid:(", Cell(icell)%Centroid(1), Cell(icell)%Centroid(2), Cell(icell)%Centroid(3), &
               !          ") | X:[", x_axis(i), x_axis(i+1), &
               !          "] Y:[", y_axis(j), y_axis(j+1), &
               !          "] Z:[", z_axis(k), z_axis(k+1), "]"
               !       !$OMP END CRITICAL(vof_write_lock)

               !    END IF
            END DO
         END DO
      END DO
      !$OMP END PARALLEL DO


      ! --- 逐層 (k 軸) VOF 與體積檢驗區塊 ---
      BLOCK
         INTEGER :: i_chk, j_chk, k_chk, idx_chk
         REAL(KIND=real_kind) :: k_vof_sum, total_vof_sum, dV_local

         total_vof_sum = 0.0_real_kind
         ! WRITE(*,*) "=========================================================================================="
         ! WRITE(*,*) " [compute_V5solid_vof] Z-Layer (k) Breakdown Analysis"
         ! WRITE(*,*) "=========================================================================================="
         ! WRITE(*,*) "k", "Z-Bounds [min, max]", "Sum(VOF)", "Layer Vol (m3)", "Cumulative Vol"
         ! WRITE(*,*) "------------------------------------------------------------------------------------------"

         DO k_chk = V5_fluid_kstart, V5_fluid_kend
            k_vof_sum = 0.0_real_kind
            DO j_chk = V5_fluid_jstart, V5_fluid_jend
               DO i_chk = V5_fluid_istart, V5_fluid_iend
                  idx_chk = i_chk + (j_chk - 1) * Nx_tot(1) + (k_chk - 1) * Nx_tot(1) * Nx_tot(2)
                  k_vof_sum = k_vof_sum + V5solid_vof(idx_chk)
               END DO
            END DO

            ! 假設為均勻網格計算單格體積
            dV_local = (x_axis(2)-x_axis(1)) * (y_axis(2)-y_axis(1)) * (z_axis(k_chk+1)-z_axis(k_chk))
            total_vof_sum = total_vof_sum + k_vof_sum

            ! WRITE(*,*) "",k_chk, z_axis(k_chk), z_axis(k_chk+1),&
            !    k_vof_sum, k_vof_sum * dV_local,&
            !    total_vof_sum * dV_local
         END DO

         ! --- X 軸 Diagnostics ---
         ! WRITE(*,*) "------------------------------------------------------------------------------------------"
         ! WRITE(*,*) " [compute_V5solid_vof] X-Axis (i) Breakdown Analysis"
         ! WRITE(*,*) "------------------------------------------------------------------------------------------"
         DO i_chk = V5_fluid_istart, V5_fluid_iend
            k_vof_sum = 0.0_real_kind
            DO k_chk = V5_fluid_kstart, V5_fluid_kend
               DO j_chk = V5_fluid_jstart, V5_fluid_jend
                  idx_chk = i_chk + (j_chk - 1) * Nx_tot(1) + (k_chk - 1) * Nx_tot(1) * Nx_tot(2)
                  k_vof_sum = k_vof_sum + V5solid_vof(idx_chk)
               END DO
            END DO
            !WRITE(*,*) &
            !   "i = ", i_chk, x_axis(i_chk), x_axis(i_chk+1), k_vof_sum
         END DO

         ! --- Y 軸 Diagnostics ---
         ! WRITE(*,*) "------------------------------------------------------------------------------------------"
         ! WRITE(*,*) " [compute_V5solid_vof] Y-Axis (j) Breakdown Analysis"
         ! WRITE(*,*) "------------------------------------------------------------------------------------------"
         DO j_chk = V5_fluid_jstart, V5_fluid_jend
            k_vof_sum = 0.0_real_kind
            DO k_chk = V5_fluid_kstart, V5_fluid_kend
               DO i_chk = V5_fluid_istart, V5_fluid_iend
                  idx_chk = i_chk + (j_chk - 1) * Nx_tot(1) + (k_chk - 1) * Nx_tot(1) * Nx_tot(2)
                  k_vof_sum = k_vof_sum + V5solid_vof(idx_chk)
               END DO
            END DO
            !WRITE(*,*) "j = ", j_chk, y_axis(j_chk), y_axis(j_chk+1), k_vof_sum
         END DO
         WRITE(*,*) "=========================================================================================="

         ! --- Single Cell Detailed Sampling Diagnostics ---
         WRITE(*,*) "------------------------------------------------------------------------------------------"
         WRITE(*,*) " [compute_V5solid_vof] Single Cell Sampling Detail Check"
         WRITE(*,*) "------------------------------------------------------------------------------------------"
         idx_chk = 21 + (21 - 1) * Nx_tot(1) + (20 - 1) * Nx_tot(1) * Nx_tot(2)
         WRITE(*,*) " Core Cell (21,21,20) [0.0~0.05, 0.0~0.05, -0.05~0] VOF = ", V5solid_vof(idx_chk)

         idx_chk = 24 + (24 - 1) * Nx_tot(1) + (20 - 1) * Nx_tot(1) * Nx_tot(2)
         WRITE(*,*) " Outer Cell (24,24,20) [0.15~0.2, 0.15~0.2, -0.05~0] VOF = ", V5solid_vof(idx_chk)
      END BLOCK
   END SUBROUTINE compute_V5solid_vof


   !=======================================================================
   ! Subroutine: Update_Fluid_Solid_VOF
   ! Purpose: 將 VFIFE 算出的固體 VOF 同步回 Truchas Matl 數據庫並確保總合守恆
   !=======================================================================
   SUBROUTINE Update_Fluid_Solid_VOF(solid_vof)
      USE kind_module,      ONLY: int_kind, real_kind
      USE parameter_module, ONLY: nmat
      USE matl_utilities,   ONLY: MATL_GET, UPDATE_MATL
      IMPLICIT NONE

      ! 補回傳入參數宣告
      REAL(KIND=real_kind), INTENT(IN) :: solid_vof(:)

      ! 區域變數
      REAL(KIND=real_kind), ALLOCATABLE :: VF_New(:,:)
      REAL(KIND=real_kind) :: fluid_sum, factor, vof_val
      INTEGER(KIND=int_kind) :: i, j, k, global_id, local_id, m, solid_mat_idx

      solid_mat_idx = V5_mat_id

      ALLOCATE(VF_New(0:nmat, ncells))
      VF_New = 0.0_real_kind

      CALL MATL_GET(VOF = VF_New(1:nmat, :))

      DO k = V5_fluid_kstart, V5_fluid_kend
         DO j = V5_fluid_jstart, V5_fluid_jend
            DO i = V5_fluid_istart, V5_fluid_iend

               global_id = i + (j - 1) * Nx_tot(1) + (k - 1) * Nx_tot(1) * Nx_tot(2)
               local_id = MAKE_LOCAL(global_id, ncells)

               IF (local_id /= -1 .AND. local_id <= ncells) THEN
                  vof_val = solid_vof(global_id) ! 使用傳入的 solid_vof

                  VF_New(solid_mat_idx, local_id) = vof_val

                  fluid_sum = 0.0_real_kind
                  DO m = 1, nmat
                     IF (m /= solid_mat_idx) THEN
                        fluid_sum = fluid_sum + VF_New(m, local_id)
                     END IF
                  END DO

                  IF (fluid_sum > 1.0e-12_real_kind) THEN
                     factor = (1.0_real_kind - vof_val) / fluid_sum
                     DO m = 1, nmat
                        IF (m /= solid_mat_idx) THEN
                           VF_New(m, local_id) = VF_New(m, local_id) * factor
                        END IF
                     END DO
                  ELSE
                     IF (solid_mat_idx /= 1) THEN
                        VF_New(1, local_id) = 1.0_real_kind - vof_val
                     END IF
                  END IF

               END IF

            END DO
         END DO
      END DO

      IF (solid_mat_idx > 0) THEN
         WRITE(*,*) " [Update_Fluid_Solid_VOF] Check Solid VOF Max Value in VF_New: ", &
            MAXVAL(VF_New(solid_mat_idx, :))
      END IF

      CALL UPDATE_MATL(VF_New)
      DEALLOCATE(VF_New)

   END SUBROUTINE Update_Fluid_Solid_VOF

   !=======================================================================
   ! Subroutine: build_fluid_to_solid_mapping
   ! Purpose   : 反向建立流體網格 (Fluid Cell) �����含哪些固體節點 (Solid Nodes)
   !             與固體元素 (Solid Elements) 的 Head-Next 靜態鏈結����������
   !
   ! [呼�����方式]
   !   CALL build_fluid_to_solid_mapping(Nodes, Elements)
   !
   ! [執行後更新的全域變數 (OUTPUT)]
   !   1. cell_node_head(icell) : 第 icell 個流體��格包含的第一個固體節點 ID
   !   2. node_next(inode)      : 同一網格中，下一個固體節點 ID (0 表示結束)
   !   3. cell_elem_head(icell) : 第 icell 個流體網格包含的第一個鏈結索引
   !   4. elem_link_id(link_id) : 該鏈結索引對應到的真實固體元素 ID (ielem)
   !   5. elem_next(link_id)    : 同一網格中���下一個��結索引 (0 表示結��)
   !
   ! [後續使用範例 (如何在流體網格中讀取����應固體資料)]
   !
   !   ! --- 範例 A: 取得����� icell 個流體網格內的所有固體節點 ---
   !   curr_node = cell_node_head(icell)
   !   DO WHILE (curr_node > 0)
   !      ! curr_node 即為固體節點 ID������直接存取 Nodes 容器：
   !      ! node_x = Nodes%xc(1, curr_node)
   !      ! node_v = Nodes%vt(:, curr_node)
   !
   !      curr_node = node_next(curr_node) ! 移動至下一個節點
   !   END DO
   !
   !   ! --- 範例 B: 取得與第 icell 個流體網格相交��所���固體元素 ---
   !   curr_link = cell_elem_head(icell)
   !   DO WHILE (curr_link > 0)
   !      ielem = elem_link_id(curr_link) ! ielem 即為固體元素 ID，可存取 Elements 容器：
   !      ! elem_vol = Elements%vol(ielem)
   !      ! elem_rho = Elements%rho(ielem)
   !
   !      curr_link = elem_next(curr_link) ! 移動至下一個鏈結
   !   END DO
   !=======================================================================
   SUBROUTINE build_fluid_to_solid_mapping(Nodes, Elements)

      IMPLICIT NONE

      ! --- Argument List ---
      TYPE(NodeContainer),    INTENT(IN) :: Nodes
      TYPE(ElementContainer), INTENT(IN) :: Elements

      ! --- Local Variables ---
      INTEGER(int_kind) :: inode, ielem, icell, num_nodes, num_elems
      INTEGER(int_kind) :: i, j, k
      INTEGER(int_kind) :: istart, iend, jstart, jend, kstart, kend
      REAL(real_kind)   :: elem_min(3), elem_max(3)

      num_nodes = SIZE(Nodes%xc, 2)
      num_elems = SIZE(Elements%topo, 2)

      ! -------------------------------------------------------------------
      ! PART 1: 建立 流體網格 -> 固體節點 (Solid Nodes) 的反向映射
      ! -------------------------------------------------------------------
      cell_node_head = 0
      node_next      = 0

      DO inode = 1, num_nodes
         ! 1. 利用 Nodes%xc(:, inode) 找出該固體節點落在哪一個流體網格 (i, j, k)
         i = find_cell_index(Nodes%xc(1, inode), x_axis, Nx_tot(1))
         j = find_cell_index(Nodes%xc(2, inode), y_axis, Nx_tot(2))
         k = find_cell_index(Nodes%xc(3, inode), z_axis, Nx_tot(3))

         ! 2. 安全檢測：確保固體節點落在流體計算域之內
         IF (i >= 1 .AND. i <= Nx_tot(1) .AND. &
            j >= 1 .AND. j <= Nx_tot(2) .AND. &
            k >= 1 .AND. k <= Nx_tot(3)) THEN

            icell = i + (j - 1) * Nx_tot(1) + (k - 1) * Nx_tot(1) * Nx_tot(2)

            ! 3. 插入 Head-Next 靜態鏈結串列
            node_next(inode) = cell_node_head(icell)
            cell_node_head(icell) = inode
         END IF
      END DO

      ! -------------------------------------------------------------------
      ! PART 2: 建立 流體網格 -> 固體元素 (Solid Elements) 的反向映射
      ! -------------------------------------------------------------------
      cell_elem_head  = 0
      elem_next       = 0
      elem_link_id    = 0
      elem_link_count = 0

      DO ielem = 1, num_elems
         ! 1. 直接從 Elements%vertices(:,:,ielem) 計算該元素的 AABB
         elem_min = MINVAL(Elements%vertices(:,:,ielem), DIM=2)
         elem_max = MAXVAL(Elements%vertices(:,:,ielem), DIM=2)

         ! 2. 取����該元素 AABB 涵蓋的流體網格範圍，並約束於有效流體網格內 [1, Nx_tot]
         istart = MAX(1, MIN(Nx_tot(1), find_cell_index(elem_min(1), x_axis, Nx_tot(1))))
         iend   = MAX(1, MIN(Nx_tot(1), find_cell_index(elem_max(1), x_axis, Nx_tot(1))))

         jstart = MAX(1, MIN(Nx_tot(2), find_cell_index(elem_min(2), y_axis, Nx_tot(2))))
         jend   = MAX(1, MIN(Nx_tot(2), find_cell_index(elem_max(2), y_axis, Nx_tot(2))))

         kstart = MAX(1, MIN(Nx_tot(3), find_cell_index(elem_min(3), z_axis, Nx_tot(3))))
         kend   = MAX(1, MIN(Nx_tot(3), find_cell_index(elem_max(3), z_axis, Nx_tot(3))))

         ! 3. 註冊元素至所涵蓋的所有流體網格中
         DO k = kstart, kend
            DO j = jstart, jend
               DO i = istart, iend
                  icell = i + (j - 1) * Nx_tot(1) + (k - 1) * Nx_tot(1) * Nx_tot(2)

                  elem_link_count = elem_link_count + 1
                  elem_link_id(elem_link_count) = ielem
                  elem_next(elem_link_count)    = cell_elem_head(icell)
                  cell_elem_head(icell)         = elem_link_count
               END DO
            END DO
         END DO
      END DO

   END SUBROUTINE build_fluid_to_solid_mapping

   !===========================================================================
   ! Subroutine / Function: RBF Interpolation Utilities
   ! Module               : VFIFE_utils_module
   ! Purpose              : 提供基於 Wendland C2 緊��撐核函數與 AABB 篩選的 RBF 速度插值工具。
   !
   ! [使用說明]
   !   1. wendland_c2_kernel:
   !      - 輸入正規化距離 r (0.0 <= r <= 1.0)，回傳權重值。
   !      - 具備 PURE 與 ELEMENTAL 屬性，支援向量化運算。
   !
   !   2. interpolate_rbf_velocity:
   !      - 傳入流體網格中心座標 xc_cell(3)、特徵邊長 cell_h_size 及影響倍率。
   !      - 內部自動進行 AABB 包絡盒快速判定，並以距離平方 (dist_sq) 篩選固體節點，
   !        將固體節點速度 Nodes%vt 插值至流體網格。
   !
   ! [依賴關係]
   !   - USE VFIFE_Data_module (取得 int_kind, real_kind, Nodes, V5_minX, V5_maxX)
   !===========================================================================

   ! =====================================================================
   ! 工具 1: Wendland C2 緊支撐核函數 (ELEMENTAL 支援向量化)
   ! =====================================================================
   PURE ELEMENTAL FUNCTION wendland_c2_kernel(r) RESULT(phi)

      IMPLICIT NONE
      REAL(KIND=real_kind), INTENT(IN) :: r
      REAL(KIND=real_kind)             :: phi

      IF (r >= 0.0_real_kind .AND. r <= 1.0_real_kind) THEN
         phi = ((1.0_real_kind - r)**4) * (4.0_real_kind * r + 1.0_real_kind)
      ELSE
         phi = 0.0_real_kind
      END IF
   END FUNCTION wendland_c2_kernel


   ! =====================================================================
   ! 工具 2: RBF + AABB 速度插值 Subroutine (距離平方優化版)
   ! =====================================================================
   SUBROUTINE interpolate_rbf_velocity(xc_cell, cell_h_size, slider_ratio, vel_interp)

      IMPLICIT NONE

      ! --- 輸入與輸出宣告 ---
      REAL(KIND=real_kind), INTENT(IN) :: xc_cell(3)
      REAL(KIND=real_kind), INTENT(IN) :: cell_h_size
      REAL(KIND=real_kind), INTENT(IN) :: slider_ratio
      REAL(KIND=real_kind), INTENT(OUT) :: vel_interp(3)

      ! --- 區域變數 ---
      REAL(KIND=real_kind) :: expanded_aabb_min(3), expanded_aabb_max(3)
      REAL(KIND=real_kind) :: center_aabb(3), half_extents(3)
      REAL(KIND=real_kind) :: R_support, R_support_sq
      REAL(KIND=real_kind) :: dx, dy, dz, dist_sq, dist, r_norm, weight, sum_weight
      REAL(KIND=real_kind) :: sum_vel(3)
      INTEGER(KIND=int_kind) :: n

      vel_interp = 0.0_real_kind
      sum_vel    = 0.0_real_kind
      sum_weight = 0.0_real_kind

      ! 1. 計��� RBF 物理影響半徑與其平方
      R_support    = 1.5_real_kind * cell_h_size * slider_ratio
      R_support_sq = R_support**2

      ! 2. 依據 R_support 計算膨脹後的 AABB 範圍
      center_aabb  = 0.5_real_kind * (V5_maxX + V5_minX)
      half_extents = 0.5_real_kind * (V5_maxX - V5_minX) + R_support
      expanded_aabb_min = center_aabb - half_extents
      expanded_aabb_max = center_aabb + half_extents

      ! 3. 快速 AABB 篩選：若 xc_cell 超出膨��後的 AABB，��接歸���返回
      IF (xc_cell(1) < expanded_aabb_min(1) .OR. xc_cell(1) > expanded_aabb_max(1) .OR. &
         xc_cell(2) < expanded_aabb_min(2) .OR. xc_cell(2) > expanded_aabb_max(2) .OR. &
         xc_cell(3) < expanded_aabb_min(3) .OR. xc_cell(3) > expanded_aabb_max(3)) THEN
         RETURN
      END IF

      ! 4. 局部 Wendland C2 RBF 加權插值 (採���距離平方快速篩選)
      DO n = 1, nnd
         dx = xc_cell(1) - Nodes%xc(1, n)
         dy = xc_cell(2) - Nodes%xc(2, n)
         dz = xc_cell(3) - Nodes%xc(3, n)

         dist_sq = dx**2 + dy**2 + dz**2

         IF (dist_sq <= R_support_sq) THEN
            ! 僅在確定落於影響半徑內時才開根號計算 r_norm
            dist   = SQRT(dist_sq)
            r_norm = dist / R_support
            weight = wendland_c2_kernel(r_norm)

            sum_weight = sum_weight + weight
            sum_vel(1) = sum_vel(1) + weight * Nodes%vt(1, n)
            sum_vel(2) = sum_vel(2) + weight * Nodes%vt(2, n)
            sum_vel(3) = sum_vel(3) + weight * Nodes%vt(3, n)
         END IF
      END DO

      ! 5. 權重歸一���
      IF (sum_weight > 1.0e-12_real_kind) THEN
         vel_interp = sum_vel / sum_weight
      END IF

   END SUBROUTINE interpolate_rbf_velocity

   !===========================================================================
   ! Subroutine: update_fluid_mapping
   ! Purpose   : 計算最新固體 AABB、表面快取、VOF（並同步至 Truchas 數據庫），
   !             最後將固體節點速度插值至流體網格。
   ! Module    : VFIFE_FSCoupled_module
   !===========================================================================
   SUBROUTINE update_fluid_mapping()

      IMPLICIT NONE

      ! --- 區域變數 ---
      INTEGER(KIND=int_kind) :: i, j, k, icell
      REAL(KIND=real_kind)   :: xc_cell(3), vel_interp(3)
      REAL(KIND=real_kind)   :: dx_cell, dy_cell, dz_cell, cell_h_size
      REAL(KIND=real_kind)   :: total_vof, max_vel
      INTEGER(KIND=int_kind) :: active_cells

      ! ------------------------------------------------------------------
      ! [驗證程式碼] 確認 update_fluid_mapping 使用由 V5Setup 建立的最新快取與 AABB
      ! ------------------------------------------------------------------
      ! WRITE(*,*) "=========================================="
      ! WRITE(*,*) " [update_fluid_mapping] Starting Mapping..."
      ! WRITE(*,*) "   Current V5_time           :", V5_time
      ! WRITE(*,*) "   Surface Faces (from cache):", num_surf_faces
      ! WRITE(*,*) "   Solid AABB X-range        :", V5_minX(1), " to ", V5_maxX(1)
      ! WRITE(*,*) "   Solid AABB Y-range        :", V5_minX(2), " to ", V5_maxX(2)
      ! WRITE(*,*) "   Solid AABB Z-range        :", V5_minX(3), " to ", V5_maxX(3)
      ! WRITE(*,*) "=========================================="


      ! 1. 計算固體最新 AABB 包絡盒，更新 V5_fluid_istart/iend 等網格索引範圍
      !CALL compute_solid_aabb()

      ! 2. 更新外露固體表面快取資訊
      !CALL build_surface_cache()
      ! 驗證程式碼：確認 surf_node 座標是否有隨時間微幅改變
      ! WRITE(*,*) '[update_fluid_mapping] Time Step ', V5_time, &
      !    ' Surf Node 1 X:', surf_node1(1, 1), &
      !    ' Surf Node 1 Y:', surf_node1(2, 1), &
      !    ' Surf Node 1 Z:', surf_node1(3, 1)

      ! 3. 動態配置並計算流體網格的 V5solid_vof
      IF (.NOT. ALLOCATED(V5solid_vof)) THEN
         ALLOCATE(V5solid_vof(ncells))
         V5solid_vof = 0.0_real_kind
      END IF

      CALL compute_V5solid_vof(V5solid_vof)
      ! -------------------------------------------------------------------
      ! [新增] 更新流體網格的固體鄰接/包含旗標 (V5_ingbr)
      ! 凡是固體體積率 VOF 大於 0 (給予極小容差如 1.0d-4) 的網格皆標示為 1
      ! -------------------------------------------------------------------
      V5_ingbr = 0
      WHERE (V5solid_vof > 1.0e-4_real_kind)
         V5_ingbr = 1
      END WHERE

      ! 驗證程式碼：確認 V5_ingbr 旗標已正確更新
      ! WRITE(*,*) ' [update_fluid_mapping] Updated V5_ingbr=1 Cell Count:', COUNT(V5_ingbr == 1)
      ! ---------------------------------------------------
      ! 將 V5solid_vof 同步寫回 Truchas Matl 數據庫並維持體積守恆
      ! (傳入固體 VOF 陣列與網格總數 ncells)
      ! ---------------------------------------------------
      CALL Update_Fluid_Solid_VOF(V5solid_vof)

      ! ---------------------------------------------------
      ! V5solid_vof 體積守恆動態診斷輸出 (支援非均勻網格)
      ! ---------------------------------------------------
      BLOCK
         REAL(KIND=real_kind) :: sum_vof, total_solid_vol, dV
         INTEGER(KIND=int_kind) :: bi, bj, bk, bcell

         sum_vof = 0.0_real_kind
         total_solid_vol = 0.0_real_kind

         DO bk = V5_fluid_kstart, V5_fluid_kend
            DO bj = V5_fluid_jstart, V5_fluid_jend
               DO bi = V5_fluid_istart, V5_fluid_iend
                  bcell = bi + (bj - 1) * Nx_tot(1) + (bk - 1) * Nx_tot(1) * Nx_tot(2)
                  IF (V5solid_vof(bcell) > 0.0_real_kind) THEN
                     dV = (x_axis(bi+1) - x_axis(bi)) * &
                        (y_axis(bj+1) - y_axis(bj)) * &
                        (z_axis(bk+1) - z_axis(bk))
                     sum_vof = sum_vof + V5solid_vof(bcell)
                     total_solid_vol = total_solid_vol + V5solid_vof(bcell) * dV
                  END IF
               END DO
            END DO
         END DO

         WRITE(*,*) '=========================================='
         WRITE(*,*) ' [update_fluid_mapping] V5solid_vof VOLUME VERIFICATION'
         WRITE(*,*) '=========================================='
         WRITE(*,*) ' Sum of V5solid_vof           :', sum_vof
         WRITE(*,*) ' Calculated Solid Volume (m3) :', total_solid_vol
         WRITE(*,*) '=========================================='
      END BLOCK

      ! ---------------------------------------------------
      ! 將固體節點速度 (Nodes%vt) 插值至流體網格 (V5solid_vel)
      ! ---------------------------------------------------
      IF (.NOT. ALLOCATED(V5solid_vel)) THEN
         ALLOCATE(V5solid_vel(3, ncells))
      END IF

      ! 全域陣列一次性清零 (記憶體層級連續賦值，效能最高)
      V5solid_vel = 0.0_real_kind
      total_vof    = 0.0_real_kind
      max_vel      = 0.0_real_kind
      active_cells = 0

      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, j, k, icell, xc_cell, vel_interp, dx_cell, dy_cell, dz_cell, cell_h_size) &
      !$OMP SHARED(V5_fluid_istart, V5_fluid_iend, V5_fluid_jstart, V5_fluid_jend, V5_fluid_kstart, V5_fluid_kend) &
      !$OMP SHARED(Nx_tot, x_axis, y_axis, z_axis, V5solid_vof, V5solid_vel, Slider_influence_ratio) &
      !$OMP REDUCTION(+:total_vof, active_cells) REDUCTION(max:max_vel)
      DO k = V5_fluid_kstart, V5_fluid_kend
         DO j = V5_fluid_jstart, V5_fluid_jend
            DO i = V5_fluid_istart, V5_fluid_iend

               icell = i + (j - 1) * Nx_tot(1) + (k - 1) * Nx_tot(1) * Nx_tot(2)

               ! 僅對有固體涵蓋的網格進行速度插值
               IF (V5solid_vof(icell) > 0.001_real_kind) THEN

                  ! 1. 計算該非均勻流體網格中心座標與特徵邊長
                  dx_cell = x_axis(i+1) - x_axis(i)
                  dy_cell = y_axis(j+1) - y_axis(j)
                  dz_cell = z_axis(k+1) - z_axis(k)

                  xc_cell(1) = 0.5_real_kind * (x_axis(i) + x_axis(i+1))
                  xc_cell(2) = 0.5_real_kind * (y_axis(j) + y_axis(j+1))
                  xc_cell(3) = 0.5_real_kind * (z_axis(k) + z_axis(k+1))

                  ! 計算幾何特徵尺寸 (3D對角線長)
                  cell_h_size = SQRT(dx_cell**2 + dy_cell**2 + dz_cell**2)

                  ! 2. 呼叫 RBF + AABB 插值常式
                  CALL interpolate_rbf_velocity(xc_cell, cell_h_size, &
                     Slider_influence_ratio, vel_interp)

                  ! 3. 賦值至流體網格速度陣列
                  V5solid_vel(1, icell) = vel_interp(1)
                  V5solid_vel(2, icell) = vel_interp(2)
                  V5solid_vel(3, icell) = vel_interp(3)

                  ! 4. 統計量累加
                  total_vof    = total_vof + V5solid_vof(icell)
                  active_cells = active_cells + 1
                  max_vel      = MAX(max_vel, SQRT(SUM(vel_interp**2)))

               END IF

            END DO
         END DO
      END DO
      !$OMP END PARALLEL DO


      ! 5. [診斷輸出] 統計更新結果
      ! WRITE(*,*) '--------------------------------------------------'
      ! WRITE(*,*) ' [update_fluid_mapping] Active Solid Cells (>0.001) = ', active_cells
      ! WRITE(*,*) ' [update_fluid_mapping] Total Interp VOF Sum    = ', total_vof
      ! WRITE(*,*) ' [update_fluid_mapping] Max Interp Solid Vel   = ', max_vel, ' m/s'
      ! WRITE(*,*) '--------------------------------------------------'

   END SUBROUTINE update_fluid_mapping


   !=======================================================================
   ! Subroutine: V5Solid_Feedback
   ! Purpose: 依照最新 VOF 與固體插值速度 (V5solid_vel)，將速度加權反饋給流體網格 Zone(icell)%Vc
   !=======================================================================
   SUBROUTINE V5Solid_Feedback()
      IMPLICIT NONE

      ! 宣告區域變數
      INTEGER(KIND=int_kind) :: i, j, k, icell
      REAL(KIND=real_kind)   :: V5_s_vof, fluid_vc_tmp(3)

      ! 診斷統計變數
      INTEGER(KIND=int_kind) :: feedback_cells
      REAL(KIND=real_kind)   :: max_fluid_vc_before, max_fluid_vc_after

      feedback_cells       = 0
      max_fluid_vc_before  = 0.0_real_kind
      max_fluid_vc_after   = 0.0_real_kind

      ! 僅對固體涵蓋的流體網格 AABB 範圍內更新速度
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, j, k, icell, V5_s_vof, fluid_vc_tmp) &
      !$OMP SHARED(V5_fluid_istart, V5_fluid_iend) &
      !$OMP SHARED(V5_fluid_jstart, V5_fluid_jend) &
      !$OMP SHARED(V5_fluid_kstart, V5_fluid_kend) &
      !$OMP SHARED(Nx_tot, V5solid_vof, V5solid_vel, Zone) &
      !$OMP REDUCTION(+:feedback_cells) &
      !$OMP REDUCTION(max:max_fluid_vc_before, max_fluid_vc_after)
      DO k = V5_fluid_kstart, V5_fluid_kend
         DO j = V5_fluid_jstart, V5_fluid_jend
            DO i = V5_fluid_istart, V5_fluid_iend

               ! 計算 1D 流體網格索引
               icell = i + (j - 1) * Nx_tot(1) + (k - 1) * Nx_tot(1) * Nx_tot(2)
               V5_s_vof   = V5solid_vof(icell)

               ! 僅針對有固體佔據的網格做 IBM 速度加權
               IF (V5_s_vof > 0.01_real_kind) THEN

                  ! 暫存更新前的流體速度與統計最大值
                  fluid_vc_tmp(:) = Zone(icell)%Vc(:)
                  max_fluid_vc_before = MAX(max_fluid_vc_before, SQRT(SUM(fluid_vc_tmp**2)))

                  ! 依照 VOF 進行固體與流體速度的加權混合
                  Zone(icell)%Vc(1) = V5solid_vel(1, icell) * V5_s_vof &
                     + fluid_vc_tmp(1) * (1.0_real_kind - V5_s_vof)

                  Zone(icell)%Vc(2) = V5solid_vel(2, icell) * V5_s_vof &
                     + fluid_vc_tmp(2) * (1.0_real_kind - V5_s_vof)

                  Zone(icell)%Vc(3) = V5solid_vel(3, icell) * V5_s_vof &
                     + fluid_vc_tmp(3) * (1.0_real_kind - V5_s_vof)

                  ! 統計更新後的流體速度與作用網格數
                  max_fluid_vc_after = MAX(max_fluid_vc_after, SQRT(SUM(Zone(icell)%Vc(:)**2)))
                  feedback_cells     = feedback_cells + 1
               END IF

            END DO
         END DO
      END DO
      !$OMP END PARALLEL DO

      ! =========================================================
      ! [驗證程式碼] 流體網格反饋作用統計輸出
      ! =========================================================
      WRITE(*,*) ' [V5Solid_Feedback] Coupled Cells Count      = ', feedback_cells
      WRITE(*,*) ' [V5Solid_Feedback] Max Fluid Vel (Before)   = ', max_fluid_vc_before, ' m/s'
      WRITE(*,*) ' [V5Solid_Feedback] Max Fluid Vel (After)    = ', max_fluid_vc_after, ' m/s'

   END SUBROUTINE V5Solid_Feedback


END MODULE VFIFE_FSCoupled_module



```

---
# 🔗 參考資料


---