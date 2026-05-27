---
type: 📝 Research
created: 2026-05-27 13:24
modified: 2026-05-27 13:26
tags:
  - "#Truchas"
  - WSL
  - VFIFE
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
MODULE VFIFE_Core_module
   USE VFIFE_Utils_module  ! 引用 1-1, 1-2 等小工具
   !SHANE 記得把 MAKE_FILE_NAME 開回來
   !USE output_module,             ONLY: MAKE_FILE_NAME
   !use omp_lib
   IMPLICIT NONE

   ! ==========================================================
   ! 全域控制變數與常數
   ! ==========================================================
   INTEGER, SAVE :: nnd                           ! 總節點數 (CARD 6 算出來的)
   INTEGER, SAVE :: nel                           ! 總單元數 (CARD 7 算出來的)
   INTEGER, SAVE :: ndof                          ! 每個節點的自由度 (通常是 3)
   INTEGER, SAVE :: nyDistor                      ! 單元扭曲判定標記
   !REAL(8), SAVE :: time                         ! 當前時步 delta (底下CARD 2已經有了)
   REAL(8), SAVE :: acctime                       ! 累積物理時間

   ! ==========================================================
   ! 歷史與材料狀態陣列 (從舊 SOLID_module 移植過來)
   ! ==========================================================
   REAL(8), ALLOCATABLE, SAVE :: xct(:), yct(:), zct(:)  ! 當前收斂幾何座標
   REAL(8), ALLOCATABLE, SAVE :: elplas(:)               ! 塑性應變歷史
   REAL(8), ALLOCATABLE, SAVE :: sigmaP(:)               ! 舊時步應力
   REAL(8), ALLOCATABLE, SAVE :: epslonP(:)              ! 舊時步應變
   REAL(8), ALLOCATABLE, SAVE :: PLalphaP(:)             ! 塑性內變量 Alpha
   REAL(8), ALLOCATABLE, SAVE :: PLrP(:)                 ! 塑性內變量 r
   REAL(8), ALLOCATABLE, SAVE :: pstress(:,:)            ! 主應力陣列 (3, nel)


   ! CARD 1
   CHARACTER(LEN=512) :: project_name, temp_str
   INTEGER :: Check_V5_Loading  ! --- 為了控制 V5 Echo 輸出新增的開關 ---


   ! ==========================================================
   ! 時間與收斂控制變數 (來自 CARD 2)
   ! ==========================================================
   INTEGER, SAVE :: minstp                        ! 起始時步 (Start_Step)
   INTEGER, SAVE :: maxstp                        ! 最大時步 (Max_Step)
   REAL(8), SAVE :: delta                         ! 時步大小 (Time_Step_Delta)
   REAL(8), SAVE :: alpha                         ! 虛擬阻尼常數 (Damping_Alpha)
   REAL(8), SAVE :: toler                         ! 收斂容許誤差 (Convergence_Toler)

   ! CARD 3
   INTEGER, SAVE :: ifbody, iacc, iforce2, iforce3, iforce4, isequel

   ! CARD 4
   INTEGER, SAVE :: iprob, iprobA, numout , isee, iplane, icontact
   REAL(8), SAVE :: thick

   ! ==========================================================
   ! 節點層級 (Node-level) 全域動態陣列 -> 來自原 CARD 6
   ! ==========================================================
   REAL(8), ALLOCATABLE, SAVE :: x_coord(:,:)     ! (nnd, 3) 節點座標
   REAL(8), ALLOCATABLE, SAVE :: rifix(:,:)       ! (nnd, 3) 固定邊界條件
   REAL(8), ALLOCATABLE, SAVE :: d(:,:), dn(:,:), dnt(:,:)
   REAL(8), ALLOCATABLE, SAVE :: vt(:,:), at(:,:)
   REAL(8), ALLOCATABLE, SAVE :: force(:,:), fsum(:,:) ! (nnd,3)

   ! 【關鍵伏筆】動力學與 bmass 共用的節點總質量陣列
   REAL(8), ALLOCATABLE, SAVE :: node_mass(:)     ! (nnd) 每個節點累積的總質量

   ! ==========================================================
   ! 單元層級 (Element-level) 全域動態陣列 -> 來自原 CARD 7 拆分
   ! ==========================================================
   INTEGER, ALLOCATABLE, SAVE :: elem_topo(:,:)   ! (nel, 5) -> [ID, N1, N2, N3, N4]
   INTEGER, ALLOCATABLE, SAVE :: elem_mat(:,:)    ! (nel, 5) -> 材料性質相關整數
   REAL(8), ALLOCATABLE, SAVE :: elem_vol(:)      ! (nel)    -> 單元體積




   ! CARD 7
   ! --- 現代化動態陣列宣告 --- nel*#
   REAL(8), ALLOCATABLE, SAVE :: rnode(:,:)    ! nel*10
   REAL(8), ALLOCATABLE, SAVE :: sigma3D(:,:)  ! nel*6
   REAL(8), ALLOCATABLE, SAVE :: xmass(:), pint(:)  ! nel*27, nel*24

   ! CARD 8
   INTEGER, SAVE :: nummat ! 材料數量
   INTEGER, SAVE :: MAX_MAT_PARAMS
   REAL(8), ALLOCATABLE, SAVE :: e(:,:) ! (nummat, MAX_MAT_PARAMS) -> 材料屬性





   ! CARD 10: 雖然有讀取，但考慮到大部分情境都���������������������������������������������9.81所以現版本讀取後不特別應用
   INTEGER, SAVE :: nptsG  ! 重力時序資料數
   REAL(8), ALLOCATABLE, SAVE :: grav_table(:,:)  ! (nptsG, 2) -> Time, Value

   ! CARD 15
   INTEGER, SAVE :: numif, current_pts, max_pts  ! 重力點數、受力歷史總數
   REAL(8), ALLOCATABLE, SAVE :: force_table(:,:,:) ! (numif, max_pts, 2)

   ! CARD 18
   INTEGER, SAVE :: i_node, i_dir, i_hist  ! 外力點數、受力歷史總數
   INTEGER, ALLOCATABLE, SAVE :: force_node_map(:,:) ! (nnd, 3) -> Dir, Hist_ID

   ! CARD Output
   INTEGER, ALLOCATABLE, SAVE :: out_node(:), out_type(:), out_dir(:)

















   ! 只公開關鍵的大�����������節程���
   PUBLIC :: readata1
   PUBLIC :: bmass
   PUBLIC :: dynamic
   !PUBLIC :: compute_internal

CONTAINS

   ! ==========================================================
   ! CHAPTER 1: 數據讀取與初始化 (關鍵步驟)
   ! ==========================================================
   SUBROUTINE readata1(file_to_open)
      IMPLICIT NONE
      CHARACTER(LEN=*), INTENT(IN) :: file_to_open
      INTEGER :: unit_dat, i_err, comment_pos, i, j, k
      CHARACTER(LEN=512) :: line, clean_line
      REAL(8) :: temp_val
      LOGICAL :: found

      ! CARD 1
      INTEGER :: p

      ! CARD 3

      ! CARD 6

      ! CARD 7

      ! CARD 8

      ! CARD 10:

      ! CARD 15

      ! CARD 18

      ! CARD Output


      ! CHECK
      INTEGER :: echo_lun ! 檔案單元編號 (Logical Unit Number)


      ! ==========================================
      ! READ dat file
      ! ==========================================
      OPEN(NEWUNIT=unit_dat, FILE=TRIM(file_to_open), STATUS='OLD', ACTION='READ', IOSTAT=i_err)
      IF (i_err /= 0) THEN
         WRITE(*,*) " [ERROR] Cannot open file: ", TRIM(file_to_open)
         RETURN
      END IF

      ! --- CARD 12~14: Ground Acceleration (iacc = 1) --- Disabled in original
      ! --- CARD 19~20: Harmonic Force Loading (iforce3 = 1) --- Disabled in original
      ! --- CARD 21~24: Stirring/Central Force Loading (iforce4 = 1) --- Disabled in original

      ! ==========================================
      ! CARD 1: Project Title
      ! ==========================================
      CALL FIND_CARD(unit_dat, "CARD 1")

      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         ! 遇到結束符號 / 或是檔案結尾則退出
         IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT

         ! 跳過空行與註解
         IF (LEN_TRIM(ADJUSTL(line)) == 0 .OR. INDEX(ADJUSTL(line), "!") == 1) CYCLE

         ! --- 標籤掃描區 (可隨意調動順序) ---

         ! 1. 讀取 Project_Title
         IF (INDEX(line, "Project_Title") > 0) THEN
            p = INDEX(line, ":", BACK=.TRUE.)
            IF (p > 0) THEN
               temp_str = ADJUSTL(line(p+1:))
               IF (INDEX(temp_str, "/") > 0) temp_str = temp_str(1:INDEX(temp_str, "/")-1)
               project_name = TRIM(ADJUSTL(temp_str))
               WRITE(*, '(" [V5] Project: ", A)') TRIM(project_name)
            END IF
            CYCLE

            ! 2. 讀取 V5 檢查開關
         ELSE IF (INDEX(line, "Check_V5_Loading") > 0) THEN
            Check_V5_Loading = INT(GET_VALUE_AFTER_COLON(line))
            IF (Check_V5_Loading == 1) THEN
               WRITE(*,*) " [V5] Check is ENABLED. File will be generated."
            END IF
            CYCLE
         END IF

      END DO

      ! ==========================================
      ! CARD 2: Time Control
      ! ==========================================
      CALL FIND_CARD(unit_dat, "CARD 2")
      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT

         ! 跳��空��與��解
         IF (LEN_TRIM(ADJUSTL(line)) == 0 .OR. INDEX(ADJUSTL(line), "!") == 1) CYCLE

         ! 使用極簡標籤配對，順序可隨意調動
         IF (INDEX(line, "Start_Step") > 0) THEN
            minstp = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "Max_Step") > 0) THEN
            maxstp = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "Time_Step_Delta") > 0) THEN
            delta = GET_VALUE_AFTER_COLON(line)
            CYCLE
         ELSE IF (INDEX(line, "Damping_Alpha") > 0) THEN
            alpha = GET_VALUE_AFTER_COLON(line)
            CYCLE
         ELSE IF (INDEX(line, "Convergence_Toler") > 0) THEN
            toler = GET_VALUE_AFTER_COLON(line)
            CYCLE
         END IF
      END DO
      WRITE(*, '(" [V5] CARD 2 Loaded. MaxStep:", I0, " Delta:", F10.7)') maxstp, delta

      ! ==========================================
      ! CARD 3: Switches (開關參數讀取)
      ! ==========================================
      CALL FIND_CARD(unit_dat, "CARD 3")
      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         ! 遇到檔案結束或斜線結束符號則退出
         IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT

         ! 跳過空行與註解 (!)
         IF (LEN_TRIM(ADJUSTL(line)) == 0 .OR. INDEX(ADJUSTL(line), "!") == 1) CYCLE

         ! 標籤比對�����：只要 .dat 裡面有對應的括號變數名，順序可調動
         IF (INDEX(line, "(ifbody)") > 0) THEN
            ifbody = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "(iacc)") > 0) THEN
            iacc = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "(iforce2)") > 0) THEN
            iforce2 = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "(iforce3)") > 0) THEN
            iforce3 = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "(iforce4)") > 0) THEN
            iforce4 = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "(isequel)") > 0) THEN
            isequel = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         END IF
      END DO

      ! ==========================================
      ! CARD 4: Output & Geometry Control
      ! ==========================================
      CALL FIND_CARD(unit_dat, "CARD 4")
      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT

         ! 跳過空行與註解
         IF (LEN_TRIM(ADJUSTL(line)) == 0 .OR. INDEX(ADJUSTL(line), "!") == 1) CYCLE

         ! 標籤掃描區 (順序可調動)
         IF (INDEX(line, "(iprob)") > 0) THEN
            iprob = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "(iprobA)") > 0) THEN
            iprobA = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "(numout)") > 0) THEN
            numout = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "(isee)") > 0) THEN
            isee = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "(iplane)") > 0) THEN
            iplane = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "(icontact)") > 0) THEN
            icontact = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "(thick)") > 0) THEN
            thick = GET_VALUE_AFTER_COLON(line)
            CYCLE
         END IF
      END DO

      ! ==========================================
      ! CARD 6: Node Data (矩陣讀取)
      ! ==========================================
      ! 注意：這裡假設你已經��先��道 nnd 或是檔���中會先定義。
      ! �����������的 dat 格式，我們先掃描一次 CARD 6 ���出���多少節點
      CALL FIND_CARD(unit_dat, "CARD 6")
      nnd = 0
      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT
         IF (LEN_TRIM(ADJUSTL(line)) > 0) nnd = nnd + 1
      END DO

      ! 這裡觸發動態記憶體分配 (非常重要！)
      WRITE(*,*) " [V5] Detected Nodes (nnd):", nnd
      ALLOCATE(x_coord(nnd, 3), rifix(nnd, 3))
      ALLOCATE(d(nnd, 3), dn(nnd, 3), dnt(nnd, 3), vt(nnd, 3), at(nnd, 3))
      ALLOCATE(force(nnd,3), fsum(nnd,3))

      ! 回到 CARD 6 開頭讀入數據
      REWIND(unit_dat)
      CALL FIND_CARD(unit_dat, "CARD 6")
      DO i = 1, nnd
         READ(unit_dat, *) j, x_coord(i,1), x_coord(i,2), x_coord(i,3), &
            rifix(i,1), rifix(i,2), rifix(i,3)
      END DO
      WRITE(*,*) " [V5] CARD 6 Node Coordinates Loaded."

      ! ==========================================
      ! CARD 7: Element Topology
      ! ==========================================
      CALL FIND_CARD(unit_dat, "CARD 7")
      nel = 0

      ! 根據你的 dat 格式，����������������先掃描一次 CARD 7 算出有多少 element
      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT
         IF (LEN_TRIM(ADJUSTL(line)) > 0) nel = nel + 1
      END DO

      WRITE(*,*) " [V5] Detected Elements (nel):", nel
      ALLOCATE(rnode(nel, 10), sigma3D(nel, 6))
      ALLOCATE(xmass(nel*27), pint(nel*24)) ! 根據你原本的宣告需求

      REWIND(unit_dat)
      CALL FIND_CARD(unit_dat, "CARD 7")
      DO i = 1, nel
         ! ID, N1, N2, N3, N4,
         ! MatGrp, MatModel, Row, Col, Layer
         READ(unit_dat, *) rnode(i,1), rnode(i,2), rnode(i,3), rnode(i,4), rnode(i,5), &
            rnode(i,6), rnode(i,7), rnode(i,8), rnode(i,9), rnode(i,10)
      END DO
      WRITE(*,*) " [V5] CARD 7 Topology Loaded."

      ! 配合你原本的配置，同步配置這些新矩陣
      ALLOCATE(elem_topo(nel, 5), elem_mat(nel, 5))
      elem_topo(:, 1:5) = INT(rnode(:, 1:5)) ! 元素矩陣
      elem_mat(:, 1:5)  = INT(rnode(:, 6:10)) ! 材料矩陣

      ALLOCATE(elem_vol(nel))
      ALLOCATE(node_mass(nnd)) ! 使用 CARD 6 算出來的總節點數 nnd

      ! ==========================================
      ! CARD 8、9: Materials (材料參數細節讀取)
      ! Shane:日後可以改成輸入: 1, 3, 4 來讀取1,3,4材料
      ! ==========================================
      CALL FIND_CARD(unit_dat, "CARD 8")
      WRITE(*,*) " [DEBUG] Parsing Material Details..."

      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         IF (i_err /= 0 .OR. INDEX(line, "/") > 0) EXIT
         IF (LEN_TRIM(ADJUSTL(line)) == 0 .OR. INDEX(ADJUSTL(line), "!") == 1) CYCLE

         ! 1. 抓取總材料數並配置陣列
         IF (INDEX(line, "Total_Materials:") > 0) THEN
            nummat = INT(GET_VALUE_AFTER_COLON(line))
            IF (.NOT. ALLOCATED(e)) ALLOCATE(e(nummat, MAX_MAT_PARAMS))
            e = 0.0d0
            WRITE(*,*) " [V5] Total Materials allocated:", nummat
            CYCLE
         END IF

         ! 2. 偵測到新的材料組別 (處理 Material_Group)
         IF (INDEX(line, "Material_Group") > 0) THEN
            j = INT(GET_VALUE_AFTER_COLON(line))
            IF (j <= 0 .OR. j > nummat) CYCLE

            WRITE(*,*) " [DEBUG] Reading Group:", j

            ! 內層迴圈：讀取該組別內的參數
            DO
               READ(unit_dat, '(A)', IOSTAT=i_err) line
               ! 遇到結束符號退出
               IF (i_err /= 0 .OR. INDEX(line, "/") > 0) EXIT
               ! 跳過空行與註解
               IF (LEN_TRIM(ADJUSTL(line)) == 0 .OR. INDEX(ADJUSTL(line), "!") == 1) CYCLE

               ! 【關鍵】檢查是否撞到下一個 Material_Group
               ! (不管����面有沒有括號，只要是新的組別標籤就退回並交給外���)
               IF (INDEX(line, "Material_Group") > 0) THEN
                  BACKSPACE(unit_dat)
                  EXIT
               END IF

               ! --- 參數讀取區 (只要標籤��了，��序隨��調動��可��取) ---
               ! 使用 ELSE IF + CYCLE 加速判斷
               ! --- 參數讀取區 (標籤極簡化，確保 100% 匹配) ---
               IF (INDEX(line, "(mtyp1)") > 0) THEN
                  e(j, 1) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(mtyp2)") > 0) THEN
                  e(j, 2) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(rho)") > 0) THEN
                  e(j, 3) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(e)") > 0) THEN
                  e(j, 4) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(v)") > 0) THEN
                  e(j, 5) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(tau)") > 0) THEN
                  e(j, 6) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
                  ! CARD 9 進階屬性
               ELSE IF (INDEX(line, "(s_tens)") > 0) THEN
                  e(j, 7) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(s_frac)") > 0) THEN
                  e(j, 8) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(Et)") > 0) THEN
                  e(j, 9) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(beta)") > 0) THEN
                  e(j, 10) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(Phi)") > 0) THEN
                  e(j, 11) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(c)") > 0) THEN
                  e(j, 12) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               END IF


            END DO
         END IF
      END DO




      ! ==========================================
      ! CARD 10: Gravity History (ifbody = 1)
      ! Shane: 目前讀取後沒有使用
      ! 而是直接在 apply_external_forces 中指定 g 為 9.8
      ! ==========================================
      IF (ifbody == 1) THEN
         CALL FIND_CARD(unit_dat, "CARD 10")
         nptsG = 0
         DO
            READ(unit_dat, '(A)', IOSTAT=i_err) line
            IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT
            IF (LEN_TRIM(ADJUSTL(line)) > 0) nptsG = nptsG + 1
         END DO

         WRITE(*,*) " [V5] Gravity Points (nptsG):", nptsG
         ALLOCATE(grav_table(nptsG, 2))

         REWIND(unit_dat)
         CALL FIND_CARD(unit_dat, "CARD 10")
         DO i = 1, nptsG
            READ(unit_dat, *) grav_table(i,1), grav_table(i,2)
         END DO
         WRITE(*,*) " [V5] CARD 10 Gravity Table Loaded."
      END IF

      ! ==========================================
      ! CARD 15: Force History (DYNAMIC ALLOCATION)
      ! 外力
      ! 搭配CARD 18
      ! Shane: 目前讀取後沒有使用
      ! 而是直接在 apply_external_forces 中指定外力與作用節點
      ! ==========================================
      IF (iforce2 == 1) THEN
         CALL FIND_CARD(unit_dat, "CARD 15")

         ! --- 第一階段：掃描以確定動態大小 ---
         numif = 0
         max_pts = 0
         DO
            READ(unit_dat, '(A)', IOSTAT=i_err) line
            IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT

            IF (INDEX(line, "Total_Histories") > 0) numif = INT(GET_VALUE_AFTER_COLON(line))

            IF (INDEX(line, "History_ID:") > 0) THEN
               current_pts = 0
               DO
                  READ(unit_dat, '(A)', IOSTAT=i_err) line
                  IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT
                  ! 遇到下一個 ID 或結束標記，退回並計算
                  IF (INDEX(line, "History_ID:") > 0) THEN
                     BACKSPACE(unit_dat)
                     EXIT
                  END IF
                  ! 簡單檢查��否�����據��（��含��號��������空��
                  IF (LEN_TRIM(ADJUSTL(line)) > 0 .AND. INDEX(line, ".") > 0) THEN
                     current_pts = current_pts + 1
                  END IF
               END DO
               IF (current_pts > max_pts) max_pts = current_pts
            END IF
         END DO

         ! --- 第二階段：根據掃描結果進行 ALLOCATE ---
         IF (numif > 0 .AND. max_pts > 0) THEN
            IF (ALLOCATED(force_table)) DEALLOCATE(force_table)
            ALLOCATE(force_table(numif, max_pts, 2))
            force_table = 0.0d0

            ! 回到開頭重新讀取數值
            REWIND(unit_dat)
            CALL FIND_CARD(unit_dat, "CARD 15")
            DO
               READ(unit_dat, '(A)', IOSTAT=i_err) line
               IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT

               IF (INDEX(line, "History_ID:") > 0) THEN
                  j = INT(GET_VALUE_AFTER_COLON(line))
                  i = 1
                  DO
                     READ(unit_dat, '(A)', IOSTAT=i_err) line
                     IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT
                     IF (INDEX(line, "History_ID:") > 0) THEN
                        BACKSPACE(unit_dat)
                        EXIT
                     END IF
                     IF (LEN_TRIM(ADJUSTL(line)) == 0) CYCLE

                     READ(line, *, IOSTAT=i_err) force_table(j, i, 1), force_table(j, i, 2)
                     IF (i_err == 0) i = i + 1
                  END DO
               END IF
            END DO
            WRITE(*, '(" [V5] Force Table Allocated: (", I0, ",", I0, ",2)")') numif, max_pts
         END IF
      END IF

      ! ==========================================
      ! CARD 18: Node Force Assignment 搭配 CARD 15
      ! ==========================================
      IF (iforce2 == 1) THEN
         CALL FIND_CARD(unit_dat, "CARD 18")
         WRITE(*,*) " [DEBUG] Mapping Forces to Nodes..."

         ! 存儲每個節點對應的 History ID
         IF (.NOT. ALLOCATED(force_node_map)) ALLOCATE(force_node_map(nnd, 3))
         force_node_map = 0

         DO
            READ(unit_dat, '(A)', IOSTAT=i_err) line
            ! 遇到 / 或檔案結尾則跳出
            IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT
            IF (LEN_TRIM(ADJUSTL(line)) == 0 .OR. INDEX(ADJUSTL(line), "!") == 1) CYCLE

            ! 讀取: 節點ID, 方向, 歷時ID
            ! 使用整數讀取，避免 temp_val (REAL) 轉換產生的精度問題
            READ(line, *, IOSTAT=i_err) i_node, i_dir, i_hist

            IF (i_err == 0) THEN
               ! 安全性檢查：確保索引在 nnd*3 的範圍內
               IF (i_node >= 1 .AND. i_node <= nnd .AND. i_dir >= 1 .AND. i_dir <= 3) THEN
                  force_node_map(i_node, i_dir) = i_hist
               ELSE
                  WRITE(*, '(" [ERROR] CARD 18 Invalid Assignment: Node", I0, " Dir", I0)') i_node, i_dir
               END IF
            END IF
         END DO
      END IF

      ! ==========================================
      ! CARD Output: Output Request
      ! ==========================================
      ! --- readata1 內的 CARD Output ---
      CALL FIND_CARD(unit_dat, "CARD Output")
      i = 0
      ! 第一次掃描計算數量
      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT
         IF (LEN_TRIM(ADJUSTL(line)) > 0) i = i + 1
      END DO

      ! 檢查資料行數是否滿足 CARD 4 的 numout 設���
      IF (numout > i) THEN
         WRITE(*, '(/, A, I0, A, I0, A)') " [Error] CARD Output line count (", i, &
            ") is less than the required numout (", numout, "). Please check the data file."
         STOP
      END IF

      ALLOCATE(out_node(numout), out_type(numout), out_dir(numout))

      REWIND(unit_dat)
      CALL FIND_CARD(unit_dat, "CARD Output")
      DO i = 1, numout
         READ(unit_dat, *) out_node(i), out_type(i), out_dir(i)
         WRITE(*, '(" [V5] Monitored Node:", I0, " Type:", I0, " Dir:", I0)') &
            out_node(i), out_type(i), out_dir(i)
      END DO


      ! ==========================================
      ! LOAD FINISHED
      ! ==========================================
      CLOSE(unit_dat)
      WRITE(*,*) " [V5] All CARDs Loaded successfully."

      ! ==========================================
      ! [Check Data] 將讀取結果輸出至獨立檔案進行比對
      ! ==========================================

      if (Check_V5_Loading == 1) then

         !OPEN(UNIT=echo_lun, FILE=trim(MAKE_FILE_NAME('V5_Data_Echo_Check.txt')), STATUS='REPLACE')
         OPEN(NEWUNIT=echo_lun, FILE=trim('V5_Data_Echo_Check.txt'), STATUS='REPLACE')

         WRITE(echo_lun, *) "=== V5 DATA LOADER ECHO CHECK ==="
         WRITE(echo_lun, *) "Check_V5_Loading:",  Check_V5_Loading
         WRITE(echo_lun, *) "Project Title : ", TRIM(temp_str)
         WRITE(echo_lun, *) " "
         ! --- CARD 2, 3, 4 ---
         WRITE(echo_lun, *) "[CARD 2-4 Controls]"
         WRITE(echo_lun, '(A, I10)') "  Start_Step     : ", minstp
         WRITE(echo_lun, '(A, I10)') "  Max_Step      : ", maxstp
         WRITE(echo_lun, '(A, ES15.7)') "  Time_Step_Delta    : ", delta
         WRITE(echo_lun, '(A, F10.4)') "  Damping_Alpha : ", alpha
         WRITE(echo_lun, '(A, ES15.7)') "  Convergence_Toler    : ", toler

         WRITE(echo_lun, '(A, 6I5)')   "  Switches      : ", ifbody, iacc, iforce2, iforce3, iforce4, isequel

         WRITE(echo_lun, '(A, 7I10)')   "  Output and Geometry Control      : " &
            , iprob, iprobA, numout, isee, iforce4, iplane, icontact
         WRITE(echo_lun, '(A, F10.4)') "  Thickness     : ", thick
         WRITE(echo_lun, *) " "

         ! --- CARD 6: Nodes (全量輸出以便比對) ---
         WRITE(echo_lun, *) "[CARD 6 Nodes]"
         DO i = 1, nnd
            WRITE(echo_lun, '(I8, 3F15.6, 3F5.0)') i, x_coord(i,1), x_coord(i,2), x_coord(i,3), &
               rifix(i,1), rifix(i,2), rifix(i,3)
         END DO
         WRITE(echo_lun, *) " "


         ! --- CARD 7: Elements (全量輸出) ---
         WRITE(echo_lun, *) "[CARD 7 Elements]"
         DO i = 1, nel
            WRITE(echo_lun, '(I8, 4I8, 5I8)')   &
               INT(rnode(i,1)), INT(rnode(i,2)), INT(rnode(i,3)), INT(rnode(i,4)), INT(rnode(i,5)), &
               INT(rnode(i,6)), INT(rnode(i,7)), INT(rnode(i,8)), INT(rnode(i,9)), INT(rnode(i,10))

         END DO
         WRITE(echo_lun, *) " "
         ! --- CARD 8 & 9: Materials ---
         WRITE(echo_lun, *) "[CARD 8-9 Materials]"
         WRITE(echo_lun, '(A, I2)') "Total_Materials: ", nummat

         DO j = 1, nummat
            WRITE(echo_lun, '(A, I2)') "Material Group: ", j

            ! 對於 mtyp1, mtyp2 這種本質是編號的，可以用 F10.0 (不顯示小數)
            WRITE(echo_lun, '(A, F10.0)') "  (mtyp1): ", e(j, 1)
            WRITE(echo_lun, '(A, F10.0)') "  (mtyp2): ", e(j, 2)

            ! 對於物理參數，統一使用 E 格式以確保精度完整
            WRITE(echo_lun, '(A, ES15.7)') "  (rho):   ", e(j, 3)
            WRITE(echo_lun, '(A, ES15.7)') "  (e) (Pa):", e(j, 4)
            WRITE(echo_lun, '(A, ES15.7)') "  (v):     ", e(j, 5)
            WRITE(echo_lun, '(A, ES15.7)') "  (tau):   ", e(j, 6)
            WRITE(echo_lun, '(A, ES15.7)') "  (s_tens):", e(j, 7)
            WRITE(echo_lun, '(A, ES15.7)') "  (s_frac):", e(j, 8)
            WRITE(echo_lun, '(A, ES15.7)') "  (Et):    ", e(j, 9)
            WRITE(echo_lun, '(A, ES15.7)') "  (beta):  ", e(j, 10)
            WRITE(echo_lun, '(A, ES15.7)') "  (Phi):   ", e(j, 11)
            WRITE(echo_lun, '(A, ES15.7)') "  (c) (Pa):", e(j, 12)
         END DO
         WRITE(echo_lun, *) " "
         ! --- CARD 10 & 11: Gravity History ---
         IF (ifbody == 1 .AND. ALLOCATED(grav_table)) THEN
            WRITE(*,*) "[CARD 10] Gravity Table:"
            DO i = 1, nptsG
               WRITE(echo_lun, '("     Pt", I2, ": T=", F8.4, " Val=", F8.4)') i, grav_table(i,1), grav_table(i,2)
            END DO
         END IF

         ! --- CARD 15: Force History ---
         IF (iforce2 == 1 .AND. ALLOCATED(force_table)) THEN
            WRITE(echo_lun, *) "[CARD 15 Force History]"
            DO j = 1, numif
               WRITE(echo_lun, '(A, I3)') "History ID: ", j
               DO k = 1, 100
                  IF (k > 1 .AND. force_table(j,k,1) == 0.0) EXIT
                  WRITE(echo_lun, '(F10.5, E15.7)') force_table(j,k,1), force_table(j,k,2)
               END DO
            END DO
         END IF

         ! --- CARD 18  ---
         IF (iforce2 == 1 .AND. ALLOCATED(force_node_map)) THEN
            WRITE(echo_lun, *) "[CARD 18] Node-Force Assignments:"
            DO i = 1, nnd
               IF (ANY(force_node_map(i,:) > 0)) &
                  WRITE(echo_lun,  '("   Node", I4, " -> DirX:", I2, " DirY:", I2, " DirZ:", I2)') &
                  i, force_node_map(i,1), force_node_map(i,2), force_node_map(i,3)
            END DO
         END IF

         ! --- CARD Output  ---
         DO i = 1, numout
            WRITE(echo_lun, '(" CARD Output:", I0, " Type:", I0, " Dir:", I0)') &
               out_node(i), out_type(i), out_dir(i)
         END DO

         CLOSE(echo_lun)
         WRITE(*,*) " [V5] Verification file 'V5_Data_Echo_Check.txt' has been generated."


      endif

   END SUBROUTINE readata1

   ! =========================================================
   ! CHAPTER 1.5: 計算單元���積���分���節���總質量 (現代化雙層概念版 - 混合平行版)
   ! =========================================================
   SUBROUTINE bmass()
      IMPLICIT NONE
      INTEGER :: i
      INTEGER :: n1, n2, n3, n4
      REAL(8) :: x1, x2, x3, x4, y1, y2, y3, y4, z1, z2, z3, z4
      REAL(8) :: x21, y21, z21, x31, y31, z31, x41, y41, z41
      REAL(8), ALLOCATABLE :: elem_mass(:)      ! (nel) -> 【新增】各四面體單元總質量
      REAL(8), ALLOCATABLE :: elem_mass_per_node(:) ! (nel) -> 單元分給單一節點的質量


      ! 1. 安全性檢查：確保所有需要的矩陣都已經正確在記憶體���配���
      IF (.NOT. ALLOCATED(elem_topo) .OR. .NOT. ALLOCATED(x_coord) .OR. &
         .NOT. ALLOCATED(node_mass)) THEN
         WRITE(*,*) "Fatal: [bmass] Required arrays are not allocated."
         STOP
      END IF
      ALLOCATE(elem_mass(nel), elem_mass_per_node(nel))

      ! 2. 重要動作：初始化本地節點總質量矩陣，全部歸零準備累加
      node_mass = 0.0d0

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
      !$OMP SHARED(nel, elem_topo, x_coord, e, elem_vol, elem_mat, elem_mass, elem_mass_per_node, node_mass)
      DO i = 1, nel

         ! 4. 提取四面體的 4 個節點編號
         n1 = elem_topo(i, 2)
         n2 = elem_topo(i, 3)
         n3 = elem_topo(i, 4)
         n4 = elem_topo(i, 5)

         ! 5. 根據節點編號，抓取 3D 空間座標
         x1 = x_coord(n1, 1);  y1 = x_coord(n1, 2);  z1 = x_coord(n1, 3)
         x2 = x_coord(n2, 1);  y2 = x_coord(n2, 2);  z2 = x_coord(n2, 3)
         x3 = x_coord(n3, 1);  y3 = x_coord(n3, 2);  z3 = x_coord(n3, 3)
         x4 = x_coord(n4, 1);  y4 = x_coord(n4, 2);  z4 = x_coord(n4, 3)

         ! 6. 計算三個邊向量
         x21 = x2 - x1;  y21 = y2 - y1;  z21 = z2 - z1
         x31 = x3 - x1;  y31 = y3 - y1;  z31 = z3 - z1
         x41 = x4 - x1;  y41 = y4 - y1;  z41 = z4 - z1

         ! 7. 使用純量三重積公式計算四面體體積
         elem_vol(i) = (x41 * (y21*z31 - y31*z21) + &
            y41 * (x31*z21 - x21*z31) + &
            z41 * (x21*y31 - x31*y21)) / 6.0d0

         ! 8. ��材料��度對��修��】
         !    A. elem_mat(i, 1) 儲存的是第 i 個單元的材料群組編號 j
         !    B. 直接去 e(j, 3) 查表抓出該組別的密度 (rho)
         !    C. 計算並儲存該四面體單元的「總質量」(體積 * 密度)
         !    D. 計算並��存該四面體單元的「������點的質量」
         elem_mass(i) = elem_vol(i) * e(elem_mat(i, 1), 3)
         elem_mass_per_node(i) = (elem_mass(i)) / 4.0d0

         ! 9. 【核心動作】多執行緒累加回本地陣列
         ! [OpenMP ATOMIC 關鍵防護]：
         ! 因為多個執行緒會同時存取同一個處理器記憶體中的 node_mass，此處必須使用 ATOMIC 防範 Data Race。
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

      WRITE(*,*) " [V5] Subroutine bmass processed elements (Hybrid Parallel Ready)."

      ! 在計算完體積後立刻印出

      WRITE(*,*) " [DEBUG] Element Volume calculated:", elem_vol
      WRITE(*,*) " [DEBUG] Node Mass calculated:", node_mass(4)

   END SUBROUTINE bmass


   ! ==========================================================
   ! CHAPTER 2: 動態記憶體分配邏輯 (關鍵步驟)
   ! ==========================================================
   SUBROUTINE dynamic()
      ! 這裡放決定陣列大小的邏輯，並呼叫 Utils 裡的分配程序
      IMPLICIT NONE
      INTEGER :: step  ! 時間步迭代子
      INTEGER :: i,j,k  ! 迴圈用的變數




      maxstp = 10
      DO step = minstp, maxstp

         ! A. 每個時步開始，全域節點總合力矩陣 fsum 必須清空歸零，準備重新累加
         fsum = 0.0d0

         ! B. 【核心步驟 3.1】計算外力 (包含 CARD 10 重力、CARD 15/18 節點外力歷史)
         !    這裡會依據當前時間 (step * delta) 更新外力並累加至 fsum
         CALL apply_external_forces(nnd, step, delta, node_mass, fsum, ifbody)
         IF (step == 1) WRITE(*,*) " [V5] apply_external_forces DONE"



         ! C. 【核心步驟 3.2】計算內力 (呼叫階段��重��戲)
         !    遍歷四面體單元，算出內力並用 !$OMP ATOMIC 減回/累加至 fsum
         ! [防禦性程式設計]: 如果剛度為 0，直接跳過內部力計算，確保剛體模式穩定
         IF (e(1,4) < 1.0d-12) THEN
            WRITE(*,*) " Matrix E = 0"
         else
            CALL compute_internal(nel, nnd, step, delta, x_coord, dn, fsum)
            IF (step == 1) WRITE(*,*) " [V5] compute_internal DONE"
         END IF


         ! D. 【核心步驟 2.4】執行顯式時間積分 (中心差分法)
         !    將所需的節點陣列明確傳入，利用 fsum 更新位移 dn
         CALL time_integration(nnd, delta, alpha, node_mass, fsum, at, vt, dn)
         IF (step == 1) WRITE(*,*) " [V5] time_integration DONE"
         WRITE(*,*) "Step:", step, " Node 4 Disp:", dn(4, 1), " Acc:", at(4, 1)

         ! E. 【核��步驟 2.5���施加固����邊界����件約���
         !    根據邊界���件矩陣 rifix，強制將約束節點的物理量歸���
         CALL apply_boundary_conditions(nnd, rifix, dn, vt, at)
         IF (step == 1) WRITE(*,*) " [V5] apply_boundary_conditions DONE"

         ! F. 【核心步驟 2.6】檔案輸出與監控
         ! 在 dynamic 迴圈中，計算合力之後，寫出當前狀態：
         WRITE(*,*) "STEP:", step, " Node 4 Mass:", node_mass(4), " Force_X:", fsum(4, 1)
         !    最�����������一哩路：輸出監控與 VTK 檔案

         CALL manage_output(step)
         IF (step == 1) WRITE(*,*) " [V5] manage_output DONE"

      END DO

      WRITE(*,*) " [V5] Simulation completed successfully."

   END SUBROUTINE dynamic


! ==========================================================
   ! CHAPTER 3.1: 全局外力計算 (重力場 + 預留使用者自訂時程 + 預留���體耦合)
   ! ==========================================================
   SUBROUTINE apply_external_forces(nnd, step, delta, node_mass, fsum, ifbody)
      IMPLICIT NONE
      INCLUDE 'omp_lib.h'

      ! --------------------------------------------------------
      ! 傳入引���規格宣��� (方針 A：嚴格控管 INTENT，無全域依賴)
      ! --------------------------------------------------------
      INTEGER, INTENT(IN)    :: nnd, step, ifbody
      REAL(8), INTENT(IN)    :: delta
      REAL(8), INTENT(IN)    :: node_mass(nnd)   ! 來自 bmass 算好的節點集中質量
      REAL(8), INTENT(INOUT) :: fsum(nnd, 3)     ! 注入目標：全局不平衡力帳本

      ! --------------------------------------------------------
      ! 區域變數宣告 (每個執行緒獨立擁有)
      ! --------------------------------------------------------
      INTEGER :: i
      REAL(8) :: current_time
      REAL(8) :: gravity_acc

      ! 1. 計算當前絕對物理時間 (用於未來時程外力內插或流體邊界時間軸對齊)
      current_time = dble(step) * delta

      ! --------------------------------------------------------
      ! 2. OpenMP 平行化外力注入 (符合 Fortran Column-Major 記憶體鐵律)
      ! --------------------------------------------------------
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, gravity_acc, ifbody) &
      !$OMP SHARED(nnd, node_mass, fsum)
      DO i = 1, nnd

         ! ===================================================
         ! 【物理項 A】: 靜態重力場負載 (F = m * g)
         ! ===================================================
         gravity_acc = -9.81d0

         ! 只有當 ifbody 為 1 時，才對所有具有質量的節點施加重力
         IF (ifbody == 1) THEN
            fsum(i, 3) = fsum(i, 3) + node_mass(i) * gravity_acc
         END IF


         ! ===================================================
         ! 【未來擴充：使用者自訂節點外力時程 (CARD 15/18)】
         ! ===================================================
         ! 說明：若未來有新使用者需要使用舊版的特定節點時間序列受力，
         !       可在此處直接對接 readata1 讀入的時程陣列進行線性內插。
         ! 【臨時硬編碼測試】：直接對第 4 號節點施加 X 方向 1.0 N 的力
         ! ===================================================
         IF (i == 4) THEN
            fsum(i, 1) = fsum(i, 1) + 1.0d0  ! 在 X 方向施加 1.0 N
            fsum(i, 2) = fsum(i, 2) + 0.0d0  ! Y 方向無力
            fsum(i, 3) = fsum(i, 3) + 0.0d0  ! Z 方向無力
         END IF

         ! ===================================================
         ! 【未來展望：流固耦合 FSI ��據注入區】
         ! ===================================================
         ! 說明：當未來與 Truchas 大專案對接時，流體傳過來的壓力和剪切力會轉換成節點水動力。
         !       屆時請擴充本程��引數，傳入 f_fluid(nnd, 3)���並解開下���三行：
         !
         ! fsum(i, 1) = fsum(i, 1) + f_fluid(i, 1)
         ! fsum(i, 2) = fsum(i, 2) + f_fluid(i, 2)
         ! fsum(i, 3) = fsum(i, 3) + f_fluid(i, 3)

      END DO
      !$OMP END PARALLEL DO

   END SUBROUTINE apply_external_forces






   ! ==========================================================
   ! CHAPTER 3.2: 全局內力計算與節點等效力組裝 (3D 四面體實體單元)
   ! ==========================================================
   SUBROUTINE compute_internal(nel, nnd, step, delta, x_coord, dn, fsum)
      IMPLICIT NONE
      INCLUDE 'omp_lib.h'

      ! --------------------------------------------------------
      ! 傳入引數規格宣告
      ! --------------------------------------------------------
      INTEGER, INTENT(IN)    :: nel, nnd, step
      REAL(8), INTENT(IN)    :: delta
      REAL(8), INTENT(IN)    :: x_coord(nnd, 3)  ! 初始無應變絕對座標 (CARD 6)
      REAL(8), INTENT(IN)    :: dn(nnd, 3)       ! 當前時步累積的節點位移矩陣
      REAL(8), INTENT(INOUT) :: fsum(nnd, 3)     ! 內力注入目標

      ! --------------------------------------------------------
      ! 區域變數宣告 (每個執行緒獨立，保障線程安全)
      ! --------------------------------------------------------
      INTEGER :: ielem
      INTEGER :: n1, n2, n3, n4
      INTEGER :: mat_grp, mat_model

      REAL(8) :: vol
      REAL(8) :: eps(6), sig(6)
      REAL(8) :: f_global(4, 3)

      ! 每個單元當前物理變形後的最新 3D 座標 (State 3)
      REAL(8) :: xc(4, 3)

      ! 幾何投影與 B 矩陣代數變數
      REAL(8) :: xl2, xl3, yl3, xl4, yl4, zl4
      REAL(8) :: b2, b3, b4, r2, r3, r4, o2, o3, o4, a1
      REAL(8) :: Q(3,3)

      REAL(8) :: E_mod, nu_poim, factor, factor_G




      ! ========================================================
      ! 🚀 OpenMP 單元大迴圈 (完美對齊 DEFAULT(NONE) 防護網)
      ! ========================================================
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(ielem, n1, n2, n3, n4, mat_grp, mat_model, vol, eps, sig, f_global, xc) &
      !$OMP PRIVATE(xl2, xl3, yl3, xl4, yl4, zl4, b2, b3, b4, r2, r3, r4, o2, o3, o4, a1, Q) &
      !$OMP PRIVATE(E_mod, nu_poim, factor, factor_G) &
      !$OMP SHARED(nel, elem_topo, elem_mat, elem_vol, sigma3D, x_coord, e, dn, fsum)


      DO ielem = 1, nel

         ! 1. 提取拓撲資訊
         n1 = elem_topo(ielem, 2)
         n2 = elem_topo(ielem, 3)
         n3 = elem_topo(ielem, 4)
         n4 = elem_topo(ielem, 5)

         mat_grp   = elem_mat(ielem, 1)
         mat_model = elem_mat(ielem, 2)

         ! 2. ⚡【關鍵突破】疊加初始座標與最新位移，解出當前 3D 真實幾何位置
         xc(1, :) = x_coord(n1, :) + dn(n1, :)
         xc(2, :) = x_coord(n2, :) + dn(n2, :)
         xc(3, :) = x_coord(n3, :) + dn(n3, :)
         xc(4, :) = x_coord(n4, :) + dn(n4, :)

         ! 3. 載入歷史應力
         sig(:) = sigma3D(ielem, :)

         ! ===================================================
         ! ⚙️ 核心步驟 A: 幾何變形與協同旋轉局部投影
         !    將當前最新 3D 座標傳入，計算隨體旋轉矩陣 Q 與局部幾何參數
         ! ===================================================
         CALL local_co_rotational_proj( &
            xc(1,:), xc(2,:), xc(3,:), xc(4,:), &
            xl2, xl3, yl3, xl4, yl4, zl4, vol, a1, &
            b2, b3, b4, r2, r3, r4, o2, o3, o4, Q)

         ! ===================================================
         ! ⚙️ 核心步驟 B: 計算真實應變 (還原舊版 fintiso3 精隨)
         ! ===================================================
         ! 提取局部相對淨變形量 (以局部座標直接計算應變增量)
         eps(1) = (b2*xl2 + b3*xl3 + b4*xl4) / a1 - 1.0d0 ! 減 1 得到淨工程線應變
         eps(2) = (r3*yl3 + r4*yl4) / a1 - 1.0d0
         eps(3) = (o4*zl4) / a1 - 1.0d0
         eps(4) = (o3*yl3 + o4*yl4 + r4*zl4) / a1
         eps(5) = (o2*xl2 + o3*xl3 + o4*xl4 + b4*zl4) / a1
         eps(6) = (r2*xl2 + r3*xl3 + b3*yl3 + r4*xl4 + b4*yl4) / a1

         ! ===================================================
         ! ⚙️ 核心步驟 C: 3D 固體力學純彈性本構計算 (應力更新)
         ! ===================================================
         ! 1. 從現代化材料庫 e 撈取材料常數 (擺脫死板索引)
         E_mod   = e(mat_grp, 1)  ! 楊氏模數 Young's Modulus
         nu_poim = e(mat_grp, 2)  ! 卜松比 Poisson's Ratio

         ! 2. 計算 3D 拉梅常數 (Lame Constants) 與彈性係數
         factor = E_mod / ((1.0d0 + nu_poim) * (1.0d0 - 2.0d0 * nu_poim))

         ! 3. 依據全量工程應��� eps，直接更新當前 6 個 3D 應力分量 (sig)
         sig(1) = factor * ((1.0d0 - nu_poim)*eps(1) + nu_poim*eps(2) + nu_poim*eps(3)) ! sigma_x
         sig(2) = factor * (nu_poim*eps(1) + (1.0d0 - nu_poim)*eps(2) + nu_poim*eps(3)) ! sigma_y
         sig(3) = factor * (nu_poim*eps(1) + nu_poim*eps(2) + (1.0d0 - nu_poim)*eps(3)) ! sigma_z

         ! 剪應力分量 (G = E / (2*(1+nu)))
         factor_G = E_mod / (2.0d0 * (1.0d0 + nu_poim))
         sig(4) = factor_G * eps(4) ! sigma_yz
         sig(5) = factor_G * eps(5) ! sigma_xz
         sig(6) = factor_G * eps(6) ! sigma_xy

         ! 將最��應力回寫至全局歷史陣��，供 VTK 輸出或下一個時步參考
         sigma3D(ielem, :) = sig(:)

         ! ===================================================
         ! ⚙️ 核心步驟 D: Dr. Wu 平衡反推法與座標逆旋轉
         ! ===================================================
         CALL dr_wu_equilibrium_backsolve( &
            vol, a1, sig, xl2, xl3, yl3, yl4, zl4, &
            b2, b3, b4, r2, r3, r4, o2, o3, o4, Q, f_global)

         ! ===================================================
         ! 🔒 核心步驟 E: !$OMP ATOMIC 安全力學組裝
         ! ===================================================
         !$OMP ATOMIC
         fsum(n1, 1) = fsum(n1, 1) - f_global(1, 1)
         !$OMP ATOMIC
         fsum(n1, 2) = fsum(n1, 2) - f_global(1, 2)
         !$OMP ATOMIC
         fsum(n1, 3) = fsum(n1, 3) - f_global(1, 3)

         !$OMP ATOMIC
         fsum(n2, 1) = fsum(n2, 1) - f_global(2, 1)
         !$OMP ATOMIC
         fsum(n2, 2) = fsum(n2, 2) - f_global(2, 2)
         !$OMP ATOMIC
         fsum(n2, 3) = fsum(n2, 3) - f_global(2, 3)

         !$OMP ATOMIC
         fsum(n3, 1) = fsum(n3, 1) - f_global(3, 1)
         !$OMP ATOMIC
         fsum(n3, 2) = fsum(n3, 2) - f_global(3, 2)
         !$OMP ATOMIC
         fsum(n3, 3) = fsum(n3, 3) - f_global(3, 3)

         !$OMP ATOMIC
         fsum(n4, 1) = fsum(n4, 1) - f_global(4, 1)
         !$OMP ATOMIC
         fsum(n4, 2) = fsum(n4, 2) - f_global(4, 2)
         !$OMP ATOMIC
         fsum(n4, 3) = fsum(n4, 3) - f_global(4, 3)

      END DO
      !$OMP END PARALLEL DO



   CONTAINS
! =======================================================
      ! SUBROUTINE: 局部協同旋轉幾何投影 (補齊未宣告變數版)
      ! =======================================================
      SUBROUTINE local_co_rotational_proj(x1, x2, x3, x4, &
         xl2, xl3, yl3, xl4, yl4, zl4, &
         vol, a1, b2, b3, b4, r2, r3, r4, o2, o3, o4, QMatrix)
         IMPLICIT NONE
         REAL(8), INTENT(IN)  :: x1(3), x2(3), x3(3), x4(3)
         REAL(8), INTENT(OUT) :: xl2, xl3, yl3, xl4, yl4, zl4, vol, a1
         REAL(8), INTENT(OUT) :: b2, b3, b4, r2, r3, r4, o2, o3, o4
         REAL(8), INTENT(OUT) :: QMatrix(3,3)

         ! 區域幾何向量與純量
         REAL(8) :: v21(3), v31(3), v41(3)
         REAL(8) :: ex(3), ey(3), ez(3)
         REAL(8) :: rlen

         ! 💡 補齊編報錯誤的未宣告局部變數 (隨體座標系定義下，這些分量皆為 0)
         REAL(8) :: yl2, zl2, zl3

         yl2 = 0.0d0
         zl2 = 0.0d0
         zl3 = 0.0d0

         ! 1. 計算變形後的邊向量
         v21 = x2 - x1
         v31 = x3 - x1
         v41 = x4 - x1

         ! 2. 建立隨體座標���底
         rlen = sqrt(dot_product(v21, v21))
         IF (rlen > 1.0e-12) THEN
            ex = v21 / rlen
         ELSE
            ex = (/1.0d0, 0.0d0, 0.0d0/)
         END IF

         ez(1) = ex(2)*v31(3) - ex(3)*v31(2)
         ez(2) = ex(3)*v31(1) - ex(1)*v31(3)
         ez(3) = ex(1)*v31(2) - ex(2)*v31(1)
         rlen = sqrt(dot_product(ez, ez))
         IF (rlen > 1.0e-12) THEN
            ez = ez / rlen
         ELSE
            ez = (/0.0d0, 0.0d0, 1.0d0/)
         END IF

         ey(1) = ez(2)*ex(3) - ez(3)*ex(2)
         ey(2) = ez(3)*ex(1) - ez(1)*ex(3)
         ey(3) = ez(1)*ex(2) - ez(2)*ex(1)

         QMatrix(1, :) = ex
         QMatrix(2, :) = ey
         QMatrix(3, :) = ez

         ! 3. 投影計算局部座標
         xl2 = dot_product(v21, ex)
         xl3 = dot_product(v31, ex)
         yl3 = dot_product(v31, ey)
         xl4 = dot_product(v41, ex)
         yl4 = dot_product(v41, ey)
         zl4 = dot_product(v41, ez)

         vol = (xl4 * (xl2 * yl3)) / 6.0d0
         a1  = vol * 6.0d0

         ! 4. B 矩陣幾何因子計算
         b2 = (yl3*zl4);  b3 = 0.0d0;      b4 = (xl2*yl3)
         r2 = 0.0d0;      r3 = (xl2*zl4);  r4 = (-xl2*xl3)
         o2 = (xl3*yl4 - xl4*yl3); o3 = (xl4*xl2); o4 = (xl2*yl3)

      END SUBROUTINE local_co_rotational_proj

      ! =======================================================
      ! SUBROUTINE: Dr. Wu 靜力平衡反推力學核心 (完整型別宣告版)
      ! =======================================================
      SUBROUTINE dr_wu_equilibrium_backsolve(vol, a1, s, xl2, xl3, yl3, yl4, zl4, &
         b2, b3, b4, r2, r3, r4, o2, o3, o4, QMatrix, f_out)
         IMPLICIT NONE

         ! 1. 傳入引數規格宣告 (強型別防護)
         REAL(8), INTENT(IN)  :: vol, a1, s(6)
         REAL(8), INTENT(IN)  :: xl2, xl3, yl3, yl4, zl4
         REAL(8), INTENT(IN)  :: b2, b3, b4, r2, r3, r4, o2, o3, o4
         REAL(8), INTENT(IN)  :: QMatrix(3,3)
         REAL(8), INTENT(OUT) :: f_out(4,3)

         ! 2. 內部區域變數宣告
         REAL(8) :: f(12), fq(4,3), c1, c2, c3
         REAL(8) :: yl2_val, zl2_val, zl3_val, xl4_tmp

         ! 隨體座標系定義下的固定 0 元素純量
         yl2_val = 0.0d0
         zl2_val = 0.0d0
         zl3_val = 0.0d0
         xl4_tmp = xl4

         ! 3. 依據 3D 應力分量計算 2, 3, 4 號節點的局部力
         f = 0.0d0
         f(4)  = vol * (b2*s(1) + r2*s(4) + o2*s(6)) / a1
         f(7)  = vol * (b3*s(1) + r3*s(4) + o3*s(6)) / a1
         f(8)  = vol * (r3*s(2) + b3*s(4) + o3*s(5)) / a1
         f(10) = vol * (b4*s(1) + r4*s(4) + o4*s(6)) / a1
         f(11) = vol * (r4*s(2) + b4*s(4) + o4*s(5)) / a1
         f(12) = vol * (o4*s(3) + r4*s(5) + b4*s(6)) / a1

         ! 4. 運用 Dr. Wu 靜力平衡公式反推 1 號節點力與其餘分量
         c3 = yl2_val*xl3 - yl3*xl2
         IF (abs(c3) > 1.0e-12) THEN
            f(1) = -(f(4) + f(7) + f(10))
            f(5) = (f(4)*yl2_val + f(7)*yl3 - f(8)*xl3 + f(10)*yl4 - f(11)*xl4_tmp) / xl2
            f(2) = -(f(5) + f(8) + f(11))
            c1   = (f(11)*zl4 - f(12)*yl4)
            c2   = (f(10)*zl4 - f(12)*xl4_tmp)
            f(6) = (c1*xl3 - c2*yl3) / c3
            f(9) = (c2*yl2_val - c1*xl2) / c3
            f(3) = -(f(6) + f(9) + f(12))
         ELSE
            ! 防禦性力學機制���若退化，採用標準四面體靜力平衡解
            f(1) = -(f(4) + f(7) + f(10))
            f(2) = -(f(5) + f(8) + f(11))
            f(3) = -(f(6) + f(9) + f(12))
         END IF

         ! 5. 透過旋轉矩陣 QMatrix 轉回 3D 全局座標系
         fq(1,1) = QMatrix(1,1)*f(1) + QMatrix(2,1)*f(2) + QMatrix(3,1)*f(3)
         fq(1,2) = QMatrix(1,2)*f(1) + QMatrix(2,2)*f(2) + QMatrix(3,2)*f(3)
         fq(1,3) = QMatrix(1,3)*f(1) + QMatrix(2,3)*f(2) + QMatrix(3,3)*f(3)

         fq(2,1) = QMatrix(1,1)*f(4) + QMatrix(2,1)*f(5) + QMatrix(3,1)*f(6)
         fq(2,2) = QMatrix(1,2)*f(4) + QMatrix(2,2)*f(5) + QMatrix(3,2)*f(6)
         fq(2,3) = QMatrix(1,3)*f(4) + QMatrix(2,3)*f(5) + QMatrix(3,3)*f(6)

         fq(3,1) = QMatrix(1,1)*f(7) + QMatrix(2,1)*f(8) + QMatrix(3,1)*f(9)
         fq(3,2) = QMatrix(1,2)*f(7) + QMatrix(2,2)*f(8) + QMatrix(3,2)*f(9)
         fq(3,3) = QMatrix(1,3)*f(7) + QMatrix(2,3)*f(8) + QMatrix(3,3)*f(9)

         fq(4,1) = QMatrix(1,1)*f(10) + QMatrix(2,1)*f(11) + QMatrix(3,1)*f(12)
         fq(4,2) = QMatrix(1,2)*f(10) + QMatrix(2,2)*f(11) + QMatrix(3,2)*f(12)
         fq(4,3) = QMatrix(1,3)*f(10) + QMatrix(2,3)*f(11) + QMatrix(3,3)*f(12)

         f_out = fq
      END SUBROUTINE dr_wu_equilibrium_backsolve

   END SUBROUTINE compute_internal





   ! ==========================================================
   ! CHAPTER 2.4: 顯式時間積分 (中心差分法 - 模式 1 OpenMP 平行版)
   ! ==========================================================
   SUBROUTINE time_integration(nnd, delta, alpha, node_mass, fsum, at, vt, dn)
      IMPLICIT NONE
      INCLUDE 'omp_lib.h'

      ! 傳入引數規格宣告
      INTEGER, INTENT(IN)    :: nnd
      REAL(8), INTENT(IN)    :: delta, alpha
      REAL(8), INTENT(IN)    :: node_mass(nnd)
      REAL(8), INTENT(IN)    :: fsum(nnd, 3)
      REAL(8), INTENT(INOUT) :: at(nnd, 3)
      REAL(8), INTENT(INOUT) :: vt(nnd, 3)
      REAL(8), INTENT(INOUT) :: dn(nnd, 3)

      INTEGER :: i, j
      REAL(8) :: denom, coeff_v, coeff_a

      ! 1. 預先計算���式 1 的標準加權分母與係數，避免在迴圈內重複做昂貴的除法
      denom   = 2.0d0 + alpha * delta
      coeff_v = 2.0d0 - alpha * delta
      coeff_a = 2.0d0 * delta

      ! 2. 核心節點迴圈 (OpenMP 平行化加速)
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, j) &
      !$OMP SHARED(nnd, node_mass, fsum, at, vt, dn, delta, denom, coeff_v, coeff_a)
      DO i = 1, nnd

         ! 如果節點質量為零(防護機制)，跳過不計算加速度，避免除以零
         IF (node_mass(i) > 1.0d-14) THEN

            ! 遍歷 X, Y, Z 三個方向 (j = 1:X, 2:Y, 3:Z)
            DO j = 1, 3
               ! A. 牛頓第二運動定律更新當前加速度: a = F_sum / M
               at(i, j) = fsum(i, j) / node_mass(i)

               ! B. 模式 1 速度更新公式:
               !    vt_new = ((2 - alpha*dt)*vt_old + 2*dt*at) / (2 + alpha*dt)
               vt(i, j) = (coeff_v * vt(i, j) + coeff_a * at(i, j)) / denom

               ! C. 位移更新公式: dn_new = dn_old + vt_new * dt
               dn(i, j) = dn(i, j) + vt(i, j) * delta
            END DO

         ELSE
            ! 孤立節點或無質量節點物理量直接歸零
            at(i, :) = 0.0d0
            vt(i, :) = 0.0d0
         END IF

      END DO
      !$OMP END PARALLEL DO

   END SUBROUTINE time_integration

! ==========================================================
   ! CHAPTER 2.5: 施加固定邊界條件約束 (修正型別宣告與編碼版)
   ! ==========================================================
   SUBROUTINE apply_boundary_conditions(nnd, rifix, dn, vt, at)
      IMPLICIT NONE
      INCLUDE 'omp_lib.h'

      ! 1. 傳入引數規格宣告 (強型別防護)
      INTEGER, INTENT(IN)    :: nnd
      REAL(8), INTENT(IN)    :: rifix(nnd, 3)
      REAL(8), INTENT(INOUT) :: dn(nnd, 3)
      REAL(8), INTENT(INOUT) :: vt(nnd, 3)
      REAL(8), INTENT(INOUT) :: at(nnd, 3)

      ! 2. 內部區域變數宣告
      INTEGER :: i, j

      ! 3. 核心約束平行迴圈
      !$OMP PARALLEL DO DEFAULT(NONE) &
      !$OMP PRIVATE(i, j) &
      !$OMP SHARED(nnd, rifix, dn, vt, at)
      DO i = 1, nnd
         DO j = 1, 3

            ! 判斷是否為約束方向 (使用大於 0.9d0 作為浮點數安全判定)
            IF (rifix(i, j) > 0.9d0) THEN

               dn(i, j) = 0.0d0  ! Displacement Reset
               vt(i, j) = 0.0d0  ! Velocity Reset
               at(i, j) = 0.0d0  ! Acceleration Reset

            END IF

         END DO
      END DO
      !$OMP END PARALLEL DO

   END SUBROUTINE apply_boundary_conditions

   ! ==========================================================
   ! CHAPTER 2.6: 檔案輸出與監控
   ! ==========================================================

   SUBROUTINE manage_output(step)

      IMPLICIT NONE
      INTEGER, INTENT(IN) :: step
      INTEGER :: i, node, dir, otype
      REAL(8) :: value

      IF (MOD(step, 1) /= 0) RETURN

      !$OMP MASTER
      OPEN(UNIT=77, FILE='Node_Monitor_History.txt', ACCESS='APPEND', STATUS='UNKNOWN')

      DO i = 1, numout
         node  = out_node(i)
         otype = out_type(i)
         dir   = out_dir(i)

         ! 根據 out_type 選擇監控對象 (0:位移, 1:速度, 2:加速度)
         SELECT CASE (otype)
          CASE (0); value = dn(node, dir)
          CASE (1); value = vt(node, dir)
          CASE (2); value = at(node, dir)
          CASE DEFAULT; value = 0.0d0
         END SELECT

         WRITE(77, '(I10, I5, I5, 1PE20.10)') step, node, dir, value
      END DO

      CLOSE(77)
      !$OMP END MASTER
      !$OMP BARRIER
   END SUBROUTINE manage_output


END MODULE VFIFE_Core_module

```

---
# 🔗 參考資料


---