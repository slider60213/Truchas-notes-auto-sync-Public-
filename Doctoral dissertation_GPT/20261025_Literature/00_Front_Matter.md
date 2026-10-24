# A Reproducible Truchas Platform for Rheological Modeling of Coastal and Hydraulic Hazards

[Doctoral candidate's official English name]

Graduate Institute of Hydrological and Oceanic Sciences

National Central University

Advisor: Professor Tso-Ren Wu

[Degree date to be confirmed]

## Abstract

Scientific use of a specialized computational fluid dynamics platform depends on both its physical models and the ability to reconstruct the environment in which those models run. This dissertation develops and assesses a research workflow around the laboratory's Truchas/Splash3D platform, connecting rheological applications, containerized deployment, and agent-assisted simulation management. The physical applications concern local scour at Guandu Bridge and landslide-generated tsunami scenarios at Guishan Island. Their assessment distinguishes comparisons with field observations from comparisons between numerical configurations.

At Guandu Bridge, layered approach-flow boundaries reproduce principal features of measured tidal velocities more effectively than uniform boundary means. Recalculation of reported section–layer comparisons gives mean absolute differences of 0.0359 m/s for eight non-boundary ebb pairs and 0.0525 m/s for nine interior flood pairs. Local movable-bed experiments predict additional scour of 1.36–2.17 m, 1.95–2.71 m, and 4.41–5.75 m at approach velocities of 5, 6, and 8 m/s, respectively. Historical changes near P5 remain underpredicted by the idealized flat-bed configuration. At Guishan Island, a sample-based rheological configuration and a low-viscosity experiment reproduce the broad MTD3 deposit footprint with different settling histories. A diffuse material treatment changes extracted surface excursions, and regional tsunami calculations produce conditional Yilan maximum elevations approaching 1.5 m.

Deployment records document operation of the solver in WSL2/LXD environments. A 560000-cell benchmark reaches the selected output after 14 h 06 min on the legacy four-worker configuration and 4 h 27 min on a ten-worker 32-bit WSL configuration. The resulting factor of 3.17 measures a combined configuration difference rather than isolated container overhead. Reported surface comparisons show small aggregate differences together with a local 15 m discrepancy requiring diagnosis. Workflow demonstrations document parameter editing, sequential execution, post-processing, and bounded retries, including an unresolved MPI failure.

The integrated findings support preservation and continued assessment of the specialized platform. They also show that deposit agreement, numerical consistency, normal execution, and physical validity require different evidence. The dissertation establishes a traceable basis for that assessment and identifies the remaining requirements for constitutive reproducibility, controlled performance benchmarking, and reliable agent assistance.

Keywords: Truchas; Splash3D; rheology; local scour; landslide tsunami; reproducible computation; WSL2; LXD; scientific workflow

## Acknowledgements

[To be completed by the candidate. Committee membership, personal acknowledgements, and funding details are intentionally left for confirmation.]

## Contents

Chapter 1 Research motivation and scope

Chapter 2 Literature review

Chapter 3 Numerical framework and assessment methods

Chapter 4 Guandu Bridge flow and local scour

Chapter 5 Guishan Island landslide and tsunami scenarios

Chapter 6 Containerized deployment and numerical consistency

Chapter 7 Agent-assisted simulation workflows

Chapter 8 Conclusions and future work

References

Appendix A Reported velocity comparison data

## Principal symbols and abbreviations

| Symbol or abbreviation | Meaning |
| --- | --- |
| u and U | Velocity vector and streamwise component |
| p and ρ | Pressure and density |
| S and γ̇ | Strain-rate tensor and scalar shear-rate invariant |
| μ_A and μ_B | Unyielded and yielded viscosity parameters |
| τ₀ and γ̇_y | Stress intercept and transition shear rate |
| fₘ | Material volume fraction |
| η | Free-surface elevation relative to the defined datum |
| d_s | Additional scour depth below the initial bed |
| DBM | Discontinuous bi-viscous model |
| LES | Large-eddy simulation |
| PLIC and VOF | Piecewise linear interface calculation and volume of fluid |
| RFM | Rigid fluid method |
| MPI | Message Passing Interface |
| WSL2 | Windows Subsystem for Linux 2 |
| LXD | System-container and virtual-machine manager |
| MAE and RMSE | Mean absolute error and root-mean-square error |
| MTD | Mass transport deposit |
