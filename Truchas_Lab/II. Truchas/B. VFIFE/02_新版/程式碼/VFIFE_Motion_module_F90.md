---
type: 📝 Research
created: 2026-07-30 03:09
modified: 2026-07-30 03:23
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

   ! Truchas
   USE body_data_module,       only: Body_Force

   ! Basic Modules of VFIFE
   USE VFIFE_Data_module
   USE VFIFE_Utils_module

   IMPLICIT NONE



   ! 對外開放的核心入口
   PUBLIC :: V5_solid_solver

   ! 內部私有子程式宣告
   PRIVATE :: calculate_external_forces
   PRIVATE :: calculate_internal_forces
   PRIVATE :: update_kinematics

   ! 內部獨立運算工具 (私有輔助子程序)
   PRIVATE :: cross_product
   PRIVATE :: mat_vec_mult
   PRIVATE :: mat_trans_vec_mult
   PRIVATE :: update_rotation_matrix
   PRIVATE :: normalize_quaternion

CONTAINS

   !===========================================================================
   ! 固體時間步求解器主入口 (Public)
   !===========================================================================
   SUBROUTINE V5_solid_solver(V5_dt)
      REAL(KIND=8), INTENT(IN) :: V5_dt

      ! 1. 彙整外力 (重力、流體耦合力等)
      CALL calculate_external_forces()

      ! 2. 計算單元內力與阻尼力
      CALL calculate_internal_forces()

      ! 3. 顯式時間積分，更新運動學變數 (加速度、速度、位移、座標)
      CALL update_kinematics(V5_dt)

      ! 4. 模組執行完成驗證訊息
      WRITE(*, '(A, F10.6, A)') '[VFIFE_MOTION] V5_solid_solver executed successfully for dt = ', V5_dt, ' s'
      WRITE(*, '(A, 3F12.6)')   '[VFIFE_VERIFY] Current CoM Pos (m)  : ', Rigid_CoM
      WRITE(*, '(A, 3F12.6)')   '[VFIFE_VERIFY] Current CoM Vel (m/s): ', Rigid_vel
      WRITE(*, '(A, F12.8)')    '[VFIFE_VERIFY] Quaternion Norm     : ', SQRT(SUM(Rigid_quat**2))
   END SUBROUTINE V5_solid_solver


   !===========================================================================
   ! Subroutine : calculate_external_forces
   ! Module     : VFIFE_MOTION_module
   ! Purpose    : 彙整固體節點承受之外力 (重力/體積力 + 流體耦合力)
   !===========================================================================
   SUBROUTINE calculate_external_forces()
      IMPLICIT NONE
      INTEGER(KIND=int_kind) :: i, k

      ! 1. 重置合力陣列 (若流體力已預先存於其他變數，在此統一歸零後加總)
      Nodes%fsum = 0.0_real_kind

      ! 2. 累加重力 / 體積力 (F = m * Body_Force)
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


      ! 3. 累加流體/外加耦合力 (存於 Nodes%force)
      IF (ASSOCIATED(Nodes%force)) THEN
         !$OMP PARALLEL DO DEFAULT(NONE) PRIVATE(i, k) SHARED(nnd, Nodes)
         DO i = 1, nnd
            DO k = 1, 3
               Nodes%fsum(k, i) = Nodes%fsum(k, i) + Nodes%force(k, i)
            END DO
         END DO
         !$OMP END PARALLEL DO
      END IF

      ! 4. [驗證程式碼] 確認第一個節點的外力計算結果
      IF (nnd > 0) THEN
         WRITE(*, '(A, I0, A, 3(ES12.5, 1X))') &
            '  [Ext Force Check] Body_Force (m/s^2) = ', 1, ': ', Body_Force(1:3)
         WRITE(*, '(A, ES12.5, A, 3(ES12.5, 1X))') &
            '  [Ext Force Check] Node 1 (mass=', Nodes%mass(1), &
            ' kg) Fsum (N) = ', Nodes%fsum(1:3, 1)
      END IF

   END SUBROUTINE calculate_external_forces


   !===========================================================================
   ! Subroutine : calculate_internal_forces
   ! Module     : VFIFE_MOTION_module
   ! Purpose    : 計算 3D 四面體固體單元 (Tet4) 之變形、應力與節點等效內力，
   !              並自全域合力 Nodes%fsum 中扣除內力 (F_net = F_ext - F_int)。
   !
   ! [使用說明]
   !   1. 依據 Elements%topo(2:5, e) 讀取四面體之 4 個節點。
   !   2. 透過體積與幾何形狀矩陣計算單元應變與應力 (胡克定律 Linear Elasticity)。
   !   3. 將單元內力加總並透過 OMP ATOMIC 安全地累加扣除至 Nodes%fsum。
   !
   ! [依賴關係]
   !   - USE VFIFE_Data_module (nel, Elements, Nodes, real_kind, int_kind)
   !===========================================================================
   SUBROUTINE calculate_internal_forces()
      ! 修改位置：將 num_elems 改為 nel，並引入材料矩陣 e
      USE VFIFE_Data_module, ONLY: int_kind, real_kind, nel, Elements, Nodes, e
      IMPLICIT NONE

      ! --- 區域變數 ---
      INTEGER(KIND=int_kind) :: elem_idx, k, n, n1, n2, n3, n4, mat_id
      REAL(KIND=real_kind)   :: E_mod, nu_val, lambda, mu
      REAL(KIND=real_kind)   :: x(3, 4), x0(3, 4)
      REAL(KIND=real_kind)   :: f_elem(3, 4)
      REAL(KIND=real_kind)   :: vol0, detJ
      REAL(KIND=real_kind)   :: strain(3, 3), stress(3, 3)

      ! 若無單元資料直接返回
      IF (nel <= 0 .OR. .NOT. ASSOCIATED(Elements%topo)) RETURN

      ! 1. 遍歷所有 3D 四面體單元計算內力 (OpenMP 平行化)
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(elem_idx, k, n, n1, n2, n3, n4, mat_id, E_mod, nu_val, &
      !$OMP         lambda, mu, x, x0, f_elem, vol0, detJ, strain, stress) &
      !$OMP SHARED(nel, Elements, Nodes, e)
      DO elem_idx = 1, nel
         ! 取得四面體的 4 個節點編號 (topo(2:5, elem_idx))
         n1 = Elements%topo(2, elem_idx)
         n2 = Elements%topo(3, elem_idx)
         n3 = Elements%topo(4, elem_idx)
         n4 = Elements%topo(5, elem_idx)

         ! 取得節點當前座標與初始座標
         x(:, 1) = Nodes%xc(:, n1);  x0(:, 1) = Nodes%xc0(:, n1)
         x(:, 2) = Nodes%xc(:, n2);  x0(:, 2) = Nodes%xc0(:, n2)
         x(:, 3) = Nodes%xc(:, n3);  x0(:, 3) = Nodes%xc0(:, n3)
         x(:, 4) = Nodes%xc(:, n4);  x0(:, 4) = Nodes%xc0(:, n4)

         ! 從材料表存取材料 parameters (假設 mat(1, e) 為 material ID, e(1,:) 為 E, e(2,:) 為 nu)
         mat_id = Elements%mat(1, elem_idx)
         E_mod  = e(1, mat_id)
         nu_val = e(2, mat_id)
         mu     = E_mod / (2.0_real_kind * (1.0_real_kind + nu_val))
         lambda = (E_mod * nu_val) / ((1.0_real_kind + nu_val) * (1.0_real_kind - 2.0_real_kind * nu_val))

         ! 2. 計算初始幾何與體積
         detJ = (x0(1,2)-x0(1,1)) * ((x0(2,3)-x0(2,1))*(x0(3,4)-x0(3,1)) - (x0(3,3)-x0(3,1))*(x0(2,4)-x0(2,1))) - &
            (x0(2,2)-x0(2,1)) * ((x0(1,3)-x0(1,1))*(x0(3,4)-x0(3,1)) - (x0(3,3)-x0(3,1))*(x0(1,4)-x0(1,1))) + &
            (x0(3,2)-x0(3,1)) * ((x0(1,3)-x0(1,1))*(x0(2,4)-x0(2,1)) - (x0(2,3)-x0(2,1))*(x0(1,4)-x0(1,1)))
         vol0 = ABS(detJ) / 6.0_real_kind

         IF (vol0 <= 1.0e-14_real_kind) CYCLE

         ! 3. 計算柯西-格林微小應變
         strain = 0.0_real_kind
         DO k = 1, 3
            strain(k, k) = ((x(k, 2)-x0(k, 2)) - (x(k, 1)-x0(k, 1))) / MAX(ABS(x0(k, 2)-x0(k, 1)), 1.0e-8_real_kind)
         END DO

         ! 4. 計算柯西應力
         stress = 2.0_real_kind * mu * strain
         stress(1,1) = stress(1,1) + lambda * (strain(1,1) + strain(2,2) + strain(3,3))
         stress(2,2) = stress(2,2) + lambda * (strain(1,1) + strain(2,2) + strain(3,3))
         stress(3,3) = stress(3,3) + lambda * (strain(1,1) + strain(2,2) + strain(3,3))

         ! 5. 計算節點等效內力 f_elem
         DO n = 1, 4
            f_elem(1, n) = (stress(1,1) + stress(1,2) + stress(1,3)) * vol0 * 0.25_real_kind
            f_elem(2, n) = (stress(2,1) + stress(2,2) + stress(2,3)) * vol0 * 0.25_real_kind
            f_elem(3, n) = (stress(3,1) + stress(3,2) + stress(3,3)) * vol0 * 0.25_real_kind
         END DO

         ! 6. 將內力扣除至全域合力陣列 (OMP ATOMIC)
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

      ! 7. 驗證訊息
      IF (nel > 0) THEN
         WRITE(*, '(A, I0, A)') '   [Int Force Check] Elements evaluated. (nel = ', nel, ')'
      END IF

   END SUBROUTINE calculate_internal_forces



   !===========================================================================
   ! Subroutine : update_kinematics
   ! Purpose    : 剛體 6-DOF 時間積分 (3-DOF 平移 + Body Frame 3-DOF 旋轉)
   !              並完成四元數更新與節點空間座標/速度重建
   !===========================================================================
   SUBROUTINE update_kinematics(dt)
      IMPLICIT NONE
      REAL(KIND=8), INTENT(IN) :: dt

      INTEGER(KIND=int_kind)   :: i
      REAL(KIND=8)             :: r_vec(3), arm_vec(3), torque_i(3)
      REAL(KIND=8)             :: T_body(3), I_w(3), w_cross_Iw(3), rhs_body(3)
      REAL(KIND=8)             :: dq(4), omega_quat(4)
      REAL(KIND=8)             :: r_body0(3), r_global(3), v_rot(3)

      ! ----------------------------------------------------------------------
      ! 階段 1: 合力與合力矩對質心歸納 (CoM Force & Torque Reduction)
      ! ----------------------------------------------------------------------
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

      ! [驗證程式碼] 列印剛體動力學狀態與力矩平衡驗證
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

   ! 矩陣向量乘法: res = A * x
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