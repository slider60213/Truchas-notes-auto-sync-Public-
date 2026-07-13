---
type: 📝 Research
created: 2026-06-19 04:28
modified: 2026-07-14 04:30
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
   ![475|475](pics/Pasted%20image%2020260713161006.png)
   ![|475](pics/Pasted%20image%2020260626184206.png)
5. **Debug Mode (Optional):** If you need to view error logs for troubleshooting, launch the application using `Truchas_WSL_DEBUG.bat` instead. 
6. **Select WSL Environment:** Choose your target WSL environment. *(By default, the GUI selects your last-used environment. You can import additional WSL environments by clicking the ➕ button.)*  
   ![475](pics/Pasted%20image%2020260714041429.png)

7. **Run Simulation:** Select your target LXD container and choose an existing `.inp` file to execute the simulation. 
8. **Configure AI Integration:** Connect to your preferred AI platform by entering your API key. 
   ![|475](pics/Pasted%20image%2020260714041717.png)

## Customize

### GUI Theme

- To customize the shortcut icon or loading screen, add your custom `.ico` or `.png` files to the assets directory. (For detailed instructions, see: `Truchas_App_Project\theme\ReadMe.md`).
- Relaunch the GUI and select your new theme from the dropdown menu located under the `Dev Terminal` button.

![|475](pics/Pasted%20image%2020260714042516.png)
![|475](pics/Pasted%20image%2020260714042410.png)

### Adding Languages

- To add or customize a language, mirror the existing directory structure under the locales directory: `Truchas_WSL_GUI/Truchas_App_Project/locales/`
	
- Localization files must strictly adhere to the following naming convention and hierarchy: `[Language] / [Python Module Name] / [Class Name].json`

---
# 📝 內容紀錄

## 未來完成：

- 互動式創建新.inp (尚未對接)
- AI AGENT (尚未對接)



---
# 🔗 參考資料


---