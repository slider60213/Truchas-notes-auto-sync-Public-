---
type: 📝 Research
created: 2026-07-25 02:06
modified: 2026-07-25 04:03
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


## CHANGE MESH

![525](pics/Pasted%20image%2020260725030110.png)

![525](pics/Pasted%20image%2020260725030217.png)

![525](pics/Pasted%20image%2020260725030337.png)

## CHANGE MESH+RATIO

![525](pics/Pasted%20image%2020260725030640.png)

![525](pics/Pasted%20image%2020260725030728.png)

![525](pics/Pasted%20image%2020260725030745.png)

## AUTO SIM. & FIX


![525](pics/Pasted%20image%2020260725032231.png)


![|525](pics/Pasted%20image%2020260725032309.png)


![|525](pics/Pasted%20image%2020260725032355.png)



![|525](pics/Pasted%20image%2020260725033657.png)

![|525](pics/Pasted%20image%2020260725033816.png)

### GEMINI vs GEMMA 4 B
- Gemini-2.5-pro
![525](pics/Pasted%20image%2020260725040050.png)
- Gemma-4B
![525](pics/Pasted%20image%2020260725040243.png)

Decide total task amount and `.inp` file settings based on the prompt content.
![525](pics/Pasted%20image%2020260725020956.png)

Try to conduct simulations tasks sequentially. The AGENT will fix the `inp` file based on error messages in the `log` file and retry the simulation until it succeeds or reaches the retry limit (5 times).
![525](pics/Pasted%20image%2020260725021030.png)

Once a simulation is completed normally, the post-processing will be conducted.
![525](pics/Pasted%20image%2020260725021052.png)

Since the AGENT can only solve problems utilizing the providing tools (e.g.: update_mesh.py, update_numerics.py, etc), it is not guaranteed to handle all circumstances. In this prompt test, Task 11 encountered an error caused by `MPI_Recv`, which was neither recorded in the BUG manual nor solvable with the current tool set.
![|525](pics/Pasted%20image%2020260725021324.png)


![525](pics/Pasted%20image%2020260725021353.png)



---
# 🔗 參考資料


---