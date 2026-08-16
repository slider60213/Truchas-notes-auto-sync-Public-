










## 160-WSL Comp
[Truchas-WSL_2.5.3_Guishan_Landslide](../Truchas_Lab/II.%20Truchas/C.%20Truchsa-WSL/03_%20Truchas-2.5.3/Truchas-WSL_2.5.3_Guishan_Landslide.md)
To optimize computational throughput for large-scale free-surface hydrodynamic simulations, the numerical solver (Truchas) was benchmarked across hardware configurations and virtualized operating environments. The control dataset—established from previous reporting benchmarks executed on Machine 160 utilizing a 4-CPU parallel domain decomposition—served as the reference baseline ($N = 8,000$ spatial grid nodes at $t = 125.02\text{ s}$). Performance metrics and field-scale accuracy were quantitatively evaluated against three comparative groups: Machine 160 (4 CPUs, repeatability check), Machine 160 (10 CPUs, parallel scalability test), and a containerized WSL-LXD environment (10 CPUs, platform migration test).

As detailed in Table 4.X, migrating the simulation framework to the WSL-LXD platform with 10-CPU parallel processing yielded a substantial reduction in wall-clock time, decreasing from 14 hours 06 minutes to 4 hours 27 minutes—a speedup factor of 3.16. Statistical cross-comparison confirms that this computational acceleration maintained exceptional physical fidelity. The WSL-LXD implementation achieved a Mean Absolute Error (MAE) of $0.0204\text{ m}$, a Root Mean Square Error (RMSE) of $0.3420\text{ m}$, a negligible mean bias of $0.0041\text{ m}$, and a coefficient of determination ($R^2$) of $0.9953$ relative to the baseline. Furthermore, spatial residual analysis revealed that $99.00\%$ of all grid locations maintained absolute water surface elevation deviations below $0.10\text{ m}$.

The isolated maximum discrepancy ($15.0000\text{ m}$) observed at spatial coordinates $(1025.00, -875.00)$ in both 10-CPU deployments is attributed to minor phase shifts in wave-front propagation interacting with the VOF (Volume of Fluid) isosurface reconstruction algorithm at the wetting-and-drying boundary layer. Such localized artifacts do not reflect systemic numerical instability or global energy dissipation. Consequently, the containerized WSL-LXD architecture with 10-CPU parallel execution is validated as a robust, highly efficient computational workflow for subsequent numerical investigations.











