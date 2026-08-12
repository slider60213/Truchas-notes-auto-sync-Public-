# Chapter 1: Motivation

## 1.1 Research Background and Motivation

  身為中央水海所博士候選人，我的研究動機十分單純，我對地球科學議題沒有絲毫熱忱，我的研究動力僅來自於，希望幫我的指導教授實現發揚 truchas 的夢想，因此在長達六年的學術生涯中，我並沒有選擇使用現今 CFD 熱門的 FLUENT、FLOW3D 或 OpenFoam 作為研究工具，然而研究前期由於我學藝不精，對於發展程式完全沒有頭緒，因此中期透過執行關渡橋局部沖刷以及龜山島山崩海嘯等實作計劃來熟悉模式，而後到了今年我準備拼畢業，此時恰逢 AI 浪潮爆發，AI 工具大幅加快我研究進度的同時，也讓我深深的體認到當前實驗室的 truchas 版本過於老舊，不僅程式語法止步於 2000 年，後續開發的程式碼也寫得相當隨意，部分變數混用、程式碼排版凌亂、還充斥著各種特定情境才適用的段落，很多時候使用者沒有修改到那些，連自己都不知道在哪被任意添加的 source code，就會導致結果失準。即使完美地避開上述問題，更嚴峻的問題是，這套 truchas-2.0.0 或 truchas-2.5.3 基本只在海嘯科學研究室的機台被使用，這不僅僅因為受眾群體小，而是連實驗室畢業的學長姐們都不再使用自己熟悉的 truchas，紛紛轉為使用 OpenFoam 或其他 CFD 軟體，究其原因，就是因為適用性過差，以下幾點可以充分說明此問題：首先是語法過時，這導致搭配模擬運行的重要套件如 PGSLib、Chaco 等程式，必須仰賴極古老版本的編譯套件，進而衍生第二個問題安裝不易，過時程式難以在逐步更新的 Windows 系統上使用，雖然有 VM 及 Virtual Box 可以模仿 LINUX 環境，但其安裝過程冗雜，實際運行的模擬效能也相當緩慢，勉強能用於教學，但完全不適合用於研究，因此過去使用 truchas 的最後可能性只剩安裝於 LINUX 機台，同樣地，這會需要安裝一堆過時軟體，並且隱含著第三個問題，機台版 trucahs 時不時會發生相同模擬設置卻有不同成果的問題，此類問題多伴隨記憶體 ALLOCATE、 DEALLOCATE 錯誤，或是變數宣告精度等細節發生。以上問題在過去或許不甚嚴重，然而隨著 AI 與 GPU 計算的興起，truchas 與其他 CFD 軟體間的差距可謂是日新月異，商業軟體的 FLUENT 與 FLOW3D 已然隨著時代的腳步實現了 AI AGENT 與 GPU 運算，開源模式的 OpenFoam 則是得益於使用者與社群眾多，因此也陸續發展出適用 AI AGENT 與 GPU 運算的版本，反觀，實驗室所使用的 truchas (或者常被稱為 Splash3D) 雖然確實陸續發表雙黏性流及流固耦合等拓展方向，礙於受眾群體過小，儼然逐漸淪為孤芳自賞。因此我的研究目標即是，將現今實驗室散落的 truchas 版本，整合為移植性更高、適用性更廣的 版本，並且目標是在 Window 上流場運行。
![|325](pics/Pasted%20image%2020260813025935.png)

![|325](pics/Pasted%20image%2020260813025951.png)

![|325](pics/Pasted%20image%2020260813030029.png)

![|325](pics/Pasted%20image%2020260813030012.png)

Numerical simulation of coastal and maritime hazards, such as landslide tsunamis and local scour around hydro-structures, plays a vital role in coastal engineering and disaster mitigation. Over the past decades, High-Performance Computing (HPC) software suites, such as Truchas, have been widely recognized for their capabilities in modeling complex multiphase flows and fluid-structure interactions (FSI).

However, traditional HPC simulation workflows heavily rely on legacy, dedicated Linux servers or bare-metal machines. These legacy environments present significant operational bottlenecks:
1. **Infrastructure Isolation**: Legacy system configurations impede seamless integration with modern development tools, software libraries, and automated execution pipelines.
2. **Workflow Rigidity**: Pre-processing, grid generation, parameter tuning, and post-processing often require extensive manual intervention, which reduces research productivity and increases human error.
3. **Inaccessibility to AI Frameworks**: The rapid advance of artificial intelligence (AI) and Large Language Model (LLM) agents provides powerful capabilities for workflow automation, real-time debugging, and dynamic parameter validation. Nevertheless, legacy HPC environments are fundamentally incompatible with these modern Python-based AI frameworks.

To address these challenges, there is an urgent need to modernize traditional simulation infrastructure. By migrating legacy HPC codes to containerized environments and integrating modern AI agent frameworks, we can bridge the gap between classical numerical modeling and cutting-edge software engineering.

---

## 1.2 Problem Statement and Research Scope

While migrating computational fluid dynamics (CFD) packages to modern containerized environments—such as Windows Subsystem for Linux 2 (WSL2) combined with Linux Containers (LXD)—offers high portability, several critical scientific and engineering questions remain:

* **Performance Integrity**: Does containerized execution on WSL2/LXD compromise computational efficiency or parallel scalability compared to bare-metal legacy systems?
* **Agentic Automation**: How can LLM-driven AI agents (e.g., via LangGraph) be systematically orchestrated to supervise parameter configuration, automate pre/post-processing, and handle execution errors in complex numerical schemes?
* **Physical Validation**: Can the modernized, AI-assisted framework reproduce accurate hydrodynamic physics and match legacy baseline results in real-world disaster scenarios?

This thesis focuses on modernizing the Truchas simulation suite within a WSL2+LXD containerized framework, establishing an LLM-driven AI agent workflow for simulation control, and validating the integrated framework using a real-world benchmark case: **Landslide Tsunami at Guishan Island**.

---

## 1.3 Research Objectives

The primary objective of this doctoral dissertation is to construct a modernized, automated, and AI-assisted computational framework for coastal disaster simulations. The specific objectives are outlined as follows:

1. **Environment Migration and Containerization**: Establish a fully portable, containerized Truchas execution environment using WSL2 and LXD with parallel processing capability (116-parallel configuration).
2. **Reconstruction of Structural/Fluid Modules**: Modernize and reconstruct core computational modules (including VFIFE/V5Slider) to enhance interoperability with modern Python-based automation pipelines.
3. **Development of LLM-Driven AI Agent Workflow**: Design and implement an intelligent agent architecture utilizing LangGraph to automate simulation pre-processing, parameter validation, execution supervision, and error handling.
4. **Validation via Benchmark Case Study**: Execute a comparative analysis between the legacy bare-metal setup and the modernized WSL2+AI Agent framework using the Guishan Island landslide tsunami simulation as a physical benchmark.

---

## 1.4 Thesis Organization

This dissertation is structured into five chapters, organized as follows:

* **Chapter 1 (Motivation)**: Outlines the research background, identifies key operational challenges in legacy HPC systems, defines research objectives, and presents the thesis scope.
* **Chapter 2 (Framework Modernization: Truchas on WSL2/LXD)**: Details the migration architecture, LXD container deployment, WSL2 environment configuration, and code module reconstruction (VFIFE).
* **Chapter 3 (LLM-Driven AI Agent and Workflow Automation)**: Describes the design and implementation of the LangGraph AI agent, automated pipeline execution, GUI integration (V5Slider), and error-handling routines.
* **Chapter 4 (Case Study & Performance Benchmark: Guishan Island Landslide Tsunami)**: Presents the physical setup, numerical results, efficiency benchmarks, and comparative validation between legacy and modernized setups.
* **Chapter 5 (Case Study & Performance Benchmark: Guandu Bridge Local Scour)**: Presents the physical setup, numerical results, efficiency benchmarks, and comparative validation between legacy and modernized setups.
* **Chapter 6 (Conclusions and Future Work)**: Summarizes the key scientific contributions, acknowledges current technical limitations, and discusses future perspectives regarding GPU acceleration and digital twin integration.

---

## 1.5 Key Conceptual Framework

The overarching architecture connecting environment migration, AI orchestration, and physical validation is illustrated in Figure 1.1.

![Figure 1.1: Schematic representation of the modernized AI-assisted simulation framework](attachments/fig1_1_framework_overview.png)

> **Figure 1.1 Description**: Overview of the modernized workflow, illustrating the transition from legacy bare-metal execution to the WSL2/LXD container environment integrated with LangGraph AI Agents and Python-driven automation pipelines.