---
type: 📝 Research
created: 2026-05-14 01:41
modified: 2026-06-04 03:10
tags:
  - "#Truchas"
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
- 被使用於 [fluid_flow_module_F90](fluid_flow_module_F90.md)

`SOLID_module.f90` 是 VFIFE 固體計算模組的核心入口，其架構嚴格遵循「檔案與流程管理（`solid3D`）→ 記憶體分配（`dynamic`）→ 數據讀取與初始化（`readata1` / `chkdata` / `bmass`）→ 動力演進求解（`esolv`）」的序列邏輯。,,,

身為流體數值模式專家，我根據原始碼為您詳細梳理這個模組的層級化架構：

1. 模組入口與檔案管理：`subroutine solid3D`

這是模組的最外層接口，主要負責環境準備：

- **檔案操作**：開啟所有必要的輸入（`.dat`）與輸出（`.plt`, `.txt`）檔案單元（Unit 5, 6, 7, 45...）。,
- **流程觸發**：設定最大記憶體容量（`maxq`）並呼叫 `dynamic` 進入核心控制層。,

2. 核心控制與記憶體管理器：`subroutine dynamic`

此子程序扮演「調度員」的角色，負責系統級的設置：

- **動態記憶體模擬**：VFIFE 使用一個巨大的 `real*8` 陣列 `ar`，透過手動計算索引偏移量（如 `npint`, `nfeli`）來模擬動態分配，這在早期 Fortran 程式碼中很常見。,,
- **讀取標頭與控制參數**：讀取並輸出 `CARD 1` 至 `CARD 4` 的全域物理與時間控制參數（如 `maxstp`, `delta`）。,
- **協調初始化順序**：依序呼叫 `readata1`（讀檔）、`chkdata`（校核）、`bmass`（算質量）以及最後的求解器 `esolv`。,,

3. 數據解析器：`subroutine readata1`

負責解析複雜的外部輸入文件：

- **幾何與屬性讀取**：具體處理 `CARD 6`（節點）、`CARD 7`（單元）、`CARD 8-9`（材料屬性）。,,,
- **力函數載入**：讀取重力歷時（`CARD 10-11`）以及各種外力歷史（`CARD 15-24`）。,,

4. 前處理工具集：`chkdata` 與 `bmass`

在開始計算前確保物理合理性：

- **chkdata**：檢查材料參數是否完整（例如金屬是否給了抗拉強度、土壤是否給了內摩擦角）。,,
- **bmass**：根據單元體積與密度計算 **節點集中質量（Lumped Mass）**，這是後續 F=ma 運算的基礎。,,

5. 動力演進求解器：`subroutine esolv`

這是 VFIFE 最吃重的演算法核心，包含時間積分循環：

- **時間步進**：執行顯式 **中心差分法（Central Difference Method）**。,
- **單元計算**：在每一時步遍歷所有單元，呼叫 `fintiso3` 進行協同旋轉架構下的內力計算。,,
- **流固耦合對接**：處理流體壓力插值（`IGPRESSURE`）並將其轉化為節點外力 `pforce`。,,
- **應力彙整**：呼叫 `stress` 將各單元的應力分量加權平均至節點，供視覺化輸出。,

```
subroutine esolv(...)
  ! 1. 初始化：將 xc 設定為初始座標
  ! ...
  do 2222 nstep = 1, maxstp
    ! (A) 更新當前瞬時座標 (使用上一時步算好的 d)
    xc(i) = xct(i) + d(j)  ! [1], [2]

    ! (B) 計算內力 (基於剛更新的 xc)
    call fintiso3(..., xc, ...)  ! [3], [4]

    ! (C) 流固耦合：取得壓力並積分為節點力
    ! 使用 xc 取得壓力點 IGPOINT 並計算 pforce
    ! [3], [5]

    ! (D) 更新 VOF2 (僅在流體週期結尾執行)
    if (nstep == maxstp) call update_vof2(...) ! [6], [7]

    ! (E) 計算外力 (重力、地震力等)
    call fextl(..., xct, ...)  ! [8], [9]

    ! (F) 運動積分 (牛頓第二定律 F=ma)
    ! 計算新的位移增量 dp
    dp(j) = c1*(fsum/xmass) + c2*d(j) - c3*dn(j) ! [10], [11]

    ! (G) 關鍵更新步 (將「舊的運動」固化到基準座標)
    ! 注意：這裡加的是進入迴圈時那個舊的 d，而非剛算好的 dp
    xct(i) = xct(i) + d(j)  ! [12], [13]

    ! (H) 準備下一圈的位移變數
    d(i) = dt1(i) - db(i)  ! 更新相對位移 d 供下一圈 (A) 步驟使用 [14], [15]
  end do
end subroutine
```








原版 `bmass` 的本質就是：**「遍歷每個四面體單元 $\rightarrow$ 用向量公式算出體積 $\rightarrow$ 乘上密度得到總質量 $\rightarrow$ 平均平分給 12 個自由度並寫入 `xmeli`」**

---

# 👨‍💻 以後

[VFIFE_Driver_module_F90](../../02_新版/程式碼/VFIFE_Driver_module_F90.md)

[VFIFE_Utils_module_F90](../../02_新版/程式碼/VFIFE_Utils_module_F90.md)
[VFIFE_Data_module_F90](../../02_新版/程式碼/VFIFE_Data_module_F90.md)

---
## 📝 內容紀錄

 過時用法 gfortran 無法編譯
 ielapsed_time = TIMEF()     ielapsed_time = TIMEF()    

```fortran
subroutine solid3D
	! 引用全域資料模組，ar 是存儲池，maxq 是最大容量限制
	use Datasave_module,		only: ar,maxq
	! 引用輸出模組，用於產生與主程式一致的檔名
	use output_module,			only:MAKE_FILE_NAME,input_file
	use parameter_module, 		only: 	string_len

	! 使用隱含宣告，a-h, o-z 開頭的變數均為雙精度浮點數 (real*8)
	implicit real*8(a-h,o-z)

	character(LEN = string_len)		::	input_data_name

	! 設定 ar 陣列的最大索引值為 200 萬
	maxq = 2000000

	! 處理檔名：將輸入檔名（如 filename.inp）去掉後四個字元並加上 .dat
	input_data_name=input_file(1:LEN_TRIM(input_file)-4)// '.dat'

	! --- 開啟所有必要的檔案單元 (Units) ---
	
	! Unit 5: 讀取固體模組的參數設定檔 (.dat)
	open (unit=5, FILE=TRIM(input_data_name))    
	
	! Unit 6: 輸出 IN.txt，通常用於檢查讀入的資料是否正確 (Echo Check)
	open (unit=6, FILE=TRIM(MAKE_FILE_NAME('IN.txt')))          
	
	! Unit 7: 輸出 out.txt，記錄一般運算訊息
	open (unit=7, position='append', FILE=TRIM(MAKE_FILE_NAME('out.txt')))
	
	! Unit 45: 輸出 3Dplot.plt，供 Tecplot 等繪圖軟體使用的幾何檔
	open (unit=45, position='append', FILE=TRIM(MAKE_FILE_NAME('3Dplot.plt')))
	
	! Unit 88: 輸出 check.txt，除錯用
	open (unit=88, position='append', FILE=TRIM(MAKE_FILE_NAME('check.txt')))
	
	! Unit 99: 輸出 dis.txt，記錄位移量 (Displacement)
	open (unit=99, position='append', FILE=TRIM(MAKE_FILE_NAME('dis.txt')))
	
	! Unit 98: 輸出 pressure.txt，記錄流體傳回的壓力資料
	open (unit=98, position='append', FILE=TRIM(MAKE_FILE_NAME('pressure.txt')))
	  
	! Unit 50: 輸出 Force.txt，記錄結構受力狀況
	open (unit=50, position='append', FILE=TRIM(MAKE_FILE_NAME('Force.txt')))

	! 進入核心記憶體分配程序
	call dynamic()

	! 運算結束後關閉所有檔案
	close (unit=5)
	close (unit=6)
	close (unit=7)
	close (unit=45)
	close (unit=88)
	close (unit=99)
	close (unit=98)
	close (unit=50)

	end subroutine solid3D
```




```fortran
subroutine dynamic()
	! 引用多個模組變數，包含記憶體池 ar、最大容量 maxq、耦合壓力 sigma3D 等
	use Datasave_module,	only: ar,maxq,sigma3D
	use time_step_module,   only: cycle_number ! 讀取當前模擬的步數
	use Datasave_module,	only: iprob,iprobA,isee,iplane,delta,alpha,toler,gravity,thick
	use Datasave_module,	only: nnd,nel,nummat,numout,ifbody,iacc,ndof,iforce2,iforce3,iforce4

    implicit real*8(a-h,o-z)
    dimension head(20)              ! 標題緩衝區
	integer::face_judge(500000)     ! 邊界判定陣列
	integer::count = 0

    count = count + 1

! 如果是模擬的第一個步數 (cycle_number=1)，初始化 ar 陣列為 0
if (cycle_number .eq. 1) then
	do 100 i=1,maxq
100		ar(i) = 0.d0

! --- 讀取 .dat 檔案內的控制卡 (Control Cards) ---
! 讀取標題 (TITLE) 並回顯至 Unit 6 (IN.txt)
      read(5,1300)head
      write(6,1400)head
      write(6,1500)

! 讀取核心規模參數：
! nnd: 節點數 / nel: 單元數 / nummat: 材料種類 / minstp,maxstp: 最小最大迭代步數
! delta, alpha: 數值積分參數 / toler: 收斂容許值
      read(5,*)nnd,nel,nummat,minstp,maxstp,delta,alpha,toler
       if (maxstp .lt. minstp) maxstp = minstp
      write(6,1600)nnd,nel,nummat,minstp,maxstp,delta,alpha,toler

! 讀取載重與數值選項：
! ifbody: 體積力(重力)開關 / iacc: 初始加速度選項 / isequel: 續跑選項
      read(5,*)ifbody,iacc,iforce2,iforce3,iforce4,isequel
      write(6,1700)ifbody,iacc,iforce2,iforce3,iforce4,isequel

! 讀取輸出與幾何選項：
! iprob: 問題類型 / numout: 監測點數量 / iplane: 平面問題選項 / thick: 結構厚度
      read(5,*)iprob,iprobA,numout,isee,iplane,thick
      write(6,1800)iprob,iprobA,numout,isee,iplane,thick

endif
```

- ** `meq1` vs `meq2` **：你可以看到 `meq1` 通常用於「力 (force)」、「位移 (nd)」等與節點自由度直接相關的長度；而 `meq2` 則用於「應力 (stress)」、「座標 (xc)」等與單元或積分點性質相關的空間。
    
- ** `nxct, nyct, nzct` **：這是你做流固耦合（FSI）時最關鍵的變數。它們代表了結構在變形後的「實體位置」，流體模組會依此判斷橋墩在哪裡、沖刷到哪裡。
    
- **塑性與高斯點**：後段的 `nsigmaP`, `nepslonP` 顯示這個模組考慮了**彈塑性（Elasto-plasticity）**。如果你的研究涉及土體或是結構損壞，這部分會非常重要。
```fortran
! --- 空間規模計算 ---
      ndof   = 3              ! 自由度 (3D)
      meq    = nnd*ndof       ! 總節點自由度
      meq1   = nel*9*ndof     ! 針對單元的自由度分配 (可能包含積分點或高階項)
      meq2   = nel*9          ! 針對單元的純量數據分配
      maxout = numout
      if (numout.eq.0) maxout = 1

! --- 物理量在 ar() 內的起點索引 ---
      npint   = 1             ! Internal Force (內力向量)
      nfeli   = npint  + meq1 ! Element Internal Force (單元層級內力)
      nxmass  = nfeli  + meq1 ! Nodal Mass (節點質量)
      nxmeli  = nxmass + meq1 ! Element Mass (單元質量)
      nd      = nxmeli + meq1 ! Displacement (位移向量)
      nat     = nd     + meq1 ! Acceleration (加速度 at)
      nvt     = nat    + meq1 ! Velocity (速度 vt)
      ndt     = nvt    + meq1 ! Displacement Increment (位移增量)
      ndpt    = ndt    + meq1 ! Displacement at t-step
      ndnt    = ndpt   + meq1 ! Displacement at n-step
      ndb     = ndnt   + meq1 ! Boundary conditions (邊界條件)
      
      nxc     = ndb    + meq1 ! Initial X Coordinate (初始 X 座標)
      nyc     = nxc    + meq2 ! Initial Y Coordinate
      nzc     = nyc    + meq2 ! Initial Z Coordinate
      
      nxct    = nzc    + meq2 ! Current X Coordinate (當前 X 實體座標)
      nyct    = nxct   + meq2 ! Current Y Coordinate
      nzct    = nyct   + meq2 ! Current Z Coordinate

! --- 主應力與積分點數據 (Gauss Points / Principal Stresses) ---
      nsxPT   = nzct   + meq2 ! Principal Stress X (主應力 X)
      nsyPT   = nsxPT  + meq2 ! Principal Stress Y
      nszPT   = nsyPT  + meq2 ! Principal Stress Z
      nstPT   = nszPT  + meq2 ! Total Principal Stress
      nssMAX  = nstPT  + meq2 ! Maximum Shear Stress (最大剪應力)
      nssMIN  = nssMAX + meq2 ! Minimum Shear Stress
      nssANG  = nssMIN + meq2 ! Stress Angle (應力角)
      nPTno   = nssANG + meq2 ! Point Number (點編號)
      
      nfsum   = nPTno  + meq2 ! Net Force sum (合力 Fsum = Force - Pint)
      nforce  = nfsum  + meq1 ! External Force (外力)
      nifix   = nforce + meq1 ! Fixed degrees index (約束/固定點索引)

! --- 拓樸、材料與塑性相關 ---
      nnode   = nifix   + meq1 ! Node connectivity (單元節點連結關係，10*nel)
      nem     = nnode   + 10*nel ! Element Materials (材料參數，25*nummat)
      nkout  = nem      + 25*nummat ! Monitoring node indices (輸出節點索引)
      ndp    = nkout    +  4*maxout ! Displacement history P (位移歷史)
      ndn    = ndp      + meq1

! --- 高階/高斯點應力應變資料 ---
      nelpl    = ndn       + meq1
      nxGauss  = nelpl     + meq2 ! Gauss point X
      nyGauss  = nxGauss   + meq2 ! Gauss point Y
      nsxGauss = nyGauss   + meq2 ! Stress X at Gauss points
      nsyGauss = nsxGauss  + meq2
      nszGauss = nsyGauss  + meq2
      nstGauss = nszGauss  + meq2
      nsigmaP  = nstGauss  + meq2 ! Plastic stress (塑性應力)
      nepslonP = nsigmaP   + 4*meq2 ! Plastic strain (塑性應變)
      nPLalphaP= nepslonP  + 4*meq2
      nPLrP    = nPLalphaP + 4*meq2 ! Plastic hardening parameter
      
      maxindex = nPLrP     + meq2 ! 最終算出的總需求大小
```

```fortran
! --- 檢查所需總空間是否超過 ar() 的宣告上限 (maxq) ---
      if (maxindex.gt.maxq) then
        print *,' There is not enough dimension available.'
        print *,' ==> Please increase no. in ar(...) & maxq = ....'
        write(*,*)' NOT enough dimension available...needed = ',maxindex
        stop  ! 空間不足，強制停止程式
      endif
```


```fortran
if (cycle_number .eq. 1) then
! --- 呼叫主要子程序 ---

      ! 讀取詳細數據：座標、約束條件、材料性質等
      call readata1(nnd,nel,nummat,numout,ifbody,iacc,ndof,ar(nnode),&
                  iforce2,iforce3,iforce4,ar(nxc),ar(nyc),ar(nzc),ar(nifix),&
                  ar(nem),ar(nkout))
	print *, 'call readata1 -- complete!'

      ! 數據校準與一致性檢查
      call chkdata(nel,nummat,ar(nem),ar(nnode))
      print *, 'call chkdata -- complete!'

      ! 計算單元質量與節點質量分配
      call bmass(nel,ar(nnode),ar(nxc),ar(nyc),ar(nzc),ar(nxmeli))
      print *, 'call bmass -- complete!'
	  
	  ! 慣性項判定 (如果 count 滿足條件，執行邊界或慣性計算)
	  if(count == 1) then
		  call inertia(nnd,nel,nummat,ar(nnode),ar(nxc),ar(nyc),ar(nzc),face_judge)     
		  print *, 'call inertia -- complete!'
      endif
endif

```

- ** `readata1` 的角色**：它負責解析 `.dat` 檔中的 **CARD 6 (節點)** 到 **CARD 11 (輸出需求)**。它會把讀入的數字塞進 `ar(nxc)` (初始座標)、`ar(nnode)` (單元組成) 等位置。
    
- ** `bmass` 的角色**：VFIFE 是顯式動力學，需要節點質量來解 $a = F/m$。`bmass` 根據單元體積與密度計算出 `ar(nxmeli)`。
    
- ** `esolv` 的巨量參數**：
    
    - **輸入端**：`ar(nforce)` (外力)、`ar(nxmass)` (質量)。
        
    - **狀態端**：`ar(nxct)` (當前位置)、`ar(nvt)` (速度)。
        
    - **計算端**：`ar(npint)` (計算出來的結構內力)。
        
- **格式化敘述 (`1600`, `1700`, `1800`)**：這些是當初程式讀取控制卡後，寫入到 `IN.txt` (Unit 6) 的格式，讓你檢查讀進去的參數對不對。
- 
```fortran
! 記錄計算耗時 (Start)
      ielapsed_time = TIMEF()     

      ! 物理量演進核心：計算力平衡、更新座標與應力
      ! 此處將 ar() 的各個起點位址傳入，在 esolv 內部會被視為獨立陣列
      call esolv(nel,nnd,ndof,ifbody,iacc,numout,iforce2,iforce3,&
                iforce4,ar(nxmass),ar(nxmeli),ar(nfsum),ar(nforce),&
                ar(npint),ar(nfeli),ar(nifix),ar(nd),ar(ndt),ar(nvt),&
                ar(nat),ar(nxc),ar(nyc),ar(nzc),ar(nxct),ar(nyct),ar(nzct),ar(nnode),&
                ar(nem),ar(nkout),minstp,maxstp,ar(ndb),ar(ndnt),&
                ar(ndpt),ar(ndn),ar(ndp),isequel,ar(nelpl),&
                ar(nxGauss),ar(nyGauss),ar(nsxGauss),ar(nsyGauss),&
                ar(nszGauss),ar(nstGauss),ar(nsigmaP),ar(nepslonP),&
                ar(nPLalphaP),ar(nPLrP),ar(nsxPT),ar(nsyPT),ar(nszPT),&
                ar(nstPT),ar(nssMAX),ar(nssMIN),ar(nssANG),ar(nPTno),face_judge)

      ! 記錄計算耗時 (End)
      ielapsed_time = TIMEF()                   

      print *,'call esolv ---- complete! '

      return
      end
```

---
## 🔗 參考資料
-