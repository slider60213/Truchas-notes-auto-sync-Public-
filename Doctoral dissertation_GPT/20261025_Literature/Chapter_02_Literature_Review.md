# Chapter 2 Literature Review

## 2.1 Three dimensional flow and local scour

### 2.1.1 Foundation geometry and flow structure

Local scour is a coupled response of the flow and the bed around an obstruction. Downflow, separation, and wake motion redistribute the forcing near a foundation, while the developing hole changes the subsequent flow. Roulund et al. (2005) combined numerical and experimental investigation around a circular pile, providing a reference for evaluating three-dimensional flow and scour together. The relevance to Guandu Bridge is methodological: both the hydrodynamics and the bed response require assessment. The circular-pile geometry itself is not a direct analogue for every component of the bridge foundations.

Baykal et al. (2015) examined flow and scour around a vertical circular cylinder with a model that represents sediment transport and bed morphology. This provides a useful contrast to the present rheological formulation. A transport model describes sediment fluxes and the resulting bed update, whereas a rheological continuum describes material deformation and movement through stresses. The formulations should be compared through observables and documented assumptions rather than ranked by the number of empirical coefficients alone.

For a complex foundation, several geometric scales may influence the flow simultaneously. Columns, connecting members, pile caps, and a protective mound can each redirect the approach flow. Their relative exposure changes as scour progresses. A representative-pier calculation must therefore state which components are resolved, which are embedded within a fixed solid description, and which lie below the initial bed. Similar minimum elevations do not establish that two models resolve the same erosion mechanism.

The comparison extends beyond isolated piles. Ni et al. (2021) used circular pile-group experiments to assess geometry-dependent scour under steady clear-water flow. Vuong et al. (2024) used LES, VOF and DBM for complex foundations, linking exposed-pile arrangement with scour and pressure. This establishes complex-pier DBM modeling as prior work. The contribution of the Guandu application must therefore be defined through its observations, boundary treatment and particular foundation scenarios, with any shared model or dataset identified explicitly.

### 2.1.2 Tidal boundaries and field assessment

A tidal river introduces a further issue: a section can contain velocities of opposite signs at different depths. Replacing that distribution with one mean can preserve net transport while losing the vertical structure that controls foundation exposure. The Guandu measurements make this distinction explicit. The appropriate modeling question is how much of the observed structure the boundary must retain to reproduce interior measurements.

Field assessment also depends on the spatial and temporal support of the data. A section–layer mean summarizes many observations, a point profile resolves vertical structure at one location, and a surface drifter follows a path influenced by the near-surface flow. These measurements should not be pooled as interchangeable evidence. They constrain different aspects of the model. A surface streamline that resembles a drifter track can coexist with an inaccurate deep velocity field.

When boundary conditions are selected from the same campaign used for assessment, the resulting comparison is partly conditional on the observations. Excluding boundary sections is a useful diagnostic because it reduces direct prescription, but it does not create a new independent campaign. A stronger predictive test would use a different tide, discharge, or survey period with the parameterization fixed beforehand. This distinction is central to the interpretation of Chapter 4.

Yu et al. (2023) based complex-pier tidal experiments on site conditions at a sea-crossing bridge. Chu et al. (2025) compared bidirectional and unidirectional forcing and found reversal-associated backfilling and changes in scour symmetry. Peng et al. (2026) showed that water depth, current speed and skew can jointly alter scour around cap–pile-group foundations. Together, these results make the forcing history a necessary part of a comparison with Guandu. Two fixed approach angles can identify conditional spatial responses without reproducing the erosion and recovery within repeated tidal cycles.

### 2.1.3 Cohesive beds and protection systems

The SRICOS research program investigated scour rates in cohesive soils at bridge piers (Briaud et al., 1999). Its relevance here is that the rate and duration of erosion matter alongside a maximum depth. A constitutive representation of a cohesive bed must likewise be assessed over time. A simulated hole that appears to stabilize during a short run need not represent an equilibrium under a complete flood hydrograph.

Protection adds another class of mechanics. Suaznabar et al. (2017) developed a computational approach to assess riprap-rock stability using fluid–structure interaction and laboratory assessment. This addresses a different observable from scour around a fixed protective shape. The latter can diagnose how the prescribed shape redirects flow, but cannot determine the onset of stone movement. For Guandu Bridge, separating these questions avoids interpreting a fixed-riprap experiment as a complete protection-performance test.

The remaining application gap is therefore specific. The model needs to connect realistic approach-flow structure and documented foundation geometry with a material description that transfers across locations and conditions. The large P5 discrepancy is valuable evidence for that gap. A convincing extension would evaluate bank geometry, bed heterogeneity, and protection permeability separately, with matched observations and numerical sensitivity checks.

The Erosion Function Apparatus of Briaud et al. (2001) measures a hydraulic erosion-rate relation; it does not measure the same quantity as a rotational rheometer. Time-dependent clear-water scour experiments also show why an end-of-run depth needs a duration context (Melville and Chiew, 1999), although their sand-bed scaling cannot be adopted unchanged for cohesive sediment. DBM has been used for muddy beds around offshore turbine foundations (Vuong et al., 2023) and for flow and scour around an echinoid test (Lin et al., 2024). These are useful tests of the formulation across geometries, while site-specific erosion rates and sediment structure remain separate constraints. The forensic study of Shuang-Yuan Bridge further demonstrates the need to connect hydraulic scenarios with foundation stability before making a failure assessment (Wu et al., 2014b).

## 2.2 Rheology and landslide generated waves

### 2.2.1 Yield stress and continuum idealization

Liu and Mei (1989) analyzed the slow spreading of a Bingham-fluid sheet on an inclined plane. Their formulation illustrates how finite yield stress changes the relation between forcing, motion, and final shape. It also identifies a controlled setting in which a constitutive idealization can be evaluated. Transferring such a description to a natural landslide requires additional assumptions about material composition, pore conditions, and deformation rate.

Wu et al. (2020) developed a three-dimensional Bingham-type landslide model and assessed rheological-flow cases. Vuong et al. (2020) extended the investigation to slump-generated tsunamis, including a laboratory comparison and sensitivity to material parameters. Together they establish the published methodological background of the laboratory framework. The Guishan study is an application of that framework with a reconstructed source and site-specific material information. It should not be presented as the initial invention of the underlying Bingham or volume-of-fluid methods.

A finite-viscosity approximation to an unyielded region is computationally convenient, but it permits deformation that an ideal rigid plug would not. The discontinuous bi-viscous model further allows the low-rate branch to be selected independently. An empirical curve fitted to apparent viscosity is another distinct object. Its agreement with a sample measurement does not demonstrate that it has the same yield structure as the piecewise model. This distinction must remain visible when a numerical configuration is labeled DBM but uses a fitted viscosity function.

Huang and García (1998) extended slope-flow analysis to Herschel–Bulkley rheology, showing that shear thinning changes runout and final deposit form. This makes constitutive selection a potentially observable source uncertainty. Frigaard and Nouar (2005) examined the convergence and physical fidelity of regularized viscoplastic calculations. Their analysis motivates distinguishing the measured constitutive curve from the finite-viscosity approximation used to compute low-rate motion. Agreement with a final footprint is insufficient to assess both choices independently.

### 2.2.2 Source motion and observable deposits

The tsunami source depends on how the moving material displaces water through time. Volume alone does not specify that process. Acceleration, deformation, submergence, and the surrounding bathymetry influence the generated disturbance. A final deposit constrains an outcome of those processes, while a wave record constrains part of their time history. They are complementary observations rather than substitutes.

Huang (2018) investigated northern-flank mass failure at Guishan Island using marine geophysical data. Deffontaines et al. (2022) supplied a broader structural and geomorphic interpretation of the volcanic island. These studies provide the geological setting and reconstruction constraints used in the application. They do not determine every parameter needed by the numerical source model. In particular, an idealized pre-failure cone is an assumption added to the observed terrain and deposit information.

If two rheologies produce similar footprints, the deposit comparison has not uniquely selected between them. Additional constraints could include thickness distribution, source scar volume, material sampling, or independent evidence of wave effects. The appropriate research question is which combinations of assumptions remain compatible with the available observations. Chapter 5 follows this conditional interpretation rather than treating one matching footprint as proof of the historical motion.

The laboratory sliding-mass experiments and numerical comparisons of Liu et al. (2005) provide controlled evidence for three-dimensional wave generation. Wu et al. (2014a) subsequently combined partial-cell fluid treatment with DEM translation and rotation for moving blocks. Huang et al. (2024) developed the RFM approach and assessed sphere entry and a semispherical-slide tsunami. These are published rigid-body capabilities. Coupling such bodies with a deformable DBM phase in one mixed failure remains a separate development and validation problem.

At volcanic-island scale, Grilli et al. (2019) combined collapse geometry with observations of the Anak Krakatau tsunami and compared granular and fluid source descriptions. Haridhi et al. (2023) developed a hypothetical source using offshore geophysical constraints near northern Sumatra. These studies illustrate different evidential settings: reconstruction of an observed tsunami and conditional assessment of a potential source. The MTD3 comparison belongs to a conditional reconstruction because equivalent historical wave observations are unavailable. Hu et al. (2024) further illustrate the value of combining independent records when assessing possible earthquake and landslide source contributions at Pingtung. Chao et al. (2018) examined rapid seismic constraints for a Greenland landslide. Neither application supplies the missing Guishan source history, but both identify observations that could reduce its uncertainty.

### 2.2.3 Interfaces and regional propagation

Hirt and Nichols (1981) introduced the fractional-volume basis of the volume-of-fluid method for tracking free boundaries. In the present multiphase application, material fractions also define the distribution of mobile sediment or landslide material. Geometrical interface reconstruction and a diffusive material treatment can produce different local fraction profiles. The surface diagnostic must therefore be specified along with the governing equations.

This issue is especially important when a selected isosurface represents the water level. In mixed cells, moving the threshold changes the extracted position. A reduction in an extracted crest can arise from a change in dynamics, a change in material distribution, or the extraction procedure. These alternatives can be distinguished by inspecting vertical fraction profiles and testing thresholds while retaining the same numerical solution.

Regional propagation adds a scale transition. A source-region Navier–Stokes calculation and a shallow-water propagation model do not evolve identical state variables. An elevation snapshot contains less information than the full three-dimensional velocity and material fields. Its use is a modeling approximation whose adequacy depends on the transfer time, remaining source motion, momentum treatment, and wave scales. This is why an elevation-only transfer should be described explicitly rather than assumed to be a fully conservative coupling.

Abadie et al. (2012) used a three-dimensional Navier–Stokes calculation for generation and a Boussinesq model for propagation. Regional COMCOT forecasting work provides another example of matching model extent to an operational task (Lin et al., 2015). Depth-integrated wave-runup benchmarks address wetting and drying (Lynett et al., 2002), while dispersive-wave analysis demonstrates dependence on source length scales (Kirby et al., 2013). Consequently, a regional shallow-water calculation requires a scale assessment rather than an assumption that all source wavelengths are resolved.

For the Noto tsunami, Lo et al. (2026) introduced time-evolving landslide-induced seabed forcing from Splash3D into COMCOT and examined the difference from instantaneous initialization. This is directly relevant to the elevation-only transfer at 10 s in Chapter 5. Comparing several transfer times with a continuously forced calculation would test the omitted generation, while a common surface-extraction definition would separate transfer error from interface diagnostics. The broader kinematic synthesis of Løvholt et al. (2015) supports evaluating source duration and deformation together, rather than selecting a transfer time from convenience.

## 2.3 Numerical assessment and reproducible computation

### 2.3.1 Physical validation and numerical consistency

Physical validation compares a calculation with observations of the modeled system. A numerical consistency comparison instead asks whether two implementations or configurations produce sufficiently similar outputs. A legacy simulation can be a useful reference for the second question even when it is not a measured truth. Confusing these comparisons can make a software migration appear to validate a physical model that has not been tested against nature.

The acceptance criterion should follow the quantity of interest. For a tsunami source, relevant outputs may include the generated surface field, material trajectory, and momentum. For scour, they may include minimum elevation, hole shape, and time evolution. An aggregate field correlation can remain high while a local error affects one of these outputs materially. A useful evaluation therefore includes local diagnostics and application-specific quantities alongside global statistics.

Celik et al. (2008) describe how to estimate and report discretization uncertainty. Their procedure provides a separate line of evidence from comparison with field observations or a legacy executable. A numerical platform migration can reproduce the reference solution while retaining its discretization error. Conversely, a refined calculation can differ from the reference without being less accurate. Chapter 6 therefore treats agreement across environments as a consistency result and does not claim grid convergence from the platform comparisons.

### 2.3.2 Preserving the computational experiment

Sandve et al. (2013) emphasize tracking the steps that produce a computational result, including software versions, parameters, and transformations. Wilson et al. (2014) discuss practices such as version control, modular organization, and automated checks that improve scientific software development. The common implication for this dissertation is that the reproducible object is the complete experiment, not only the final executable or figure.

The customized Truchas workflow contains several transformations capable of changing a reported result. Terrain is rotated and interpolated; material fractions are converted to surfaces; restart outputs are renumbered; and different binaries may be used under the same descriptive version label. Each transformation needs its own provenance. Without that record, a discrepancy can be attributed incorrectly to the physical solver when it originated during preprocessing or extraction.

Preservation should also include failed experiments. A log that records a missing dependency or an MPI error can delimit the conditions under which a workflow operates. Removing failed attempts from an archive would prevent reconstruction of the intervention that produced the final result. This is particularly relevant to agent-assisted retries, where several input revisions may precede normal termination.

### 2.3.3 Containerized environments

Kurtzer et al. (2017) describe scientific containers as a means of moving a computational environment between resources. The relevance to legacy modeling is dependency preservation: a container can retain a compatible userspace and software stack. Portability of that stack remains distinct from scalability and from numerical equivalence after migration.

Microsoft's WSL documentation distinguishes WSL1's translation-based architecture from WSL2's Linux kernel within a lightweight utility virtual machine (Microsoft, 2026). LXD documentation distinguishes system containers, which share the host kernel, from virtual machines with their own kernels (Canonical, 2026). In a WSL2/LXD arrangement, these mechanisms are layered. It is therefore inaccurate to describe the complete arrangement as containing no virtual machine.

These architectural descriptions do not predict the runtime of a particular CFD case. Hardware, worker count, compiler options, memory access, and output placement all matter. A useful benchmark changes one factor at a time where possible and records the complete configuration. When several factors differ, the measured speedup should be reported as a configuration comparison. Chapter 6 uses this interpretation for the available timing table.

Boettiger (2015) explains how container images support dependency preservation and reuse. Di Tommaso et al. (2017) combine containerized computation with an explicit workflow system. The latter work concerns bioinformatics, but the architectural distinction is applicable here: preserving the environment and preserving the sequence of operations are complementary. Neither publication predicts the runtime or numerical equivalence of the WSL2/LXD configuration used in this dissertation.

## 2.4 Tool assisted and agent assisted workflows

### 2.4.1 Execution graphs and model assistance

Yao et al. (2023) investigated language models that interleave reasoning and actions through external tools. This provides conceptual background for a simulation assistant that reads a task, invokes parameter-editing functions, observes logs, and decides whether to continue. The published results do not establish performance for Truchas. That performance must be assessed on the actual simulation workflow and failure set.

Many operations in the laboratory pipeline are deterministic. Output conversion, restart preparation, and monotonic numbering can be implemented by scripts without a language model. The model-assisted component is most relevant where a natural-language request must be mapped to an experiment or where diagnostic evidence requires interpretation. Keeping these responsibilities distinct makes it possible to test whether the model adds value beyond a scripted baseline.

Xu et al. (2025) presented CFDAgent, with separate preprocessing, solver and post-processing roles and tests including canonical sphere flows. This is a closer CFD comparison than general tool-use demonstrations. Its tested flow solver, geometry pathway and quantities of interest differ from the Truchas–DBM workflow. The appropriate comparison is therefore task coverage, numerical checks and intervention recording; success rates from a different benchmark cannot be assigned to the present system.

### 2.4.2 Execution success and scientific correctness

A retry policy needs an explicit definition of success. Normal process termination is an execution outcome. Scientific success also requires the requested physical configuration, an adequate simulation duration, complete outputs, and acceptable numerical diagnostics. An agent that changes viscosity, geometry, or forcing until a run succeeds may solve an execution problem while changing the experiment.

The workflow should therefore preserve immutable scientific intent and record each permitted numerical or operational change. Some interventions can be bounded in advance, such as correcting a known formatting error. Others require researcher review because they change the discretization or physical assumptions. The distinction is methodological rather than a claim that automated operation is inherently unreliable.

### 2.4.3 Evidence needed for evaluation

The available demonstrations show feasibility for selected edits and sequential tasks. A systematic evaluation would additionally define a task set, expected outcomes, known failure causes, and allowed interventions. It would report success rates, false repairs, time, resource use, and the fraction of cases requiring researcher intervention. Repeated trials would be needed if model outputs vary.

The documented MPI_Recv failure is particularly informative because it lies outside the provided tool coverage. It demonstrates a boundary of the current workflow. The proper response is to preserve the failure state and expand or revise the supported diagnostics through controlled development. It is not evidence that a larger language model would necessarily repair the numerical environment correctly.

## 2.5 Synthesis of research gaps

The physical literature motivates three-dimensional treatment of geometry, deformation, and material interfaces, while the applications show that boundary and constitutive information remain limiting. The reproducibility literature motivates preserving the full sequence from observation to figure, while the deployment records show why a packaged environment still needs numerical assessment. The agent literature motivates tool-mediated assistance, while the demonstrations show that execution and scientific correctness must be evaluated separately.

These gaps define a common research program: preserve and assess a specialized modeling capability without treating operational convenience as physical validation. The following chapters apply that principle to the numerical formulation, the two field applications, the container migration, and the simulation-management workflow.
