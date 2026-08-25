---
type: 📝 Research
created: 2026-08-25 23:15
modified: 2026-08-26 00:20
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


[聊天紀錄_編譯功能 # TURN 109](../C.%20Truchsa-WSL/02_Truchas-2.0.2/00_聊天紀錄/Gemini/移植-Truchas-編譯器版本確認/聊天紀錄_編譯功能.md#TURN%20109)
編譯成64位元

[聊天紀錄_編譯功能 # TURN 113](../C.%20Truchsa-WSL/02_Truchas-2.0.2/00_聊天紀錄/Gemini/移植-Truchas-編譯器版本確認/聊天紀錄_編譯功能.md#TURN%20113)
PGSLib 改用 `gfortran` 編譯，而不是那個會崩潰的 `lf95`


[聊天紀錄_編譯功能 # TURN 116](../C.%20Truchsa-WSL/02_Truchas-2.0.2/00_聊天紀錄/Gemini/移植-Truchas-編譯器版本確認/聊天紀錄_編譯功能.md#TURN%20116)
有**兩個編譯選項檔在強迫系統使用 lf95。** 既然 PGSLib 內部寫死了編譯器，我們直接用 `sed` 把這兩份檔案裡的 `lf95` 通通換成 `gfortran`。同時，我們也要把之前在總設定檔看到的 `--chk` 參數拔掉，因為 `gfortran` 看到這個參數會直接報錯。

[聊天紀錄_編譯功能 # TURN 159](../C.%20Truchsa-WSL/02_Truchas-2.0.2/00_聊天紀錄/Gemini/移植-Truchas-編譯器版本確認/聊天紀錄_編譯功能.md#TURN%20159)  
修正 `src/options/libraries`
根據 `GNUmakefile.sub` 的第 217 行和第 114 行，主程式 `$(CODE)` 的最終連結指令是： `$(FL) $(FFLAGS) $< $(USER_LIBS) -o $(bindir)/$(executable)` 這代表 **PGSLIB 的庫檔案路徑是被封裝在 $(USER_LIBS) 變數裡的**。而這個變數又是透過第 84 行 `include $(optdir)/libraries` 從 `src/options/libraries` 這個檔案定義出來的。


[聊天紀錄_編譯功能 # TURN 163](../C.%20Truchsa-WSL/02_Truchas-2.0.2/00_聊天紀錄/Gemini/移植-Truchas-編譯器版本確認/聊天紀錄_編譯功能.md#TURN%20163)  

---
# 🔗 參考資料


---