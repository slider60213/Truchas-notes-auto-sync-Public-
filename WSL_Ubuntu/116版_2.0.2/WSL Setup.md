---
type: 📝 Research
created: 2026-05-14 02:15
modified: 2026-05-14 02:17
tags:
  - "#Truchas"
  - 116版
  - WSL
  - 64位元
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
中文版：[[安裝教學_20260408]]

---
# 🦖 以前


---
# 👨‍💻 以後


---
# 📝 內容紀錄

### 1. Install WSL

Open **Power Shell** and enter the following command to install WSL:   
`wsl --install -d Ubuntu-24.04`
  
After the installation is complete, **restart your computer.** 
![](pics/Pasted%20image%2020260404234938.png)

Once the computer restarts, an account creation screen may automatically appear. You can proceed to enter your username and password. In the future, you can create dedicated environments under this account. This will not affect the subsequent installation of **Truchas-Lab**. Our primary goal here is to enable access to WSL-related commands.

![](pics/Pasted%20image%2020260405000204.png)

---

### 2. Extract .7z file to .tar and move to D: Drive

Right-click to extract `Truchas_Lab_116_20260408_ENG_2.7z`.

You will get the compressed file: `Truchas_Lab_116_20260408_ENG.tar`.

Move the `.tar` file to the **D: drive**, or note the file path of the `.tar` file to modify the command in Step 3.

---

### 3. Create Folder "WSL_Truchas" on D: Drive

Open **Power Shell** and enter the following command to create a folder on the D: drive: `mkdir D:\WSL_Truchas`
  
Next, enter the following command in PowerShell to import the prepared WSL environment (use spaces between arguments, not line breaks). If you moved the `.tar` file to the D: drive, the command will be:

`wsl --import Truchas-Lab D:\WSL_Truchas D:\Truchas_Lab_116_20260408_ENG.tar`

**Breakdown of the command:** * `wsl`: Enable WSL functionality.

- `--import`: Use the import function.
    
- `Truchas-Lab`: The name given to the WSL environment after import.
    
- `D:\WSL_Truchas`: The destination path for the import.
    
- `D:\Truchas_Lab_116_20260408_ENG.tar`: The location of the file to be imported.
    

If an error message appears, please confirm if the `.tar` file is indeed in the D: drive; otherwise, update the command with its actual location.

If you are unfortunate enough to have an old version already installed, please refer to the " FAQ - Starting Over " section at the bottom of this document.

Once installed, enter `wsl -d Truchas-Lab` to log into the default environment. The login interface will display system status and usage instructions.

![](pics/Pasted%20image%2020260408032744.png)![](pics/Pasted%20image%2020260408034752.png)![](pics/Pasted%20image%2020260408034806.png)

You can customize the login command to something else. In PowerShell, enter `notepad $PROFILE` to open the profile (ensure you are not logged into WSL yet). Add the following line at the end:

`function ABCD { wsl -d Truchas-Lab }`

In the future, simply typing `ABCD` in PowerShell will log you into **Truchas-Lab**.

---

### 4. Related Commands

Basically, all the commands you will need are listed on the login interface. If you want to see them again, open a new tab and log in.

**After logging into WSL:** 
  
- `run_compile`: Automatic compilation.
    
- `run_sim`: Automatically jump to `116.../problems/tests` and run simulation.
    
- `gmv`: Open GMV software.
    
- `pwd_win`: Display current Windows path.
    
- `open_win`: Open current directory in Windows Explorer.
    
- `exit`: Normal exit (background processes may continue running).
    
- `bye`: Safe exit (stops everything before exiting).
  

**After exiting WSL:** * `wsl --shutdown`: Terminate all WSL processes completely.

---

### FAQ

#### Starting Over: The Universal Solution

1. Completely close all WSL processes:
    
    `wsl --shutdown`
    
2. List and unregister (delete) the faulty Ubuntu:
    
    `wsl -l -v`
    
    `wsl --unregister Ubuntu`
    
3. Unregister (delete) the previously failed Truchas-Lab import:
    
    `wsl --unregister Truchas-Lab`
    
4. Confirm the list is empty (it should only show "No installed distributions"):
    
    `wsl -l -v`
    
5. Create a clean storage path:
    
    `mkdir D:\WSL_Truchas -ErrorAction SilentlyContinue`
    
6. Re-import Truchas-Lab:
    
    (Refer to Installation Step 4)
    

#### Quick Fix for PowerShell Lag

A. It might be an antivirus issue; try turning it off.

B. We can directly delete or reset the "troublesome" configuration file to return PowerShell to a clean state. Enter the following steps in the PowerShell window:

1. Identify which file is causing the lag:
    
    `test-path $PROFILE` (If this hangs, skip to Step 2).
    
2. Force delete the configuration file:
    
    `Remove-Item $PROFILE -Force`
    
3. Test if performance is restored:
    
    Close PowerShell and reopen it. If the prompt appears within 1 second, the fix was successful.
    

#### File Transfer

Tested methods for moving files between the PC and the container on Win 11 desktops:

1. Xftp
    
2. Windows Explorer (Normal folder navigation)
    
3. Linux commands Files with the suffix `.Zone.Identifier` may be generated in the same location; these can be safely deleted.
    

However, sometimes `.inp` files fail to simulate correctly after being moved due to conflicts between Windows and Linux line-ending formats or file permissions. Try replacing the `fix` function in `~/.bashrc` with the version below.

After logging into WSL, enter `nano ~/.bashrc` to edit the file, or use `open_win` to edit via the Windows interface. Once done, restart WSL or enter `source ~/.bashrc` to apply the settings. Then, `cd` to the file path and enter `fix [filename]` to repair it.

Bash

```
# --- Ultimate Quick Fix Function (WSL/Windows File Recovery) ---
fix() {
    local target_file="$1"

    if [ -z "$target_file" ]; then
        echo "❌ Usage: fix [filename]"
        return 1
    fi

    if [ ! -e "$target_file" ]; then
        echo "❌ Error: File '$target_file' not found"
        return 1
    fi

    echo "⚙️ Executing deep repair: $target_file ..."

    # 1. Force convert to Linux line-ending format (Remove Windows \r)
    dos2unix "$target_file" 2>/dev/null

    # 2. Ensure full permissions (777: Read, Write, Execute for everyone)
    chmod 777 "$target_file"

    # 3. Ensure ownership returns to WSL user (Avoid root or Windows locks)
    # Use sudo to ensure enforcement
    sudo chown userslider60213:userslider60213 "$target_file"

    echo "✅ [Done] Line endings, 777 permissions, and ownership corrected."
}
```