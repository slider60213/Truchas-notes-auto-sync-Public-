---
type: 📝 Research
created: 2026-08-25 23:15
modified: 2026-08-26 00:00
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

UbikSolve 是 Truchas 的線性方程組求解器（Linear Solver），它是整個程式中對 Fortran 90 語法要求最嚴格的部分。

[聊天紀錄_編譯功能 # TURN 118](../C.%20Truchsa-WSL/02_Truchas-2.0.2/00_聊天紀錄/Gemini/移植-Truchas-編譯器版本確認/聊天紀錄_編譯功能.md#TURN%20118)
編譯成64位元
是使用 platform 這個變數來決定編譯目錄

[聊天紀錄_編譯功能 # TURN 123](../C.%20Truchsa-WSL/02_Truchas-2.0.2/00_聊天紀錄/Gemini/移植-Truchas-編譯器版本確認/聊天紀錄_編譯功能.md#TURN%20123)
**UbikSolve/Makeutils。** 既然 `makeutilsdir = ../Makeutils`，這代表真正的編譯規則（包括那個死掉的 `f90` 指令）都定義在 `packages/ubiksolve/Makeutils` 資料夾內。只要我們把這裡面的規則「現代化」，以後你修改 `src` 重新編譯時，它就會自動使用 `gfortran`。

- 徹底修改 `Makeutils` 內的規則
- 修正 `UbikSolve/config.mak`


[聊天紀錄_編譯功能 # TURN 127](../C.%20Truchsa-WSL/02_Truchas-2.0.2/00_聊天紀錄/Gemini/移植-Truchas-編譯器版本確認/聊天紀錄_編譯功能.md#TURN%20127)
重新挑戰


---
# 🔗 參考資料


---