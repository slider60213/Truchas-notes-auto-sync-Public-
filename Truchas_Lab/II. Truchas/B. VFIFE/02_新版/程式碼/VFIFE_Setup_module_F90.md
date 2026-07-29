---
type: 📝 Research
created: 2026-06-04 03:10
modified: 2026-07-30 03:53
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

   ! Truchas
   USE mesh_gen_module,        only: x_axis, y_axis, z_axis
   USE property_data_module,   only: density

   IMPLICIT NONE


   PUBLIC :: V5Setup
   PUBLIC :: Geometry
   PUBLIC :: nodemass
   PUBLIC :: face_judgement


CONTAINS



   SUBROUTINE V5Setup()
      IMPLICIT NONE
      CALL Geometry()
      WRITE(*,*) ' [V5] Geometry finish'
      CALL nodemass()
      WRITE(*,*) ' [V5] nodemass finish'
      CALL face_judgement()
      WRITE(*,*) ' [V5] face_judgement finish'

      ! 計算 AABB 範圍與外露面快取
      CALL compute_solid_aabb()
      WRITE(*,*) ' [V5] compute_solid_aabb finish'
      CALL build_surface_cache()
      WRITE(*,*) ' [V5] build_surface_cache finish'
   END SUBROUTINE V5Setup



   ! =========================================================
   ! Geometry: 計算四面體幾何屬性 (頂點、形心、質心、面法向、體積)
   ! =========================================================
   SUBROUTINE Geometry()
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
      WRITE(*,*) ' [OMP Status] Active (OpenMP Enabled)'
      WRITE(*,*) ' [OMP Check] Total Threads Allocated:', OMP_GET_NUM_THREADS()
      !$OMP END SINGLE

      ! 讓所有平行 Thread 都印出自己的 ID
      WRITE(*,*) ' [OMP Check] Hello from Thread ID:', OMP_GET_THREAD_NUM()
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

         ! 2. 儲存頂點座標 elem_vertices(3, 4, nel)
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

         ! 5. 計算各面之面積與指向外側之單位法向量
         ! 修改後 (確保繞向與 build_surface_cache 統一)：
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

         ! 6. 四面體體積計算 (純量三重��������)
         x21 = p2(1) - p1(1); y21 = p2(2) - p1(2); z21 = p2(3) - p1(3)
         x31 = p3(1) - p1(1); y31 = p3(2) - p1(2); z31 = p3(3) - p1(3)
         x41 = p4(1) - p1(1); y41 = p4(2) - p1(2); z41 = p4(3) - p1(3)

         elem_vol(i) = (x41 * (y21*z31 - y31*z21) + &
            y41 * (z21*x31 - z31*x21) + &
            z41 * (x21*y31 - x31*y21)) / 6.0d0

         ! 負體積/���轉單元檢查
         IF (elem_vol(i) <= 0.0d0) THEN
            WRITE(*, '(A,I8,A,ES12.5)') " [Fatal Error] Negative or Zero Volume detected at Element ", &
               i, ", Vol = ", elem_vol(i)
            STOP "Execution halted due to mesh geometry error."
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
         END IF

      END SUBROUTINE compute_face_geom

   END SUBROUTINE Geometry

   ! =========================================================
   ! 計算單元體積與質量，分配累加成節點質量
   ! =========================================================
   SUBROUTINE nodemass()
      IMPLICIT NONE
      INTEGER :: i ! 迴圈用的變數
      INTEGER :: n1, n2, n3, n4 ! 組成四面體的四個節點


      ! 1. 安全性檢查：確保所有需要的矩陣都已經正確配置
      IF (.NOT. ALLOCATED(elem_topo) .OR. .NOT. ALLOCATED(elem_mat) .OR. &
         .NOT. ALLOCATED(elem_vol) .OR. .NOT. ALLOCATED(node_mass)) THEN
         WRITE(*,*) "Fatal: Required arrays are not allocated in nodemass."
         STOP
      END IF

      ! 2. 重要動作：初始化相關矩陣，全部歸零準備累加
      IF (ALLOCATED(elem_rho)) elem_rho = 0.0d0
      IF (ALLOCATED(elem_mass)) elem_mass = 0.0d0
      IF (ALLOCATED(elem_mass_per_node)) elem_mass_per_node = 0.0d0
      IF (ALLOCATED(node_mass)) node_mass = 0.0d0

      ! 3. 核心迴圈：遍歷四面體單元 (1 到 nel)
      ! [OpenMP 平行化開關]：
      ! 【修正��補齊 OpenMP SHARED 變數列表 (e, elem_mat) 避免編譯錯誤
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, n1, n2, n3, n4) &
      !$OMP SHARED(nel, elem_topo, x_coord, e, elem_mat, elem_vol, elem_rho, elem_mass, elem_mass_per_node, node_mass)
      DO i = 1, nel

         ! 4. 提取四面體的 4 個節點編號
         ! elem_topo(i,j) 的 j 從 1~5
         ! 代表四面體編號 + 組成的四個節點
         n1 = elem_topo(2, i)
         n2 = elem_topo(3, i)
         n3 = elem_topo(4, i)
         n4 = elem_topo(5, i)

         ! 5. 計算四面體單元的質量
         !  A. elem_mat(1,i) = j 代表第 i 個單元的材料編號為j
         !  B. 直接去 e(3, j) 查表抓出第j號材料的密度 (rho)
         !  C. 計算並儲存該四面體單元的「總質量」(體積 * 密度)
         !  D. 計算並儲存該四面體單元的「每個節點質��」
         elem_rho(i) = e(3, elem_mat(1, i))
         elem_mass(i) = elem_vol(i) * elem_rho(i)
         elem_mass_per_node(i) = (elem_mass(i)) / 4.0d0

         ! 6. 【核心動作】多執行緒累加回本地陣列
         ! [OpenMP ATOMIC 關鍵防護]：
         ! 因為多個執行緒會同時存取同一個處理器記憶體中的 node_mass
         ! 此處必須使用 ATOMIC 防範 Data Race。
         !$OMP ATOMIC
         node_mass(n1) = node_mass(n1) + elem_mass_per_node(i)
         !$OMP ATOMIC
         node_mass(n2) = node_mass(n2) + elem_mass_per_node(i)
         !$OMP ATOMIC
         node_mass(n3) = node_mass(n3) + elem_mass_per_node(i)
         !$OMP ATOMIC
         node_mass(n4) = node_mass(n4) + elem_mass_per_node(i)

      END DO
      !$OMP END PARALLEL DO

      ! =========================================================
      ! 【PGSLib 平行化通訊區】 跨處理器邊界節點質量總和
      ! =========================================================
      ! 必須在 OpenMP 區段外部執行。當本地的所有執行緒都把質量加好之後，
      ! 再調用 PGSLib 把不同處理器之間重疊的交界面節點質量進行全域 SCATTER_SUM。
      !
      ! CHARACTER(LEN=*) :: trace_id = "node_mass_trace"
      ! CALL PGSLib_SCATTER_SUM(node_mass, trace_id)
      ! =========================================================

      WRITE(*,*) " [V5] Subroutine nodemass processed elements (Hybrid Parallel Ready)."

      ! 在計算完體積後立刻印出

      WRITE(*,*) " [V5] Sample Node Mass (Node 1):", node_mass(MIN(1, nnd))
      WRITE(*,*) " [V5] Sample Node Mass (Node 2):", node_mass(MIN(2, nnd))
      WRITE(*,*) " [V5] Sample Node Mass (Node 3):", node_mass(MIN(3, nnd))
      WRITE(*,*) " [V5] Sample Node Mass (Node 4):", node_mass(MIN(4, nnd))

      density(V5_mat_id) = sum(elem_mass) / sum(elem_vol)
      write(*,*) " [V5] VFIFE_Material: ", V5_mat_id
      write(*,*) " [V5] VFIFE_Mass: ", sum(elem_mass)
      write(*,*) " [V5] VFIFE_Volume: ", sum(elem_vol)
      write(*,*) " [V5] VFIFE_Density: ", density(V5_mat_id)


   END SUBROUTINE nodemass

   ! =========================================================
   ! [全面修復版] 配合 (4, nel) 與 (3, nnd) 記憶體連續性優化的外接面判斷
   ! =========================================================
   SUBROUTINE face_judgement()

      IMPLICIT NONE
      ! ---------------------------------------------------
      ! 局部變數宣告 (Local Variables)
      ! ---------------------------------------------------
      INTEGER :: i, j, m, current
      INTEGER :: n1, n2, n3, n4
      INTEGER :: total_faces
      ! 幾何計算區域變數
      REAL(8) :: p1(3), p2(3), p3(3), p4(3), p_center(3)

      ! 使用 64 位元整數儲存特徵碼，防止大規模網格的節點數相乘溢位
      INTEGER(8), ALLOCATABLE :: face_keys(:)

      ! 完美調整為行優先結構：第一維度是面的絕對總編號，第二維度是屬性欄位 (1:elem_id, 2:local_face)
      INTEGER, ALLOCATABLE    :: face_mapping(:,:)
      INTEGER, ALLOCATABLE    :: sort_index(:)     ! 一維索引排序陣列

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
      ! 動態評估安全 Base 與 Key 上限提醒
      ! ---------------------------------------------------
      ! INT64 最大值約 9.22E18，(Base)^3 不能超過此上限 => Base 上限約 2,097,152
      IF (nnd > 2000000) THEN
         WRITE(*,*) "Warning: [face_judgement] Total nodes (nnd) exceeds 2,000,000 safety threshold."
         WRITE(*,*) "         64-bit integer face_key might overflow!"
      ELSE
         WRITE(*,*) " [face_judgement] Max node limit for 64-bit Face Key:", 2000000, " (Current nnd:", nnd, ")"
      END IF
      ALLOCATE(face_keys(total_faces))

      ! 對調配置維度，確���與寫入時的 face_mapping(total_faces, 2) 完全一致
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

         ! 配合 elem_topo(5, nel) 的結構，第一維度是欄位，第二維度是單元索引
         n1 = elem_topo(2, i)
         n2 = elem_topo(3, i)
         n3 = elem_topo(4, i)
         n4 = elem_topo(5, i)

         ! 面 1 (n1, n2, n3)
         ! 生成面���唯一特徵編碼 face_key
         CALL pack_face(n1, n2, n3, face_keys(m+1))
         ! 記錄 face_key 所對應的單元編號與面編號
         face_mapping(m+1, 1) = i
         face_mapping(m+1, 2) = 1

         ! 面 2 (n1, n4, n2)
         CALL pack_face(n1, n4, n2, face_keys(m+2))
         face_mapping(m+2, 1) = i
         face_mapping(m+2, 2) = 2

         ! 面 3 (n2, n4, n3)
         CALL pack_face(n2, n4, n3, face_keys(m+3))
         face_mapping(m+3, 1) = i
         face_mapping(m+3, 2) = 3

         ! 面 4 (n3, n4, n1)
         CALL pack_face(n3, n4, n1, face_keys(m+4))
         face_mapping(m+4, 1) = i
         face_mapping(m+4, 2) = 4
      END DO
      !$OMP END PARALLEL DO

      ! 初始化索引陣列 (1, 2, 3, ..., total_faces)
      DO i = 1, total_faces
         sort_index(i) = i
      END DO

      ! ---------------------------------------------------
      ! 3. 執行高效一維快速索引排序 (Index-Quicksort)
      ! ---------------------------------------------------
      CALL quicksort_idx(face_keys, sort_index, 1, total_faces)

      ! ---------------------------------------------------
      ! 4. 線性對比鄰居：相同的 64 位元特徵碼代表是共用面
      ! ---------------------------------------------------
      current = 1
      DO WHILE (current < total_faces)
         i = sort_index(current)
         j = sort_index(current+1)

         IF (face_keys(i) == face_keys(j)) THEN
            ! 標記為內部面 (0)
            ! 寫入時嚴格遵循 face_judge(local_face, elem_id) 的行優先順序
            face_judge(face_mapping(i, 2), face_mapping(i, 1)) = 0
            face_judge(face_mapping(j, 2), face_mapping(j, 1)) = 0
            current = current + 2 ! 匹配成功，成對跳過
         ELSE
            current = current + 1 ! 獨有面，維持預設值 1
         END IF
      END DO

      ! ---------------------------------------------------
      ! [DEBUG] 驗證輸出程式碼（針對單個或少量單元測試案例）
      ! ---------------------------------------------------
      WRITE(*,*) "=========================================="
      WRITE(*,*) " [DEBUG] FACE JUDGEMENT VERIFICATION"
      WRITE(*,*) "=========================================="
      WRITE(*,*) " Total Elements (nel):", nel
      WRITE(*,*) " Total Faces to check:", total_faces
      WRITE(*,*) ""
      WRITE(*,*) " [1] Generated Face Keys & Pack Verification:"
#ifdef DEBUG_MODE
      ! 只有在編譯時開啟 -DDEBUG_MODE 才會把這段迴圈編進去
      DO i = 1, total_faces
         WRITE(*, '(A,I5,A,I12,A,I8,A,I2)') &
            "   Face Index ", i, " -> Key: ", face_keys(i), &
            " | From Elem: ", face_mapping(i, 1), &
            " | Local Face: ", face_mapping(i, 2)
      END DO
#endif

      WRITE(*,*) ""
      WRITE(*,*) " [2] Sorted Index Verification (By Quicksort):"
      WRITE(*, '(A,16I4)') "   sort_index = ", sort_index(1:min(16, size(sort_index)))

      WRITE(*,*) ""
      WRITE(*,*) " [3] Final Face Judgement Output:"
#ifdef DEBUG_MODE
      ! 只有在編譯時開啟 -DDEBUG_MODE 才會把這段迴圈編進去
      DO i = 1, nel
         WRITE(*, '(A,I5,A,4I3)') &
            "   Element ", i, &
            " -> face_judge(1:4) = ", face_judge(:, i)
      END DO
#endif

      WRITE(*,*) ""
      WRITE(*,*) " [3] Final Topo Topology Summary:"
      ! 利用 Fortran 內建的 COUNT 矩陣函數，瞬���算出一共有���少個 0 與 1
      i = COUNT(face_judge == 1) ! 外接面總數
      j = COUNT(face_judge == 0) ! 內部面總數

      WRITE(*, '(A,I8)') "   Total External Boundary Faces (Value 1): ", i
      WRITE(*, '(A,I8)') "   Total Internal Connected Faces (Value 0): ", j
      WRITE(*, '(A,I8)') "   Verification Sum (Must equal total_faces):", i + j

      WRITE(*,*) "=========================================="


      ! ---------------------------------------------------
      ! 5. 釋放局部動態記憶體 (安全防護機制)
      ! ---------------------------------------------------
      !IF (ALLOCATED(face_keys))    DEALLOCATE(face_keys)
      !IF (ALLOCATED(face_mapping)) DEALLOCATE(face_mapping)
      !IF (ALLOCATED(sort_index))   DEALLOCATE(sort_index)
      WRITE(*,*) " [V5] Column-major Cache-optimized Face Judgement completed."

   CONTAINS


      ! =========================================================
      ! 內部子程序：將 3 個節點排序後根據 nnd 動態進位壓成 64 位元特徵碼
      ! =========================================================
      SUBROUTINE pack_face(n1, n2, n3, key)
         USE VFIFE_Data_module, ONLY: nnd
         INTEGER, INTENT(IN) :: n1, n2, n3
         INTEGER(8), INTENT(OUT) :: key
         INTEGER(8) :: nodes(3), temp, base

         nodes(1) = INT(n1, 8)
         nodes(2) = INT(n2, 8)
         nodes(3) = INT(n3, 8)

         ! 簡單三元 Bubble Sort 確保由小到大排序 (n1 <= n2 <= n3)
         IF (nodes(1) > nodes(2)) THEN; temp = nodes(1); nodes(1) = nodes(2); nodes(2) = temp; END IF
         IF (nodes(2) > nodes(3)) THEN; temp = nodes(2); nodes(2) = nodes(3); nodes(3) = temp; END IF
         IF (nodes(1) > nodes(2)) THEN; temp = nodes(1); nodes(1) = nodes(2); nodes(2) = temp; END IF

         ! 動態 Base：取大於全域總節點數 nnd 的最小安全進位基數
         base = INT(nnd + 1, 8)

         ! 採用動態 Base 多項式進位，徹底解決 Key 溢位問題
         key = (nodes(1) * base + nodes(2)) * base + nodes(3)
      END SUBROUTINE pack_face

      ! =========================================================
      ! 內部子程序：針對一維特徵陣列進行雙指標索引排序 (防溢位、絕對穩定版)
      ! 【修正】引入穩健的分割迴圈，徹底解決指針重疊與無窮遞迴問題
      ! =========================================================
      RECURSIVE SUBROUTINE quicksort_idx(keys, idx, left, right)
         INTEGER(8), INTENT(IN)  :: keys(:)
         INTEGER, INTENT(INOUT)  :: idx(:)
         INTEGER, INTENT(IN)     :: left, right
         INTEGER :: i, j, temp_idx
         INTEGER(8) :: pivot_key

         IF (left >= right) RETURN

         pivot_key = keys(idx((left + right) / 2))
         i = left
         j = right

         DO WHILE (i <= j)
            DO WHILE (keys(idx(i)) < pivot_key)
               i = i + 1
            END DO
            DO WHILE (keys(idx(j)) > pivot_key)
               j = j - 1
            END DO
            IF (i <= j) THEN
               temp_idx = idx(i)
               idx(i) = idx(j)
               idx(j) = temp_idx
               i = i + 1
               j = j - 1
            END IF
         END DO

         IF (left < j)  CALL quicksort_idx(keys, idx, left, j)
         IF (i < right) CALL quicksort_idx(keys, idx, i, right)

      END SUBROUTINE quicksort_idx



   END SUBROUTINE face_judgement







END MODULE VFIFE_Setup_module


```

---
# 🔗 參考資料


---