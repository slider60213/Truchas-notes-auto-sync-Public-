---
type: 📝 Research
created: 2026-06-04 03:08
modified: 2026-08-06 03:50
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

   ! Truchas
   USE kind_module, ONLY: int_kind, real_kind, log_kind
   USE pgslib_module, ONLY: PGSLIB_GS_Trace

   IMPLICIT NONE

   PUBLIC :: Link_VFIFE_Containers

   ! 固體節點平行通訊「地圖」，用於每一步質量與受力同步
   TYPE(PGSLIB_GS_Trace), POINTER, SAVE :: V5_Trace => NULL()
   ! 紀錄每個節點屬於哪一個處理器 (Rank)，作為 face_judgement 的邊界判定依據
   INTEGER, ALLOCATABLE, SAVE :: V5_Node_PE(:)

   ! ==========================================================
   ! 1. VFIFE 控制參數與旗標
   ! ==========================================================
   LOGICAL(KIND=log_kind), SAVE :: V5Slider !Physics namelist
   LOGICAL, SAVE                :: is_V5_initialized = .FALSE.
   LOGICAL, SAVE                :: is_V5_deformable = .FALSE.
   LOGICAL, SAVE                :: is_first_step = .FALSE.
   REAL(KIND=real_kind), SAVE   :: V5_time = 0.0d0
   INTEGER, SAVE                :: V5_mat_id  ! 會在 MATERIAL_INPUT 中設定
   INTEGER, SAVE, ALLOCATABLE   :: V5_ingbr(:) ! ncells

   ! 全域網格與自由度計數器
   INTEGER, SAVE, TARGET        :: nnd          ! 總節點數
   INTEGER, SAVE, TARGET        :: nel          ! 總單元數
   INTEGER, SAVE                :: ndof = 3     ! 3D 空間自由度
   CHARACTER(LEN=512), SAVE     :: V5_dat_name  ! 檔案名稱

   ! CARD 1
   CHARACTER(LEN=512), SAVE     :: project_name
   INTEGER, SAVE                :: Is_Deformable_Body
   INTEGER, SAVE                :: Check_V5_Loading

   ! CARD 2: Time Control
   REAL(KIND=real_kind), SAVE, TARGET        :: V5_User_dt



   ! CARD 3: 整合到下方(Node-level）
   ! x_coord
   ! rifix

   ! CARD 4: 整合到下方(Element-level)
   ! rnode


   ! CARD 5: 材料屬性
   INTEGER, SAVE :: nummat
   INTEGER, SAVE :: MAX_MAT_PARAMS = 20
   REAL(KIND=real_kind), ALLOCATABLE, SAVE :: e(:,:) ! (MAX_MAT_PARAMS, nummat)

   ! e(1:MAX_MAT_PARAMS, nummat)
   ! 1: Physical_Type (mtyp1)
   ! 2: Model_Type (mtyp2)
   ! 3: Density (rho)
   ! 4: Youngs_Modulus (e) (Pa)
   ! 5: Poisson_Ratio (v)
   ! 6: Relaxation_Time (tau)
   ! 7: Tensile_Strength (s_tens) (Pa)
   ! 8: Fracture_Stress (s_frac) (Pa)
   ! 9: Tangent_Modulus (Et)
   ! 10: Hardening_Beta (beta)
   ! 11: Internal_Friction_Angle (Phi)
   ! 12: Cohesion (c) (Pa)


   ! ==========================================================
   ! 2. 節點層級 (Node-level) 全域實體陣列 (TARGET)
   ! ==========================================================
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: x_coord(:,:)     ! (3, nnd) 瞬時幾何座標
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: x_coord0(:,:)    ! (3, nnd) 初始基準幾何座標
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: rifix(:,:)       ! (3, nnd) 固定邊界條件
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: d(:,:)           ! (3, nnd) 累積位移
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: dn(:,:)          ! (3, nnd)
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: dnt(:,:)         ! (3, nnd)
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: vt(:,:)          ! (3, nnd) 節點速度
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: vt_half(:,:)     ! (3, nnd) 節點半步速度 - 蛙躍法
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: at(:,:)          ! (3, nnd) 節點加速度
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: force(:,:)       ! (3, nnd) 節點合外力 (包含流體作用力)
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: fsum(:,:)        ! (3, nnd) 內外力合力累積陣列
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: node_mass(:)     ! (nnd) 每個節點累積的總質量

   ! ==========================================================
   ! 3. 單元層級 (Element-level) 全域實體陣列 (TARGET)
   ! ==========================================================
   INTEGER, ALLOCATABLE, SAVE, TARGET :: elem_topo(:,:)         ! (5, nel) -> [ID, N1, N2, N3, N4]
   INTEGER, ALLOCATABLE, SAVE, TARGET :: elem_mat(:,:)          ! (5, nel) -> 材料性質指標
   INTEGER, ALLOCATABLE, SAVE, TARGET :: face_judge(:,:)        ! (4, nel) -> 單元面判定矩陣 (1:外露面)
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: elem_vol(:)            ! (nel)    -> 單元體積
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: elem_rho(:)            ! (nel)    -> 單元密度
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: elem_mass(:)           ! (nel)    -> 單元總質量
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: elem_mass_per_node(:)  ! (nel)    -> 單元分配至頂點的質量(OMP用)

   ! 單元幾何資訊
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: elem_vertices(:,:,:)   ! (3, 4, nel) 4個頂點座標
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: elem_facecenter(:,:,:) ! (3, 4, nel) 4個面形心座標
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: elem_center(:,:)       ! (3, nel)    單元質心座標
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: elem_area(:,:)         ! (4, nel)    4個面的面積
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: elem_normal(:,:,:)     ! (3, 4, nel) 4個面指向單元外的單位法向量
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: elem_pressure(:,:)     ! (4, nel)    4個面的壓力
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: elem_velocity(:,:,:)   ! (3, 4, nel) 4個面的速度
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: elem_density(:,:)      ! (4, nel)    4個面的密度


   ! 歷史狀態物理量 (CARD 7 & 塑性歷史)
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: rnode(:,:)             ! (10, nel) 拓樸材料綜合矩陣
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: sigma3D(:,:)           ! (6, nel)  現時步應力陣列
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: sigmaP(:,:)            ! (6, nel)  舊時步歷史應力
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: epslonP(:,:)           ! (6, nel)  舊時步歷史應變
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: pstress(:,:)           ! (3, nel)  主應力矩陣
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: elplas(:)              ! (nel) 塑性歷史狀態
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: PLalphaP(:)            ! (nel) 塑性內變量 Alpha
   REAL(KIND=real_kind), ALLOCATABLE, SAVE, TARGET :: PLrP(:)                ! (nel) 塑性內變量 r

   ! ==========================================================
   ! 4. 流體 / 固體 VOF 與表面採樣變數
   ! ==========================================================
   REAL(real_kind), ALLOCATABLE, SAVE :: V5solid_vof(:) ! (ncells) 流體網格對應的固體 VOF 體積分數
   REAL(real_kind), ALLOCATABLE, SAVE :: V5solid_vof_t0(:)
   REAL(KIND=real_kind), SAVE :: V5_minX(3), V5_maxX(3)
   INTEGER, SAVE :: V5_fluid_istart, V5_fluid_iend
   INTEGER, SAVE :: V5_fluid_jstart, V5_fluid_jend
   INTEGER, SAVE :: V5_fluid_kstart, V5_fluid_kend

   INTEGER, SAVE :: num_surf_faces = 0
   REAL(KIND=real_kind), ALLOCATABLE, SAVE :: surf_node1(:,:)
   REAL(KIND=real_kind), ALLOCATABLE, SAVE :: surf_node2(:,:)
   REAL(KIND=real_kind), ALLOCATABLE, SAVE :: surf_node3(:,:)

   ! --- 流體網格 -> 固體節點/元素 的靜態反向鏈結串列 (Head-Next Structure) ---
   INTEGER(int_kind), ALLOCATABLE :: cell_node_head(:)  ! 大小: ncells (儲存第一個節點ID)
   INTEGER(int_kind), ALLOCATABLE :: node_next(:)       ! 大小: num_solid_nodes (下一個節點ID)

   INTEGER(int_kind), ALLOCATABLE :: cell_elem_head(:)  ! 大小: ncells (儲存第一個元素ID)
   INTEGER(int_kind), ALLOCATABLE :: elem_next(:)       ! 大小: max_elem_links (串列鏈結)
   INTEGER(int_kind), ALLOCATABLE :: elem_link_id(:)    ! 紀錄鏈結節點對應的實際 Element ID
   INTEGER(int_kind) :: elem_link_count


   REAL(KIND=real_kind), ALLOCATABLE :: V5solid_vel(:, :) ! (3, ncells) 固體回傳到流體的速度

   !=======================================================================
   ! ��固耦合 - 壓力採樣控制參數
   ! num_p_samples = 1 : 採樣面心 (預設，���算速度最快)
   ! num_p_samples = 3 : 採樣 3 個頂點
   ! num_p_samples = 4 : 採樣面心 + 3 個頂點
   ! num_p_samples = N : 支援��意 N 點通用重心座標採樣
   !=======================================================================
   INTEGER(int_kind) :: num_p_samples = 1

   ! =====================================================================
   ! 滑動塊體 (Slider) 與流體網格映射 (RBF + AABB) 相關變數
   ! =====================================================================
   ! Slider_influence_ratio: 滑動塊體影響範圍權重係數
   ! 預設值: 1.0_real_kind (即 100% 原範圍；若改為 1.2_real_kind 代表放大 20% 影響範圍)
   real(real_kind) :: Slider_influence_ratio = 1.2_real_kind

   ! base_support_radius: 基準 RBF 緊支撐影響半徑
   real(real_kind) :: base_support_radius

   ! ==========================================================
   ! 剛體 6-DOF 狀態變數 (Rigid Body 6-DOF State Variables)
   ! ==========================================================
   REAL(KIND=real_kind), SAVE :: V5_Rigid_mass         = 0.0_real_kind  ! 剛體總質量 (M)
   REAL(KIND=real_kind), SAVE :: V5_Rigid_CoM(3)       = 0.0_real_kind  ! 當前質心空間座標 (x_CoM)
   REAL(KIND=real_kind), SAVE :: V5_Rigid_CoM0(3)      = 0.0_real_kind  ! 初始質心空間座標 (x_CoM0)
   REAL(KIND=real_kind), SAVE :: V5_Rigid_vel(3)       = 0.0_real_kind  ! 質心平移速度 (v_CoM)
   REAL(KIND=real_kind), SAVE :: V5_Rigid_acc(3)       = 0.0_real_kind  ! 質心平移加速度 (a_CoM)

   REAL(KIND=real_kind), SAVE :: V5_Rigid_Ibody(3,3)   = 0.0_real_kind  ! Body Frame 下之恆定轉動慣量矩陣
   REAL(KIND=real_kind), SAVE :: V5_Rigid_invIbody(3,3)= 0.0_real_kind  ! Body Frame 下轉動慣量矩陣之逆矩陣
   REAL(KIND=real_kind), SAVE :: V5_Rigid_omega_body(3) = 0.0_real_kind ! Body Frame 下之角速度
   REAL(KIND=real_kind), SAVE :: V5_Rigid_omega_global(3)= 0.0_real_kind ! Global Frame 下之角速度
   REAL(KIND=real_kind), SAVE :: V5_Rigid_alpha_body(3)= 0.0_real_kind  ! Body Frame 下之角加速度

   ! 姿態預設為無旋轉狀態 (Unit Quaternion & Identity Matrix)
   ! 當前姿態四元數 [q0, q1, q2, q3]
   REAL(KIND=real_kind), SAVE :: V5_Rigid_quat(4)      = (/ 1.0_real_kind, 0.0_real_kind, 0.0_real_kind, 0.0_real_kind /)
   ! 當前姿態旋轉矩陣 (R)
   REAL(KIND=real_kind), SAVE :: V5_Rigid_Rmat(3,3)    = RESHAPE((/ 1.0_real_kind, 0.0_real_kind, 0.0_real_kind, &
      0.0_real_kind, 1.0_real_kind, 0.0_real_kind, &
      0.0_real_kind, 0.0_real_kind, 1.0_real_kind /), (/3,3/))
   REAL(KIND=real_kind), SAVE :: V5_Rigid_Ftotal(3)    = 0.0_real_kind  ! 質心總合外力 (F_total)
   REAL(KIND=real_kind), SAVE :: V5_Rigid_Ttotal(3)    = 0.0_real_kind  ! 質心總合外力矩 (T_total, Global Frame)

   ! 定義物理量容忍極限 (可放在模組的全域常數區)
   REAL(KIND=real_kind), PARAMETER :: V5_EPS_FORCE  = 1.0E-12_real_kind ! N
   REAL(KIND=real_kind), PARAMETER :: V5_EPS_TORQUE = 1.0E-12_real_kind ! N-m
   REAL(KIND=real_kind), PARAMETER :: V5_EPS_VEL    = 1.0E-12_real_kind ! m/s
   REAL(KIND=real_kind), PARAMETER :: V5_EPS_OMEGA  = 1.0E-12_real_kind ! rad/s

   ! 剛體初始化狀態旗標
   LOGICAL, SAVE :: is_rigid_initialized = .FALSE.

   ! 可變形體動態物理質量屬性 (Global Frame)
   REAL(KIND=real_kind), SAVE :: Current_Body_Mass
   REAL(KIND=real_kind), SAVE :: Current_Body_CoM(3)
   REAL(KIND=real_kind), SAVE :: Current_Body_I(3,3)

   ! ==========================================================
   ! 5. 衍生型別容器 (Container DDT) 與全域物件
   ! ==========================================================
   TYPE :: NodeContainer
      REAL(KIND=real_kind), POINTER :: xc(:,:)        => NULL() ! 指向 x_coord (3, nnd)
      REAL(KIND=real_kind), POINTER :: xc0(:,:)       => NULL() ! 指向 x_coord0 (3, nnd)
      REAL(KIND=real_kind), POINTER :: d(:,:)         => NULL() ! 指向 d (3, nnd)
      REAL(KIND=real_kind), POINTER :: dn(:,:)        => NULL() ! 指向 dn (3, nnd)
      REAL(KIND=real_kind), POINTER :: dnt(:,:)       => NULL() ! 指向 dnt (3, nnd)
      REAL(KIND=real_kind), POINTER :: vt(:,:)        => NULL() ! 指向 vt (3, nnd)
      REAL(KIND=real_kind), POINTER :: vt_half(:,:)   => NULL() ! 指向 vt_half (3, nnd) - 半步速度 (蛙躍法)
      REAL(KIND=real_kind), POINTER :: at(:,:)        => NULL() ! 指向 at (3, nnd)
      REAL(KIND=real_kind), POINTER :: force(:,:)     => NULL() ! 指向 force (3, nnd)
      REAL(KIND=real_kind), POINTER :: fsum(:,:)      => NULL() ! 指向 fsum (3, nnd)
      REAL(KIND=real_kind), POINTER :: mass(:)        => NULL() ! 指向 node_mass (nnd)
      REAL(KIND=real_kind), POINTER :: fix(:,:)       => NULL() ! 指向 rifix (3, nnd)
   END TYPE NodeContainer

   TYPE :: ElementContainer
      INTEGER, POINTER :: topo(:,:)          => NULL() ! 指向 elem_topo (5, nel)
      INTEGER, POINTER :: mat(:,:)           => NULL() ! 指向 elem_mat (5, nel)
      INTEGER, POINTER :: face_judge(:,:)    => NULL() ! 指向 face_judge (4, nel)
      REAL(KIND=real_kind), POINTER :: rnode(:,:)          => NULL() ! 指向 rnode (10, nel)
      REAL(KIND=real_kind), POINTER :: vol(:)              => NULL() ! 指向 elem_vol (nel)
      REAL(KIND=real_kind), POINTER :: rho(:)              => NULL() ! 指向 elem_rho (nel)
      REAL(KIND=real_kind), POINTER :: mass(:)             => NULL() ! 指向 elem_mass (nel)
      REAL(KIND=real_kind), POINTER :: vertices(:,:,:)    => NULL() ! 指向 elem_vertices (3, 4, nel)
      REAL(KIND=real_kind), POINTER :: facecenter(:,:,:)  => NULL() ! 指向 elem_facecenter (3, 4, nel)
      REAL(KIND=real_kind), POINTER :: center(:,:)        => NULL() ! 指向 elem_center (3, nel)
      REAL(KIND=real_kind), POINTER :: area(:,:)          => NULL() ! 指向 elem_area (4, nel)
      REAL(KIND=real_kind), POINTER :: normal(:,:,:)      => NULL() ! 指向 elem_normal (3, 4, nel)
      REAL(KIND=real_kind), POINTER :: pressure(:,:)      => NULL() ! 新增：指向 elem_pressure (4, nel)
      REAL(KIND=real_kind), POINTER :: velocity(:,:,:)    => NULL() ! 新增：指向 elem_velocity (3, 4, nel)
      REAL(KIND=real_kind), POINTER :: density(:,:)       => NULL() ! 新增：指向 elem_density (4, nel)
      REAL(KIND=real_kind), POINTER :: sigma3D(:,:)       => NULL() ! 指向 sigma3D (6, nel)
      REAL(KIND=real_kind), POINTER :: sigmaP(:,:)        => NULL() ! 指向 sigmaP (6, nel)
      REAL(KIND=real_kind), POINTER :: epslonP(:,:)       => NULL() ! 指向 epslonP (6, nel)
      REAL(KIND=real_kind), POINTER :: pstress(:,:)       => NULL() ! 指向 pstress (3, nel)
      REAL(KIND=real_kind), POINTER :: elplas(:)          => NULL() ! 指向 elplas (nel)
      REAL(KIND=real_kind), POINTER :: PLalphaP(:)        => NULL() ! 指向 PLalphaP (nel)
      REAL(KIND=real_kind), POINTER :: PLrP(:)            => NULL() ! 指向 PLrP (nel)
   END TYPE ElementContainer

   TYPE(NodeContainer), SAVE    :: Nodes
   TYPE(ElementContainer), SAVE :: Elements

CONTAINS

   ! ==========================================================
   ! [Link Containers] 將全域扁平陣列綁定至節點與單元指針容器
   ! ==========================================================
   SUBROUTINE Link_VFIFE_Containers()
      IMPLICIT NONE

      ! --- 1. 綁定節點容器 (Nodes) ---
      IF (ALLOCATED(x_coord))  Nodes%xc    => x_coord
      IF (ALLOCATED(x_coord0)) Nodes%xc0   => x_coord0
      IF (ALLOCATED(d))        Nodes%d     => d
      IF (ALLOCATED(dn))       Nodes%dn    => dn
      IF (ALLOCATED(dnt))      Nodes%dnt   => dnt
      IF (ALLOCATED(vt))       Nodes%vt    => vt
      IF (ALLOCATED(vt_half))  Nodes%vt_half => vt_half
      IF (ALLOCATED(at))       Nodes%at    => at
      IF (ALLOCATED(force))    Nodes%force => force
      IF (ALLOCATED(fsum))     Nodes%fsum  => fsum
      IF (ALLOCATED(node_mass))Nodes%mass  => node_mass
      IF (ALLOCATED(rifix))    Nodes%fix   => rifix


      ! --- 2. 綁定單元容器 (Elements) ---
      IF (ALLOCATED(elem_topo))       Elements%topo       => elem_topo
      IF (ALLOCATED(elem_mat))        Elements%mat        => elem_mat
      IF (ALLOCATED(elem_vol))        Elements%vol        => elem_vol
      IF (ALLOCATED(elem_mass))       Elements%mass       => elem_mass
      IF (ALLOCATED(elem_center))     Elements%center     => elem_center
      IF (ALLOCATED(elem_vertices))   Elements%vertices   => elem_vertices
      IF (ALLOCATED(elem_facecenter)) Elements%facecenter => elem_facecenter
      IF (ALLOCATED(elem_area))       Elements%area       => elem_area
      IF (ALLOCATED(elem_normal))     Elements%normal     => elem_normal
      IF (ALLOCATED(elem_pressure))   Elements%pressure   => elem_pressure
      IF (ALLOCATED(elem_velocity))   Elements%velocity   => elem_velocity
      IF (ALLOCATED(elem_density))    Elements%density    => elem_density
      IF (ALLOCATED(face_judge))      Elements%face_judge => face_judge
      IF (ALLOCATED(sigma3D))         Elements%sigma3D    => sigma3D
      IF (ALLOCATED(sigmaP))          Elements%sigmaP     => sigmaP
      IF (ALLOCATED(epslonP))         Elements%epslonP    => epslonP
      IF (ALLOCATED(pstress))         Elements%pstress    => pstress
      IF (ALLOCATED(elplas))          Elements%elplas     => elplas
      IF (ALLOCATED(PLalphaP))        Elements%PLalphaP   => PLalphaP
      IF (ALLOCATED(PLrP))            Elements%PLrP       => PLrP

   END SUBROUTINE Link_VFIFE_Containers
END MODULE VFIFE_Data_module


```
---
# 🔗 參考資料


---