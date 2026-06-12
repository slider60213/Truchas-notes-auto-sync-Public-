---
type: 📝 Research
created: 2026-05-14 01:44
modified: 2026-05-22 03:03
tags:
  - "#Truchas"
  - Truchas/VFIFE
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
被使用於
- [fluid_flow_module_F90](fluid_flow_module_F90.md)
- [SOLID_module_F90](SOLID_module_F90.md)

---
# 👨‍💻 以後


---
## 📝 內容紀錄

116 中使用的是 moving_solid_module.F90，由於只會在 moving_solid>0 時生效，因此暫時未移除。

`moving_rigid_module.F90` 是 VFIFE 中實作浸沒邊界法（IBM）的關鍵橋樑，主要負責將流體的壓力場轉換為固體表面的受力，並管理流固耦合所需的幾何資訊。

以下為該模組的架構拆解、關鍵變數註解與核心邏輯說明：

一、 模組角色與變數意義

此模組定義了流體（Truchas）與剛體（DEM/VFIFE）進行數據交換的公共緩衝區。

|變數名稱|物理意義 (專家建議定義)|功能說明|
|---|---|---|
|**NB_DEM**|**TotalRigidBodies**|定義模擬中剛體塊體的總數量。|
|**solid_vof 2**|**RigidBodyVOF**|儲存每個網格被固體佔據的體積分率（0.0~1.0）。|
|**cell_vels**|**SolidCellVelocity**|記錄固體在該網格位置的運動速度，用於後續速度混合。|
|**IGPOINT**|**IntegrationPoints**|固體表面單元上的壓力積分點座標（X, Y, Z）。|
|**IGPRESSURE**|**SurfacePressure**|由流體網格插值得到，施加在固體積分點上的壓力值。|
|**fnigp**|**PointsPerFace**|每個固體單元面（Face）所擁有的積分點數量。|
|**solidii**|**IBMIterationCount**|目前處於第幾次 IBM 流固耦合迭代迴圈中。|

--------------------------------------------------------------------------------

二、 核心子程序解析

1. `subroutine interpolation` (界面壓力插值)

這是本模組最重要的程序，決定了「水如何推動固體」。

- **搜尋階段 (Search)**：程式會遍歷每個固體積分點，判斷其落在編號為 `n` 的流體網格內。
- **數值過濾階段 (Filtering)**：
    - 檢查該網格的 `fluidVof(n)` 是否大於等於 **0.3**。
    - **邏輯判定**：若網格太乾（< 0.3），程式會搜尋其 6 個相鄰網格（`Ngbr_cell`），尋找流體佔比較高的鄰居來提供壓力值。
- **平均計算 (Averaging)**：將找到的有效壓力 `Zone%P` 進行算術平均，得到插值後的壓力 `WP` 並寫入 `IGPRESSURE`。
 

```fortran
!=======================================================================
! 塊體受壓點壓力插值計算迴圈
!=======================================================================
do NB = 1, NB_DEM
    np(:,:,:) = IGPOINT(NB,:,:,:)

    P_num = zero
    
    ! 遍歷網格搜尋受壓點所在的網格編號
    do n = 1, ncells 
        ! 透過計算網格邊界極值來判斷點的位置
        call Find_Face_Centroid (n, x_min, x_max, y_min, y_max, z_min, z_max)

        do pface = 1, 4
            do ipoint = 1, fnigp
                ! 判斷座標是否落在網格內
                if (np(pface,ipoint,1) .gt. X_min .and. np(pface,ipoint,1) .le. X_max .and. &
                    np(pface,ipoint,2) .gt. Y_min .and. np(pface,ipoint,2) .le. Y_max .and. &
                    np(pface,ipoint,3) .gt. Z_min .and. np(pface,ipoint,3) .le. Z_max) then
                    P_num(pface,ipoint) = n
                    cell_found = .true.
                end if 
            end do 
        end do
    end do 


    ! 壓力賦值邏輯：判斷網格流體狀態並取平均壓力
    WP = zero
    WP0 = zero
    do pface = 1, 4
        do ipoint = 1, fnigp  
            n = P_num(pface,ipoint)
            counter = zero
            P_sum = zero
            
            ! 若該網格流體佔比足夠，直接取值；否則搜尋鄰近網格
            if (fluidVof(n) .GE. 0.3) then 
                counter = counter + 1
                P_sum = P_sum + Zone(n)%P
            else
                do f = 1, nfc
                    ngbr = Mesh(n)%Ngbr_cell(f)
                    if (fluidVof(ngbr) .GE. 0.3) then
                        counter = counter + 1
                        P_sum = P_sum + zone(ngbr)%p
                    end if
                end do 
            endif
            
            ! 計算最終分配給 DEM 塊體受壓點的壓力
            WP(pface,ipoint) = P_sum / counter
            IGPRESSURE(NB,pface,ipoint) = wp(pface,ipoint)
        end do 
    end do 
end do
```



2. `subroutine Find_Face_Centroid` (邊界範圍判定)

- **功能**：計算特定流體網格在空間中的幾何極值（`x_min`, `x_max` 等）。
- **目的**：提供給 `interpolation` 作為點對胞（Point-in-Cell）搜尋的幾何邊界判斷基準


---
## 🔗 參考資料
-