---
type: 📝 Research
created: 2026-07-30 03:45
modified: 2026-08-08 02:14
tags:
  - "#Truchas"
  - Truchas/VFIFE
  - 電腦/WINDOWS/WSL
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

1. 啟用開關：在 `&PHYSICS` 中新增了開關 `V5Slider`，有寫好預設值 `.flase.` 。
2. 材料編號：現在會自動創建材料編號 V5_mat_id，數值是 inp 檔中的材料數量再+1，因此 inp 檔材料設定必須連號不可跳號。
3. 固體參數：現在會讀取與 .inp 檔同名的 .V5 檔。 （ABC.inp  $\Rightarrow$ ABC.V5）

---
# 📝 內容紀錄

```fortran

&PHYSICS
    V5Slider               = .true.
 
/


&MATERIAL

    Material_Name           = 'water'
    Material_Number         = 1
    priority                = 1

/

&MATERIAL

    Material_Name           = 'solid'
    Material_Number         = 2
    priority                = 2


/

&MATERIAL

    Material_Name           = 'air'
    Material_Number         = 3
    Material_Feature        = 'background'
    priority                = 3


/



```

---
# 🔗 參考資料


---