---
type: 📝 Research
created: 2026-06-04 03:10
modified: 2026-07-30 03:21
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

   ! Basic Modules of VFIFE
   USE VFIFE_Data_module
   USE VFIFE_Utils_module

   IMPLICIT NONE

   PUBLIC :: read_data, check_data
   PRIVATE:: FIND_CARD
CONTAINS

   ! ==========================================================
   ! [Read Dat File] 數據讀取與初始化 (關鍵步驟)
   ! ==========================================================
   SUBROUTINE read_data(file_to_open)
      IMPLICIT NONE
      CHARACTER(LEN=*), INTENT(IN) :: file_to_open
      CHARACTER(LEN=512) :: line
      CHARACTER(LEN=512) :: temp_str  ! 區域字串解析暫存
      INTEGER :: unit_dat   ! 讀取 dat 檔用的變數
      INTEGER :: i_err      ! 判斷錯誤的變數
      INTEGER :: i, j       ! 迴圈用的變數
      INTEGER :: p          ! 區域字串切割指標

      ! ==========================================
      ! READ dat file
      ! ==========================================
      OPEN(NEWUNIT=unit_dat, FILE=TRIM(file_to_open), &
         STATUS='OLD', ACTION='READ', IOSTAT=i_err)
      IF (i_err /= 0) THEN
         WRITE(*,*) " [ERROR] Cannot open file: ", TRIM(file_to_open)
         STOP
      END IF


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
            IF (p > 0 .AND. p < LEN(line)) THEN
               temp_str = ADJUSTL(line(p+1:))
               IF (INDEX(temp_str, "/") > 0) temp_str = temp_str(1:INDEX(temp_str, "/")-1)
               project_name = TRIM(ADJUSTL(temp_str))
               !WRITE(*, '(" [V5] Project: ", A)') TRIM(project_name)
               WRITE(*,*) " [V5] Project: ", TRIM(project_name)
            END IF
            CYCLE
         END IF

         ! 2. 讀取 Deformable_Body 是否為可變形體
         IF (INDEX(line, "Deformable_Body") > 0) THEN
            Deformable_Body = INT(GET_VALUE_AFTER_COLON(line))
            WRITE(*,*) " [V5] Deformable_Body: ", Deformable_Body
            if (Deformable_Body == 1) then
               is_V5_deformable = .TRUE.
            end if
            CYCLE
         END IF

         ! 3. 讀取 V5 檢查開關
         IF (INDEX(line, "Check_V5_Loading") > 0) THEN
            Check_V5_Loading = INT(GET_VALUE_AFTER_COLON(line))
            IF (Check_V5_Loading == 1) THEN
               WRITE(*,*) " [V5] Check is ENABLED. File will be generated."
            END IF
            CYCLE
         END IF

      END DO
      WRITE(*,*) " [V5] Card 1 Loaded."

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
            V5_dt = GET_VALUE_AFTER_COLON(line)
            CYCLE
         ELSE IF (INDEX(line, "Damping_Alpha") > 0) THEN
            alpha = GET_VALUE_AFTER_COLON(line)
            CYCLE
         ELSE IF (INDEX(line, "Convergence_Toler") > 0) THEN
            toler = GET_VALUE_AFTER_COLON(line)
            CYCLE
         END IF
      END DO
      WRITE(*,*) " [V5] Card 2 Loaded."



      ! ==========================================
      ! CARD 6: Node Data (矩陣讀取)
      ! ==========================================
      CALL FIND_CARD(unit_dat, "CARD 6")
      nnd = 0
      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT
         line = ADJUSTL(line)
         IF (LEN_TRIM(line) > 0 .AND. INDEX(line, "!") /= 1) nnd = nnd + 1
      END DO

      WRITE(*,*) " [V5] Detected Nodes (nnd):", nnd
      ! 全域動態矩陣配置

      ALLOCATE(d(3, nnd), dn(3, nnd), dnt(3, nnd), vt(3, nnd), at(3, nnd), SOURCE=0.0d0)
      ALLOCATE(force(3, nnd), fsum(3, nnd), SOURCE=0.0d0)
      ALLOCATE(node_mass(nnd), SOURCE=0.0d0)

      REWIND(unit_dat)
      ALLOCATE(x_coord(3, nnd), rifix(3, nnd), SOURCE=0.0d0)
      CALL FIND_CARD(unit_dat, "CARD 6")
      DO i = 1, nnd
         READ(unit_dat, *) j, x_coord(1,i), x_coord(2,i), x_coord(3,i), &
            rifix(1,i), rifix(2,i), rifix(3,i)
      END DO



      ! 初始瞬時與基準座標與初始幾何對齊
      IF (.NOT. ALLOCATED(x_coord0)) ALLOCATE(x_coord0(3, nnd), SOURCE=0.0d0)
      x_coord0 = x_coord

      WRITE(*,*) " [V5] CARD 6 Node Coordinates Loaded."

      ! ==========================================
      ! CARD 7: Element Topology
      ! ==========================================
      CALL FIND_CARD(unit_dat, "CARD 7")
      nel = 0
      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         IF (i_err /= 0 .OR. INDEX(ADJUSTL(line), "/") == 1) EXIT
         line = ADJUSTL(line)
         IF (LEN_TRIM(line) > 0 .AND. INDEX(line, "!") /= 1) nel = nel + 1
      END DO

      WRITE(*,*) " [V5] Detected Elements (nel):", nel




      ! 補上單元歷史狀態與物理量陣列配置
      ALLOCATE(sigma3D(6, nel), SOURCE=0.0d0)
      ALLOCATE(sigmaP(6, nel), epslonP(6, nel), pstress(3, nel), SOURCE=0.0d0)
      ALLOCATE(elplas(nel), PLalphaP(nel), PLrP(nel), SOURCE=0.0d0)

      ALLOCATE(elem_vol(nel), elem_rho(nel), elem_mass(nel), elem_mass_per_node(nel), SOURCE=0.0d0)
      ALLOCATE(face_judge(4, nel), SOURCE=0)
      ALLOCATE(elem_vertices(3, 4, nel), elem_facecenter(3, 4, nel), SOURCE=0.0d0)
      ALLOCATE(elem_center(3, nel), elem_area(4, nel), elem_normal(3, 4, nel), SOURCE=0.0d0)


      REWIND(unit_dat)
      ALLOCATE(rnode(10, nel), SOURCE=0.0d0)
      CALL FIND_CARD(unit_dat, "CARD 7")
      DO i = 1, nel
         READ(unit_dat, *) rnode(1,i), rnode(2,i), rnode(3,i), rnode(4,i), rnode(5,i), &
            rnode(6,i), rnode(7,i), rnode(8,i), rnode(9,i), rnode(10,i)
      END DO
      WRITE(*,*) " [V5] CARD 7 Topology Loaded."

      ALLOCATE(elem_topo(5, nel), elem_mat(5, nel), SOURCE=0)
      elem_topo(1:5, :) = INT(rnode(1:5, :))
      elem_mat(1:5, :)  = INT(rnode(6:10, :))




      ! ==========================================
      ! CARD 8: Materials (材料參數細節讀取 - 動態組數版)
      ! Shane: 自動偵測出現的 Material_Group 數量並動態配置
      ! ==========================================
      CALL FIND_CARD(unit_dat, "CARD 8")
      WRITE(*,*) " [V5] Parsing Material Details..."

      ! --- 階段 1：預掃描 calculate nummat ---
      nummat = 0
      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         IF (i_err /= 0 .OR. INDEX(line, "/") > 0) EXIT
         IF (LEN_TRIM(ADJUSTL(line)) == 0 .OR. INDEX(ADJUSTL(line), "!") == 1) CYCLE

         IF (INDEX(line, "Material_Group") > 0) THEN
            nummat = nummat + 1
         END IF
      END DO

      WRITE(*,*) " [V5] Detected Active Material Groups (nummat):", nummat

      ! 動態配置材料矩陣
      IF (.NOT. ALLOCATED(e)) ALLOCATE(e(MAX_MAT_PARAMS, nummat), SOURCE=0.0d0)
      write(*,*) " [V5] Max material parameters allowed: ", MAX_MAT_PARAMS

      ! --- 回到 CARD 8 開頭，依序讀入各組數據 ---
      REWIND(unit_dat)
      CALL FIND_CARD(unit_dat, "CARD 8")

      j = 0  ! 用來當作矩陣 e(:, j) 的實際陣列索引 (1 ~ nummat)

      DO
         READ(unit_dat, '(A)', IOSTAT=i_err) line
         IF (i_err /= 0 .OR. INDEX(line, "/") > 0) EXIT
         IF (LEN_TRIM(ADJUSTL(line)) == 0 .OR. INDEX(ADJUSTL(line), "!") == 1) CYCLE

         ! 偵測到新的材料組別
         IF (INDEX(line, "Material_Group") > 0) THEN
            j = j + 1  ! 推進到下一個配置好的陣列位置

            WRITE(*,*) " [V5] Loading Material Group into Slot:", j

            ! 內層迴圈：讀取����組別內的參數
            DO
               READ(unit_dat, '(A)', IOSTAT=i_err) line
               IF (i_err /= 0 .OR. INDEX(line, "/") > 0) EXIT
               IF (LEN_TRIM(ADJUSTL(line)) == 0 .OR. INDEX(ADJUSTL(line), "!") == 1) CYCLE

               ! 遇到下一組材料，退回一行並跳出內層迴圈
               IF (INDEX(line, "Material_Group") > 0) THEN
                  BACKSPACE(unit_dat)
                  EXIT
               END IF

               ! --- 參數讀取區 ---
               IF (INDEX(line, "(mtyp1)") > 0) THEN
                  e(1, j) = GET_VALUE_AFTER_COLON(line)
               ELSE IF (INDEX(line, "(mtyp2)") > 0) THEN
                  e(2, j) = GET_VALUE_AFTER_COLON(line)
               ELSE IF (INDEX(line, "(rho)") > 0) THEN
                  e(3, j) = GET_VALUE_AFTER_COLON(line)
               ELSE IF (INDEX(line, "(e)") > 0 .AND. INDEX(line, "(mtyp") == 0) THEN
                  e(4, j) = GET_VALUE_AFTER_COLON(line)
               ELSE IF (INDEX(line, "(v)") > 0) THEN
                  e(5, j) = GET_VALUE_AFTER_COLON(line)
               ELSE IF (INDEX(line, "(tau)") > 0) THEN
                  e(6, j) = GET_VALUE_AFTER_COLON(line)
                  ! CARD 9 進階屬性
               ELSE IF (INDEX(line, "(s_tens)") > 0) THEN
                  e(7, j) = GET_VALUE_AFTER_COLON(line)
               ELSE IF (INDEX(line, "(s_frac)") > 0) THEN
                  e(8, j) = GET_VALUE_AFTER_COLON(line)
               ELSE IF (INDEX(line, "(Et)") > 0) THEN
                  e(9, j) = GET_VALUE_AFTER_COLON(line)
               ELSE IF (INDEX(line, "(beta)") > 0) THEN
                  e(10, j) = GET_VALUE_AFTER_COLON(line)
               ELSE IF (INDEX(line, "(Phi)") > 0) THEN
                  e(11, j) = GET_VALUE_AFTER_COLON(line)
               ELSE IF (INDEX(line, "(c)") > 0 .AND. INDEX(line, "(s_frac)") == 0) THEN
                  e(12, j) = GET_VALUE_AFTER_COLON(line)
               END IF

            END DO

            IF (INDEX(line, "/") > 0) EXIT
         END IF
      END DO



      ! Shane:
      ! 舊版的CARD 3~5、10~18是很醜的各種花式自訂外力
      ! 我一度有移植好參數讀取跟物理計算
      ! 但實用性跟可讀性實在太低了
      ! 你應該根據研究需求來自己改程式
      WRITE(*,*) " [V5] All CARDs Loaded successfully."

      ! 指針容器初始化
      ! 未來 SOUBROUTINE 調用變數就不用逐一引入
      ! 而是可直接傳入 Nodes, Elements 來作為INPUT
      call Link_VFIFE_Containers()
      WRITE(*,*) " [V5] read_data: VFIFE_containers init finish"

      ! ==========================================
      ! LOAD FINISHED
      ! ==========================================
      CLOSE(unit_dat)

   END SUBROUTINE read_data

   ! ==========================================
   ! [Check Dat File] 將讀取結果輸出至獨立檔案進行比對
   ! ==========================================
   SUBROUTINE check_data()
      IMPLICIT NONE

      INTEGER :: i, j    ! 迴圈用的變數
      INTEGER :: unit_check

      IF (Check_V5_Loading == 1) THEN

         OPEN(NEWUNIT=unit_check, FILE='V5_Dat_Check.txt', STATUS='REPLACE')

         WRITE(unit_check, *) "=== V5 DATA CHECK ==="
         WRITE(unit_check, *) "Project Title   : ", TRIM(project_name)
         WRITE(unit_check, *) "Deformable_Body:", Deformable_Body
         WRITE(unit_check, *) "Check_V5_Loading:", Check_V5_Loading
         WRITE(unit_check, *) " "

         ! --- CARD 2, 3, 4 ---
         WRITE(unit_check, *) "[CARD 2-4 Controls]"
         WRITE(unit_check, '(A, I10)') "  Start_Step         : ", minstp
         WRITE(unit_check, '(A, I10)') "  Max_Step           : ", maxstp
         WRITE(unit_check, '(A, ES15.7)') "  Time_Step_Delta    : ", V5_dt
         WRITE(unit_check, '(A, F10.4)') "  Damping_Alpha      : ", alpha
         WRITE(unit_check, '(A, ES15.7)') "  Convergence_Toler  : ", toler
         WRITE(unit_check, *) " "

         ! --- CARD 6: Nodes (全量輸出以便比對) ---
         WRITE(unit_check, *) "[CARD 6 Nodes]"
         WRITE(unit_check, '(A, I10)') "  Node         : ", nnd
         DO i = 1, nnd
            WRITE(unit_check, '(I8, 3F15.6, 3F5.0)') i, x_coord(1,i), x_coord(2,i), x_coord(3,i), &
               rifix(1,i), rifix(2,i), rifix(3,i)
         END DO
         WRITE(unit_check, *) " "

         ! --- CARD 7: Elements (全量輸出) ---
         WRITE(unit_check, *) "[CARD 7 Elements]"
         WRITE(unit_check, '(A, I10)') "  Element      : ", nel
         DO i = 1, nel
            WRITE(unit_check, '(I8, 4I8, 5I8)')   &
               INT(rnode(1,i)), INT(rnode(2,i)), INT(rnode(3,i)), INT(rnode(4,i)), INT(rnode(5,i)), &
               INT(rnode(6,i)), INT(rnode(7,i)), INT(rnode(8,i)), INT(rnode(9,i)), INT(rnode(10,i))
         END DO
         WRITE(unit_check, *) " "

         ! --- CARD 8: Materials ---
         WRITE(unit_check, *) "[CARD 8 Materials]"
         WRITE(unit_check, '(A, I2)') "Total_Materials: ", nummat

         DO j = 1, nummat
            WRITE(unit_check, '(A, I2)') "Material Group: ", j

            WRITE(unit_check, '(A, F10.0)') "  (mtyp1): ", e(1, j)
            WRITE(unit_check, '(A, F10.0)') "  (mtyp2): ", e(2, j)

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


         CLOSE(unit_check)
         WRITE(*,*) " [V5] Verification file 'V5_Dat_Check.txt' has been generated."

      END IF

   END SUBROUTINE check_data


   ! ==========================================================
   ! (1-1) SUBROUTINE FIND_CARD: �j�M���w���Ҩí��m����
   ! ==========================================================
   SUBROUTINE FIND_CARD(u_num, tag)
      INTEGER, INTENT(IN) :: u_num
      CHARACTER(LEN=*), INTENT(IN) :: tag
      CHARACTER(LEN=512) :: line, compressed_line
      INTEGER :: f_ios, comment_pos, i, j, line_count
      CHARACTER(LEN=64) :: search_tag
      CHARACTER(LEN=512) :: actual_filename
      LOGICAL :: is_opened

      ! 1. �ǳƼ��Ҧr�� (�۰��ର &TAG �åh�������Ů�)
      search_tag = "&"
      j = 2
      DO i = 1, LEN_TRIM(tag)
         IF (tag(i:i) /= ' ') THEN
            search_tag(j:j) = tag(i:i)
            j = j + 1
         END IF
      END DO

      ! 2. �ɮת��A�ˬd�P���Э��m (�T�O�i�ݮi��[cite: 1])
      INQUIRE(UNIT=u_num, OPENED=is_opened, NAME=actual_filename)
      IF (.NOT. is_opened) THEN
         WRITE(*,*) " [ERROR] Unit", u_num, " is NOT opened!"
         STOP
      ELSE
         ! �z�쥻�N�� REWIND�A�o��u�D�u��Ū���v�D�`���n[cite: 1]
         REWIND(u_num)
      END IF

      ! 3. �v�汽�y
      line_count = 0
      DO
         READ(u_num, '(A)', IOSTAT=f_ios) line
         line_count = line_count + 1

         IF (f_ios < 0) THEN
            WRITE(*, '("Fatal: [", A, "] not found in ", A)') &
               TRIM(search_tag), TRIM(actual_filename)
            STOP
         END IF

         ! �簣����[cite: 1]
         comment_pos = INDEX(line, "!")
         IF (comment_pos > 0) line = line(1:comment_pos-1)

         ! ���Y�r�� (�h���Ů�P Tab)[cite: 1]
         compressed_line = ""
         j = 1
         DO i = 1, LEN_TRIM(line)
            IF (line(i:i) /= ' ' .AND. line(i:i) /= ACHAR(9)) THEN
               compressed_line(j:j) = line(i:i)
               j = j + 1
            END IF
         END DO

         ! ��T�ǰt���Ҷ}�Y
         IF (INDEX(compressed_line, TRIM(search_tag)) == 1) THEN
            WRITE(*,*) " [V5] Found Section ", TRIM(search_tag), &
               " at line: ", line_count
            EXIT
         END IF
      END DO
   END SUBROUTINE FIND_CARD
END MODULE VFIFE_Input_module


```

---
# 🔗 參考資料


---