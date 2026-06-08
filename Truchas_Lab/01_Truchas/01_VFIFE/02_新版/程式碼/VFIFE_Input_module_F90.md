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
MODULE VFIFE_Input_module

   USE VFIFE_Data_module
   USE VFIFE_Utils_module  ! 引用 1-1, 1-2 等小工具

   IMPLICIT NONE

   PUBLIC :: read_dat, check_dat

CONTAINS

   ! ==========================================================
   ! [Read Dat File] 數據讀取與初始化 (關鍵步驟)
   ! ==========================================================
   SUBROUTINE read_dat(file_to_open)
      IMPLICIT NONE
      CHARACTER(LEN=*), INTENT(IN) :: file_to_open
      CHARACTER(LEN=512) :: line
      INTEGER :: unit_dat   ! 讀取dat檔用的變數
      INTEGER :: i_err      ! 判斷錯誤的變數
      INTEGER :: i, j       ! 迴圈用的變數

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

         ! 跳過空行與註解
         IF (LEN_TRIM(ADJUSTL(line)) == 0 .OR. INDEX(ADJUSTL(line), "!") == 1) CYCLE

         ! 使用極簡標籤配對，順序可隨意調動
         IF (INDEX(line, "Start_Step") > 0) THEN
            minstp = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "Max_Step") > 0) THEN
            maxstp = INT(GET_VALUE_AFTER_COLON(line))
            CYCLE
         ELSE IF (INDEX(line, "Time_Step_Delta") > 0) THEN
            delta_T = GET_VALUE_AFTER_COLON(line)
            CYCLE
         ELSE IF (INDEX(line, "Damping_Alpha") > 0) THEN
            alpha = GET_VALUE_AFTER_COLON(line)
            CYCLE
         ELSE IF (INDEX(line, "Convergence_Toler") > 0) THEN
            toler = GET_VALUE_AFTER_COLON(line)
            CYCLE
         END IF
      END DO
      WRITE(*, '(" [V5] CARD 2 Loaded. MaxStep:", I0, " delta_T:", F10.7)') maxstp, delta_T

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

         ! 標籤比對:只要.dat 裡面有對應的括號變數名，順序可調動
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

      CALL FIND_CARD(unit_dat, "CARD 6")
      nnd = 0
      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT
         IF (LEN_TRIM(ADJUSTL(line)) > 0) nnd = nnd + 1
      END DO

      ! 計算矩陣尺寸
      WRITE(*,*) " [V5] Detected Nodes (nnd):", nnd
      ALLOCATE(x_coord(3, nnd), rifix(3, nnd), SOURCE=0.0d0)
      ALLOCATE(d(3, nnd), dn(3, nnd), dnt(3, nnd), vt(3, nnd), at(3, nnd), SOURCE=0.0d0)
      ALLOCATE(force(3, nnd), fsum(3, nnd), SOURCE=0.0d0)

      ! 回到 CARD 6 開頭讀入數據
      REWIND(unit_dat)
      CALL FIND_CARD(unit_dat, "CARD 6")
      DO i = 1, nnd
         READ(unit_dat, *) j, x_coord(1,i), x_coord(2,i), x_coord(3,i), &
            rifix(1,i), rifix(2,i), rifix(3,i)
      END DO
      WRITE(*,*) " [V5] CARD 6 Node Coordinates Loaded."

      ! ==========================================
      ! CARD 7: Element Topology
      ! ==========================================
      CALL FIND_CARD(unit_dat, "CARD 7")
      nel = 0

      ! 根據 CARD 7 讀取矩陣尺寸
      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT
         IF (LEN_TRIM(ADJUSTL(line)) > 0) nel = nel + 1
      END DO

      WRITE(*,*) " [V5] Detected Elements (nel):", nel
      ALLOCATE(rnode(10, nel), sigma3D(6, nel), SOURCE=0.0d0)
      ALLOCATE(xmass(nel*27), pint(nel*24), SOURCE=0.0d0)

      REWIND(unit_dat)
      CALL FIND_CARD(unit_dat, "CARD 7")
      DO i = 1, nel
         ! ID, N1, N2, N3, N4,
         ! MatGrp, MatModel, Row, Col, Layer
         READ(unit_dat, *) rnode(1,i), rnode(2,i), rnode(3,i), rnode(4,i), rnode(5,i), &
            rnode(6,i), rnode(7,i), rnode(8,i), rnode(9,i), rnode(10,i)
      END DO
      WRITE(*,*) " [V5] CARD 7 Topology Loaded."

      ! 配合你原本的配置，同步配置這些新矩陣
      ALLOCATE(elem_topo(5, nel), elem_mat(5, nel), SOURCE=0)
      elem_topo(1:5, :) = INT(rnode(1:5, :)) ! 元素矩陣
      elem_mat(1:5, :)  = INT(rnode(6:10, :)) ! 材料矩陣




      ! ==========================================
      ! CARD 8、9: Materials (材料參數細節讀取)
      ! Shane:日後可以改成輸入: 1, 3, 4 來讀取材料1,3,4
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
            IF (.NOT. ALLOCATED(e)) ALLOCATE(e(MAX_MAT_PARAMS, nummat))
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

               ! 偵測到新的材料組別
               IF (INDEX(line, "Material_Group") > 0) THEN
                  BACKSPACE(unit_dat)
                  EXIT
               END IF


               ! --- 參數讀取區 (標籤極簡化，確保 100% 匹配) ---
               IF (INDEX(line, "(mtyp1)") > 0) THEN
                  e(1, j) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(mtyp2)") > 0) THEN
                  e(2, j) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(rho)") > 0) THEN
                  e(3, j) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(e)") > 0) THEN
                  e(4, j) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(v)") > 0) THEN
                  e(5, j) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(tau)") > 0) THEN
                  e(6, j) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
                  ! CARD 9 進階屬性
               ELSE IF (INDEX(line, "(s_tens)") > 0) THEN
                  e(7, j) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(s_frac)") > 0) THEN
                  e(8, j) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(Et)") > 0) THEN
                  e(9, j) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(beta)") > 0) THEN
                  e(10, j) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(Phi)") > 0) THEN
                  e(11, j) = GET_VALUE_AFTER_COLON(line)
                  CYCLE
               ELSE IF (INDEX(line, "(c)") > 0) THEN
                  e(12, j) = GET_VALUE_AFTER_COLON(line)
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
         ALLOCATE(grav_table(nptsG, 2), SOURCE=0.0d0)

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
            ALLOCATE(force_table(numif, max_pts, 2), SOURCE=0.0d0)


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
         IF (.NOT. ALLOCATED(force_node_map)) ALLOCATE(force_node_map(3, nnd), SOURCE=0)

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
      ! --- read_dat 內的 CARD Output ---
      CALL FIND_CARD(unit_dat, "CARD Output")
      i = 0
      ! 第一次掃描計算數量
      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT
         IF (LEN_TRIM(ADJUSTL(line)) > 0) i = i + 1
      END DO

      ! 根據掃描結果進行 ALLOCATE
      IF (numout > i) THEN
         WRITE(*, '(/, A, I0, A, I0, A)') " [Error] CARD Output line count (", i, &
            ") is less than the required numout (", numout, "). Please check the data file."
         STOP
      END IF

      ALLOCATE(out_node(numout), out_type(numout), out_dir(numout), SOURCE=0)

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
   END SUBROUTINE read_dat

   ! ==========================================
   ! [Check Dat File] 將讀取結果輸出至獨立檔案進行比對
   ! ==========================================
   SUBROUTINE check_dat()
      IMPLICIT NONE

      INTEGER :: i, j, k    ! 迴圈用的變數
      INTEGER :: unit_check

      if (Check_V5_Loading == 1) then


         OPEN(NEWUNIT=unit_check, FILE=trim('V5_Dat_Check.txt'), STATUS='REPLACE')

         WRITE(unit_check, *) "=== V5 DATA CHECK ==="
         WRITE(unit_check, *) "Check_V5_Loading:",  Check_V5_Loading
         WRITE(unit_check, *) "Project Title : ", TRIM(temp_str)
         WRITE(unit_check, *) " "
         ! --- CARD 2, 3, 4 ---
         WRITE(unit_check, *) "[CARD 2-4 Controls]"
         WRITE(unit_check, '(A, I10)') "  Start_Step     : ", minstp
         WRITE(unit_check, '(A, I10)') "  Max_Step      : ", maxstp
         WRITE(unit_check, '(A, ES15.7)') "  Time_Step_Delta    : ", delta_T
         WRITE(unit_check, '(A, F10.4)') "  Damping_Alpha : ", alpha
         WRITE(unit_check, '(A, ES15.7)') "  Convergence_Toler    : ", toler

         WRITE(unit_check, '(A, 6I5)')   "  Switches      : ", ifbody, iacc, iforce2, iforce3, iforce4, isequel

         WRITE(unit_check, '(A, 7I10)')   "  Output and Geometry Control      : " &
            , iprob, iprobA, numout, isee, iforce4, iplane, icontact
         WRITE(unit_check, '(A, F10.4)') "  Thickness     : ", thick
         WRITE(unit_check, *) " "

         ! --- CARD 6: Nodes (全量輸出以便比對) ---
         WRITE(unit_check, *) "[CARD 6 Nodes]"
         DO i = 1, nnd
            WRITE(unit_check, '(I8, 3F15.6, 3F5.0)') i, x_coord(1,i), x_coord(2,i), x_coord(3,i), &
               rifix(1,i), rifix(2,i), rifix(3,i)
         END DO
         WRITE(unit_check, *) " "


         ! --- CARD 7: Elements (全量輸出) ---
         WRITE(unit_check, *) "[CARD 7 Elements]"
         DO i = 1, nel
            WRITE(unit_check, '(I8, 4I8, 5I8)')   &
               INT(rnode(1,i)), INT(rnode(2,i)), INT(rnode(3,i)), INT(rnode(4,i)), INT(rnode(5,i)), &
               INT(rnode(6,i)), INT(rnode(7,i)), INT(rnode(8,i)), INT(rnode(9,i)), INT(rnode(10,i))

         END DO
         WRITE(unit_check, *) " "
         ! --- CARD 8 & 9: Materials ---
         WRITE(unit_check, *) "[CARD 8-9 Materials]"
         WRITE(unit_check, '(A, I2)') "Total_Materials: ", nummat

         DO j = 1, nummat
            WRITE(unit_check, '(A, I2)') "Material Group: ", j

            ! 對於 mtyp1, mtyp2 這種本質是編號的，可以用 F10.0 (不顯示小數)
            WRITE(unit_check, '(A, F10.0)') "  (mtyp1): ", e(1, j)
            WRITE(unit_check, '(A, F10.0)') "  (mtyp2): ", e(2, j)

            ! 對於物理參數，統一使用 E 格式以確保精度完整
            WRITE(unit_check, '(A, ES15.7)') "  (rho):   ", e(3, j)
            WRITE(unit_check, '(A, ES15.7)') "  (e) (Pa):", e(4, j)
            WRITE(unit_check, '(A, ES15.7)') "  (v):     ", e(5, j)
            WRITE(unit_check, '(A, ES15.7)') "  (tau):   ", e(6, j)
            WRITE(unit_check, '(A, ES15.7)') "  (s_tens):", e(7, j)
            WRITE(unit_check, '(A, ES15.7)') "  (s_frac):", e(8, j)
            WRITE(unit_check, '(A, ES15.7)') "  (Et):    ", e(9, j)
            WRITE(unit_check, '(A, ES15.7)') "  (beta):  ", e(10, j)
            WRITE(unit_check, '(A, ES15.7)') "  (Phi):   ", e(11, j)
            WRITE(unit_check, '(A, ES15.7)') "  (c) (Pa):", e(12, j)
         END DO
         WRITE(unit_check, *) " "
         ! --- CARD 10 & 11: Gravity History ---
         IF (ifbody == 1 .AND. ALLOCATED(grav_table)) THEN
            WRITE(*,*) "[CARD 10] Gravity Table:"
            DO i = 1, nptsG
               WRITE(unit_check, '("     Pt", I2, ": T=", F8.4, " Val=", F8.4)') i, grav_table(i,1), grav_table(i,2)
            END DO
         END IF

         ! --- CARD 15: Force History ---
         IF (iforce2 == 1 .AND. ALLOCATED(force_table)) THEN
            WRITE(unit_check, *) "[CARD 15 Force History]"
            DO j = 1, numif
               WRITE(unit_check, '(A, I3)') "History ID: ", j
               DO k = 1, 100
                  IF (k > 1 .AND. force_table(j,k,1) == 0.0) EXIT
                  WRITE(unit_check, '(F10.5, E15.7)') force_table(j,k,1), force_table(j,k,2)
               END DO
            END DO
         END IF

         ! --- CARD 18  ---
         IF (iforce2 == 1 .AND. ALLOCATED(force_node_map)) THEN
            WRITE(unit_check, *) "[CARD 18] Node-Force Assignments:"
            DO i = 1, nnd
               IF (ANY(force_node_map(i,:) > 0)) &
                  WRITE(unit_check,  '("   Node", I4, " -> DirX:", I2, " DirY:", I2, " DirZ:", I2)') &
                  i, force_node_map(i,1), force_node_map(i,2), force_node_map(i,3)
            END DO
         END IF

         ! --- CARD Output  ---
         DO i = 1, numout
            WRITE(unit_check, '(" [CARD Output] Node:", I0, " Type:", I0, " Dir:", I0)') &
               out_node(i), out_type(i), out_dir(i)
         END DO

         CLOSE(unit_check)
         WRITE(*,*) " [V5] Verification file 'V5_Dat_Check.txt' has been generated."


      endif

   END SUBROUTINE check_dat

END MODULE VFIFE_Input_module

```

---
# 🔗 參考資料


---