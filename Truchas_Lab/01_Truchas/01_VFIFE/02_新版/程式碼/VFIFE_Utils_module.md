---
type: 📝 Research
created: 2026-05-27 13:25
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
MODULE VFIFE_Utils_module
   !�j��n�D�Ҳդ��Ҧ����l�{�ǳ��������T�ŧi�ܼ�
   IMPLICIT NONE

   ! �u���}����u��A�O���������b
   PRIVATE
   PUBLIC :: FIND_CARD
   PUBLIC :: GET_VALUE_AFTER_COLON
   ! ���ӥi�b���[�J PUBLIC :: ALLOCATE_VFIFE_ARRAYS

CONTAINS

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
            WRITE(*,*) " [DEBUG] Found Section ", TRIM(search_tag), &
               " at line: ", line_count
            EXIT
         END IF
      END DO
   END SUBROUTINE FIND_CARD

   ! ==========================================================
   ! (1-2) FUNCTION GET_VALUE_AFTER_COLON
   ! ==========================================================
   FUNCTION GET_VALUE_AFTER_COLON(line) RESULT(val)
      CHARACTER(LEN=*), INTENT(IN) :: line
      REAL(8) :: val
      INTEGER :: pos, ios
      val = 0.0d0
      pos = INDEX(line, ":")
      IF (pos > 0) THEN
         READ(line(pos+1:), *, IOSTAT=ios) val
      END IF
   END FUNCTION GET_VALUE_AFTER_COLON

END MODULE VFIFE_Utils_module

```
---
# 🔗 參考資料


---