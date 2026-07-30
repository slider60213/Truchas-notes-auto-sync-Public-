---
type: 📝 Research
created: 2026-07-30 03:09
modified: 2026-07-31 04:39
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

```fortran
MODULE VFIFE_MOTION_module

   USE VFIFE_CMF_module



   ! Truchas
   USE body_data_module,       only: Body_Force



   ! Basic Modules of VFIFE
   USE VFIFE_Data_module
   USE VFIFE_Utils_module

   IMPLICIT NONE




   ! 子程式宣告
   PUBLIC :: calculate_external_forces
   PUBLIC :: calculate_internal_forces
   PUBLIC :: update_kinematics

   ! 內部獨立運算工具 (輔助子程序)
   PRIVATE :: cross_product
   PRIVATE :: mat_vec_mult
   PRIVATE :: mat_trans_vec_mult
   PRIVATE :: update_rotation_matrix
   PRIVATE :: normalize_quaternion

CONTAINS


   !===========================================================================
   ! Subroutine : calculate_external_forces
   ! Module     : VFIFE_MOTION_module
   ! Purpose    : 彙整固體節點承受之外力 (重力/體積力 + 流體壓力 + Cd 剪力)
   !===========================================================================
   SUBROUTINE calculate_external_forces()
      IMPLICIT NONE
      INTEGER(KIND=int_kind) :: i, j, k
      INTEGER(KIND=int_kind) :: n1, n2, n3
      REAL(KIND=real_kind)   :: f_node(3), f_press(3), f_shear(3)
      REAL(KIND=real_kind)   :: f_fluid_total(3)
      REAL(KIND=real_kind)   :: v_solid_face(3), u_rel(3), u_rel_norm, u_rel_tangent(3)
      REAL(KIND=real_kind)   :: Cd, rho_local, area, norm(3)

      ! 設定表面阻力/剪力係數 (可視需要改為全域參數設定)
      Cd = 0.05_real_kind

      ! 0. 清空本時間步的流體受力容器
      IF (ASSOCIATED(Nodes%force)) Nodes%force(:, :) = 0.0_real_kind



      ! 2. 計算流體作用力 (正向壓力 + 切向剪力) 並分配至固體節點
      f_fluid_total = 0.0_real_kind

      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, j, n1, n2, n3, area, norm, v_solid_face, u_rel, u_rel_norm, u_rel_tangent) &
      !$OMP PRIVATE(rho_local, f_press, f_shear, f_node) &
      !$OMP SHARED(nel, face_judge, elem_topo, Elements, Nodes, Cd) &
      !$OMP REDUCTION(+:f_fluid_total)
      DO i = 1, nel
         DO j = 1, 4
            IF (face_judge(j, i) /= 1) CYCLE

            SELECT CASE (j)
             CASE (1); n1 = elem_topo(3, i); n2 = elem_topo(4, i); n3 = elem_topo(5, i)
             CASE (2); n1 = elem_topo(2, i); n2 = elem_topo(5, i); n3 = elem_topo(4, i)
             CASE (3); n1 = elem_topo(2, i); n2 = elem_topo(3, i); n3 = elem_topo(5, i)
             CASE (4); n1 = elem_topo(2, i); n2 = elem_topo(4, i); n3 = elem_topo(3, i)
            END SELECT

            area      = Elements%area(j, i)
            norm(:)   = Elements%normal(:, j, i)
            rho_local = Elements%density(j, i) ! 動態採樣流體密度

            ! --- [A] 正向壓力項：F_press = - P * A * n ---
            f_press(:) = -Elements%pressure(j, i) * area * norm(:)

            ! --- [B] 切向剪力項 (Cd) ---
            IF (ASSOCIATED(Nodes%vt)) THEN
               v_solid_face(:) = (Nodes%vt(:, n1) + Nodes%vt(:, n2) + Nodes%vt(:, n3)) / 3.0_real_kind
            ELSE
               v_solid_face(:) = 0.0_real_kind
            END IF

            ! 相對速度與切線方向投影
            u_rel(:)         = Elements%velocity(:, j, i) - v_solid_face(:)
            u_rel_tangent(:) = u_rel(:) - DOT_PRODUCT(u_rel, norm) * norm(:)
            u_rel_norm       = SQRT(SUM(u_rel_tangent(:)**2))

            ! 使用採樣到的動態密度 rho_local 計算剪力
            IF (u_rel_norm > 1.0E-6_real_kind .AND. rho_local > 0.0_real_kind) THEN
               f_shear(:) = 0.5_real_kind * rho_local * Cd * u_rel_norm * u_rel_tangent(:) * area
            ELSE
               f_shear(:) = 0.0_real_kind
            END IF

            ! --- [C] 面受力總合，均分至 3 個節點 ---
            f_node(:) = (f_press(:) + f_shear(:)) / 3.0_real_kind

            ! 寫入全域容器 (使用 ATOMIC 防範 Data Race)
            !$OMP ATOMIC
            Nodes%force(1, n1) = Nodes%force(1, n1) + f_node(1)
            !$OMP ATOMIC
            Nodes%force(2, n1) = Nodes%force(2, n1) + f_node(2)
            !$OMP ATOMIC
            Nodes%force(3, n1) = Nodes%force(3, n1) + f_node(3)

            !$OMP ATOMIC
            Nodes%force(1, n2) = Nodes%force(1, n2) + f_node(1)
            !$OMP ATOMIC
            Nodes%force(2, n2) = Nodes%force(2, n2) + f_node(2)
            !$OMP ATOMIC
            Nodes%force(3, n2) = Nodes%force(3, n2) + f_node(3)

            !$OMP ATOMIC
            Nodes%force(1, n3) = Nodes%force(1, n3) + f_node(1)
            !$OMP ATOMIC
            Nodes%force(2, n3) = Nodes%force(2, n3) + f_node(2)
            !$OMP ATOMIC
            Nodes%force(3, n3) = Nodes%force(3, n3) + f_node(3)

            !$OMP ATOMIC
            Nodes%fsum(1, n1) = Nodes%fsum(1, n1) + f_node(1)
            !$OMP ATOMIC
            Nodes%fsum(2, n1) = Nodes%fsum(2, n1) + f_node(2)
            !$OMP ATOMIC
            Nodes%fsum(3, n1) = Nodes%fsum(3, n1) + f_node(3)

            !$OMP ATOMIC
            Nodes%fsum(1, n2) = Nodes%fsum(1, n2) + f_node(1)
            !$OMP ATOMIC
            Nodes%fsum(2, n2) = Nodes%fsum(2, n2) + f_node(2)
            !$OMP ATOMIC
            Nodes%fsum(3, n2) = Nodes%fsum(3, n2) + f_node(3)

            !$OMP ATOMIC
            Nodes%fsum(1, n3) = Nodes%fsum(1, n3) + f_node(1)
            !$OMP ATOMIC
            Nodes%fsum(2, n3) = Nodes%fsum(2, n3) + f_node(2)
            !$OMP ATOMIC
            Nodes%fsum(3, n3) = Nodes%fsum(3, n3) + f_node(3)

            f_fluid_total(:) = f_fluid_total(:) + f_node(:) * 3.0_real_kind
         END DO
      END DO
      !$OMP END PARALLEL DO

      ! 3. 累加重力 / 體積力
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, k) &
      !$OMP SHARED(nnd, Nodes, Body_Force)
      DO i = 1, nnd
         IF (Nodes%mass(i) > 0.0_real_kind) THEN
            DO k = 1, 3
               Nodes%fsum(k, i) = Nodes%fsum(k, i) + Nodes%mass(i) * Body_Force(k)
            END DO
         END IF
      END DO
      !$OMP END PARALLEL DO

      ! =========================================================
      ! [驗證程式碼]
      ! =========================================================
      WRITE(*, '(A, 3(ES12.5, 1X))') &
         '  [Ext Force Check] Total Hydrodynamic Force (Press+Shear) on Nodes (N) = ', f_fluid_total(1:3)

   END SUBROUTINE calculate_external_forces


!===========================================================================
   ! Subroutine : calculate_internal_forces
   ! Module     : VFIFE_MOTION_module
   ! Purpose    : 計算 3D 四面體固體單元 (Tet4) 之 CMF 剛體分離、純變形應變、
   !              靜平衡節點等效內力，並自全域合力 Nodes%fsum 中扣除內力
   !              (F_net = F_ext - F_int)。
   !
   ! [作用說明]
   !   1. 依據 Elements%topo(2:5, elem_idx) 讀取四面體之 4 個節點座標。
   !   2. 呼叫 calc_rotation_R 計算剛體旋轉 Q 與 CMF 局部純變形向量 etahead。
   !   3. 呼叫 calc_B_matrix_coeff 與 calc_element_strain 計算幾何係數及 Cauchy 應變。
   !   4. 透過廣義 Hooke 定律計算應力，並以 calc_local_forces_equilibrium 求解靜平衡內力。
   !   5. 將局部內力轉回全域座標系，透過 OMP ATOMIC 安全地自 Nodes%fsum 中扣除。
   !
   ! [依賴關係]
   !   - USE VFIFE_Data_module (nel, Elements, Nodes, e)
   !   - USE VFIFE_CMF_module  (calc_rotation_R, calc_B_matrix_coeff,
   !                            calc_element_strain, calc_local_forces_equilibrium)
   !===========================================================================
   SUBROUTINE calculate_internal_forces()

      IMPLICIT NONE

      ! --- 區域變數 ---
      INTEGER(KIND=int_kind) :: elem_idx, k, n, n1, n2, n3, n4, mat_id
      REAL(KIND=real_kind)   :: E_mod, nu_val, lambda, mu
      REAL(KIND=real_kind)   :: x(3, 4), x0(3, 4)
      REAL(KIND=real_kind)   :: f_elem(3, 4), f_local(3, 4)
      REAL(KIND=real_kind)   :: vol0, a1
      REAL(KIND=real_kind)   :: strain(6), stress(6)

      ! --- CMF 相關變數 ---
      REAL(KIND=real_kind)   :: Rtheta(3, 3), Q(3, 3)
      REAL(KIND=real_kind)   :: etahead(3, 4), v21(3), v31(3), v41(3)
      REAL(KIND=real_kind)   :: b(4), r(4), o(4)
      LOGICAL                :: is_distorted

      ! 1. 前置判斷：若無單元資料或物體為完全剛體 (is_V5_deformable = .FALSE.)，直接返回不計算內力
      IF (nel <= 0 .OR. .NOT. ASSOCIATED(Elements%topo)) RETURN
      IF (.NOT. is_V5_deformable) RETURN

      ! 2. 遍歷所有 3D 四面體單元計算內力 (OpenMP 平行化)
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(elem_idx, k, n, n1, n2, n3, n4, mat_id, E_mod, nu_val, &
      !$OMP         lambda, mu, x, x0, f_elem, f_local, vol0, a1, &
      !$OMP         strain, stress, Rtheta, Q, etahead, v21, v31, v41, &
      !$OMP         b, r, o, is_distorted) &
      !$OMP SHARED(nel, Elements, Nodes, e, is_V5_deformable)
      DO elem_idx = 1, nel

         ! 取得 4 個節點編號 (topo(1,:) 為單元類型或編號，topo(2:5,:) 為節點 ID)
         n1 = Elements%topo(2, elem_idx)
         n2 = Elements%topo(3, elem_idx)
         n3 = Elements%topo(4, elem_idx)
         n4 = Elements%topo(5, elem_idx)

         ! 取得 4 個節點座標 (x: 當前, x0: 初始)
         x(:, 1) = Nodes%xc(:, n1);  x0(:, 1) = Nodes%xc0(:, n1)
         x(:, 2) = Nodes%xc(:, n2);  x0(:, 2) = Nodes%xc0(:, n2)
         x(:, 3) = Nodes%xc(:, n3);  x0(:, 3) = Nodes%xc0(:, n3)
         x(:, 4) = Nodes%xc(:, n4);  x0(:, 4) = Nodes%xc0(:, n4)

         ! 取得材料參數 (e(1,:) 為楊氏模數, e(2,:) 為泊松比)
         mat_id = Elements%mat(1, elem_idx)
         E_mod  = e(1, mat_id)
         nu_val = e(2, mat_id)
         mu     = E_mod / (2.0_real_kind * (1.0_real_kind + nu_val))
         lambda = (E_mod * nu_val) / ((1.0_real_kind + nu_val) * (1.0_real_kind - 2.0_real_kind * nu_val))

         ! A. CMF 分離剛體運動：計算旋轉矩陣 Rtheta、座標轉換矩陣 Q 與 CMF 純變形向量
         CALL calc_rotation_R(x0, x, Q, Rtheta, etahead, v21, v31, v41)

         ! B. 計算四面體 B 矩陣幾何係數 (b, r, o) 與體積 6V0 (a1)
         CALL calc_B_matrix_coeff(v21, v31, v41, a1, vol0, b, r, o, is_distorted)
         IF (is_distorted .OR. vol0 <= 1.0e-14_real_kind) CYCLE

         ! C. 計算 CMF 局部 Cauchy 應變與應力
         CALL calc_element_strain(etahead, b, r, o, a1, strain)

         ! 廣義 Hooke 定律 (計算 6 個應力分量)
         stress(1) = (lambda + 2.0_real_kind*mu)*strain(1) + lambda*(strain(2) + strain(3))
         stress(2) = (lambda + 2.0_real_kind*mu)*strain(2) + lambda*(strain(1) + strain(3))
         stress(3) = (lambda + 2.0_real_kind*mu)*strain(3) + lambda*(strain(1) + strain(2))
         stress(4) = mu * strain(4)
         stress(5) = mu * strain(5)
         stress(6) = mu * strain(6)

         ! D. 依靜平衡關係計算 CMF 局部節點力 f_local，並透過 Q 轉回全域座標系 f_elem
         CALL calc_local_forces_equilibrium(v21, v31, v41, vol0, a1, b, r, o, stress, f_local)

         DO n = 1, 4
            f_elem(:, n) = MATMUL(Q, f_local(:, n))
         END DO

         ! E. 將內力扣除至全域合力陣列 (OMP ATOMIC 確保多線程寫入安全)
         !$OMP ATOMIC
         Nodes%fsum(1, n1) = Nodes%fsum(1, n1) - f_elem(1, 1)
         !$OMP ATOMIC
         Nodes%fsum(2, n1) = Nodes%fsum(2, n1) - f_elem(2, 1)
         !$OMP ATOMIC
         Nodes%fsum(3, n1) = Nodes%fsum(3, n1) - f_elem(3, 1)

         !$OMP ATOMIC
         Nodes%fsum(1, n2) = Nodes%fsum(1, n2) - f_elem(1, 2)
         !$OMP ATOMIC
         Nodes%fsum(2, n2) = Nodes%fsum(2, n2) - f_elem(2, 2)
         !$OMP ATOMIC
         Nodes%fsum(3, n2) = Nodes%fsum(3, n2) - f_elem(3, 2)

         !$OMP ATOMIC
         Nodes%fsum(1, n3) = Nodes%fsum(1, n3) - f_elem(1, 3)
         !$OMP ATOMIC
         Nodes%fsum(2, n3) = Nodes%fsum(2, n3) - f_elem(2, 3)
         !$OMP ATOMIC
         Nodes%fsum(3, n3) = Nodes%fsum(3, n3) - f_elem(3, 3)

         !$OMP ATOMIC
         Nodes%fsum(1, n4) = Nodes%fsum(1, n4) - f_elem(1, 4)
         !$OMP ATOMIC
         Nodes%fsum(2, n4) = Nodes%fsum(2, n4) - f_elem(2, 4)
         !$OMP ATOMIC
         Nodes%fsum(3, n4) = Nodes%fsum(3, n4) - f_elem(3, 4)

      END DO
      !$OMP END PARALLEL DO

      ! =========================================================
      ! [驗證程式碼] 檢查內力計算結果與全域合力輸出
      ! =========================================================
      IF (nel > 0) THEN
         WRITE(*, '(A, I0)') '  [VFIFE CMF Verification] Calculation completed for nel = ', nel
         WRITE(*, '(A, 3ES14.6)') '  [VFIFE CMF Verification] Node 1 force (fsum): ', Nodes%fsum(:, 1)
      END IF

   END SUBROUTINE calculate_internal_forces



   !===========================================================================
   ! Subroutine : update_kinematics
   ! Purpose    : 剛體 6-DOF 時間積分 (3-DOF 平移 + Body Frame 3-DOF 旋轉)
   !              並完成四元數更新與節點空間座標/速度重建
   !===========================================================================
   SUBROUTINE update_kinematics(dt)
      USE VFIFE_Data_module
      IMPLICIT NONE

      REAL(KIND=real_kind), INTENT(IN) :: dt

      INTEGER(KIND=int_kind)  :: i
      REAL(KIND=real_kind)    :: arm_vec(3), torque_i(3)
      REAL(KIND=real_kind)    :: T_body(3), I_w(3), w_cross_Iw(3), rhs_body(3)
      REAL(KIND=real_kind)    :: dq(4), omega_quat(4)
      REAL(KIND=real_kind)    :: r_body0(3), r_global(3), v_rot(3)

      ! ----------------------------------------------------------------------
      ! 階段 1: 合力與合力矩對質心歸納 (CoM Force & Torque Reduction)
      ! ----------------------------------------------------------------------
      ! 若為可變形體 (Deformable Body)，不進行全域剛體 6-DOF 時間積分
      IF (is_V5_deformable) RETURN

      Rigid_Ftotal = 0.0_real_kind
      Rigid_Ttotal = 0.0_real_kind

      DO i = 1, nnd
         ! 1.1 累加總合力 (Global Frame)
         Rigid_Ftotal = Rigid_Ftotal + Nodes%fsum(:, i)

         ! 1.2 計算當前節點對質心的臂力向量 r = x_node - x_CoM
         arm_vec = Nodes%xc(:, i) - Rigid_CoM

         ! 1.3 計算節點外力產生之矩 tau = arm x fsum
         CALL cross_product(arm_vec, Nodes%fsum(:, i), torque_i)

         ! 1.4 累加總外力矩 (Global Frame)
         Rigid_Ttotal = Rigid_Ttotal + torque_i
      END DO

      ! ----------------------------------------------------------------------
      ! 階段 2: 質心 3-DOF 平移時間積分 (Central Translation)
      ! ----------------------------------------------------------------------
      IF (Rigid_mass > 0.0_real_kind) THEN
         Rigid_acc = Rigid_Ftotal / Rigid_mass
      ELSE
         Rigid_acc = 0.0_real_kind
      END IF

      Rigid_vel = Rigid_vel + Rigid_acc * dt
      Rigid_CoM = Rigid_CoM + Rigid_vel * dt

      ! ----------------------------------------------------------------------
      ! 階段 3: Body Frame 尤拉轉動方程式求解 (3-DOF Rotation in Body Frame)
      ! ----------------------------------------------------------------------
      ! 3.1 將 Global Frame 下的外力矩轉換至 Body Frame: T_body = R^T * T_global
      CALL mat_trans_vec_mult(Rigid_Rmat, Rigid_Ttotal, T_body)

      ! 3.2 計算陀螺力矩項: omega_body x (I_body * omega_body)
      CALL mat_vec_mult(Rigid_Ibody, Rigid_omega_body, I_w)
      CALL cross_product(Rigid_omega_body, I_w, w_cross_Iw)

      ! 3.3 右端項 RHS = T_body - omega_body x (I_body * omega_body)
      rhs_body = T_body - w_cross_Iw

      ! 3.4 求解 Body Frame 角加速度: alpha_body = I_body^-1 * RHS
      CALL mat_vec_mult(Rigid_invIbody, rhs_body, Rigid_alpha_body)

      ! 3.5 時間積分更新 Body Frame 角速度
      Rigid_omega_body = Rigid_omega_body + Rigid_alpha_body * dt

      ! 3.6 將 Body Frame 角速度轉換回 Global Frame: omega_global = R * omega_body
      CALL mat_vec_mult(Rigid_Rmat, Rigid_omega_body, Rigid_omega_global)

      ! ----------------------------------------------------------------------
      ! 階段 4: 四元數與姿態旋轉矩陣更新 (Quaternion & Pose Update)
      ! ----------------------------------------------------------------------
      ! 4.1 四元數時間微分: dq/dt = 0.5 * q (x) [0, omega_global]
      omega_quat = [ 0.0_real_kind, Rigid_omega_global(1), Rigid_omega_global(2), Rigid_omega_global(3) ]

      dq(1) = 0.5_real_kind * (-Rigid_quat(2)*omega_quat(2) - Rigid_quat(3)*omega_quat(3) - Rigid_quat(4)*omega_quat(4))
      dq(2) = 0.5_real_kind * ( Rigid_quat(1)*omega_quat(2) + Rigid_quat(3)*omega_quat(4) - Rigid_quat(4)*omega_quat(3))
      dq(3) = 0.5_real_kind * ( Rigid_quat(1)*omega_quat(3) - Rigid_quat(2)*omega_quat(4) + Rigid_quat(4)*omega_quat(2))
      dq(4) = 0.5_real_kind * ( Rigid_quat(1)*omega_quat(4) + Rigid_quat(2)*omega_quat(3) - Rigid_quat(3)*omega_quat(2))

      ! 4.2 顯式時間積分四元數
      Rigid_quat = Rigid_quat + dq * dt

      ! 4.3 四元數單位化 (防止數值漂移)
      CALL normalize_quaternion(Rigid_quat)

      ! 4.4 依據更新後四元數重建旋轉矩陣 R
      CALL update_rotation_matrix(Rigid_quat, Rigid_Rmat)

      ! ----------------------------------------------------------------------
      ! 階段 5: 各節點運動學重建 (Node Kinematic Reconstruction)
      ! ----------------------------------------------------------------------
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, r_body0, r_global, v_rot) &
      !$OMP SHARED(nnd, Nodes, Rigid_CoM0, Rigid_CoM, Rigid_vel, Rigid_omega_global, Rigid_Rmat)
      DO i = 1, nnd
         ! 5.1 計算初始 Body Frame 相對座標向量: r_body0 = x0 - CoM0
         r_body0 = Nodes%xc0(:, i) - Rigid_CoM0

         ! 5.2 旋轉至當前 Global Frame 相對座標: r_global = R * r_body0
         r_global(1) = Rigid_Rmat(1,1)*r_body0(1) + Rigid_Rmat(1,2)*r_body0(2) + Rigid_Rmat(1,3)*r_body0(3)
         r_global(2) = Rigid_Rmat(2,1)*r_body0(1) + Rigid_Rmat(2,2)*r_body0(2) + Rigid_Rmat(2,3)*r_body0(3)
         r_global(3) = Rigid_Rmat(3,1)*r_body0(1) + Rigid_Rmat(3,2)*r_body0(2) + Rigid_Rmat(3,3)*r_body0(3)

         ! 5.3 重建當前節點空間座標: x_i = CoM + r_global
         Nodes%xc(:, i) = Rigid_CoM + r_global

         ! 5.4 重建當前節點空間速度: v_i = v_CoM + omega_global x r_global
         v_rot(1) = Rigid_omega_global(2)*r_global(3) - Rigid_omega_global(3)*r_global(2)
         v_rot(2) = Rigid_omega_global(3)*r_global(1) - Rigid_omega_global(1)*r_global(3)
         v_rot(3) = Rigid_omega_global(1)*r_global(2) - Rigid_omega_global(2)*r_global(1)

         Nodes%vt(:, i) = Rigid_vel + v_rot
      END DO
      !$OMP END PARALLEL DO

      ! =========================================================
      ! [驗證程式碼] 列印剛體動力學狀態與力矩平衡驗證
      ! =========================================================
      WRITE(*, '(A, 3(ES12.5, 1X))') '  [Rigid Kinematics] Total Force  (N)   = ', Rigid_Ftotal
      WRITE(*, '(A, 3(ES12.5, 1X))') '  [Rigid Kinematics] Total Torque (N-m) = ', Rigid_Ttotal
      WRITE(*, '(A, 3(ES12.5, 1X))') '  [Rigid Kinematics] Omega Body (rad/s) = ', Rigid_omega_body

   END SUBROUTINE update_kinematics


   !===========================================================================
   ! Helper Subroutines : 向量與矩陣運算工具 (私有)
   !===========================================================================

   ! 外積運算: res = u x v
   PURE SUBROUTINE cross_product(u, v, res)
      IMPLICIT NONE
      REAL(KIND=8), INTENT(IN)  :: u(3), v(3)
      REAL(KIND=8), INTENT(OUT) :: res(3)

      res(1) = u(2) * v(3) - u(3) * v(2)
      res(2) = u(3) * v(1) - u(1) * v(3)
      res(3) = u(1) * v(2) - u(2) * v(1)
   END SUBROUTINE cross_product

   ! ���陣向量乘法: res = A * x
   PURE SUBROUTINE mat_vec_mult(A, x, res)
      IMPLICIT NONE
      REAL(KIND=8), INTENT(IN)  :: A(3,3), x(3)
      REAL(KIND=8), INTENT(OUT) :: res(3)

      res(1) = A(1,1)*x(1) + A(1,2)*x(2) + A(1,3)*x(3)
      res(2) = A(2,1)*x(1) + A(2,2)*x(2) + A(2,3)*x(3)
      res(3) = A(3,1)*x(1) + A(3,2)*x(2) + A(3,3)*x(3)
   END SUBROUTINE mat_vec_mult

   ! 轉置矩陣向量乘法: res = A^T * x
   PURE SUBROUTINE mat_trans_vec_mult(A, x, res)
      IMPLICIT NONE
      REAL(KIND=8), INTENT(IN)  :: A(3,3), x(3)
      REAL(KIND=8), INTENT(OUT) :: res(3)

      res(1) = A(1,1)*x(1) + A(2,1)*x(2) + A(3,1)*x(3)
      res(2) = A(1,2)*x(1) + A(2,2)*x(2) + A(3,2)*x(3)
      res(3) = A(1,3)*x(1) + A(2,3)*x(2) + A(3,3)*x(3)
   END SUBROUTINE mat_trans_vec_mult

   ! 由四元數 q = [q0, q1, q2, q3] 計算 3x3 旋轉矩陣 R
   PURE SUBROUTINE update_rotation_matrix(q, R)
      IMPLICIT NONE
      REAL(KIND=8), INTENT(IN)  :: q(4)
      REAL(KIND=8), INTENT(OUT) :: R(3,3)
      REAL(KIND=8)              :: q0, q1, q2, q3

      q0 = q(1); q1 = q(2); q2 = q(3); q3 = q(4)

      R(1,1) = 1.0_real_kind - 2.0_real_kind * (q2**2 + q3**2)
      R(1,2) = 2.0_real_kind * (q1*q2 - q0*q3)
      R(1,3) = 2.0_real_kind * (q1*q3 + q0*q2)

      R(2,1) = 2.0_real_kind * (q1*q2 + q0*q3)
      R(2,2) = 1.0_real_kind - 2.0_real_kind * (q1**2 + q3**2)
      R(2,3) = 2.0_real_kind * (q2*q3 - q0*q1)

      R(3,1) = 2.0_real_kind * (q1*q3 - q0*q2)
      R(3,2) = 2.0_real_kind * (q2*q3 + q0*q1)
      R(3,3) = 1.0_real_kind - 2.0_real_kind * (q1**2 + q2**2)
   END SUBROUTINE update_rotation_matrix

   ! 四元數單位化
   PURE SUBROUTINE normalize_quaternion(q)
      IMPLICIT NONE
      REAL(KIND=8), INTENT(INOUT) :: q(4)
      REAL(KIND=8)                :: norm_val

      norm_val = SQRT(SUM(q**2))
      IF (norm_val > 1.0e-12_real_kind) THEN
         q = q / norm_val
      ELSE
         q = [ 1.0_real_kind, 0.0_real_kind, 0.0_real_kind, 0.0_real_kind ]
      END IF
   END SUBROUTINE normalize_quaternion

END MODULE VFIFE_MOTION_module


```
---
# 🔗 參考資料


---