---
type: 📝 Research
created: 2026-06-04 03:10
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

建立固體資訊

---
# 📝 內容紀錄
```fortran
MODULE VFIFE_Setup_module

   ! Basic Modules of VFIFE
   USE VFIFE_Utils_module
   USE VFIFE_Data_module
   USE VFIFE_Parallel_module

   ! Truchas
   USE mesh_gen_module,        only: x_axis, y_axis, z_axis
   USE property_data_module,   only: density
   USE kind_module,            only: int_kind, real_kind, log_kind

   ! Parallel
   use parallel_info_module,   only: p_info
   use pgslib_module,          only: PGSLib_GLOBAL_SUM, PGSlib_Collate, pgslib_dist





   IMPLICIT NONE


   PUBLIC :: V5Setup
   PUBLIC :: Geometry
   PUBLIC :: nodemass
   PUBLIC :: compute_body_mass_properties
   PUBLIC :: face_judgement


CONTAINS



   SUBROUTINE V5Setup()
      IMPLICIT NONE

      ! 計算四面體幾何屬性
      CALL Geometry()
      !WRITE(*,*) ' [V5Setup] Geometry finish'

      ! 計算質量
      ! 節點質量計算：剛體僅初始化執行一次；可變形體每步重新計算
      IF (.NOT. is_V5_deformable .AND. .NOT. is_V5_initialized) THEN
         CALL nodemass()
      ELSE IF (is_V5_deformable) THEN
         CALL nodemass()
      END IF
      !WRITE(*,*) ' [V5Setup] nodemass finish'

      ! 計算密度
      density(V5_mat_id) = sum(elem_mass) / sum(elem_vol)

      ! === 修改內容：呼叫剛體/可變形體通用的物理屬性計算 ===
      CALL compute_body_mass_properties()
      !WRITE(*,*) ' [V5Setup] compute_body_mass_properties finish'


      ! 計算面判定
      ! 網格外接面拓撲判斷：無論剛體或可變形體，拓撲結構不變，僅需初始化執行一次
      IF (.NOT. is_V5_initialized) THEN
         CALL face_judgement()
         !WRITE(*,*) ' [V5Setup] face_judgement finish'
      END IF


      ! 計算 AABB 範圍
      CALL compute_solid_aabb()
      !WRITE(*,*) ' [V5Setup] compute_solid_aabb finish'

      ! 計算外露面快取
      CALL build_surface_cache()
      !WRITE(*,*) ' [V5Setup] build_surface_cache finish'
      ! 驗證程式碼：確認 surf_node 座標是否有隨時間微幅改變
      !WRITE(*,*) ' [V5Setup] Time Step ', V5_time, ' Surf Node 1 Z:', surf_node1(3, 1)


   END SUBROUTINE V5Setup




   SUBROUTINE Geometry()
      ! =========================================================
      ! Geometry: 計算四面體幾何屬性 (頂點、形心、質心、面法向、體積)
      ! =========================================================
      IMPLICIT NONE
      INTEGER :: i
      INTEGER :: n1, n2, n3, n4
      REAL(8) :: p1(3), p2(3), p3(3), p4(3)
      REAL(8) :: x21, y21, z21, x31, y31, z31, x41, y41, z41
      REAL(8) :: f_area(4), f_norm(3, 4)
      INTEGER :: OMP_GET_NUM_THREADS, OMP_GET_THREAD_NUM

      IF (.NOT. ALLOCATED(elem_topo) .OR. .NOT. ALLOCATED(x_coord)) THEN
         WRITE(*,*) "Fatal: [Geometry] Required arrays are not allocated."
         STOP
      END IF

#ifdef _OPENMP
      ! 1. 手動宣告 OpenMP 函式為整數型別（免 use omp_lib）
      !INTEGER :: OMP_GET_NUM_THREADS, OMP_GET_THREAD_NUM

      !$OMP PARALLEL
      !$OMP SINGLE
      if (.NOT. is_V5_initialized) THEN
         WRITE(*,*) ' [OMP Status] Active (OpenMP Enabled)'
         WRITE(*,*) ' [OMP Check] Total Threads Allocated:', OMP_GET_NUM_THREADS()
      END IF
      !$OMP END SINGLE

      ! 讓所有平行 Thread 都印出自己的 ID
      if (.NOT. is_V5_initialized) THEN
         WRITE(*,*) ' [OMP Check] Hello:', OMP_GET_THREAD_NUM()
      END IF
      !$OMP END PARALLEL
#else
      WRITE(*,*) ' [OMP Status] Disabled (Sequential Mode)'
#endif



      !$OMP PARALLEL DO PRIVATE(i, n1, n2, n3, n4, p1, p2, p3, p4, &
      !$OMP                     x21, y21, z21, x31, y31, z31, x41, y41, z41, &
      !$OMP                     f_area, f_norm) &
      !$OMP SHARED(nel, elem_topo, x_coord, elem_vertices, elem_facecenter, &
      !$OMP        elem_center, elem_area, elem_normal, elem_vol)
      DO i = 1, nel

         ! 1. 取得頂點索引與 3D 座標
         n1 = elem_topo(2, i); n2 = elem_topo(3, i)
         n3 = elem_topo(4, i); n4 = elem_topo(5, i)

         p1 = x_coord(1:3, n1)
         p2 = x_coord(1:3, n2)
         p3 = x_coord(1:3, n3)
         p4 = x_coord(1:3, n4)

         ! 2. 儲存���點座標 elem_vertices(3, 4, nel)
         elem_vertices(:, 1, i) = p1
         elem_vertices(:, 2, i) = p2
         elem_vertices(:, 3, i) = p3
         elem_vertices(:, 4, i) = p4

         ! 3. 計算 4 個面的形心 elem_facecenter(3, 4, nel)
         elem_facecenter(:, 1, i) = (p2 + p3 + p4) / 3.0d0
         elem_facecenter(:, 2, i) = (p1 + p3 + p4) / 3.0d0
         elem_facecenter(:, 3, i) = (p1 + p2 + p4) / 3.0d0
         elem_facecenter(:, 4, i) = (p1 + p2 + p3) / 3.0d0

         ! 4. 計算單元質心 elem_center(3, nel)
         elem_center(:, i) = (p1 + p2 + p3 + p4) / 4.0d0

         ! 5. ���算各面之面積與指向外側之單位法向量
         ! 修���後 (確保繞向與 build_surface_cache 統�����)：
         ! Face 1: N2-N3-N4
         CALL compute_face_geom(p2, p3, p4, p1, f_area(1), f_norm(:, 1))
         ! Face 2: N1-N4-N3
         CALL compute_face_geom(p1, p4, p3, p2, f_area(2), f_norm(:, 2))
         ! Face 3: N1-N2-N4
         CALL compute_face_geom(p1, p2, p4, p3, f_area(3), f_norm(:, 3))
         ! Face 4: N1-N3-N2
         CALL compute_face_geom(p1, p3, p2, p4, f_area(4), f_norm(:, 4))

         elem_area(:, i)     = f_area
         elem_normal(:,:, i) = f_norm


         ! 6. 四面體體積計算 (純量三重積法)
         IF (.NOT. is_V5_deformable .AND. .NOT. is_V5_initialized) THEN
            x21 = p2(1) - p1(1); y21 = p2(2) - p1(2); z21 = p2(3) - p1(3)
            x31 = p3(1) - p1(1); y31 = p3(2) - p1(2); z31 = p3(3) - p1(3)
            x41 = p4(1) - p1(1); y41 = p4(2) - p1(2); z41 = p4(3) - p1(3)

            elem_vol(i) = (x41 * (y21*z31 - y31*z21) + &
               y41 * (z21*x31 - z31*x21) + &
               z41 * (x21*y31 - x31*y21)) / 6.0d0

            ! 負體積/���轉單元檢查
            IF (elem_vol(i) <= 0.0d0) THEN
               WRITE(*,*) " [Fatal Error] Negative or Zero Volume detected at Element ", &
                  i, ", Vol = ", elem_vol(i)
               STOP "Execution halted due to mesh geometry error."
            END IF
         END IF
      END DO
      !$OMP END PARALLEL DO


   CONTAINS

      ! =========================================================
      ! 內部子程序：計算三角形面面積與外向單位法向量
      ! =========================================================
      SUBROUTINE compute_face_geom(pa, pb, pc, popp, area, normal)
         IMPLICIT NONE
         REAL(8), INTENT(IN)  :: pa(3), pb(3), pc(3), popp(3)
         REAL(8), INTENT(OUT) :: area
         REAL(8), INTENT(OUT) :: normal(3)

         REAL(8) :: u(3), v(3), cross_vec(3), opp_vec(3)
         REAL(8) :: cross_len

         ! 向量 u = pb - pa, v = pc - pa
         u = pb - pa
         v = pc - pa

         ! 外積 cross_vec = u x v
         cross_vec(1) = u(2)*v(3) - u(3)*v(2)
         cross_vec(2) = u(3)*v(1) - u(1)*v(3)
         cross_vec(3) = u(1)*v(2) - u(2)*v(1)

         cross_len = SQRT(cross_vec(1)**2 + cross_vec(2)**2 + cross_vec(3)**2)

         ! 面積 = 外積模長的一半
         area = 0.5d0 * cross_len

         IF (cross_len > 1.0e-12) THEN
            normal = cross_vec / cross_len
         ELSE
            normal = 0.0d0
         END IF

         ! 確保法向量指向單元外部 (與對向點向量點積需小於零)
         opp_vec = popp - pa
         IF (DOT_PRODUCT(normal, opp_vec) > 0.0d0) THEN
            normal = -normal
            ! 如果跑到這裡，代表該單元的頂點順序 (n1,n2,n3,n4) 可能屬於左手系
         END IF

      END SUBROUTINE compute_face_geom

   END SUBROUTINE Geometry

   ! =========================================================
   ! 計算單元體積與質量，分配���加成節點質量
   ! =========================================================
   SUBROUTINE nodemass()

      IMPLICIT NONE
      INTEGER :: i, n1, n2, n3, n4

      ! ��義存放 4 個頂點貢獻的臨時陣列 (4, nel)
      REAL(KIND=8), ALLOCATABLE :: elem_mass_4v(:,:)

      ! 1. 安全性檢���������������������������������������������������������������������
      IF (.NOT. ALLOCATED(elem_topo) .OR. .NOT. ALLOCATED(elem_mat) .OR. &
         .NOT. ALLOCATED(elem_vol) .OR. .NOT. ALLOCATED(node_mass)) THEN
         WRITE(*,*) "Fatal: Required arrays are not allocated in nodemass."
         STOP
      END IF

      ! 2. 初始化與配置
      IF (ALLOCATED(elem_rho)) elem_rho = 0.0d0
      IF (ALLOCATED(elem_mass)) elem_mass = 0.0d0
      IF (ALLOCATED(node_mass)) node_mass = 0.0d0

      ALLOCATE(elem_mass_4v(4, nel))
      elem_mass_4v = 0.0d0

      ! 3. 核心迴圈：OpenMP 算出每個單元給其 4 個頂點的質量貢獻
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, n1, n2, n3, n4) &
      !$OMP SHARED(nel, elem_topo, e, elem_mat, elem_vol, elem_rho, elem_mass, elem_mass_4v, node_mass)
      DO i = 1, nel
         n1 = elem_topo(2, i)
         n2 = elem_topo(3, i)
         n3 = elem_topo(4, i)
         n4 = elem_topo(5, i)

         elem_rho(i) = e(3, elem_mat(1, i))
         elem_mass(i) = elem_vol(i) * elem_rho(i)

         ! 記錄單元對自身的 4 個頂點之貢獻
         elem_mass_4v(1:4, i) = elem_mass(i) / 4.0d0

         ! 本地單元 node_mass 累加 (非跨 Process 縫合時的基礎值)
         !$OMP ATOMIC
         node_mass(n1) = node_mass(n1) + elem_mass_4v(1, i)
         !$OMP ATOMIC
         node_mass(n2) = node_mass(n2) + elem_mass_4v(2, i)
         !$OMP ATOMIC
         node_mass(n3) = node_mass(n3) + elem_mass_4v(3, i)
         !$OMP ATOMIC
         node_mass(n4) = node_mass(n4) + elem_mass_4v(4, i)
      END DO
      !$OMP END PARALLEL DO

      ! =========================================================
      ! 【跨 MPI Process 邊界質量縫合】
      ! =========================================================
      IF (p_info%IsParallel) THEN
         ! 重設 node_mass 並透過 EN_SUM_SCATTER 自動累加並散射回全域 node_mass
         node_mass = 0.0d0
         CALL V5_EN_Sum_Scatter_1D(node_mass, elem_mass_4v)
      END IF
      ! =========================================================

      DEALLOCATE(elem_mass_4v)

      ! 主 Process 印出驗證結果
      IF (p_info%IOP) THEN
         WRITE(*,*) " [nodemass] Sample Node Mass (Node 1):", node_mass(MIN(1, nnd))
         WRITE(*,*) " [nodemass] Sample Node Mass (Node 2):", node_mass(MIN(2, nnd))
         WRITE(*,*) " [nodemass] VFIFE_Mass Total: ", SUM(elem_mass)
         WRITE(*,*) " [nodemass] VFIFE_Volume Total: ", SUM(elem_vol)
      END IF

   END SUBROUTINE nodemass


   ! =========================================================
   ! [全面修復版] 配合 (4, nel) 與 (3, nnd) 記憶體連續性優��的外接面判斷
   ! =========================================================
   SUBROUTINE face_judgement()

      IMPLICIT NONE
      ! ---------------------------------------------------
      ! 局部變數宣告 (Local Variables)
      ! ---------------------------------------------------
      INTEGER :: i, j, m, current, match_count, k
      INTEGER :: n1, n2, n3, n4
      INTEGER :: total_faces

      ! --- 平行化邊界面比對專用變數 ---
      INTEGER :: bnd_face_cnt, global_bnd_cnt, idx
      INTEGER, ALLOCATABLE :: local_bnd_idx(:)
      ! [新增修改] 專門用於收發 PGSLib 0/1 狀態的標準整數陣列
      INTEGER, ALLOCATABLE :: local_bnd_status(:)
      INTEGER(16), ALLOCATABLE :: local_bnd_keys(:), global_bnd_keys(:)
      ! [修改後] 使用 REAL(8) 作為 8-Byte 位元中介陣列，完全相容 PGSLib_Collate 介面
      REAL(8), ALLOCATABLE :: local_keys_r8(:)
      REAL(8), ALLOCATABLE :: global_keys_r8(:)

      INTEGER, ALLOCATABLE :: reconciled_judge(:)
      INTEGER :: total_external_faces, total_internal_faces
      INTEGER :: local_ext_cnt, local_int_cnt
      INTEGER :: f_elem, f_local
      INTEGER :: fn1, fn2, fn3

      ! 使用 128 位元整數儲存特徵碼，防止大規模網格的節���數���乘���位
      INTEGER(16), ALLOCATABLE :: face_keys(:)

      ! 完���調���為���優���結���：���一���度���面的絕對總���號���第二���度���屬性欄位 (1:elem_id, 2:local_face)
      INTEGER, ALLOCATABLE    :: face_mapping(:,:)
      INTEGER, ALLOCATABLE    :: sort_index(:)     ! 一維索引排序陣列
      INTEGER, ALLOCATABLE :: temp_idx(:)
      INTEGER :: count_arr(0:255)
      INTEGER :: pass, shift, byte_val
      INTEGER(16)              :: max_possible_key
      INTEGER                  :: num_passes

      ! ---------------------------------------------------
      ! 1. 安全性檢查與全域記憶體配置
      ! ---------------------------------------------------
      IF (.NOT. ALLOCATED(elem_topo)) THEN
         WRITE(*,*) "Fatal: [face_judgement] elem_topo is not allocated."
         STOP
      END IF

      ! 配合行優先，全域 face_judge 必須是 (4, nel)
      IF (.NOT. ALLOCATED(face_judge)) THEN
         ALLOCATE(face_judge(4, nel))
      END IF

      face_judge = 1 ! 預設全為外接面 (面向液體)
      total_faces = 4 * nel

      ! ---------------------------------------------------
      ! 動態評估安全 Base 與 Key 上限提醒 (已升級至 128-bit 規格)
      ! ---------------------------------------------------
      IF (nnd > 5000000000_8) THEN
         WRITE(*,*) "Warning: [face_judgement] Total nodes (nnd) exceeds 5,000,000,000 extreme safety threshold."
         WRITE(*,*) "         128-bit integer face_key might approach numerical overflow boundary!"
      ELSE
         WRITE(*,*) " [face_judgement] Total nodes (nnd):", nnd, " | 128-bit Face Key max limit: > 5 Billion nodes."
      END IF

      ALLOCATE(face_keys(total_faces))
      ALLOCATE(face_mapping(total_faces, 2))
      ALLOCATE(sort_index(total_faces))



      ! ---------------------------------------------------
      ! 2. 建立每個面的唯一特徵編碼 (Face Key)
      ! ---------------------------------------------------
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, m, n1, n2, n3, n4) &
      !$OMP SHARED(nel, elem_topo, face_keys, face_mapping)
      DO i = 1, nel
         m = (i-1)*4

         n1 = elem_topo(2, i)
         n2 = elem_topo(3, i)
         n3 = elem_topo(4, i)
         n4 = elem_topo(5, i)

         ! 面 1: 缺 N1 頂點 -> (N2, N3, N4)，右手定則法向量朝外
         CALL pack_face(n2, n3, n4, face_keys(m+1))
         face_mapping(m+1, 1) = i
         face_mapping(m+1, 2) = 1

         ! 面 2: 缺 N2 頂點 -> (N1, N4, N3)，右手定則法向量朝外
         CALL pack_face(n1, n4, n3, face_keys(m+2))
         face_mapping(m+2, 1) = i
         face_mapping(m+2, 2) = 2

         ! 面 3: 缺 N3 頂點 -> (N1, N2, N4)，右手定則法向量朝外
         CALL pack_face(n1, n2, n4, face_keys(m+3))
         face_mapping(m+3, 1) = i
         face_mapping(m+3, 2) = 3

         ! 面 4: 缺 N4 頂點 -> (N1, N3, N2)，右手定則法向量朝外
         CALL pack_face(n1, n3, n2, face_keys(m+4))
         face_mapping(m+4, 1) = i
         face_mapping(m+4, 2) = 4
      END DO
      !$OMP END PARALLEL DO

      ! 初始��索引陣列 (1, 2, 3, ..., total_faces)
      DO i = 1, total_faces
         sort_index(i) = i
      END DO

      ! ---------------------------------------------------
      ! 3. 執行高效非遞迴一維 128-bit LSD Radix Sort (O(N) 複雜度)
      ! ---------------------------------------------------
      ! 根據動態 Base 公式 calculated in pack_face 計算 Face Key 的極限最大值
      ! base = nnd + 1 -> Key_max = (nnd * base + nnd) * base + nnd
      max_possible_key = (INT(nnd, 16) * INT(nnd + 1, 16) + INT(nnd, 16)) * INT(nnd + 1, 16) + INT(nnd, 16)

      ! 動態評估需要跑幾個 Byte (128-bit 最高 Pass 1 ~ 16)
      num_passes = 0
      DO WHILE (max_possible_key > 0_16)
         num_passes = num_passes + 1
         max_possible_key = SHIFTR(max_possible_key, 8)
      END DO
      IF (num_passes == 0)  num_passes = 1
      IF (num_passes > 16) num_passes = 16  ! 128-bit ��限�� 16 ���

      WRITE(*,*) " [face_judgement] 128-bit Radix Sort dynamic passes:", num_passes, "/ 16 (Based on nnd:", nnd, ")"

      ALLOCATE(temp_idx(total_faces))

      ! 根據動態計算出的 num_passes 執行必要次數的排序迴圈
      DO pass = 0, num_passes - 1
         shift = pass * 8
         count_arr = 0

         ! (1) 統計 256 個���子���頻��� (��用 255_16 避免型別溢位)
         DO i = 1, total_faces
            byte_val = INT(IAND(SHIFTR(face_keys(sort_index(i)), shift), 255_16))
            count_arr(byte_val) = count_arr(byte_val) + 1
         END DO

         ! (2) 計算前綴和 (Prefix Sum) 決定寫入位置
         DO i = 1, 255
            count_arr(i) = count_arr(i) + count_arr(i-1)
         END DO

         ! (3) 逆向填入以保證 Stability (穩定排序)
         DO i = total_faces, 1, -1
            byte_val = INT(IAND(SHIFTR(face_keys(sort_index(i)), shift), 255_16))
            temp_idx(count_arr(byte_val)) = sort_index(i)
            count_arr(byte_val) = count_arr(byte_val) - 1
         END DO

         ! (4) 更新當前索引順序
         sort_index = temp_idx
      END DO

      DEALLOCATE(temp_idx)

      ! ---------------------------------------------------
      ! 4. 線性對比鄰居：相同的 128 位元特徵碼代表是共用面 (完整防群組漏判修復版)
      ! ---------------------------------------------------
      current = 1
      DO WHILE (current <= total_faces)
         j = current + 1
         ! 尋找連續相同 Key 的面數量
         DO WHILE (j <= total_faces)
            IF (face_keys(sort_index(current)) == face_keys(sort_index(j))) THEN
               j = j + 1
            ELSE
               EXIT
            END IF
         END DO

         match_count = j - current

         ! 若大於等於 2 個面共用此 Key，代表為內部面，全部標記為 0
         IF (match_count >= 2) THEN
            DO k = current, j - 1
               i = sort_index(k)
               face_judge(face_mapping(i, 2), face_mapping(i, 1)) = 0
            END DO
         END IF

         current = j ! 直接跨過整組相同的 Key
      END DO

      ! ---------------------------------------------------
      ! 5. 平行化處理：針對跨 CPU 邊界面的二次比對與縫合 (Reconciliation)
      ! ---------------------------------------------------
      IF (p_info%IsParallel) THEN

         ! (1) 篩選出局部 match_count == 1 且三個頂點皆為 V5_Trace 邊界節點的面
         bnd_face_cnt = 0
         DO i = 1, total_faces
            f_elem  = face_mapping(i, 1)
            f_local = face_mapping(i, 2)

            IF (face_judge(f_local, f_elem) == 1) THEN
               ! 取得該面的 3 個頂點編號
               SELECT CASE (f_local)
                CASE (1)
                  fn1 = elem_topo(3, f_elem); fn2 = elem_topo(4, f_elem); fn3 = elem_topo(5, f_elem)
                CASE (2)
                  fn1 = elem_topo(2, f_elem); fn2 = elem_topo(5, f_elem); fn3 = elem_topo(4, f_elem)
                CASE (3)
                  fn1 = elem_topo(2, f_elem); fn2 = elem_topo(3, f_elem); fn3 = elem_topo(5, f_elem)
                CASE (4)
                  fn1 = elem_topo(2, f_elem); fn2 = elem_topo(4, f_elem); fn3 = elem_topo(3, f_elem)
               END SELECT

               ! 若 3 個頂點存在跨 CPU 邊界 Trace/PE 標記上，計數加 1
               IF (ALLOCATED(V5_Node_PE)) THEN
                  IF (V5_Node_PE(fn1) /= p_info%thisPE .OR. &
                     V5_Node_PE(fn2) /= p_info%thisPE .OR. &
                     V5_Node_PE(fn3) /= p_info%thisPE) THEN
                     bnd_face_cnt = bnd_face_cnt + 1
                  END IF
               END IF
            END IF
         END DO

         ! (2) 提取待比對邊界面的 128-bit Key 與配置發散狀態陣列
         IF (bnd_face_cnt > 0) THEN
            ALLOCATE(local_bnd_keys(bnd_face_cnt))
            ALLOCATE(local_bnd_idx(bnd_face_cnt))
            ! 分配 0/1 狀���陣���並���設��� 1 (外接面)，避�� INTEGER(16) 傳遞給 PGSLib 的型���危機
            ALLOCATE(local_bnd_status(bnd_face_cnt))
            local_bnd_status = 1

            idx = 0
            DO i = 1, total_faces
               f_elem  = face_mapping(i, 1)
               f_local = face_mapping(i, 2)

               IF (face_judge(f_local, f_elem) == 1) THEN
                  SELECT CASE (f_local)
                   CASE (1)
                     fn1 = elem_topo(3, f_elem); fn2 = elem_topo(4, f_elem); fn3 = elem_topo(5, f_elem)
                   CASE (2)
                     fn1 = elem_topo(2, f_elem); fn2 = elem_topo(5, f_elem); fn3 = elem_topo(4, f_elem)
                   CASE (3)
                     fn1 = elem_topo(2, f_elem); fn2 = elem_topo(3, f_elem); fn3 = elem_topo(5, f_elem)
                   CASE (4)
                     fn1 = elem_topo(2, f_elem); fn2 = elem_topo(4, f_elem); fn3 = elem_topo(3, f_elem)
                  END SELECT

                  IF (ALLOCATED(V5_Node_PE)) THEN
                     IF (V5_Node_PE(fn1) /= p_info%thisPE .OR. &
                        V5_Node_PE(fn2) /= p_info%thisPE .OR. &
                        V5_Node_PE(fn3) /= p_info%thisPE) THEN
                        idx = idx + 1
                        local_bnd_keys(idx) = face_keys(i)
                        local_bnd_idx(idx)  = i

                        ! 驗證程式碼：確認第一筆邊界面索引收集正常
                        IF (idx == 1 .AND. p_info%IOP) THEN
                           WRITE(*,*) " [VFIFE_Setup] First boundary face indexed successfully:", local_bnd_keys(1)
                        END IF
                     END IF
                  END IF
               END IF
            END DO
         ELSE
            ALLOCATE(local_bnd_keys(0))
            ALLOCATE(local_bnd_idx(0))
            ALLOCATE(local_bnd_status(0))
         END IF

         ! (3) 利用 PGSLib 將跨 CPU 邊界面特徵碼收集至主節點 (IOP)
         ! [修改後] 增加防禦性檢查與精確 TRANSFER，避免 SIGSEGV
         WRITE(*,*) " [DEBUG Rank", p_info%thisPE, "] bnd_face_cnt =", bnd_face_cnt, &
            " allocated(local_bnd_keys) =", ALLOCATED(local_bnd_keys)
         FLUSH(6)
         IF (ALLOCATED(global_keys_r8)) DEALLOCATE(global_keys_r8)
         IF (ALLOCATED(local_keys_r8))  DEALLOCATE(local_keys_r8)

         ! 1. 安全配置 local_keys_r8
         ALLOCATE(local_keys_r8(2 * bnd_face_cnt))


         IF (bnd_face_cnt > 0 .AND. ALLOCATED(local_bnd_keys)) THEN
            local_keys_r8 = TRANSFER(local_bnd_keys(1:bnd_face_cnt), local_keys_r8)
         END IF

         WRITE(*,*) " [DEBUG Rank", p_info%thisPE, "] Prepared local_keys_r8 successfully."
         FLUSH(6)
         ! 2. 針對 PGSLib Collate 介面進行 IOP 接收端防禦 (若 PGSLib 需要預先配置)
         !    部分 PGSLib 版本要求 global 端傳入前必須先配置好或維持 Unallocated
         !    在此確保 IOP 端的 global_keys_r8 狀態明確
         IF (p_info%IOP) THEN
            IF (.NOT. ALLOCATED(global_keys_r8)) THEN
               ! 若您的 PGSLib 需要預先分配空間，可解開下一行：
               ! ALLOCATE(global_keys_r8(0))
            END IF
         END IF

         IF (p_info%IOP) THEN
            WRITE(*,*) " [DEBUG IOP] Entering PGSlib_Collate..."
            FLUSH(6)
         END IF

         CALL PGSlib_Collate(global_keys_r8, local_keys_r8)

         IF (p_info%IOP) THEN
            WRITE(*,*) " [DEBUG IOP] PGSlib_Collate finished."
            FLUSH(6)
         END IF

         ! 3. 解包資料至 global_bnd_keys
         IF (p_info%IOP) THEN
            IF (ALLOCATED(global_keys_r8)) THEN
               global_bnd_cnt = SIZE(global_keys_r8) / 2
               IF (ALLOCATED(global_bnd_keys)) DEALLOCATE(global_bnd_keys)
               ALLOCATE(global_bnd_keys(global_bnd_cnt))
               IF (global_bnd_cnt > 0) THEN
                  global_bnd_keys = TRANSFER(global_keys_r8(1:2*global_bnd_cnt), global_bnd_keys)
               END IF
            END IF
         END IF

         ! 4. 記憶體清理與驗證輸��
         IF (p_info%IOP) WRITE(*,*) " [DEBUG] Collate check - global_bnd_cnt =", global_bnd_cnt

         IF (ALLOCATED(local_keys_r8))  DEALLOCATE(local_keys_r8)
         IF (ALLOCATED(global_keys_r8)) DEALLOCATE(global_keys_r8)



         IF (p_info%IOP) WRITE(*,*) " [DEBUG] Entering Step 4 (Global Matching)..."
         ! (4) IOP 全域二次比對並更新標記
         ! [修改後] ���加 ALLOCATED 檢查與長度判斷，防止 global_bnd_cnt == 0 時觸發 SIGSEGV
         IF (p_info%IOP) THEN
            IF (ALLOCATED(global_bnd_keys)) THEN
               global_bnd_cnt = SIZE(global_bnd_keys)
            ELSE
               global_bnd_cnt = 0
            END IF

            IF (ALLOCATED(reconciled_judge)) DEALLOCATE(reconciled_judge)
            ALLOCATE(reconciled_judge(global_bnd_cnt))
            reconciled_judge = 1 ! 預設仍為外接面

            ! 只有當邊界面數量大於 1 時才需要進行雙重迴圈比對
            IF (global_bnd_cnt > 1) THEN
               DO i = 1, global_bnd_cnt - 1
                  DO j = i + 1, global_bnd_cnt
                     IF (global_bnd_keys(i) == global_bnd_keys(j)) THEN
                        reconciled_judge(i) = 0
                        reconciled_judge(j) = 0
                     END IF
                  END DO
               END DO
            END IF
         ELSE
            ! 非 IOP Rank 配給長度 0 的空陣列作為安全 Dummy
            IF (ALLOCATED(reconciled_judge)) DEALLOCATE(reconciled_judge)
            ALLOCATE(reconciled_judge(0))
         END IF
         IF (p_info%IOP) WRITE(*,*) " [DEBUG] Step 4 Finished."

         ! (5) 將 IOP 縫合結果發散 (DISTRIBUTE) 回各 PE 並更新局部的 face_judge
         ! 使用標準 INTEGER 狀態陣列傳遞，防止 INTEGER(16) 造成的記憶體覆蓋
         IF (p_info%IOP) WRITE(*,*) " [DEBUG] Preparing PGSlib_Distribute..."
         IF (p_info%IOP) WRITE(*,*) " [DEBUG] Entering pgslib_dist..."
         CALL pgslib_dist(local_bnd_status, reconciled_judge)
         IF (p_info%IOP) WRITE(*,*) " [DEBUG] pgslib_dist finished."


         DO i = 1, bnd_face_cnt
            idx = local_bnd_idx(i)
            f_elem  = face_mapping(idx, 1)
            f_local = face_mapping(idx, 2)

            ! 若 IOP 比對結果為 0 (內部面)，更新局部 face_judge
            IF (local_bnd_status(i) == 0) THEN
               face_judge(f_local, f_elem) = 0
            END IF
         END DO

         ! 清理平行化暫存陣列 (避免 Memory Leak)
         IF (ALLOCATED(local_bnd_keys))    DEALLOCATE(local_bnd_keys)
         IF (ALLOCATED(local_bnd_idx))     DEALLOCATE(local_bnd_idx)
         IF (ALLOCATED(local_bnd_status))  DEALLOCATE(local_bnd_status)
         IF (ALLOCATED(global_bnd_keys))   DEALLOCATE(global_bnd_keys)
         IF (ALLOCATED(reconciled_judge))  DEALLOCATE(reconciled_judge)

      END IF

      ! ---------------------------------------------------
      ! 6. [DEBUG] 驗證與全域統計輸出程式碼
      ! ---------------------------------------------------
      local_ext_cnt = COUNT(face_judge == 1)
      local_int_cnt = COUNT(face_judge == 0)

      IF (p_info%IsParallel) THEN
         total_external_faces = PGSLib_GLOBAL_SUM(local_ext_cnt)
         total_internal_faces = PGSLib_GLOBAL_SUM(local_int_cnt)
      ELSE
         total_external_faces = local_ext_cnt
         total_internal_faces = local_int_cnt
      END IF

      IF (p_info%IOP) THEN
         WRITE(*,*) "=========================================="
         WRITE(*,*) " [DEBUG] FACE JUDGEMENT VERIFICATION"
         WRITE(*,*) "=========================================="
         WRITE(*,*) " Total Elements (nel):", nel
         WRITE(*,*) " Total Faces to check:", total_faces
         WRITE(*,*) ""
         WRITE(*,*) " [1] Global Topology Summary (PGSLib Reconciled):"
         WRITE(*,*) "     Total External Boundary Faces (Value 1): ", total_external_faces
         WRITE(*,*) "     Total Internal Connected Faces (Value 0): ", total_internal_faces
         WRITE(*,*) "     Verification Sum (Must equal total_faces):", total_external_faces + total_internal_faces
         WRITE(*,*) "=========================================="
      END IF

      ! ---------------------------------------------------
      ! 7. 釋��局部動態記憶體 (避免 Memory Leak)
      ! ---------------------------------------------------
      IF (ALLOCATED(face_keys))    DEALLOCATE(face_keys)
      IF (ALLOCATED(face_mapping)) DEALLOCATE(face_mapping)
      IF (ALLOCATED(sort_index))   DEALLOCATE(sort_index)
      IF (ALLOCATED(temp_idx))     DEALLOCATE(temp_idx)

      IF (p_info%IOP) THEN
         WRITE(*,*) " [face_judgement] Column-major Cache-optimized Face Judgement completed."
      END IF

   CONTAINS

      ! =========================================================
      ! 內部子程序：將 3 個節點排序後根據 nnd ��態進位壓成 128 位元特徵碼
      ! =========================================================
      PURE SUBROUTINE pack_face(n1, n2, n3, key)

         INTEGER, INTENT(IN) :: n1, n2, n3
         INTEGER(16), INTENT(OUT) :: key
         INTEGER(16) :: nodes(3), temp, base

         nodes(1) = INT(n1, 16)
         nodes(2) = INT(n2, 16)
         nodes(3) = INT(n3, 16)

         ! 簡單三元 Bubble Sort 確保由小到大排序 (n1 <= n2 <= n3)
         ! 正確的三數排序網路 (Sorting Network) 確保 nodes(1) <= nodes(2) <= nodes(3)
         IF (nodes(1) > nodes(2)) THEN; temp = nodes(1); nodes(1) = nodes(2); nodes(2) = temp; END IF
         IF (nodes(1) > nodes(3)) THEN; temp = nodes(1); nodes(1) = nodes(3); nodes(3) = temp; END IF
         IF (nodes(2) > nodes(3)) THEN; temp = nodes(2); nodes(2) = nodes(3); nodes(3) = temp; END IF

         ! 動態 Base：取大於全域總節點數 nnd 的最小安全進位基數
         base = INT(nnd + 1, 16)

         ! 採������態 Base 多項���進位
         key = (nodes(1) * base + nodes(2)) * base + nodes(3)
      END SUBROUTINE pack_face



   END SUBROUTINE face_judgement




   ! =========================================================================
   ! SUBROUTINE: compute_body_mass_properties
   !
   ! [功能說明 / Description]
   !    計算固體/剛體結構的整體物理質量屬性，包含總質量 (Total Mass)、質心座標
   !    (Center of Mass, CoM) 以及相對於質心的轉動慣量張量 (Inertia Tensor)。
   !
   ! [平行化修復 / Parallel Repair]
   !    1. 利用 V5_Node_PE(i) /= p_info%thisPE 防範跨 CPU 邊界節點重複計算質量。
   !    2. 兩階���全域規約 (PGSLib_GLOBAL_SUM)：
   !       - 階段一：求得全域真��總質量與全域質心 (CoM)。
   !       - 階段二��利用全域質心求得全域轉動慣量張量 (Inertia Tensor)。
   !    3. 由 p_info%IOP 統一輸出驗證資訊，確保跨 CPU 數據一致性。
   ! =========================================================================
   SUBROUTINE compute_body_mass_properties()
      IMPLICIT NONE
      INTEGER :: i, j, k
      REAL(real_kind) :: total_m, com(3), r(3)
      REAL(real_kind) :: I_tensor(3,3)

      ! 平行化區域 (Local) 暫存變數
      REAL(real_kind) :: local_m, local_com_mom(3)
      REAL(real_kind) :: local_I(3,3)

      ! -----------------------------------------------------------------
      ! 1. 階段一：計算區域質量與質心動量 (避開重複的 Ghost ��點)
      ! -----------------------------------------------------------------
      local_m       = 0.0_real_kind
      local_com_mom = 0.0_real_kind

      DO i = 1, nnd
         ! ��讓主要所有權��於本處理器 (Owner Rank) 的���點參與累加，避免跨 CPU 重複計算
         IF (ALLOCATED(V5_Node_PE)) THEN
            IF (V5_Node_PE(i) /= p_info%thisPE) CYCLE
         END IF

         local_m       = local_m + Nodes%mass(i)
         local_com_mom = local_com_mom + Nodes%mass(i) * Nodes%xc(:, i)
      END DO

      ! -----------------------------------------------------------------
      ! ���域同步一：跨 CPU 規約求得全域總質量��全域質心 (CoM)
      ! -----------------------------------------------------------------
      IF (p_info%IsParallel) THEN
         total_m = PGSLib_GLOBAL_SUM(local_m)
         DO j = 1, 3
            com(j) = PGSLib_GLOBAL_SUM(local_com_mom(j))
         END DO
      ELSE
         total_m = local_m
         com     = local_com_mom
      END IF

      IF (total_m > 0.0_real_kind) THEN
         com = com / total_m
      ELSE
         IF (p_info%IOP) THEN
            WRITE(*,*) "Warning: [compute_body_mass_properties] Total body mass is zero or negative!"
         END IF
      END IF

      ! -----------------------------------------------------------------
      ! 2. 階段二：利用全域質心 (CoM)，計算各 CPU 區域相對於全域質心的轉動慣量張量
      ! -----------------------------------------------------------------
      local_I = 0.0_real_kind

      DO i = 1, nnd
         ! 同樣過濾非本��理器主要的邊界/Ghost 節點
         IF (ALLOCATED(V5_Node_PE)) THEN
            IF (V5_Node_PE(i) /= p_info%thisPE) CYCLE
         END IF

         r = Nodes%xc(:, i) - com

         local_I(1,1) = local_I(1,1) + Nodes%mass(i) * (r(2)**2 + r(3)**2)
         local_I(2,2) = local_I(2,2) + Nodes%mass(i) * (r(1)**2 + r(3)**2)
         local_I(3,3) = local_I(3,3) + Nodes%mass(i) * (r(1)**2 + r(2)**2)

         local_I(1,2) = local_I(1,2) - Nodes%mass(i) * r(1) * r(2)
         local_I(1,3) = local_I(1,3) - Nodes%mass(i) * r(1) * r(3)
         local_I(2,3) = local_I(2,3) - Nodes%mass(i) * r(2) * r(3)
      END DO

      ! 補全對稱矩陣分量 (確保傳入全域規約前矩陣���整)
      local_I(2,1) = local_I(1,2)
      local_I(3,1) = local_I(1,3)
      local_I(3,2) = local_I(2,3)

      ! -----------------------------------------------------------------
      ! 全域同步二���跨 CPU 規約轉動慣量��量
      ! -----------------------------------------------------------------
      IF (p_info%IsParallel) THEN
         DO j = 1, 3
            DO k = 1, 3
               I_tensor(j,k) = PGSLib_GLOBAL_SUM(local_I(j,k))
            END DO
         END DO
      ELSE
         I_tensor = local_I
      END IF

      ! 補全對稱矩陣分量
      I_tensor(2,1) = I_tensor(1,2)
      I_tensor(3,1) = I_tensor(1,3)
      I_tensor(3,2) = I_tensor(2,3)

      ! -----------------------------------------------------------------
      ! 3. 依據物體屬性賦值 (剛體 / ��變形體)
      ! -----------------------------------------------------------------
      IF (.NOT. is_V5_deformable) THEN
         ! 剛體模式：僅在未完成初始化時設定���始姿態基準量 (Body Frame)
         IF (.NOT. is_rigid_initialized) THEN
            V5_Rigid_mass     = total_m
            V5_Rigid_CoM      = com
            V5_Rigid_CoM0     = com
            V5_Rigid_Ibody    = I_tensor
            CALL invert_3x3_matrix(V5_Rigid_Ibody, V5_Rigid_invIbody)
            is_rigid_initialized = .TRUE.
         END IF
      ELSE
         ! 可變形體模式：即時更新變形後的質心與慣量
         Current_Body_Mass = total_m
         Current_Body_CoM  = com
         Current_Body_I    = I_tensor
      END IF

      ! -----------------------------------------------------------------
      ! 驗證計算結果輸出 (僅由主節點 IOP 印出驗證結果)
      ! -----------------------------------------------------------------
      IF (p_info%IOP) THEN
         WRITE(*, '(A, F12.4, A, 3F10.4)') &
            " [compute_body_mass_properties] Body Mass Properties -> Mass: ", total_m, " | CoM: ", com
         WRITE(*, '(A, 3F12.4)') &
            " [compute_body_mass_properties] Inertia Tensor Diag (Ixx, Iyy, Izz): ", &
            I_tensor(1,1), I_tensor(2,2), I_tensor(3,3)
      END IF

   END SUBROUTINE compute_body_mass_properties

END MODULE VFIFE_Setup_module




```

---
# 🔗 參考資料


---