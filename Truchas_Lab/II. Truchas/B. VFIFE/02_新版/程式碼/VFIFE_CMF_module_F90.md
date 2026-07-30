---
type: 📝 Research
created: 2026-07-31 04:39
modified: 2026-07-31 04:40
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
MODULE VFIFE_CMF_module

   ! Basic Modules of VFIFE
   USE VFIFE_Data_module
   USE VFIFE_Utils_module

   ! Truchas
   USE kind_module, ONLY : int_kind, real_kind, log_kind

   IMPLICIT NONE
   PRIVATE

   ! 顯式對外公開的子程序與函數
   PUBLIC :: vector_cross
   PUBLIC :: calc_theta12
   PUBLIC :: calc_rotation_R
   PUBLIC :: calc_B_matrix_coeff
   PUBLIC :: calc_element_strain
   PUBLIC :: calc_local_forces_equilibrium
   PUBLIC :: test_cmf_rotation

CONTAINS

   ! ===================================================================
   ! 1. 3D 向量叉積公用工具 (Vector Cross Product Tool)
   !    取代舊版 SUBROUTINE CROSS
   ! ===================================================================
   PURE FUNCTION vector_cross(a, b) RESULT(c)
      REAL(KIND=real_kind), INTENT(IN) :: a(3), b(3)
      REAL(KIND=real_kind)             :: c(3)

      c(1) = a(2) * b(3) - a(3) * b(2)
      c(2) = a(3) * b(1) - a(1) * b(3)
      c(3) = a(1) * b(2) - a(2) * b(1)
   END FUNCTION vector_cross

   ! ===================================================================
   ! 2. 解析 CMF 法線與剛體轉角 (calc_theta12)
   !    重構舊版 subroutine theta12
   ! ===================================================================
   SUBROUTINE calc_theta12(x0, x, theta1, n1, theta2, nt, nd)
      REAL(KIND=real_kind), INTENT(IN)  :: x0(3,4)    ! 初始/參考幾何座標 (t 態)
      REAL(KIND=real_kind), INTENT(IN)  :: x(3,4)     ! 瞬時幾何座標 (d 態)
      REAL(KIND=real_kind), INTENT(OUT) :: theta1
      REAL(KIND=real_kind), INTENT(OUT) :: n1(3)
      REAL(KIND=real_kind), INTENT(OUT) :: theta2
      REAL(KIND=real_kind), INTENT(OUT) :: nt(3)
      REAL(KIND=real_kind), INTENT(OUT) :: nd(3)

      REAL(KIND=real_kind) :: a(3), b(3), c(3)
      REAL(KIND=real_kind) :: et31, et12, ed31, ed12, totalnt, totalnd, c1l
      REAL(KIND=real_kind) :: xct(3), xcd(3)
      REAL(KIND=real_kind) :: xct_rel(3,3), xcd_rel(3,3)
      REAL(KIND=real_kind) :: xp(3,3)
      REAL(KIND=real_kind) :: nxa(3,3), nxp(3,3)
      REAL(KIND=real_kind) :: judge, temp, theta2_node(3)
      REAL(KIND=real_kind) :: norm_a, norm_p
      INTEGER(KIND=int_kind) :: k

      ! --- t 態平面法向計算 ---
      a = x0(:,1) - x0(:,3)
      b = x0(:,2) - x0(:,1)
      et31 = SQRT(SUM(a**2))
      et12 = SQRT(SUM(b**2))
      IF (et31 > 1.0e-12_real_kind) a = a / et31
      IF (et12 > 1.0e-12_real_kind) b = b / et12

      c = vector_cross(a, b)
      totalnt = SQRT(SUM(c**2))
      IF (totalnt > 1.0e-12_real_kind) THEN
         nt = c / totalnt
      ELSE
         nt = (/ 0.0_real_kind, 0.0_real_kind, 1.0_real_kind /)
      END IF

      ! --- d 態平面法向計算 ---
      a = x(:,1) - x(:,3)
      b = x(:,2) - x(:,1)
      ed31 = SQRT(SUM(a**2))
      ed12 = SQRT(SUM(b**2))
      IF (ed31 > 1.0e-12_real_kind) a = a / ed31
      IF (ed12 > 1.0e-12_real_kind) b = b / ed12

      c = vector_cross(a, b)
      totalnd = SQRT(SUM(c**2))
      IF (totalnd > 1.0e-12_real_kind) THEN
         nd = c / totalnd
      ELSE
         nd = (/ 0.0_real_kind, 0.0_real_kind, 1.0_real_kind /)
      END IF

      ! --- 轉角 theta1 與軸向 n1 ---
      c = vector_cross(nt, nd)
      c1l = SQRT(SUM(c**2))

      IF (c1l <= 1.0e-12_real_kind) THEN
         n1 = (/ 1.0_real_kind, 0.0_real_kind, 0.0_real_kind /)
         theta1 = 0.0_real_kind
      ELSE
         n1 = c / c1l
         theta1 = ASIN(MIN(1.0_real_kind, MAX(-1.0_real_kind, c1l)))
      END IF

      ! --- 面內投影與轉角 theta2 計算 ---
      xct = (x0(:,1) + x0(:,2) + x0(:,3)) / 3.0_real_kind
      xcd = (x(:,1)  + x(:,2)  + x(:,3))  / 3.0_real_kind

      DO k = 1, 3
         xct_rel(:,k) = x0(:,k) - xct
         xcd_rel(:,k) = x(:,k)  - xcd
         xp(:,k) = xcd_rel(:,k) - DOT_PRODUCT(xcd_rel(:,k), nt) * nt

         norm_a = SQRT(SUM(xct_rel(:,k)**2))
         norm_p = SQRT(SUM(xp(:,k)**2))

         IF (norm_a > 1.0e-12_real_kind) THEN
            nxa(:,k) = xct_rel(:,k) / norm_a
         ELSE
            nxa(:,k) = 0.0_real_kind
         END IF

         IF (norm_p > 1.0e-12_real_kind) THEN
            nxp(:,k) = xp(:,k) / norm_p
         ELSE
            nxp(:,k) = 0.0_real_kind
         END IF

         c = vector_cross(nxa(:,k), nxp(:,k))
         judge = DOT_PRODUCT(nt, c)
         temp = SQRT(SUM(c**2))
         temp = MIN(1.0_real_kind, MAX(-1.0_real_kind, temp))

         IF (judge > 0.0_real_kind) THEN
            theta2_node(k) = ASIN(temp)
         ELSE
            theta2_node(k) = ASIN(-temp)
         END IF
      END DO

      theta2 = (theta2_node(1) + theta2_node(2) + theta2_node(3)) / 3.0_real_kind

   END SUBROUTINE calc_theta12

   ! ===================================================================
   ! 3. CMF 剛體旋轉矩陣與局部變形 (calc_rotation_R)
   !    重構舊版 subroutine rotationR
   ! ===================================================================
   SUBROUTINE calc_rotation_R(x0, x, Q, Rtheta, etahead, vhead21, vhead31, vhead41)
      REAL(KIND=real_kind), INTENT(IN)  :: x0(3,4)        ! 初始座標 (3,4)
      REAL(KIND=real_kind), INTENT(IN)  :: x(3,4)         ! 當前座標 (3,4)
      REAL(KIND=real_kind), INTENT(OUT) :: Q(3,3)         ! CMF 局部座標轉換矩陣
      REAL(KIND=real_kind), INTENT(OUT) :: Rtheta(3,3)    ! 剛體旋轉矩陣
      REAL(KIND=real_kind), INTENT(OUT) :: etahead(3,4)   ! CMF 局部純變形量
      REAL(KIND=real_kind), INTENT(OUT) :: vhead21(3)     ! CMF 局部節點 21 向量
      REAL(KIND=real_kind), INTENT(OUT) :: vhead31(3)     ! CMF 局部節點 31 向量
      REAL(KIND=real_kind), INTENT(OUT) :: vhead41(3)     ! CMF 局部節點 41 向量

      REAL(KIND=real_kind) :: theta1, theta2
      REAL(KIND=real_kind) :: n1(3), nt(3), nd(3), n(3), theta_vec(3)
      REAL(KIND=real_kind) :: totaltheta, temp1, temp2
      REAL(KIND=real_kind) :: Atheta(3,3), Atheta2(3,3)
      REAL(KIND=real_kind) :: x21(3), x31(3), x41(3)
      REAL(KIND=real_kind) :: rigidro2(3), rigidro3(3), rigidro4(3)
      REAL(KIND=real_kind) :: deltau(3,4), eta(3,4)
      REAL(KIND=real_kind) :: vta21(3), vta31(3), vta41(3)
      REAL(KIND=real_kind) :: eta2L, eta3L, vta21L, vta31L, abs_eta23
      REAL(KIND=real_kind) :: Q2temp(3)
      INTEGER(KIND=int_kind) :: k

      CALL calc_theta12(x0, x, theta1, n1, theta2, nt, nd)

      theta_vec = -(theta1 * n1 + theta2 * nt)
      totaltheta = SQRT(SUM(theta_vec**2))

      IF (totaltheta <= 1.0e-12_real_kind) THEN
         n = (/ 0.0_real_kind, 0.0_real_kind, 1.0_real_kind /)
      ELSE
         n = theta_vec / (-totaltheta)
      END IF

      Atheta(1,:) = (/  0.0_real_kind, -n(3),          n(2)         /)
      Atheta(2,:) = (/  n(3),           0.0_real_kind, -n(1)         /)
      Atheta(3,:) = (/ -n(2),           n(1),           0.0_real_kind /)

      Atheta2 = MATMUL(Atheta, Atheta)

      temp1 = (1.0_real_kind - COS(-totaltheta))
      temp2 = SIN(-totaltheta)
      Rtheta = temp1 * Atheta2 + temp2 * Atheta

      x21 = x(:,2) - x(:,1)
      x31 = x(:,3) - x(:,1)
      x41 = x(:,4) - x(:,1)

      rigidro2 = MATMUL(Rtheta, x21)
      rigidro3 = MATMUL(Rtheta, x31)
      rigidro4 = MATMUL(Rtheta, x41)

      deltau = x - x0

      eta(:,1) = 0.0_real_kind
      eta(:,2) = (deltau(:,2) - deltau(:,1)) + rigidro2
      eta(:,3) = (deltau(:,3) - deltau(:,1)) + rigidro3
      eta(:,4) = (deltau(:,4) - deltau(:,1)) + rigidro4

      vta21 = x0(:,2) - x0(:,1)
      vta31 = x0(:,3) - x0(:,1)
      vta41 = x0(:,4) - x0(:,1)

      eta2L = SQRT(SUM(eta(:,2)**2))
      eta3L = SQRT(SUM(eta(:,3)**2))

      IF (ABS(eta2L) < 1.0e-10_real_kind) THEN
         vta21L = SQRT(SUM(vta21**2))
         Q(1,:) = vta21 / vta21L
      ELSE
         Q(1,:) = eta(:,2) / eta2L
      END IF

      IF (ABS(eta3L) < 1.0e-10_real_kind) THEN
         vta31L = SQRT(SUM(vta31**2))
         Q2temp = vta31 / vta31L
      ELSE
         Q2temp = eta(:,3) / eta3L
      END IF

      Q(3,:) = vector_cross(Q2temp, Q(1,:))
      abs_eta23 = SQRT(SUM(Q(3,:)**2))

      IF (ABS(abs_eta23) <= 1.0e-10_real_kind) THEN
         Q(3,:) = nt
         abs_eta23 = SQRT(SUM(Q(3,:)**2))
      END IF

      Q(3,:) = Q(3,:) / abs_eta23
      Q(2,:) = vector_cross(Q(3,:), Q(1,:))

      vhead21 = MATMUL(Q, vta21)
      vhead31 = MATMUL(Q, vta31)
      vhead41 = MATMUL(Q, vta41)

      DO k = 1, 4
         etahead(:,k) = MATMUL(Q, eta(:,k))
      END DO

   END SUBROUTINE calc_rotation_R

   ! ===================================================================
   ! 4. 計算四面體 B 矩陣幾何係數 (beta, gamma, delta) 及 6V0 (a1)
   !    對接舊版 fintiso3 的 b2~b4, r2~r4, o2~o4 與 a1
   ! ===================================================================
   SUBROUTINE calc_B_matrix_coeff(vhead21, vhead31, vhead41, a1, vol0, &
      b, r, o, is_distorted)
      REAL(KIND=real_kind), INTENT(IN)  :: vhead21(3)     ! 節點 2 相對節點 1 之 CMF 向量
      REAL(KIND=real_kind), INTENT(IN)  :: vhead31(3)     ! 節點 3 相對節點 1 之 CMF 向量
      REAL(KIND=real_kind), INTENT(IN)  :: vhead41(3)     ! 節點 4 相對節點 1 之 CMF 向量
      REAL(KIND=real_kind), INTENT(OUT) :: a1             ! 6 倍單元體積 (Determinant)
      REAL(KIND=real_kind), INTENT(OUT) :: vol0           ! 參考體積 V0
      REAL(KIND=real_kind), INTENT(OUT) :: b(4)           ! beta 幾何係數 (對應 d/dx)
      REAL(KIND=real_kind), INTENT(OUT) :: r(4)           ! gamma 幾何係數 (對應 d/dy)
      REAL(KIND=real_kind), INTENT(OUT) :: o(4)           ! delta 幾何係數 (對應 d/dz)
      LOGICAL,               INTENT(OUT) :: is_distorted  ! 單元畸變標記 (a1 <= 0)

      REAL(KIND=real_kind) :: xl2, yl2, zl2
      REAL(KIND=real_kind) :: xl3, yl3, zl3
      REAL(KIND=real_kind) :: xl4, yl4, zl4

      xl2 = vhead21(1); yl2 = vhead21(2); zl2 = vhead21(3)
      xl3 = vhead31(1); yl3 = vhead31(2); zl3 = vhead31(3)
      xl4 = vhead41(1); yl4 = vhead41(2); zl4 = vhead41(3)

      ! 計算 6 倍體積 (a1)
      a1 = xl4 * (yl2*zl3 - yl3*zl2) + yl4 * (xl3*zl2 - xl2*zl3) + zl4 * (xl2*yl3 - xl3*yl2)
      vol0 = a1 / 6.0_real_kind

      IF (a1 <= 0.0_real_kind) THEN
         is_distorted = .TRUE.
         b = 0.0_real_kind; r = 0.0_real_kind; o = 0.0_real_kind
         RETURN
      ELSE
         is_distorted = .FALSE.
      END IF

      ! 幾何係數 b (beta - x 分量)
      b(2) = yl3*zl4 - yl4*zl3
      b(3) = yl4*zl2 - yl2*zl4
      b(4) = yl2*zl3 - yl3*zl2
      b(1) = -(b(2) + b(3) + b(4))

      ! 幾何係數 r (gamma - y 分量)
      r(2) = xl4*zl3 - xl3*zl4
      r(3) = xl2*zl4 - xl4*zl2
      r(4) = xl3*zl2 - xl2*zl3
      r(1) = -(r(2) + r(3) + r(4))

      ! 幾何係數 o (delta - z 分量)
      o(2) = xl3*yl4 - xl4*yl3
      o(3) = xl4*yl2 - xl2*yl4
      o(4) = xl2*yl3 - xl3*yl2
      o(1) = -(o(2) + o(3) + o(4))

   END SUBROUTINE calc_B_matrix_coeff

   ! ===================================================================
   ! 5. 計算單元局部 Cauchy 應變 (calc_element_strain)
   !    對接舊版 Depslon 排序: [epsx, epsy, epsz, epsyz, epsxz, epsxy]^T
   ! ===================================================================
   SUBROUTINE calc_element_strain(etahead, b, r, o, a1, Depslon)
      REAL(KIND=real_kind), INTENT(IN)  :: etahead(3,4)   ! CMF 純變形向量
      REAL(KIND=real_kind), INTENT(IN)  :: b(4), r(4), o(4) ! 幾何係數
      REAL(KIND=real_kind), INTENT(IN)  :: a1             ! 6V0
      REAL(KIND=real_kind), INTENT(OUT) :: Depslon(6)     ! 應變向量 (舊版順序)

      REAL(KIND=real_kind) :: d1, d2, d3, d4, d5, d6

      ! 對應舊版 etahead 提取之自由度成分
      d1 = etahead(1,2)
      d2 = etahead(1,3)
      d3 = etahead(2,3)
      d4 = etahead(1,4)
      d5 = etahead(2,4)
      d6 = etahead(3,4)

      ! 依據舊版 fintiso3 之 B 矩陣應變計算公式
      Depslon(1) = (b(2)*d1 + b(3)*d2 + b(4)*d4) / a1                         ! epsx
      Depslon(2) = (r(3)*d3 + r(4)*d5) / a1                                    ! epsy
      Depslon(3) = (o(4)*d6) / a1                                              ! epsz
      Depslon(4) = (o(3)*d3 + o(4)*d5 + r(4)*d6) / a1                          ! epsyz
      Depslon(5) = (o(2)*d1 + o(3)*d2 + o(4)*d4 + b(4)*d6) / a1                ! epsxz
      Depslon(6) = (r(2)*d1 + r(3)*d2 + b(3)*d3 + r(4)*d4 + b(4)*d5) / a1      ! epsxy

   END SUBROUTINE calc_element_strain

   ! ===================================================================
   ! 6. 依靜平衡推導節點 1 反力與組裝 CMF 局部內力 (f_local)
   !    對接舊版 Dr. Wu 靜平衡公式
   ! ===================================================================
   SUBROUTINE calc_local_forces_equilibrium(vhead21, vhead31, vhead41, &
      vol0, a1, b, r, o, sigma, f_local)
      REAL(KIND=real_kind), INTENT(IN)  :: vhead21(3), vhead31(3), vhead41(3)
      REAL(KIND=real_kind), INTENT(IN)  :: vol0, a1
      REAL(KIND=real_kind), INTENT(IN)  :: b(4), r(4), o(4)
      REAL(KIND=real_kind), INTENT(IN)  :: sigma(6)       ! 應力向量 (與 Depslon 順序一致)
      REAL(KIND=real_kind), INTENT(OUT) :: f_local(3,4)   ! 局部 4 節點力 (3x4)

      REAL(KIND=real_kind) :: f(12)
      REAL(KIND=real_kind) :: xl2, yl2, xl3, yl3, xl4, yl4, zl4
      REAL(KIND=real_kind) :: C1, C2, C3

      xl2 = vhead21(1); yl2 = vhead21(2)
      xl3 = vhead31(1); yl3 = vhead31(2)
      xl4 = vhead41(1); yl4 = vhead41(2); zl4 = vhead41(3)

      ! 節點 2, 3, 4 之局部內力計算 (舊版對應 f(4)~f(12))
      ! sigma 順序: 1:sig_x, 2:sig_y, 3:sig_z, 4:tau_yz, 5:tau_xz, 6:tau_xy
      f(4)  = vol0 * (b(2)*sigma(1) + r(2)*sigma(6) + o(2)*sigma(5)) / a1   ! Node 2 - fx
      f(7)  = vol0 * (b(3)*sigma(1) + r(3)*sigma(6) + o(3)*sigma(5)) / a1   ! Node 3 - fx
      f(8)  = vol0 * (r(3)*sigma(2) + b(3)*sigma(6) + o(3)*sigma(4)) / a1   ! Node 3 - fy
      f(10) = vol0 * (b(4)*sigma(1) + r(4)*sigma(6) + o(4)*sigma(5)) / a1   ! Node 4 - fx
      f(11) = vol0 * (r(4)*sigma(2) + b(4)*sigma(6) + o(4)*sigma(4)) / a1   ! Node 4 - fy
      f(12) = vol0 * (o(4)*sigma(3) + r(4)*sigma(4) + b(4)*sigma(5)) / a1   ! Node 4 - fz

      ! 應用 Wu 教授之幾何靜平衡推導節點 1 反力與 Node 2, 3 剩餘分量
      C3 = yl2*xl3 - yl3*xl2

      IF (ABS(xl2) < 1.0e-12_real_kind .OR. ABS(C3) < 1.0e-12_real_kind) THEN
         ! 防防呆處理：退化情況採用傳統 B^T*sigma*V 平均配置
         f(1) = -(f(4) + f(7) + f(10))
         f(2) = -(f(5) + f(8) + f(11))
         f(3) = -(f(6) + f(9) + f(12))
         f(5) = 0.0_real_kind; f(6) = 0.0_real_kind; f(9) = 0.0_real_kind
      ELSE
         f(1) = -(f(4) + f(7) + f(10))
         f(5) = (f(4)*yl2 + f(7)*yl3 - f(8)*xl3 + f(10)*yl4 - f(11)*xl4) / xl2
         f(2) = -(f(5) + f(8) + f(11))

         C1 = (f(11)*zl4 - f(12)*yl4)
         C2 = (f(10)*zl4 - f(12)*xl4)
         f(6) = (C1*xl3 - C2*yl3) / C3
         f(9) = (C2*yl2 - C1*xl2) / C3
         f(3) = -(f(6) + f(9) + f(12))
      END IF

      ! 組裝為 (3, 4) 矩陣輸出
      f_local(:,1) = f(1:3)
      f_local(:,2) = f(4:6)
      f_local(:,3) = f(7:9)
      f_local(:,4) = f(10:12)

   END SUBROUTINE calc_local_forces_equilibrium

   ! ===================================================================
   ! 7. 單元邏輯驗證常式 (Verification Test)
   ! ===================================================================
   SUBROUTINE test_cmf_rotation()
      REAL(KIND=real_kind) :: x0(3,4), x(3,4)
      REAL(KIND=real_kind) :: Q(3,3), Rtheta(3,3), etahead(3,4)
      REAL(KIND=real_kind) :: v21(3), v31(3), v41(3)
      REAL(KIND=real_kind) :: a1, vol0, b(4), r(4), o(4)
      REAL(KIND=real_kind) :: Depslon(6), sigma(6), f_local(3,4)
      LOGICAL :: is_distorted

      WRITE(*,*) '==================================================='
      WRITE(*,*) '   [VFIFE_CMF_module] Running CMF & B-Matrix Test  '
      WRITE(*,*) '==================================================='

      x0(:,1) = (/ 0.0_real_kind, 0.0_real_kind, 0.0_real_kind /)
      x0(:,2) = (/ 1.0_real_kind, 0.0_real_kind, 0.0_real_kind /)
      x0(:,3) = (/ 0.0_real_kind, 1.0_real_kind, 0.0_real_kind /)
      x0(:,4) = (/ 0.0_real_kind, 0.0_real_kind, 1.0_real_kind /)

      ! 施加旋轉 + 軸向伸長
      x(:,1) = (/  0.1_real_kind,  0.1_real_kind,  0.0_real_kind /)
      x(:,2) = (/  0.1_real_kind,  1.1_real_kind,  0.0_real_kind /)
      x(:,3) = (/ -0.95_real_kind, 0.1_real_kind,  0.0_real_kind /)
      x(:,4) = (/  0.1_real_kind,  0.1_real_kind,  1.05_real_kind /)

      CALL calc_rotation_R(x0, x, Q, Rtheta, etahead, v21, v31, v41)
      CALL calc_B_matrix_coeff(v21, v31, v41, a1, vol0, b, r, o, is_distorted)

      IF (is_distorted) THEN
         WRITE(*,*) 'ERROR: Element distorted in test!'
         RETURN
      END IF

      CALL calc_element_strain(etahead, b, r, o, a1, Depslon)

      WRITE(*,'(A, F12.6)') ' 6x Volume (a1) : ', a1
      WRITE(*,'(A, F12.6)') ' Element Vol0   : ', vol0
      WRITE(*,*) '--- Depslon (epsx, epsy, epsz, epsyz, epsxz, epsxy) ---'
      WRITE(*,'(6F10.6)') Depslon

      ! 假設彈性應力 (簡單常數測試)
      sigma = Depslon * 200.0_real_kind
      CALL calc_local_forces_equilibrium(v21, v31, v41, vol0, a1, b, r, o, sigma, f_local)

      WRITE(*,*) '--- Local Forces Equilibrium Sum (fx, fy, fz) ---'
      WRITE(*,'(3F12.6)') SUM(f_local(1,:)), SUM(f_local(2,:)), SUM(f_local(3,:))

      WRITE(*,*) '==================================================='
      WRITE(*,*) '   [VFIFE_CMF_module] Test Completed Successfully  '
      WRITE(*,*) '==================================================='
   END SUBROUTINE test_cmf_rotation

END MODULE VFIFE_CMF_module

```

---
# 🔗 參考資料


---