# Chapter 3 Numerical Framework and Assessment Methods

## 3.1 Model lineage and scope

The numerical platform originates from the Truchas code developed at Los Alamos National Laboratory. The current upstream project describes a multiphysics platform oriented toward manufacturing processes (LANL, 2026). The laboratory's Splash3D development adapted an earlier Truchas framework for free-surface hydrodynamics, turbulence, and coastal applications. Subsequent laboratory versions include specialized rheological and moving-body modules. The names Truchas, Splash3D, and DBM therefore describe related parts of a development history rather than three independent solvers.

Published applications document complementary capabilities: moving-solid coupling (Wu et al., 2014a), deformable landslide rheology (Wu et al., 2020), local scour with DBM (Vuong et al., 2023, 2024; Lin et al., 2024), and RFM slide dynamics (Huang et al., 2024). These citations establish method lineage; the executable and input provenance must still identify which capabilities were enabled in each reported application.

Version labels alone are insufficient to identify a calculation. The application reports refer to earlier Splash3D developments, whereas the deployment work concerns customized Truchas 2.5.3 configurations. The physical results should be linked to the actual executable and inputs used at the time. A successful later migration does not imply that every historical application was rerun with that migrated binary. This distinction is retained throughout the dissertation.

The common formulation described below establishes consistent notation for interpreting the recorded experiments. Details that depend on a particular source version, such as the exact pressure solver or material-mixture rule, require confirmation against that version. A generic description of current upstream software is not substituted for an audit of the laboratory code.

## 3.2 Conservation equations and interfaces

### 3.2.1 Incompressible multiphase flow

The modeled materials are treated as incompressible phases. Their distribution is represented by material volume fractions fₘ, with 0 ≤ fₘ ≤ 1 and Σfₘ = 1 in the fluid portion of a cell. The velocity satisfies

$$
∇·u = 0.
$$

For a volume-weighted density ρ, the momentum equation is expressed in conservative notation as

$$
∂(ρu)/∂t + ∇·(ρu⊗u) = −∇p + ∇·τ + ρg.
$$

The material fractions satisfy an advection equation,

$$
∂fₘ/∂t + ∇·(fₘu) = 0.
$$

This representation permits air, water, and mobile material to share a computational domain. It does not imply that all physical processes within a sediment mixture are resolved. Grain motion, pore-water migration, fragmentation, and entrainment may require additional constitutive or transport descriptions. Their omission must be evaluated for the target observable.

The stress is written as τ = 2μ_eff S, where S is the symmetric velocity-gradient tensor. The material viscosity can depend on deformation rate. Turbulence closure adds modeled stress at unresolved scales. Surface-tension and other optional terms should be included in a case description only when enabled in the relevant calculation; their presence in a generic solver does not establish their use in the field applications.

### 3.2.2 Finite volumes and geometric reconstruction

Finite-volume discretization integrates conservation over each computational cell. The balance is determined by fluxes through its faces and local source terms. This is useful for multiphase applications because material exchange can be expressed in the same geometric framework as momentum transport. Conservation is nevertheless a property to verify from the implemented fluxes and run diagnostics, not an automatic guarantee from the method's name.

The volume-of-fluid approach represents an interface through partial cell occupancy (Hirt and Nichols, 1981). In a geometrical PLIC reconstruction, an interface cell contains a plane whose orientation is inferred from the fraction field and whose position is chosen to recover the specified volume. The original source treatment seeks to retain a relatively sharp interface during advection. The DBM-Diffused variant intentionally permits a different material distribution. Both treatments require a consistent diagnostic for reporting the water or sediment surface.

Terrain and fixed foundations are embedded in the computational geometry. Their effective representation depends on cell size and the treatment of intersected cells. A coarse mesh can preserve the approximate volume of a structure while inadequately resolving a narrow gap or local curvature. Consequently, a refinement test should assess the geometric features relevant to the process as well as global flow statistics.

## 3.3 Turbulence and temporal solution

### 3.3.1 Large eddy simulation

The project formulation uses a Smagorinsky-type closure for unresolved turbulent stresses (Smagorinsky, 1963). The eddy viscosity has the conventional form

$$
μ_t = ρ(C_s Δ)²|S|,   |S| = √(2S:S),
$$

where Δ is a grid-related filter scale and C_s is a model coefficient. The Guishan report gives C_s = 0.15 in its formulation. That value should be linked to the actual case input before it is assigned to all runs. Near-wall treatment, interface cells, and high-viscosity material can modify how the closure behaves in practice.

An LES label does not establish that all important turbulent structures are resolved. The very different horizontal spacings in the reach-scale Guandu model illustrate why resolution must be considered explicitly. The available field comparisons assess aggregated velocity structure; they do not verify a turbulence spectrum or wall-resolved stresses at each foundation. This limits the level of mechanism that can be inferred from the streamline plots.

### 3.3.2 Pressure projection and viscous stiffness

The laboratory methodology describes a predictor–projection sequence. Momentum is advanced to an intermediate state and a pressure correction is used to obtain a velocity field satisfying the discrete incompressibility condition. In schematic notation,

$$
∇·[(1/ρ)∇pⁿ⁺¹] = (∇·u*)/Δt,
$$

followed by a pressure-gradient correction of u*. The precise operators, boundary terms, and tolerance must correspond to the selected code version. This equation describes the role of the pressure solve; it is not a source-code-level specification of the complete algorithm.

Large constitutive viscosities make an explicit diffusion step restrictive because its stable time increment decreases with increasing viscosity and decreasing squared cell size. The project adopts implicit viscous treatment to address this stiffness. Implicit treatment changes the stability constraint but does not remove the need to resolve transient processes or converge the nonlinear constitutive update. Large viscosity contrasts and abrupt branch changes can still affect convergence.

## 3.4 Material descriptions

### 3.4.1 Bingham and bi-viscous models

An ideal Bingham material has a finite yield stress and a yielded relation between stress and shear rate. A numerical bi-viscous approximation replaces the ideal unyielded behavior with a finite, large viscosity. The discontinuous bi-viscous formulation allows the low-rate viscosity to be specified independently of the yielded branch. With γ̇ = √(2S:S), a scalar constitutive description is

$$
μ_r(γ̇) = μ_A for γ̇ < γ̇_y,
$$

$$
μ_r(γ̇) = μ_B + τ₀/γ̇ for γ̇ ≥ γ̇_y.
$$

The transition convention, parameter units, and treatment at the threshold are part of the constitutive specification. A very large μ_A approximates resistance but does not set deformation identically to zero. The parameter τ₀ is the intercept of the yielded branch in this notation. It should not be conflated automatically with every definition of a measured yield stress.

For Guandu material the reported values are γ̇_y = 0.53 s⁻¹, μ_B = 120.08 Pa s, and τ₀ = 63.64 Pa. The report leaves μ_A unspecified numerically. A reproducible implementation requires that missing value and the rule for mixing rheological properties in interface cells. The parameter set is therefore a documented starting point rather than a complete executable material specification.

Frigaard and Nouar (2005) provide a basis for assessing error introduced by finite-viscosity regularization. The numerical high-viscosity branch should be varied independently of measured yielded parameters. A Herschel–Bulkley description offers another constitutive comparison where shear thinning is supported by measurements (Huang and García, 1998); no such replacement is assumed for the existing Guandu simulations.

### 3.4.2 Empirical viscosity curves

The Guishan sample measurements motivated a fitted apparent-viscosity relation because the stress–rate data did not follow one simple idealization. This is a useful extension of the material-description workflow: an empirical relation can retain measured behavior over a specified range. Its scientific interpretation depends on the sampling procedure, rate interval, fitting objective, and uncertainty.

The numerical coefficients printed in the report text and the equation drawn on its fitted-curve figure are not algebraically identical. Accordingly, this dissertation does not select one expression as the implemented law. The original input or routine must resolve that discrepancy. A smooth curve should also not be called a complete regularization solely because it lacks a piecewise jump. A term proportional to 1/γ̇ is singular at zero rate unless a cutoff or alternative limit is defined.

A controlled evaluation of the proposed curve would retain the same geometry, grid, forcing, and extraction method while changing only the constitutive relation. It would compare measured stresses or viscosities, material motion, numerical residuals, and conservation. Until that comparison is available, the supported result is use of a sample-based configuration and its documented behavior. Elimination of numerical oscillations or universal improvement over DBM has not been established.

### 3.4.3 Moving bodies and mixed failure

Huang et al. (2024) established the rigid-fluid method as a published three-dimensional capability coupled to Splash3D, with sphere-entry and semispherical-slide benchmarks. It follows earlier two-way moving-solid work by Wu et al. (2014a). The qualification presentation identifies combined RFM–DBM simulation of mixed slide–slump failures as planned work. This distinction concerns the combined implementation; it does not imply that RFM itself remains unimplemented. Successful separate modules do not establish conservative or accurate interaction when both are active.

The Guishan application considered here uses deformable material representations rather than a demonstrated fully coupled mixture of independently moving blocks and rheological sediment. Mixed failures remain an important extension, but require explicit coupling equations and matched benchmarks. The same distinction applies to future stone-motion modeling around bridge protection.

Regional transfer also belongs to the numerical specification. Published two-way nested storm-surge modeling describes explicit nesting and moving-boundary choices (Tsai et al., 2022); these choices cannot be inferred for the Guishan grid from the common model family. The dynamic landslide forcing of Lo et al. (2026) supplies a specific alternative to the elevation-only snapshot in Chapter 5. A reproducible comparison must identify transferred variables, coordinate transformation, receiving bathymetry, time interpolation and subsequent forcing.

## 3.5 Execution structure and configuration provenance

The draft architecture identifies an input-reading stage, setup, and a cycle driver. Its schematic sequence is input interpretation, geometry and material initialization, an initial pressure-related prepass, and repeated material-advection and flow-solution operations. Laboratory extensions enter both during initialization and within the transient loop. Examples include bathymetry loading, gauge setup, time-dependent boundary treatment, and output processing.

This sequence explains where configuration changes can enter the experiment. An input parser may change a parameter before the solver starts; a boundary module may change forcing at every cycle; and a post-processing routine may change the reported surface after the calculation. Tracking only source-code modifications would miss the other two sources of variation.

Each case should therefore retain a configuration manifest containing the source revision, executable identity, compiler and libraries, mesh, material properties, boundary conditions, time controls, worker count, output cadence, and extraction definitions. The manifest should link derived figures to their original fields. For a restart sequence, it should also record checkpoint identity and physical time, so that output numbering cannot be mistaken for elapsed time.

## 3.6 Assessment hierarchy

The assessment proceeds from controlled constitutive or hydrodynamic cases to field comparisons and then to deployment and workflow comparisons. The published rheological benchmarks provide methodological background. The Guandu observations test application-specific flow structure. Its historical bed changes and the Guishan deposit constrain morphology, with the temporal limitations discussed in the application chapters. Cross-platform fields then test consistency relative to a numerical reference. Agent demonstrations test operational behavior.

For scalar comparisons, define e_i = q_i − q_ref,i. The reported summary measures are

$$
MAE = Σ|e_i|/N,   RMSE = √(Σe_i²/N).
$$

$$
Bias = Σe_i/N.
$$

The reference, sample support, weighting, and physical time must accompany these statistics. A coefficient of determination measures a different aspect of agreement and should not be substituted for an error magnitude. Maximum absolute difference and its location help identify local failures concealed by averages.

Grid assessment should examine the quantity of interest on multiple resolutions with consistent geometry and forcing.

The discretization-reporting procedure of Celik et al. (2008) guides this assessment, but an uncertainty estimate requires additional systematic refinement runs. Conservation checks should include material volume and any transfers between model stages. Workflow checks should verify that the requested experiment was executed, including failed attempts and any repaired inputs. These shared requirements provide the basis for interpreting the results in Chapters 4–7.
