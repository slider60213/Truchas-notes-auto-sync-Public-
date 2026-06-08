---
type: 📝 Research
created: 2026-06-04 03:10
modified: 2026-06-09 03:39
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
MODULE VFIFE_Setup_module
   USE VFIFE_Utils_module  ! 引用 1-1, 1-2 等小工具
   USE VFIFE_Data_module

   IMPLICIT NONE

   PUBLIC :: nodemass
   PUBLIC :: face_judgement

CONTAINS

   ! =========================================================
   ! 計算單元體積與質量，分配累加成節點質量
   ! =========================================================
   SUBROUTINE nodemass()
      IMPLICIT NONE
      INTEGER :: i ! 迴圈用的變數
      INTEGER :: n1, n2, n3, n4 ! 組成四面體的四個節點
      REAL(8) :: x1, x2, x3, x4, y1, y2, y3, y4, z1, z2, z3, z4 ! 四個節點的xyz
      REAL(8) :: x21, y21, z21, x31, y31, z31, x41, y41, z41 ! 四個節點之間的向量



      ! 1. 安全性檢查：確保所有需要的矩陣都已經正確配置
      IF (.NOT. ALLOCATED(elem_topo) .OR. .NOT. ALLOCATED(x_coord)) THEN
         WRITE(*,*) "Fatal: Required arrays are not allocated."
         STOP
      END IF

      ! 2. 重要動作：初始化相關矩陣，全部歸零準備累加
      ALLOCATE(elem_vol(nel), SOURCE=0.0d0)
      ALLOCATE(elem_rho(nel), SOURCE=0.0d0)
      ALLOCATE(elem_mass(nel), SOURCE=0.0d0)
      ALLOCATE(elem_mass_per_node(nel), SOURCE=0.0d0)
      ALLOCATE(node_mass(nnd), SOURCE=0.0d0)



      ! 3. 核心迴圈：遍歷四面體單元 (1 到 nel)
      ! [OpenMP 平行化開關]：
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, n1, n2, n3, n4, &
      !$OMP         x1, x2, x3, x4, &
      !$OMP         y1, y2, y3, y4, &
      !$OMP         z1, z2, z3, z4, &
      !$OMP         x21, y21, z21, &
      !$OMP         x31, y31, z31, &
      !$OMP         x41, y41, z41) &
      !$OMP SHARED(nel, elem_topo, x_coord, e, elem_vol,elem_rho, elem_mat, elem_mass, elem_mass_per_node, node_mass)
      DO i = 1, nel

         ! 4. 提取四面體的 4 個節點編號
         ! elem_topo(i,j) 的 j 從 1~5
         ! 代表四面體編號 + 組成的四個節點
         n1 = elem_topo(2, i)
         n2 = elem_topo(3, i)
         n3 = elem_topo(4, i)
         n4 = elem_topo(5, i)

         ! 5. 根據節點編號，抓取 3D 空間座標
         x1 = x_coord(1, n1);  y1 = x_coord(2, n1);  z1 = x_coord(3, n1)
         x2 = x_coord(1, n2);  y2 = x_coord(2, n2);  z2 = x_coord(3, n2)
         x3 = x_coord(1, n3);  y3 = x_coord(2, n3);  z3 = x_coord(3, n3)
         x4 = x_coord(1, n4);  y4 = x_coord(2, n4);  z4 = x_coord(3, n4)

         ! 6. 計算三個向量：從節點1指向節點2、3、4的向量
         x21 = x2 - x1;  y21 = y2 - y1;  z21 = z2 - z1
         x31 = x3 - x1;  y31 = y3 - y1;  z31 = z3 - z1
         x41 = x4 - x1;  y41 = y4 - y1;  z41 = z4 - z1

         ! 7. 使用純量三重積公式計算四面體體積
         elem_vol(i) = (x41 * (y21*z31 - y31*z21) + &
            y41 * (x31*z21 - x21*z31) + &
            z41 * (x21*y31 - x31*y21)) / 6.0d0

         ! 8. 計算四面體單元的質量
         !  A. elem_mat(1,i) = j 代表第 i 個單元的材料編號為j
         !  B. 直接去 e(3, j) 查表抓出第j號材料的密度 (rho)
         !  C. 計算並儲存該四面體單元的「總質量」(體積 * 密度)
         !  D. 計算並儲存該四面體單元的「每個節點質量」
         elem_rho(i) = e(3, elem_mat(1, i))
         elem_mass(i) = elem_vol(i) * elem_rho(i)
         elem_mass_per_node(i) = (elem_mass(i)) / 4.0d0

         ! 9. 【核心動作】多執行緒累加回本地陣列
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

      WRITE(*,*) " [DEBUG] Element Volume calculated:", elem_vol
      WRITE(*,*) " [DEBUG] Node Mass calculated:", node_mass(4)

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

      ! 使用 64 位元整數儲存特徵碼，防止大規模網格的節點數相乘溢位
      INTEGER(8), ALLOCATABLE :: face_keys(:)

      ! 【修正 1】完美調整為行優先結構：第一維度是面的絕對總編號，第二維度是屬性欄位 (1:elem_id, 2:local_face)
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
      ALLOCATE(face_keys(total_faces))

      ! 【修正 2】對調配置維度，確保與寫入時的 face_mapping(total_faces, 2) 完全一致
      ALLOCATE(face_mapping(total_faces, 2))
      ALLOCATE(sort_index(total_faces))

      ! ---------------------------------------------------
      ! 2. 建立每個面的唯一特徵編碼 (Face Key)
      ! ---------------------------------------------------
      !$OMP PARALLEL DO PRIVATE(i, m, n1, n2, n3, n4)
      DO i = 1, nel
         m = (i-1)*4

         ! 配合 elem_topo(5, nel) 的結構，第一維度是欄位，第二維度是單元索引
         n1 = elem_topo(2, i)
         n2 = elem_topo(3, i)
         n3 = elem_topo(4, i)
         n4 = elem_topo(5, i)

         ! 面 1 (n1, n2, n3)
         CALL pack_face(n1, n2, n3, face_keys(m+1))
         face_mapping(m+1, 1) = i; face_mapping(m+1, 2) = 1

         ! 面 2 (n1, n4, n2)
         CALL pack_face(n1, n4, n2, face_keys(m+2))
         face_mapping(m+2, 1) = i; face_mapping(m+2, 2) = 2

         ! 面 3 (n2, n4, n3)
         CALL pack_face(n2, n4, n3, face_keys(m+3))
         face_mapping(m+3, 1) = i; face_mapping(m+3, 2) = 3

         ! 面 4 (n3, n4, n1)
         CALL pack_face(n3, n4, n1, face_keys(m+4))
         face_mapping(m+4, 1) = i; face_mapping(m+4, 2) = 4
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
      WRITE(*, '(A,16I4)') "   sort_index = ", sort_index(1:16)

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
      ! 利用 Fortran 內建的 COUNT 矩陣函數，瞬間算出一共有多少個 0 與 1
      i = COUNT(face_judge == 1) ! 外接面總數
      j = COUNT(face_judge == 0) ! 內部面總數

      WRITE(*, '(A,I8)') "   Total External Boundary Faces (Value 1): ", i
      WRITE(*, '(A,I8)') "   Total Internal Connected Faces (Value 0): ", j
      WRITE(*, '(A,I8)') "   Verification Sum (Must equal total_faces):", i + j

      WRITE(*,*) "=========================================="

      ! ---------------------------------------------------
      ! 5. 釋放局部動態記憶體
      ! ---------------------------------------------------
      DEALLOCATE(face_keys, face_mapping, sort_index)
      WRITE(*,*) " [V5] Column-major Cache-optimized Face Judgement completed."

   CONTAINS

      ! =========================================================
      ! 內部子程序：將 3 個節點排序後壓成一個 64 位元的唯一特徵碼
      ! =========================================================
      SUBROUTINE pack_face(n1, n2, n3, key)
         INTEGER, INTENT(IN) :: n1, n2, n3
         INTEGER(8), INTENT(OUT) :: key
         INTEGER :: nmax, nmin, nmid

         nmin = MIN(n1, n2, n3)
         nmax = MAX(n1, n2, n3)
         nmid = n1 + n2 + n3 - nmin - nmax

         key = INT(nmin, 8) * 10000000000_8 + INT(nmid, 8) * 100000_8 + INT(nmax, 8)
      END SUBROUTINE pack_face

      ! =========================================================
      ! 內部子程序：針對一維特徵陣列進行雙指標索引排序 (防溢����絕對穩定版)
      ! =========================================================
      RECURSIVE SUBROUTINE quicksort_idx(keys, idx, left, right)
         INTEGER(8), INTENT(IN) :: keys(:)
         INTEGER, INTENT(INOUT)  :: idx(:)
         INTEGER, INTENT(IN)     :: left, right
         INTEGER :: i, j, temp_idx
         INTEGER(8) :: pivot_key

         ! 基礎終止條件：如果範圍小於或等於 1 個元素，直接返回
         IF (left >= right) RETURN

         ! 抓取中點作為基準值
         pivot_key = keys(idx((left + right) / 2))
         i = left
         j = right

         ! 雙指標劃分大迴圈
         DO
            DO WHILE (keys(idx(i)) < pivot_key)
               i = i + 1
            END DO
            DO WHILE (keys(idx(j)) > pivot_key)
               j = j - 1
            END DO

            ! 如果指針交叉或重合，代表這一輪劃分完成，退出大迴圈
            IF (i >= j) EXIT

            ! 交換索引
            temp_idx = idx(i)
            idx(i) = idx(j)
            idx(j) = temp_idx

            ! 移動指針繼續下一輪比對
            i = i + 1
            j = j - 1
         END DO

         ! 【關鍵修正】嚴格的分治邊界：確保遞迴範圍必定小於當前範圍，徹底杜絕無窮遞迴
         ! 使用 j 作為切分點，左半邊為 left 到 j，右半邊為 j+1 到 right
         ! 但若發生特殊邊界導致 j 等於 right，則強迫往左推一格，避免原地踏步
         IF (j == right) THEN
            CALL quicksort_idx(keys, idx, left, j - 1)
         ELSE
            CALL quicksort_idx(keys, idx, left, j)
            CALL quicksort_idx(keys, idx, j + 1, right)
         END IF

      END SUBROUTINE quicksort_idx

   END SUBROUTINE face_judgement

END MODULE VFIFE_Setup_module

```

---
# 🔗 參考資料


---