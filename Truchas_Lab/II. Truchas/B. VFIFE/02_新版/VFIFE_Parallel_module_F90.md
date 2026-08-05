---
type: 📝 Research
created: 2026-08-06 03:51
modified: 2026-08-06 03:52
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
MODULE VFIFE_Parallel_module
   USE pgslib_module, ONLY: PGSLIB_Setup_Trace, PGSLIB_Deallocate_Trace, &
      PGSLib_Global_Sum, PGSLib_Scatter_SUM
   USE parallel_info_module, ONLY: p_info


   ! Basic Modules of VFIFE
   USE VFIFE_Data_module
   USE VFIFE_Utils_module

   IMPLICIT NONE

   PRIVATE


   ! --- 全域公開副程式 ---
   PUBLIC :: V5_EN_Sum_Scatter_1D
   PUBLIC :: V5_EN_Sum_Scatter_2D

   PUBLIC :: V5_Setup_Communication
   PUBLIC :: V5_Cleanup_Communication

CONTAINS



   ! =========================================================
   ! 【1D 單元到節點加總縫合】
   ! 將 4 頂點單元貢獻 (4, nel) 累加縫合至 1D 節點陣列 (nnd)
   ! =========================================================
   SUBROUTINE V5_EN_Sum_Scatter_1D(node_array, elem_vrtx_contrib)
      USE pgslib_module, ONLY: PGSLib_Scatter_Sum
      USE VFIFE_Data_module, ONLY: elem_topo
      IMPLICIT NONE
      REAL(KIND=8), INTENT(INOUT) :: node_array(:)            ! DEST (nnd)
      REAL(KIND=8), INTENT(IN)    :: elem_vrtx_contrib(:,:)   ! SOURCE (4, nel)

      IF (p_info%IsParallel) THEN
         ! 傳入 DEST (節點陣列), SOURCE (單元頂點貢獻), INDEX (拓樸矩陣)
         ! elem_topo(2:5, :) 存放四面體的 4 個頂點編號
         CALL PGSLib_Scatter_Sum(DEST   = node_array, &
            SOURCE = elem_vrtx_contrib, &
            INDEX  = elem_topo(2:5, :))
      END IF
   END SUBROUTINE V5_EN_Sum_Scatter_1D


   ! =========================================================
   ! 【2D 向量單元到節點加總縫合】
   ! 針對 3D 向量 (如 3D 內力/外力 fsum)，逐分量進行 PGSLib_Scatter_Sum
   ! =========================================================
   SUBROUTINE V5_EN_Sum_Scatter_2D(node_force, elem_vrtx_force)
      USE pgslib_module, ONLY: PGSLib_Scatter_Sum
      USE VFIFE_Data_module, ONLY: elem_topo
      IMPLICIT NONE
      REAL(KIND=8), INTENT(INOUT) :: node_force(:,:)          ! DEST (3, nnd)
      REAL(KIND=8), INTENT(IN)    :: elem_vrtx_force(:,:,:)   ! SOURCE (3, 4, nel)

      INTEGER :: dim_id

      IF (p_info%IsParallel) THEN
         DO dim_id = 1, SIZE(node_force, 1)
            CALL PGSLib_Scatter_Sum(DEST   = node_force(dim_id, :), &
               SOURCE = elem_vrtx_force(dim_id, :, :), &
               INDEX  = elem_topo(2:5, :))
         END DO
      END IF
   END SUBROUTINE V5_EN_Sum_Scatter_2D



   ! =========================================================
   ! 【PGSLib 通訊地圖建立】 建立 VFIFE 固體網格之跨 CPU 邊界通訊 Trace 與 PE 分配
   ! =========================================================
   SUBROUTINE V5_Setup_Communication(nel, nnd, rnode)

      IMPLICIT NONE

      ! --- Arguments ---
      INTEGER,      INTENT(IN) :: nel, nnd
      REAL(KIND=8), INTENT(IN) :: rnode(10, nel)

      ! --- Local variables ---
      ! 修正：採用 2D 宣告以符合四面體頂點拓樸 (4 頂點 x nel 單元)
      INTEGER, ALLOCATABLE :: Solid_Indices(:,:)
      LOGICAL, ALLOCATABLE :: Solid_Mask(:,:)

      ! 臨時接收 PGSLib 函數回填的 2D PE 映射指針
      INTEGER, POINTER     :: Temp_PE_Map(:,:) => NULL()
      INTEGER              :: i, v

      ! <><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

      IF (p_info%IsParallel) THEN

         ! 1. 清理舊有 Trace 資源
         IF (ASSOCIATED(V5_Trace)) CALL PGSLIB_Deallocate_Trace(V5_Trace)
         NULLIFY(V5_Trace)

         ! 2. 初始化全域節點 PE 歸屬陣列 (確保 V5_Node_PE 已在模組定義)
         IF (ALLOCATED(V5_Node_PE)) DEALLOCATE(V5_Node_PE)
         ALLOCATE(V5_Node_PE(nnd))
         V5_Node_PE(:) = -1

         ! 3. 配置 2D 拓樸與遮罩空間 [1]
         ALLOCATE(Solid_Indices(4, nel))
         ALLOCATE(Solid_Mask(4, nel))

         ! 從 rnode (CARD 4) 提取頂點 ID 並轉為整數 [6]
         Solid_Indices(1:4, :) = INT(rnode(2:5, :))
         Solid_Mask(:, :)       = .TRUE.

         ! 4. 呼叫 PGSLib 建立地圖，Temp_PE_Map 會由 PGSLib 自動分配空間 [7]
         V5_Trace => PGSLib_Setup_Trace( &
            INDEX        = Solid_Indices, &
            SIZE_OF_DEST = nnd,           &
            PE_ARRAY     = Temp_PE_Map,   &
            MASK         = Solid_Mask     &
            )

         ! 5. 將單元級別的 2D PE 資訊映射至節點級別的 1D 陣列 [7, 8]
         IF (ASSOCIATED(Temp_PE_Map)) THEN
            DO i = 1, nel
               DO v = 1, 4
                  ! 根據 Solid_Indices 找到節點 ID，並填入對應的 CPU 編號
                  V5_Node_PE(Solid_Indices(v, i)) = Temp_PE_Map(v, i)
               END DO
            END DO
            ! 釋放 PGSLib 配置的臨時指針空間 [9]
            DEALLOCATE(Temp_PE_Map)
            NULLIFY(Temp_PE_Map)
         END IF

         ! 6. 釋放本地暫存陣列
         DEALLOCATE(Solid_Indices, Solid_Mask)

         ! 7. IOP 驗證輸出
         IF (p_info%IOP) THEN
            WRITE(*, '(A, I8, A, I8)') &
               " [V5_Setup_Communication] PGSLib Trace Setup complete. Nodes: ", &
               nnd, " | V5_Node_PE items: ", SIZE(V5_Node_PE)
         END IF

      ELSE
         ! 單機模式處理 [10]
         IF (ALLOCATED(V5_Node_PE)) DEALLOCATE(V5_Node_PE)
         ALLOCATE(V5_Node_PE(nnd))
         V5_Node_PE(:) = p_info%thisPE
      END IF

      RETURN
   END SUBROUTINE V5_Setup_Communication


   ! =========================================================
   ! 【PGSLib 通訊地圖清理】 釋放全域 Trace 與 PE 配置記憶體
   ! =========================================================
   SUBROUTINE V5_Cleanup_Communication()
      IMPLICIT NONE

      IF (ASSOCIATED(V5_Trace)) THEN
         CALL PGSLIB_Deallocate_Trace(V5_Trace)
      END IF
      NULLIFY(V5_Trace)

      IF (ALLOCATED(V5_Node_PE)) THEN
         DEALLOCATE(V5_Node_PE)
      END IF

      RETURN
   END SUBROUTINE V5_Cleanup_Communication

END MODULE VFIFE_Parallel_module


```


---
# 🔗 參考資料


---