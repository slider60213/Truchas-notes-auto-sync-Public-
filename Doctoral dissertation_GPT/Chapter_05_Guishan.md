# 1. Chapter 5 Guishan Island Landslide and Tsunami Scenarios

## 1.1. Introduction

Guishan Island lies approximately 10 km offshore of the Yilan Plain in northeastern Taiwan. Its volcanic terrain and adjacent submarine slopes provide a setting in which flank instability can generate waves close to an inhabited coast. Geological and geophysical studies document the island's structural complexity and offshore mass movements (Huang, 2018; Deffontaines et al., 2022). The relevant hazard question is how the geometry and mobility of a plausible failure translate into a tsunami source. A mapped deposit is valuable evidence, but it records the outcome of mass transport rather than the complete acceleration and water-displacement history.

Deformable landslides introduce uncertainty beyond source volume and position. A material can deform, spread, and settle during motion, changing its coupling with the surrounding water. Bingham-type formulations provide a continuum description of this behavior. Three-dimensional developments within the Splash3D framework have examined rheological flows and slump-generated waves against analytical or laboratory benchmarks (Wu et al., 2020; Vuong et al., 2020). These studies motivate the use of rheology in source calculations. Their benchmark performance does not, however, establish the properties of an unobserved natural event.

The problem also spans different numerical scales. A three-dimensional source model can represent vertical motion and material deformation, whereas a regional shallow-water model can propagate a prescribed disturbance over a larger area. Transferring a surface snapshot between these models requires a consistent geographical transformation and an explicit treatment of the remaining source motion and momentum. Similarly, an imposed positive and negative displacement pattern is a scenario definition, not a measured failure trajectory. These distinctions affect how regional maxima should be interpreted.

This study addresses three connected questions. Which material configurations reproduce the broad MTD3 footprint? How do density and material-interface treatment change the simulated source behavior? How do a transferred surface field and idealized directional sources affect regional elevation patterns? We examine these questions through a sequence of source experiments and regional scenarios, retaining the distinction between deposit consistency and independent validation. The resulting interpretation emphasizes the mechanisms supported by the calculations and the uncertainties that limit reconstruction of a unique event.

## 1.2. Methods

### 1.2.1. Deposit geometry and source reconstruction

The geological framework follows the northern-flank investigation of Huang (2018), which used bathymetric and acoustic observations to distinguish mass transport deposits. The simulations focus on MTD3. Deposit thickness is subtracted from the contemporary bathymetry to approximate the substrate before deposition. This operation restores a candidate basal surface. It does not recover erosion during motion, the original distribution of all failed material, or changes unrelated to the modeled event.

The reconstructed source is defined from the difference between present terrain and an idealized cone centered on the island summit. The documented cone has a radius of 800 m and a height of 350 m. This is a geometric assumption necessitated by the absence of a complete pre-failure surface. The source volume used in the subsequent wave analysis is approximately 1.32 × 10⁷ m³. Coordinates are translated to place the summit at the horizontal origin and rotated clockwise by 30° so that the modeled opening faces the positive source-domain direction. Figure 5.1 illustrates the bathymetric reconstruction.

The initial source experiments use x = −1000 to 4000 m, y = −2000 to 3000 m, and z = −300 to 400 m. The documented uniform mesh comprises 100 × 100 × 70 cells, corresponding to spacings of 50, 50, and 10 m. The initial water surface is z = 0 m. The bottom is no-slip, the upper boundary has zero prescribed pressure, and lateral boundaries are free-slip walls. These boundaries and the coarse initial mesh constrain interpretation of late-time source motion and outgoing waves. The regional calculation is a separate stage and is not assigned this source-domain mesh.

### 1.2.2. Three-dimensional flow and material representation

Splash3D solves the incompressible multiphase Navier–Stokes equations using a finite-volume formulation. Material volume fractions describe the distribution of air, water, and mobile material. In compact notation, the governing conservation statements are

$$
∇·u = 0,
$$

$$
∂(ρu)/∂t + ∇·(ρu⊗u) = −∇p + ∇·τ + ρg,
$$

$$
∂fₘ/∂t + ∇·(fₘu) = 0.
$$

Here u is velocity, p is pressure, ρ is mixture density, τ is the modeled stress tensor, g is gravitational acceleration, and fₘ is the volume fraction of material m. Volume-of-fluid tracking follows the framework introduced by Hirt and Nichols (1981), with geometric interface reconstruction in the original source treatment. The project formulation uses large-eddy simulation with a Smagorinsky closure (Smagorinsky, 1963).

The discontinuous bi-viscous model, abbreviated DBM, distinguishes a high-viscosity branch below a strain-rate threshold from a yielded branch. A scalar representation is

$$
μ(γ̇) = μ_A for γ̇ < γ̇_y.
$$

$$
μ(γ̇) = μ_B + τ₀/γ̇ for γ̇ ≥ γ̇_y.
$$

The strain-rate invariant must be defined consistently with the stress tensor when implementing this relation. The discontinuous model permits the unyielded viscosity μ_A to be specified independently of the yielded-branch parameters. It should therefore be distinguished from a conventional bi-viscous regularization with a prescribed branch connection. The formulation and its numerical treatment are discussed by Wu et al. (2020).

Guishan Island samples collected on 17 June 2023 were measured with a rotational viscometer. Their measured stress–rate relationship did not follow a simple Newtonian or Bingham idealization, and the project used a fitted viscosity–rate curve for the sample-based configuration. We refer to this configuration as the sample-based rheological case, identified as DBM in the project results. This terminology does not imply that a continuous empirical fit is mathematically identical to the piecewise constitutive law. The precise implemented curve and its low-rate regularization require confirmation from the simulation inputs because the report's printed equation and figure annotation differ.

### 1.2.3. Sensitivity experiments and diagnostic quantities

Constant dynamic viscosities of 10⁻³, 10⁵, and 10⁸ Pa s bracket mobile, intermediate, and nearly immobile behavior. They are numerical sensitivity cases rather than independently measured material states. Material densities of 2000 and 4000 kg/m³ are compared. The higher density is an extreme sensitivity bound and is not presented as an estimate of the bulk density of the deposit.

Motion is compared at three visually identified stages: first spreading to the outer mapped MTD3 boundary, settling to approximately half the depth of the basal slope, and occupying the mapped deposit area. These stages describe different parts of the deformation process. The recorded times are snapshot-based descriptors, not observations of the historical event or formally estimated confidence intervals. Spatial agreement is evaluated from the mapped footprint and the simulated distribution (Fig. 5.2).

The third-year experiments compare the original DBM-PLIC treatment with a DBM-Diffused treatment at 2000 kg/m³. Fifteen virtual gauges occupy the combinations x = 1000, 1500, and 2000 m and y = −500, −250, 0, 250, and 500 m. The comparison uses surface-elevation timing and excursions. Because the diffuse treatment changes material fractions near the interface, a difference in an extracted water surface may include a measurement-definition effect as well as a dynamical effect.

### 1.2.4. Regional and directional scenarios

The regional calculations use COMCOT, a tsunami propagation and inundation model. In the transferred-field experiment, a Splash3D surface-elevation snapshot at t = 10 s is converted from Cartesian to geographical coordinates, geometrically aligned with the receiving bathymetry, and interpolated onto the regional grid. The documented procedure transfers elevation. A transfer of depth-integrated momentum has not been established in the available methodological record. The experiment is therefore interpreted as propagation from an imposed surface state rather than a fully demonstrated conservative coupling of two solvers.

A second experiment family places an idealized source at eight positions around the island: north, northeast, east, southeast, south, southwest, west, and northwest. The reported source dimensions are approximately 500 × 266 × 100 m, with the negative displacement directed landward and the positive displacement seaward. The geometrical product is 1.33 × 10⁷ m³, close to the nominal source volume but not exactly equal to it. This geometrical volume should not be equated automatically with the integral of a signed water-surface disturbance. These experiments assess sensitivity to source placement and orientation under prescribed geometry.

The regional figure ordinate identifies the output as maximum free-surface elevation. We retain that quantity when reporting regional maxima. It differs from crest-to-trough wave height, run-up above a coastal datum, and inland flow depth. No conversion among these quantities is assumed.

## 1.3. Results

### 1.3.1. Material mobility and deposit consistency

At 2000 kg/m³, the low-viscosity experiment spreads to the mapped boundary at approximately 35 s, reaches the intermediate settling stage at 90 s, and occupies the mapped area at 265 s. The sample-based rheological case reaches the same stages at approximately 35, 110, and 280 s (Table 5.1). Both reproduce the broad direction and eventual extent of the mapped deposit, despite their different constitutive descriptions.

The 10⁵ Pa s case evolves more slowly. Initial spreading occurs at approximately 75 s and intermediate settling at 440 s. Complete occupation of the mapped area is not recorded within 1000 s. At 10⁸ Pa s, no clear movement is recorded in the original source treatment over the diagnostic interval. This sequence supports a requirement for appreciable mobility within the tested reconstruction. It does not identify 10⁻³ Pa s as the physical viscosity of MTD3.

Raising density to 4000 kg/m³ changes the stages differently. For the sample-based case, initial spreading is delayed from 35 to 40 s, while intermediate settling advances from 110 to 70 s and footprint occupation advances from 280 to 150 s. The low-viscosity case exhibits the same pattern: the corresponding times change from 35, 90, and 265 s to 40, 65, and 165 s. Some material also extends beyond the mapped footprint. Density thus changes both timing and distribution. The results cannot be summarized adequately by saying that greater density accelerates every aspect of the motion.

Table 5.1. Snapshot-based stages of material motion.

| Configuration | Density kg/m³ | Boundary spreading s | Intermediate settling s | Footprint occupation s |
| --- | ---: | ---: | ---: | ---: |
| Constant 10⁻³ Pa s | 2000 | 35 | 90 | 265 |
| Constant 10⁻³ Pa s | 4000 | 40 | 65 | 165 |
| Constant 10⁵ Pa s | 2000 | 75 | 440 | >1000 |
| Constant 10⁵ Pa s | 4000 | 95 | 240 | 1000 |
| Constant 10⁸ Pa s | 2000 | No clear motion | No clear motion | No clear motion |
| Constant 10⁸ Pa s | 4000 | No clear motion | No clear motion | No clear motion |
| Sample-based case | 2000 | 35 | 110 | 280 |
| Sample-based case | 4000 | 40 | 70 | 150 |

### 1.3.2. Source-region surface response

The material enters the water near the reconstructed opening and spreads over the shallow portion of the slope before settling into deeper water. The source calculation shows an initial depression near the entry region and an outward positive disturbance. A later rebound at the source reaches approximately 30 m at about 175 s in the representative sequence. These values describe a local three-dimensional response and should not be substituted for a regional coastal maximum.

Across the density and rheology experiments, some gauge maxima reach approximately 50 m, particularly in high-density mobile configurations. These maxima belong to a different comparison from the representative 30 m rebound. The 2024 conference presentation also reports maxima under its own set of configurations. Combining these values without their densities, gauge definitions, and simulation stages would obscure the source dependence of the result.

With DBM-Diffused enabled, positive and negative surface excursions are generally reduced while their main timing remains similar to the DBM-PLIC results. The reduction is more apparent in the intermediate-viscosity comparison. In the highly viscous diffusive case, a gauge near the opening records a late disturbance after approximately 500 s, associated with material reaching the water-entry region. The source report notes that local water fractions may fall below the 0.5 criterion used to identify the surface. Consequently, the reduced gauge response cannot yet be attributed entirely to physical mixing or enhanced energy dissipation.

### 1.3.3. Regional elevations and source direction

The COMCOT experiment initialized from the three-dimensional snapshot produces a reported maximum of approximately 30 m in waters adjacent to the source and around 15 m in part of the island's northeastern coastal area. Selected island gauges reach approximately 9 m. These outputs have different spatial supports: a maximum over a mapped domain need not coincide with a maximum sampled at a limited set of gauges.

At the mainland reference stations, the plotted maximum surface elevations reach approximately 1.5 m along the Yilan coast, with smaller values at Hualien and Chenggong (Fig. 5.3). The regional plot supports a spatially variable coastal response rather than uniform attenuation with distance. Local bathymetry, source position, and wave propagation paths all contribute to this variation.

The eight idealized directional scenarios likewise produce strong spatial differences. Their largest island-adjacent values remain close to their imposed sources and are reported to exceed 40 m. Selected mainland stations reach elevations of order 1 m, with some regional maxima near 1.5 m. Because source location and orientation vary together, these experiments establish sensitivity to their combined configuration. They do not isolate an azimuth-only effect or demonstrate that direction dominates every other uncertain source parameter.

## 1.4. Discussion

### 1.4.1. What the deposit constrains

The mapped MTD3 footprint helps reject nearly immobile configurations within the adopted source geometry. Its main contribution is to constrain the eventual reach and direction of mobile material. Similar footprint occupation in the sample-based and low-viscosity cases shows that this constraint is insufficient to identify a unique constitutive relation. Different densities also alter the chronology without necessarily eliminating broad spatial agreement.

This non-uniqueness matters for tsunami reconstruction. Two sources can arrive at similar final deposits after displacing water at different rates. The present comparison therefore supports a family of mobile reconstructions. Stronger discrimination would require deposit-thickness residuals, mass-balance checks, source-geometry ensembles, and observations independent of the footprint used for comparison. A uniformly successful reconstruction of MTD3 thickness is not established by visual footprint agreement.

### 1.4.2. Interface and model-transfer uncertainty

The diffuse-interface comparison exposes a second uncertainty: the observable itself depends on how mixed cells are interpreted. If the gauge follows a selected volume-fraction isosurface, spreading the interface can move that isosurface without an equivalent change in a uniquely defined water boundary. Testing several thresholds, examining vertical water-fraction profiles, and checking material-volume conservation would help separate this effect from a change in the wave dynamics. A smaller extracted crest alone does not establish a more accurate source calculation.

The regional transfer introduces additional assumptions. At t = 10 s the landslide-generated disturbance is still evolving. An elevation-only initialization may omit momentum and later forcing. Geometrical scaling and rotation also need to preserve the intended length and amplitude units. Until those operations and the receiving grid are fully documented, the regional maxima should be treated as conditional scenario results. They identify potentially affected sectors but do not establish a calibrated inundation forecast.

### 1.4.3. Implications for scenario assessment

The useful outcome is a structured separation of uncertainties. Material behavior influences the source motion, interface treatment influences both dynamics and extracted surface elevations, and source placement influences regional patterns. These factors should be varied and evaluated with observables appropriate to each stage. No event probability, recurrence interval, or warning lead time can be assigned from the present scenario set alone.

For Guishan Island, the modeled contrast between strong local disturbances and lower but spatially variable mainland elevations motivates continued source investigation. The numerical values are conditional on the reconstructed geometry and imposed fields. Their practical use is to guide where improved bathymetry, deposit characterization, and source-transfer validation would most reduce uncertainty.

## 1.5. Conclusions

Within the adopted reconstruction, mobile constant-viscosity and sample-based rheological cases reproduce the broad MTD3 footprint, whereas the most viscous original-interface cases do not. Their similar final extent does not determine a unique material rheology. Increasing density delays initial lateral spreading but accelerates subsequent settling and footprint occupation in the mobile cases.

The diffusive material treatment generally reduces recorded surface excursions while retaining their main timing. The dependence of surface extraction on material fraction prevents interpreting this reduction solely as physical damping. Regional calculations produce selected Yilan maximum elevations approaching 1.5 m, and idealized source scenarios demonstrate sensitivity to combined location and orientation. These findings support conditional hazard scenarios and identify the measurements and numerical checks needed for a defensible historical reconstruction.


## 1.6. Figures


![Reconstructed substrate obtained by removing mapped MTD3 thickness](pics/G1_27.png)

Figure 5.1. Candidate substrate before MTD3 deposition. The mapped deposit thickness has been subtracted from the present bathymetry. The reconstruction supplies a modeling surface and does not independently determine the pre-failure flank geometry. Source: first-year research report, Figure 3-3.

![Material movement in the representative Guishan rheological configuration](pics/G3_55.png)

Figure 5.2. Simulated material movement in the representative rheological configuration. The outlined area denotes the mapped MTD3 distribution. Colors indicate modeled material elevation. Source: third-year research report, Figure 4-1.

![Regional maximum free-surface elevations from the transferred snapshot scenario](pics/G3_139.png)

Figure 5.3. Regional maximum free-surface elevations for the transferred-snapshot experiment. Gauge labels are retained from the source plot. This is a scenario output, not a record of observed coastal elevations. Source: third-year research report, Figure 4-15.
