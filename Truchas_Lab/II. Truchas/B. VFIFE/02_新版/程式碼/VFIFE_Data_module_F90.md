---
type: 📝 Research
created: 2026-06-04 03:08
modified: 2026-06-09 03:38
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

``` fortran
MODULE VFIFE_Data_module

   IMPLICIT NONE

   CHARACTER(LEN=256)           :: V5_dat_name

   ! ==========================================================
   ! 全域控制變數與常數
   ! ==========================================================
   INTEGER, SAVE :: nnd          ! 總節點數 (CARD 6 算出來的)
   INTEGER, SAVE :: nel          ! 總單元數 (CARD 7 算出來的)
   INTEGER, SAVE :: ndof         ! 每個節點的自由度 (通常是 3)
   INTEGER, SAVE :: nyDisto      ! 單元扭曲判定標記
   REAL(8), SAVE :: acctime      ! 累積物理時間

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
   INTEGER :: Check_V5_Loading  ! 控制 V5_Dat_Check  輸出的開關
   INTEGER :: p ! 判斷 Project_Title 是否存在

   ! ==========================================================
   ! 時間與收斂控制變數 (來自 CARD 2)
   ! ==========================================================
   INTEGER, SAVE :: minstp           ! 起始時步 (Start_Step)
   INTEGER, SAVE :: maxstp           ! 最大時步 (Max_Step)
   REAL(8), SAVE :: delta_T          ! 時步大小 (Time_Step_Delta)
   REAL(8), SAVE :: alpha            ! 虛擬阻尼常數 (Damping_Alpha)
   REAL(8), SAVE :: toler            ! 收斂容許誤差 (Convergence_Toler)

   ! CARD 3
   INTEGER, SAVE :: ifbody, iacc, iforce2, iforce3, iforce4, isequel

   ! CARD 4
   INTEGER, SAVE :: iprob, iprobA, numout , isee, iplane, icontact
   REAL(8), SAVE :: thick

   ! ==========================================================
   ! 節點層級 (Node-level) 全域動態陣列 -> 來自原 CARD 6
   ! ==========================================================
   REAL(8), ALLOCATABLE, SAVE :: x_coord(:,:)     ! (3, nnd) 節點座標
   REAL(8), ALLOCATABLE, SAVE :: rifix(:,:)       ! (3, nnd) 固定邊界條件
   REAL(8), ALLOCATABLE, SAVE :: d(:,:), dn(:,:), dnt(:,:)
   REAL(8), ALLOCATABLE, SAVE :: vt(:,:), at(:,:)
   REAL(8), ALLOCATABLE, SAVE :: force(:,:), fsum(:,:) ! (3, nnd)


   ! ==========================================================
   ! 單元層級 (Element-level) 全域動態陣列 -> 來自原 CARD 7 拆分
   ! ==========================================================
   INTEGER, ALLOCATABLE, SAVE :: elem_topo(:,:)   ! (5, nel) -> [ID, N1, N2, N3, N4]
   INTEGER, ALLOCATABLE, SAVE :: elem_mat(:,:)    ! (5, nel) -> 材料性質相關整數
   REAL(8), ALLOCATABLE, SAVE :: elem_vol(:)      ! (nel)    -> 單元體積
   REAL(8), ALLOCATABLE, SAVE :: elem_rho(:)      ! (nel)    -> 單元密度
   REAL(8), ALLOCATABLE, SAVE :: elem_mass(:)      ! (nel) 各四面體單元的總質量
   REAL(8), ALLOCATABLE, SAVE :: elem_mass_per_node(:) ! (nel) 各四面體單元平分給四個節點的質量
   REAL(8), ALLOCATABLE, SAVE :: node_mass(:)     ! (nnd) 每個節點累積的總質量
   INTEGER, ALLOCATABLE, SAVE :: face_judge(:,:)   ! (4, nel) -> [F1, F2, F3, F4] 單元面判定矩陣


   ! CARD 7
   ! --- 現代化動態陣列宣告 --- nel*#
   REAL(8), ALLOCATABLE, SAVE :: rnode(:,:)    ! 10*nel
   REAL(8), ALLOCATABLE, SAVE :: sigma3D(:,:)  ! 6*nel
   REAL(8), ALLOCATABLE, SAVE :: xmass(:), pint(:)  ! 27*nel, 24*nel

   ! CARD 8
   INTEGER, SAVE :: nummat ! 材料種類數量
   INTEGER, SAVE :: MAX_MAT_PARAMS=20
   REAL(8), ALLOCATABLE, SAVE :: e(:,:) ! (MAX_MAT_PARAMS, nummat) -> 材料屬性


   ! CARD 10: 雖然有讀取，但目前沒用到
   INTEGER, SAVE :: nptsG  ! 重力時序資料數
   REAL(8), ALLOCATABLE, SAVE :: grav_table(:,:)  ! (nptsG, 2) -> Time, Value

   ! CARD 15
   INTEGER, SAVE :: numif, current_pts, max_pts  ! 重力點數、受力歷史總數
   REAL(8), ALLOCATABLE, SAVE :: force_table(:,:,:) ! (numif, max_pts, 2)

   ! CARD 18
   INTEGER, SAVE :: i_node, i_dir, i_hist  ! 外力點數、受力歷史總數
   INTEGER, ALLOCATABLE, SAVE :: force_node_map(:,:) ! (3, nnd) -> Dir, Hist_ID

   ! CARD Output
   INTEGER, ALLOCATABLE, SAVE :: out_node(:), out_type(:), out_dir(:)

   ! CHECK
   INTEGER :: unit_check ! 檔案單元編號 (Logical Unit Number)



CONTAINS




END MODULE VFIFE_Data_module

```
---
# 🔗 參考資料


---