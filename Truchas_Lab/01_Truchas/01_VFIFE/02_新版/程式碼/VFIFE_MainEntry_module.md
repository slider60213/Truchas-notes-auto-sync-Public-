---
type: 📝 Research
created: 2026-05-27 13:23
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
MODULE VFIFE_MainEntry_module
   USE VFIFE_Core_module  ! �ޥΤj���`�Greadata1, dynamic, compute_internal
   !SHANE 記得把 input_file 開回來
   !USE output_module,             ONLY: input_file

   IMPLICIT NONE          ! ��� Module �g�@���Y�i�A�j��n�D�Ҳդ��Ҧ����l�{�ǳ��������T�ŧi�ܼ�


   PRIVATE
   PUBLIC :: EXECUTE_VFIFE_SIMULATION
   character(LEN = 256),  public :: input_file

CONTAINS

   ! ==========================================================
   !  VFIFE �D����{�� (�����x�ŧO)
   ! ==========================================================
   SUBROUTINE EXECUTE_VFIFE_SIMULATION()
      CHARACTER(LEN=256)           :: V5_dat_name
      INTEGER                      :: i_err, u_inp

      WRITE(*,*) ">>> [VFIFE] Starting Simulation Workflow..."
      !input_file='V5_New_Dat_Format.inp'
      input_file='Code_devlope_test.inp'

      ! 1. ���� input_file �O�_�w�Q��� (�w�����ˬd)
      IF (LEN_TRIM(input_file) == 0) THEN
         WRITE(*,*) "Fatal: No input file specified in output_module."
         STOP
      END IF

      ! 2. �ϥ� NEWUNIT �}�ҭ�l .inp (�۰ʨ��o�t�ƽs���A�O�Ҥ��P Truchas �Ĭ�)
      OPEN(NEWUNIT=u_inp, FILE=TRIM(input_file), STATUS='OLD', IOSTAT=i_err)
      IF (i_err /= 0) THEN
         WRITE(*, '("Fatal: Cannot open [", A, "].")') TRIM(input_file)
         STOP
      END IF

      ! 3. �ʺA�ഫ�ɦW (�d�ҡGcase1.inp -> case1.dat)
      ! input_file(1:LEN_TRIM(input_file)-4) �|�I���̫�|�Ӧr�� ".inp"
      V5_dat_name = input_file(1:LEN_TRIM(input_file)-4) // '.dat'
      WRITE(*,*) " [DEBUG] V5 Solid logic will read from: ", TRIM(V5_dat_name)

      ! 4. ����֤�Ū���P�p��y�{
      WRITE(*,*) ' Shane: readata1 start'
      CALL readata1(V5_dat_name) ! �ǤJ�ഫ�᪺ .dat �ɦW
      WRITE(*,*) ' Shane: readata1 finish'

      WRITE(*,*) ' Shane: bmass start'
      CALL bmass()
      WRITE(*,*) ' Shane: bmass finish'

      WRITE(*,*) ' Shane: dynamic start'
      CALL dynamic()
      WRITE(*,*) ' Shane: dynamic finish'


      ! 5. �����ɮרòM�z
      CLOSE(u_inp)

      WRITE(*,*) ">>> [VFIFE] Simulation Completed."
   END SUBROUTINE EXECUTE_VFIFE_SIMULATION

END MODULE VFIFE_MainEntry_module

```
---
# 🔗 參考資料


---