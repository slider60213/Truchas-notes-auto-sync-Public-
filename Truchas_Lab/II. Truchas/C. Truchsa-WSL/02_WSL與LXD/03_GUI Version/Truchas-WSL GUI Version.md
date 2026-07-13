---
type: 📝 Research
created: 2026-06-19 04:28
modified: 2026-07-13 16:26
tags:
  - "#Truchas"
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

## Quick Start 
1. **Download & Extract:** Download and extract the `Truchas-WSL` and `GUI` packages into your desired directory. 
2. **Create Shortcut:** Navigate to the GUI directory and run `MakeShortcut.bat` to generate a shortcut named `Truchas_WSL_GUI`. 
   ![|475](pics/Pasted%20image%2020260626201010.png)
3. **Launch the Application:** Run `Truchas_WSL_GUI`. *(Note: If this is your first time running the application, ensure WSL2 is installed on your system.)* 
4. **Environment Setup:** Import `Truchas-WSL` via the GUI, then restart the application. 
   ![475](pics/Pasted%20image%2020260713161006.png)
   ![|475](pics/Pasted%20image%2020260626184206.png)
5. **Debug Mode (Optional):** If you need to view error logs for troubleshooting, launch the application using `Truchas_WSL_DEBUG.bat` instead. 
6. **Select WSL Environment:** Choose your target WSL environment. *(By default, the GUI selects your last-used environment. You can import additional WSL environments by clicking the ➕ button.)* 
   ![|475](pics/Pasted%20image%2020260713155744.png)
7. **Configure AI Integration:** Connect to your preferred AI platform by entering your API key. 
8. **Run Simulation:** Select your target LXD container and choose an existing `.inp` file to execute the simulation. 
9. **UI Controls:** 
   - Click the 🌐 button to toggle the interface language.
   - Click the ⟳ button to reload the GUI.

## How to Use

1. Download and extract the `Truchas-WSL` and `GUI` packages.
2. Navigate to the `GUI` directory. Run ` MakeShortcut.bat` to create a shortcut named `Truchas_WSL_GUI`.  
    ![|475](pics/Pasted%20image%2020260626201010.png)
3. Launch `Truchas_WSL_GUI`. (Note: ` WSL2 ` installation may be required during the initial setup.)
4. Import `Truchas-WSL` via the `GUI`, then restart the application.
   ![475](pics/Pasted%20image%2020260713161006.png)
   ![|475](pics/Pasted%20image%2020260626184206.png)
5. If error logs are required, please switch to using `Truchas_WSL_DEBUG.bat` instead.
6. Select your target `WSL` environment. (Default option: The one you used last time; Others: other WSL env.)
7. Import more WSL env. by clicking the ➕ button.
8. Toggle the interface language by clicking the 🌐 button.
   ![|475](pics/Pasted%20image%2020260713155744.png)
9. Choose an `LXD` container and select an Exisiting `.inp` file to execute the simulation.
10. Connect to the AI platform through API KEY.
11. Reload the GUI by clicking the ⟳ button.
12. Toggle the interface language by clicking the 🌐 button.
    ![|475](pics/Pasted%20image%2020260713160315.png)


## Customize
### Customizing Assets

- **Shortcut Icon:** To change the shortcut icon, simply replace `icon.ico` with your preferred icon file.
    
- **Splash Screen / Loading Image:** To customize the loading screen displayed when entering the WSL environment, replace `LoadingPic.png` with your custom image.
    ![|475](pics/Pasted%20image%2020260713160143.png)

### Adding Custom Languages

- To add or customize a language, mirror the existing directory structure under the locales directory: `Truchas_WSL_GUI\Truchas_App_Project\locales\`
	
- Localization files must strictly adhere to the following naming convention and hierarchy: `[Language] / [Python Module Name] / [Class Name].json`
























## 1. 創建捷徑

- 執行 `MakeShortcut.bat` 來生成捷徑 `Truchas_WSL_GUI`，未來只需要執行這個捷徑即可。
- 以下內容可自由替換：
	icon.ico 捷徑的圖示
	LoadingPic.png 操作面板的讀取畫面
![|475](pics/Pasted%20image%2020260626201010.png)


## 2. 匯入 WSL
- 點開捷徑後，若尚未安裝 WSL，會出現匯入視窗。
- 選擇下載好的 Truchas-WSL 壓縮檔後變會自動匯入。
![|475](pics/Pasted%20image%2020260626183825.png)
![|475](pics/Pasted%20image%2020260626184206.png)

##3. 啟用 WSL+執行模擬
- 點開捷徑後，若已安裝過 Truchas-WSL，會偵測出可啟用的環境。
![|474](pics/Pasted%20image%2020260625153031.png)

- 選擇環境後，會出現操作面板跟 Loading 畫面 (LoadingPic.png)。
- 可點選右下角的按鈕來切換顯示語言。
![|475](pics/Pasted%20image%2020260626202005.png)
![|475](pics/Pasted%20image%2020260626203206.png)
- 讀取完成會自動跳轉到 `problems/tests` 資料夾，若跳轉失敗則需手動執行跳轉。
- 手動跳轉方式：1. 瀏覽選擇資料夾路徑  2. 切換模擬目標環境（LXD）
- 在 `problems/tests` 下選擇已存在的.inp 檔
- 完成後點選 `run_sim` 來執行模擬
![|475](pics/Pasted%20image%2020260622151331.png)
## 3. AI 聊天界面
- 可以透過輸入 API KEY 來連結 GEMINI / CHATGPT。
- 可拖曳檔案到對話框進行詢問。
- 支援 Ctrl+滾輪縮放字體。
![|475](pics/Pasted%20image%2020260620041719.png)
![|475](pics/Pasted%20image%2020260620041753.png)

![|475](pics/Pasted%20image%2020260622151521.png)

---
# 📝 內容紀錄

## 未來完成：

- 互動式創建新.inp
- AI AGENT (尚未對接)
- 部分文字翻譯
- 自動更新通知


---
# 🔗 參考資料


---