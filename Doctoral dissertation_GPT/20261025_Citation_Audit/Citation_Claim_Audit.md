# Dissertation citation support after scope revision 25 October 2026

This record applies to the current dissertation. The two journal manuscripts and their citation audit are unchanged. Relevant full-text and body-passage checks are carried forward from the preceding audit; this scope edit does not represent a new full-text review.

## Scope and reference changes

Chapter 5 now covers three-dimensional landslide motion, deposit consistency, rheological and density sensitivity, interface treatment, and near-source surface response. Regional propagation, transferred-field initialization, directional source scenarios, associated elevations and the former Figure 5.3 have been removed throughout the dissertation. Five references whose sole use concerned those topics are excluded from the current bibliography; this is an author-requested scope change, not a finding that the publications are invalid.

Excluded in this revision: Abadie2012, Kirby2013, Lin2015, Lo2026, Lynett2002.

## Access levels

F: an accessible full article/report or author version was opened and relevant body sections reviewed. B: body passages were checked through an indexed full text or publisher preview without obtaining the complete file. A: abstract/metadata only. D: official technical documentation. Author versions and republications remain identified in the records below. These labels do not imply that every sentence of a full text was read.

{
  "original_audited_sources": 48,
  "dissertation_references": 37,
  "removed_from_dissertation_this_revision": 5,
  "access_levels_retained": {
    "B": 12,
    "F": 18,
    "D": 3,
    "A": 4
  },
  "revised_cited_paragraphs": 55,
  "revised_source_paragraph_pairs": 100
}

## Current sources and paragraph mappings

### Baykal2015 — Baykal et al. 2015

Baykal C, Sumer BM, Fuhrman DR, Jacobsen NG, Fredsøe J (2015) Numerical investigation of flow and scour around a vertical circular cylinder. Philosophical Transactions of the Royal Society A 373:20140104. https://doi.org/10.1098/rsta.2014.0104

Access level: B. Decision: revise.

Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC4275922/

Checked location: Indexed full-text Sections 2, 3 and 5; direct PMC view encountered a browser challenge

RANS k–omega hydrodynamics, separate bed/suspended load and morphological update for a vertical cylinder.

Keep as a transport–morphology alternative; do not describe it as LES, cohesive-bed rheology or Guandu validation.

- Chapter_02_Literature_Review.md — 2.1.1 Foundation geometry and flow structure — line 9: Baykal et al. (2015) examined flow and scour around a vertical circular cylinder with a model that represents sediment transport and bed morphology. This provides a useful contrast to the present rheological formulation. A transport model describes sediment fluxes and the resulting bed update, whereas a rheological continuum…

### Boettiger2015 — Boettiger 2015

Boettiger C (2015) An introduction to Docker for reproducible research. ACM SIGOPS Operating Systems Review 49:71–79. https://doi.org/10.1145/2723872.2723882

Access level: F. Decision: retain.

Source: https://arxiv.org/html/1410.0846

Checked location: Author preprint: Docker images, Dockerfiles, versioning, limitations

Dependency preservation and image archiving are explicit; the host kernel remains outside complete isolation.

The read version is the author preprint underlying the 2015 journal paper, not a verified identical journal PDF. Use only shared conceptual claims.

- Chapter_02_Literature_Review.md — 2.3.3 Containerized environments — line 95: Boettiger (2015) explains how container images support dependency preservation and reuse. Di Tommaso et al. (2017) combine containerized computation with an explicit workflow system. The latter work concerns bioinformatics, but the architectural distinction is applicable here: preserving the environment and preserving the sequence of operations are complementary. Neither…

- Chapter_06_Infrastructure.md — 6.7 Relation to reproducible workflow research — line 71: Container-based dependency preservation (Boettiger, 2015; Kurtzer et al., 2017) explains the portability objective of the migrated platform. Explicit workflow systems additionally preserve how computational steps depend on one another (Di Tommaso et al., 2017). The reported WSL2/LXD deployment addresses the environment layer; the recorded conversion, restart and extraction…

### Briaud1999 — Briaud et al. 1999

Briaud J-L, Ting F, Chen HC, Gudavilli R, Kwak K, Philogene B, Han S-W, Perugu S, Wei G, Nurtjahyo P, Cao Y, Li Y (1999) SRICOS: Prediction of Scour Rate at Bridge Piers. Report 2937-1, Texas Transportation Institute, Texas A&M University. https://library.ctr.utexas.edu/hostedpdfs/tti/2937-1.pdf

Access level: B. Decision: revise.

Source: https://library.ctr.utexas.edu/hostedpdfs/tti/2937-1.pdf

Checked location: Indexed report Chapters 1–3, especially Chapter 2; front-matter author list

SRICOS predicts scour versus time for cohesive soils and uses EFA erosion-rate measurements; laboratory erosion response differs from bulk rheometry.

Consolidate the duplicate EFA citation here. PDF endpoint opened but returned no text and screenshots failed; report body passages were obtained through the search index, not a full-file visual review.

- Chapter_02_Literature_Review.md — 2.1.3 Cohesive beds and protection systems — line 27: The SRICOS research program investigated scour rates in cohesive soils at bridge piers (Briaud et al., 1999). Its relevance here is that the rate and duration of erosion matter alongside a maximum depth. A constitutive representation of a cohesive bed must likewise be assessed over time. A simulated…

- Chapter_02_Literature_Review.md — 2.1.3 Cohesive beds and protection systems — line 33: Chapter 2 of the SRICOS report describes an erosion-rate-versus-hydraulic-shear measurement using the Erosion Function Apparatus (Briaud et al., 1999). This observable differs from bulk rheometry. Clear-water scour duration also depends on the test setting (Melville and Chiew, 1999); its uniform-sand, cylindrical-pier scope prevents direct adoption of a time-scale…

### Canonical2026 — Canonical 2026

Canonical (2026) Containers and VMs. LXD documentation, stable 5.21. Accessed 24 October 2026. https://documentation.ubuntu.com/lxd/en/stable-5.21/explanation/instances/

Access level: D. Decision: retain.

Source: https://canonical.com/lxd/docs/v5.21/explanation/instances/

Checked location: Containers and VMs; Application containers vs. system containers

System containers share the host kernel; VMs use their own kernel.

Architecture only; no inference about measured CFD speedup.

- Chapter_02_Literature_Review.md — 2.3.3 Containerized environments — line 91: Microsoft's WSL documentation distinguishes WSL1's translation-based architecture from WSL2's Linux kernel within a lightweight utility virtual machine (Microsoft, 2026). LXD documentation distinguishes system containers, which share the host kernel, from virtual machines with their own kernels (Canonical, 2026). In a WSL2/LXD arrangement, these mechanisms are layered. It is…

- Chapter_06_Infrastructure.md — 6.1 Deployment problem and design rationale — line 7: The migration strategy packages a compatible Linux userspace in LXD and operates it within WSL2. WSL2 supplies a Linux kernel in a utility virtual machine, while an LXD system container shares that kernel and isolates its userspace (Microsoft, 2026; Canonical, 2026). This arrangement allows Linux execution alongside a…

### Celik2008 — Celik et al. 2008

Celik IB, Ghia U, Roache PJ, Freitas CJ, Coleman H, Raad PE (2008) Procedure for estimation and reporting of uncertainty due to discretization in CFD applications. Journal of Fluids Engineering 130:078001. https://doi.org/10.1115/1.2960953

Access level: B. Decision: revise.

Source: https://citeseerx.ist.psu.edu/document?doi=b9db382f2350e5d948efc2ab11a5abfa3b1389b1&repid=rep1&type=pdf

Checked location: Indexed paper Preliminaries and recommended Richardson-extrapolation procedure; author-institution metadata

Iteration convergence and systematic spatial/time refinement precede a discretization error estimate.

Use as assessment guidance, not evidence that the current runs are grid converged; no GCI can be inferred from varying physical scenarios.

- Chapter_02_Literature_Review.md — 2.3.1 Physical validation and numerical consistency — line 77: Celik et al. (2008) describe how to estimate and report discretization uncertainty. Their procedure provides a separate line of evidence from comparison with field observations or a legacy executable. A numerical platform migration can reproduce the reference solution while retaining its discretization error. Conversely, a refined calculation can…

- Chapter_03_Methods.md — 3.6 Assessment hierarchy — line 133: The discretization-reporting procedure of Celik et al. (2008) guides this assessment, but an uncertainty estimate requires additional systematic refinement runs. Conservation checks should include material volume and the volume-fraction balance within each computational domain. Workflow checks should verify that the requested experiment was executed, including failed attempts and…

- Chapter_04_Guandu.md — 4.4.2 Limits of a rheological bed description — line 161: The discretization-uncertainty procedure of Celik et al. (2008) provides a basis for assessing minimum bed elevation and hole volume under refinement. The available scenario set is not such a refinement study; no numerical uncertainty interval can therefore be inferred from the spread among physical scenarios.…

- Chapter_05_Guishan.md — 5.2.1 Deposit geometry and source reconstruction — line 25: Spatial discretization uncertainty has not been quantified through a systematic refinement sequence of the type described by Celik et al. (2008).…

- Chapter_06_Infrastructure.md — 6.7 Relation to reproducible workflow research — line 71: Container-based dependency preservation (Boettiger, 2015; Kurtzer et al., 2017) explains the portability objective of the migrated platform. Explicit workflow systems additionally preserve how computational steps depend on one another (Di Tommaso et al., 2017). The reported WSL2/LXD deployment addresses the environment layer; the recorded conversion, restart and extraction…

### Deffontaines2022 — Deffontaines et al. 2022

Deffontaines B, Chang K-J, Huang P, Hsu H-H, Hsu S-K, Liu C-S, Lee C-T, Magalhaes S, Fortunato G (2022) Neotectonics of the volcanic Kuei-Shan Tao island, and geodynamic implications (NE Taiwan - SW Okinawa Trough). Tectonophysics 832:229362. https://doi.org/10.1016/j.tecto.2022.229362

Access level: F. Decision: revise.

Source: https://www.gep.ncu.edu.tw/storage/thesis/2022/2022%20Shu-Kun%20Hsu_Tec.pdf

Checked location: Sections 2 onward: geography, geological and morphostructural mapping; 17-page author-hosted article

Supports island position and structural/geomorphic setting; does not specify the simulated MTD3 rheology or the project cone.

Separate the structural-setting citation from Huang (2018) on offshore deposits; avoid a grouped citation implying both establish the same source reconstruction.

- Chapter_02_Literature_Review.md — 2.2.2 Source motion and observable deposits — line 53: Huang (2018) distinguishes offshore mass transport deposits and associates MTD2 with an initial flank collapse and MTD3 with a possible subsequent slope slump. Deffontaines et al. (2022) provide structural and geomorphic mapping of the island. The two sources support different parts of the geological setting. Neither specifies the…

- Chapter_05_Guishan.md — 5.1 Introduction — line 5: Guishan Island lies approximately 10 km offshore of the Yilan Plain in northeastern Taiwan. Deffontaines et al. (2022) document its structural and geomorphic setting. Huang (2018) interprets offshore deposits from bathymetric and acoustic data. These sources motivate investigating the link between failure geometry, material mobility and tsunami generation,…

### DiTommaso2017 — Di Tommaso et al. 2017

Di Tommaso P, Chatzou M, Floden EW, Prieto Barja P, Palumbo E, Notredame C (2017) Nextflow enables reproducible computational workflows. Nature Biotechnology 35:316–319. https://doi.org/10.1038/nbt.3820

Access level: F. Decision: retain.

Source: https://tcoffee.org/Courses/Exercises/2017_bologna_ma/biblio/nextflow2017.pdf

Checked location: Nextflow article on printed pages 316–319, especially task dependencies and Docker comparisons; distinguish adjacent Toil text

Workflow and container combination is documented in bioinformatics.

Architectural analogy only; no claim of Nextflow use or numerical CFD proof. Correct the family name Prieto Barja in the bibliography.

- Chapter_02_Literature_Review.md — 2.3.3 Containerized environments — line 95: Boettiger (2015) explains how container images support dependency preservation and reuse. Di Tommaso et al. (2017) combine containerized computation with an explicit workflow system. The latter work concerns bioinformatics, but the architectural distinction is applicable here: preserving the environment and preserving the sequence of operations are complementary. Neither…

- Chapter_06_Infrastructure.md — 6.7 Relation to reproducible workflow research — line 71: Container-based dependency preservation (Boettiger, 2015; Kurtzer et al., 2017) explains the portability objective of the migrated platform. Explicit workflow systems additionally preserve how computational steps depend on one another (Di Tommaso et al., 2017). The reported WSL2/LXD deployment addresses the environment layer; the recorded conversion, restart and extraction…

- Chapter_07_Agent_Workflows.md — 7.7 Comparison with published CFD assistance — line 91: CFDAgent provides an example of language-guided preprocessing, solver execution and post-processing (Xu et al., 2025). The accessible author preprint includes explicit user choices and confirmations of numerical settings, so the relevant comparison is interactive orchestration and demonstrated task coverage. Its sphere-flow checks do not establish autonomous recovery for…

### Frigaard2005 — Frigaard and Nouar 2005

Frigaard IA, Nouar C (2005) On the usage of viscosity regularisation methods for visco-plastic fluid flow computation. Journal of Non-Newtonian Fluid Mechanics 127:1–26. https://doi.org/10.1016/j.jnnfm.2005.01.003

Access level: B. Decision: revise.

Source: https://www.sciencedirect.com/science/article/pii/S0377025705000443

Checked location: Publisher article preview: introduction and outline of Sections 2–4; author-site attempt encountered browser verification

Examines regularization errors and physical fidelity for viscoplastic computations; does not specifically assess this laboratory’s discontinuous DBM.

Remove from the two short journal manuscripts; retain in dissertation as broader background with explicit non-transfer of its error conclusions.

- Chapter_02_Literature_Review.md — 2.2.1 Yield stress and continuum idealization — line 47: Huang and García (1998) analyze laminar Herschel–Bulkley mud flows and their runout/deposit dependence on shear thinning. This supplies a constitutive comparison for slope motion, not a turbulent bed-erosion law. Frigaard and Nouar (2005) discuss errors in viscosity-regularized viscoplastic computation more broadly. Their analysis does not directly establish the…

- Chapter_03_Methods.md — 3.4.1 Bingham and bi-viscous models — line 91: Frigaard and Nouar (2005) examine viscosity regularization more broadly; their results do not directly quantify error in this discontinuous law. The case-specific test is to vary numerical low-rate resistance while holding measured yielded parameters fixed. Herschel–Bulkley slope-flow theory supplies a separate constitutive alternative when shear thinning is supported…

### Grilli2019 — Grilli et al. 2019

Grilli ST, Tappin DR, Carey S, Watt SFL, Ward SN, Grilli AR, Engwell SL, Zhang C, Kirby JT, Schambach L, Muin M (2019) Modelling of the tsunami from the December 22, 2018 lateral collapse of Anak Krakatau volcano in the Sunda Straits, Indonesia. Scientific Reports 9:11946. https://doi.org/10.1038/s41598-019-48327-6

Access level: F. Decision: retain.

Source: https://www.nature.com/articles/s41598-019-48327-6

Checked location: Results on collapse geometry/rheologies and Methods on NHWAVE/FUNWAVE-TVD

Uses pre-/post-event geometry and observed tsunami records; source material is granular or a dense Newtonian fluid.

Supports comparison of evidential settings, not proof that either rheology is uniquely recovered or that Guishan is validated.

- Chapter_02_Literature_Review.md — 2.2.2 Source motion and observable deposits — line 59: Grilli et al. (2019) compare granular and dense-fluid source descriptions for Anak Krakatau using collapse geometry and observed tsunami records. Haridhi et al. (2023) instead construct conditional offshore-Sumatra scenarios from geophysical interpretation and slope-stability screening, with some material/loading assumptions. These examples distinguish an observed-event reconstruction from a potential-source…

- Chapter_05_Guishan.md — 5.1 Introduction — line 7: The 2018 Anak Krakatau collapse demonstrates the value of combining pre- and post-failure geometry with coastal wave observations (Grilli et al., 2019). Offshore northern Sumatra, geophysical mapping and slope-stability analysis inform conditional source scenarios, with some subsurface properties assumed (Haridhi et al., 2023). The kinematic synthesis of Løvholt…

### Haridhi2023 — Haridhi et al. 2023

Haridhi HA, Huang B-S, Wen K-L, Mirza A, Rizal S, Purnawan S, Fajri I, Klingelhoefer F, Liu C-S, Lee C-S, Wilson CR, Wu T-R, Setiawan I, Phung VB (2023) Tsunami scenario triggered by a submarine landslide offshore of northern Sumatra Island and its hazard assessment. Natural Hazards and Earth System Sciences 23:507–523. https://doi.org/10.5194/nhess-23-507-2023

Access level: F. Decision: revise.

Source: https://nhess.copernicus.org/articles/23/507/2023/

Checked location: Sections 3.1–3.4 and 4, particularly assumed subsurface parameters in 3.3

Geophysical mapping and slope-stability screening define conditional source locations; several strength/loading parameters are assumed.

Say geologically informed conditional scenarios, not independently measured or fully constrained failure properties.

- Chapter_02_Literature_Review.md — 2.2.2 Source motion and observable deposits — line 59: Grilli et al. (2019) compare granular and dense-fluid source descriptions for Anak Krakatau using collapse geometry and observed tsunami records. Haridhi et al. (2023) instead construct conditional offshore-Sumatra scenarios from geophysical interpretation and slope-stability screening, with some material/loading assumptions. These examples distinguish an observed-event reconstruction from a potential-source…

- Chapter_05_Guishan.md — 5.1 Introduction — line 7: The 2018 Anak Krakatau collapse demonstrates the value of combining pre- and post-failure geometry with coastal wave observations (Grilli et al., 2019). Offshore northern Sumatra, geophysical mapping and slope-stability analysis inform conditional source scenarios, with some subsurface properties assumed (Haridhi et al., 2023). The kinematic synthesis of Løvholt…

### Hirt1981 — Hirt and Nichols 1981

Hirt CW, Nichols BD (1981) Volume of fluid (VOF) method for the dynamics of free boundaries. Journal of Computational Physics 39:201–225. https://doi.org/10.1016/0021-9991(81)90145-5

Access level: B. Decision: revise.

Source: https://dcwan.sjtu.edu.cn/PlugIns/ckfinder/userfiles/files/Hirt%20%E5%92%8C%20Nichols%20-%201981%20-%20Volume%20of%20fluid%20%28VOF%29%20method%20for%20the%20dynamics%20of%20f%281%29.pdf

Checked location: Indexed original-paper conclusion p.224; numerical lineage cross-checked in Liu et al. (2005), Section 2.2

Supports the fractional-volume VOF concept.

Do not attribute the particular later PLIC reconstruction or laboratory diffused interface to this 1981 reference.

- Chapter_02_Literature_Review.md — 2.2.3 Interfaces and near-source surface diagnostics — line 63: Hirt and Nichols (1981) introduced the fractional-volume basis of the volume-of-fluid method for tracking free boundaries. In the present multiphase application, material fractions also define the distribution of mobile sediment or landslide material. Geometrical interface reconstruction and a diffusive material treatment can produce different local fraction profiles. The…

- Chapter_03_Methods.md — 3.2.2 Finite volumes and geometric reconstruction — line 43: The VOF approach represents an interface through partial cell occupancy (Hirt and Nichols, 1981). The later PLIC implementation in this numerical lineage is described by Liu et al. (2005, Sect. 2.2). In a geometrical PLIC reconstruction, an interface cell contains a plane whose orientation is inferred from the…

- Chapter_04_Guandu.md — 4.2.1 Hydrodynamics and rheology — line 33: The model uses the laboratory-developed Splash3D framework, derived from Truchas, to solve three-dimensional incompressible flow. Finite-volume discretization is combined with volume-of-fluid tracking of the material interfaces (Hirt and Nichols, 1981). The project formulation includes large-eddy simulation with a Smagorinsky closure (Smagorinsky, 1963). The governing equations can be written…

- Chapter_05_Guishan.md — 5.2.2 Three-dimensional flow and material representation — line 43: Here u is velocity, p is pressure, ρ is mixture density, τ is the modeled stress tensor, g is gravitational acceleration, and fₘ is the volume fraction of material m. The fractional-volume interface description follows the VOF concept of Hirt and Nichols (1981). The later PLIC reconstruction is…

### Huang2018 — Huang 2018

Huang P-C (2018) A mass failure in the northern flank of the Kueishantao Island off northeastern Taiwan: Volcanic flank collapse and submarine landslides. Master's thesis, National Central University. https://ir.lib.ncu.edu.tw/handle/987654321/75883

Access level: A. Decision: revise.

Source: https://ir.lib.ncu.edu.tw/handle/987654321/75883?locale=en-US

Checked location: Author-institution bilingual abstract; catalogue lists an index.html link, not an obtained thesis PDF

Distinguishes MTD2 as associated with initial flank collapse and MTD3 as a possible later slope-slump deposit.

Retain this indispensable local source with access limit disclosed; the project cone is a new modeling assumption, not a reconstruction established by the thesis. No unviewed thesis figure/page is claimed.

- Chapter_02_Literature_Review.md — 2.2.2 Source motion and observable deposits — line 53: Huang (2018) distinguishes offshore mass transport deposits and associates MTD2 with an initial flank collapse and MTD3 with a possible subsequent slope slump. Deffontaines et al. (2022) provide structural and geomorphic mapping of the island. The two sources support different parts of the geological setting. Neither specifies the…

- Chapter_05_Guishan.md — 5.1 Introduction — line 5: Guishan Island lies approximately 10 km offshore of the Yilan Plain in northeastern Taiwan. Deffontaines et al. (2022) document its structural and geomorphic setting. Huang (2018) interprets offshore deposits from bathymetric and acoustic data. These sources motivate investigating the link between failure geometry, material mobility and tsunami generation,…

- Chapter_05_Guishan.md — 5.2.1 Deposit geometry and source reconstruction — line 19: Huang (2018) associates MTD2 with an initial flank collapse and MTD3 with a possible subsequent slope slump. We focus on MTD3 and subtract its mapped thickness from present bathymetry to approximate the substrate before deposition. The conical restoration described below is an additional project assumption; it is not…

### HuangGarcia1998 — Huang and García 1998

Huang X, García MH (1998) A Herschel–Bulkley model for mud flow down a slope. Journal of Fluid Mechanics 374:305–333. https://doi.org/10.1017/S0022112098002845

Access level: B. Decision: revise.

Source: https://electronicsandbooks.com/edt/manual/Magazine/J/Journal%20of%20Fluid%20Mechanics/1998%20Volume%20374/S0022112098002845.pdf

Checked location: Indexed original-paper concluding discussion, printed p.329; author-institution abstract

Low-Reynolds-number laminar slope-flow theory and experiments show shear-thinning dependence of runout/deposit form.

Retain for Guishan constitutive alternatives and dissertation; remove the generic mud-flow analogy from Guandu. Do not treat the paper as a turbulent cohesive-bed erosion law.

- Chapter_02_Literature_Review.md — 2.2.1 Yield stress and continuum idealization — line 47: Huang and García (1998) analyze laminar Herschel–Bulkley mud flows and their runout/deposit dependence on shear thinning. This supplies a constitutive comparison for slope motion, not a turbulent bed-erosion law. Frigaard and Nouar (2005) discuss errors in viscosity-regularized viscoplastic computation more broadly. Their analysis does not directly establish the…

- Chapter_03_Methods.md — 3.4.1 Bingham and bi-viscous models — line 91: Frigaard and Nouar (2005) examine viscosity regularization more broadly; their results do not directly quantify error in this discontinuous law. The case-specific test is to vary numerical low-rate resistance while holding measured yielded parameters fixed. Herschel–Bulkley slope-flow theory supplies a separate constitutive alternative when shear thinning is supported…

- Chapter_05_Guishan.md — 5.2.2 Three-dimensional flow and material representation — line 57: For low-Reynolds-number laminar slope flows, Huang and García (1998) show that shear thinning can change runout and deposit form. This motivates testing constitutive alternatives when supported by sample data, but does not establish an erosion law or parameter set for Guishan material.…

### Huang2024 — Huang et al. 2024

Huang Y-X, Wu T-R, Hu S-K, Chu C-R, Wang C-Y, Zhou C (2024) A novel rigid-fluid method for landslide tsunami modeling. Physics of Fluids 36:127127. https://doi.org/10.1063/5.0235710

Access level: A. Decision: revise.

Source: https://doi.org/10.1063/5.0235710

Checked location: Publisher abstract, metadata and preview Figure captions; author/repository searches did not yield complete text

Publication and broad RFM capability are confirmed; detailed numerical and validation passages were not obtained.

Retain only concise method-lineage statements in dissertation; remove from deformable-source article. Do not claim quantitative benchmark accuracy or mixed RFM–DBM validation.

- Chapter_01_Introduction.md — 1.1 Physical modeling and computational continuity — line 13: The physical modeling builds on published rheological landslide work (Wu et al., 2020; Vuong et al., 2020), DBM scour applications (Vuong et al., 2023, 2024; Lin et al., 2024), and the rigid-fluid method (Huang et al., 2024). These establish the platform capabilities that the dissertation applies and preserves.…

- Chapter_02_Literature_Review.md — 2.2.2 Source motion and observable deposits — line 57: Liu et al. (2005) describe an experimental program with wedges and a hemisphere, but their published numerical comparisons are for wedge-shaped slides. Their Section 2.2 documents the VOF/PLIC and moving-boundary lineage. Later publications report two-way moving-solid coupling (Wu et al., 2014a) and RFM (Huang et al., 2024). These…

- Chapter_03_Methods.md — 3.1 Model lineage and scope — line 7: Wu et al. (2020) document the laboratory adaptation from Truchas to Splash3D and its rheological extensions. Later DBM applications include offshore-foundation scour (Vuong et al., 2023) and Shuang-Yuan Bridge scenarios (Vuong et al., 2024). Moving-solid publications provide a separate branch of that lineage (Wu et al., 2014a; Huang…

- Chapter_03_Methods.md — 3.4.3 Moving bodies and mixed failure — line 103: Huang et al. (2024) report RFM coupled to Splash3D, following earlier two-way moving-solid work by Wu et al. (2014a). These provide the moving-body background for a possible mixed-failure model. The qualification presentation identifies combined RFM–DBM simulation as planned work; separate published modules do not by themselves establish the…

### Kurtzer2017 — Kurtzer et al. 2017

Kurtzer GM, Sochat V, Bauer MW (2017) Singularity: Scientific containers for mobility of compute. PLOS ONE 12:e0177459. https://doi.org/10.1371/journal.pone.0177459

Access level: F. Decision: retain.

Source: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0177459

Checked location: Mobility of compute and Reproducibility subsections

Images preserve userspace/software stacks; shared host kernel remains relevant.

No inference that an image alone proves physical validity or identical performance.

- Chapter_02_Literature_Review.md — 2.3.3 Containerized environments — line 89: Kurtzer et al. (2017) describe scientific containers as a means of moving a computational environment between resources. The relevance to legacy modeling is dependency preservation: a container can retain a compatible userspace and software stack. Portability of that stack remains distinct from scalability and from numerical equivalence after…

- Chapter_06_Infrastructure.md — 6.7 Relation to reproducible workflow research — line 71: Container-based dependency preservation (Boettiger, 2015; Kurtzer et al., 2017) explains the portability objective of the migrated platform. Explicit workflow systems additionally preserve how computational steps depend on one another (Di Tommaso et al., 2017). The reported WSL2/LXD deployment addresses the environment layer; the recorded conversion, restart and extraction…

### LANL2026 — LANL 2026

LANL (2026) Truchas 3D Multiphysics Simulation of Metal Casting and Processing. Los Alamos National Laboratory project repository. Accessed 24 October 2026. https://github.com/lanl/truchas

Access level: D. Decision: retain.

Source: https://github.com/lanl/truchas

Checked location: Repository About/README description

Current project describes metal-casting and processing multiphysics.

Use only for current upstream identity; historical Splash3D lineage is supported separately by Wu et al. (2020).

- Chapter_03_Methods.md — 3.1 Model lineage and scope — line 5: The numerical platform originates from the Truchas code developed at Los Alamos National Laboratory. The current upstream project describes a multiphysics platform oriented toward manufacturing processes (LANL, 2026). The laboratory's Splash3D development adapted an earlier Truchas framework for free-surface hydrodynamics, turbulence, and coastal applications. Subsequent laboratory versions include…

### Lin2024 — Lin et al. 2024

Lin P-J, Wu T-R, Lin J-P, Chuang M-H, Huang Y-X, Chu J-J (2024) Using the discontinuous bi-viscosity model to analyze the three-dimensional flow field and local scour behavior around Claviaster libycus (Echinodermata, Echinoidea). Journal of Mechanics 40:223–238. https://doi.org/10.1093/jom/ufae019

Access level: F. Decision: revise.

Source: https://academic.oup.com/jom/article/doi/10.1093/jom/ufae019/7680005

Checked location: Sections 3.2, 3.3, 4 and 6, especially explicit experimental/numerical depths

Qualitative scour-pattern comparisons coexist with local depth overprediction; experiments use dam-break flow and sand around a sphere/test.

Replace unqualified cross-geometry validation language with the documented depth discrepancy. The source is not a cohesive Guandu field calibration.

- Chapter_01_Introduction.md — 1.1 Physical modeling and computational continuity — line 13: The physical modeling builds on published rheological landslide work (Wu et al., 2020; Vuong et al., 2020), DBM scour applications (Vuong et al., 2023, 2024; Lin et al., 2024), and the rigid-fluid method (Huang et al., 2024). These establish the platform capabilities that the dissertation applies and preserves.…

- Chapter_02_Literature_Review.md — 2.1.3 Cohesive beds and protection systems — line 35: DBM has been applied to offshore turbine foundations under waves and current (Vuong et al., 2023). Its use across geometries should not be equated with uniform quantitative accuracy. Lin et al. (2024, Sect. 3.2) report similar scour patterns around a sphere but overestimate several local depths in a…

- Chapter_04_Guandu.md — 4.4.2 Limits of a rheological bed description — line 159: A useful caution comes from Lin et al. (2024, Sect. 3.2): their DBM sphere-scour comparison reports similar patterns but overestimates several local depths. Thus, qualitative agreement of the Guandu hole shape should be assessed separately from agreement in depth.…

### LiuMei1989 — Liu and Mei 1989

Liu KF, Mei CC (1989) Slow spreading of a sheet of Bingham fluid on an inclined plane. Journal of Fluid Mechanics 207:505–529. https://doi.org/10.1017/S0022112089002685

Access level: B. Decision: revise.

Source: https://www.lmm.jussieu.fr/~lagree/COURS/MFEnv/mainM2EMN.pdf

Checked location: Indexed original-paper Section 2, shallow-layer approximation and equations 2.1–2.2; original publisher abstract

Slow thin Bingham sheet under lubrication assumptions; hydrostatic pressure and limited flow regime.

State slow-flow/slope scope. The analytical problem cannot validate turbulent bridge erosion.

- Chapter_02_Literature_Review.md — 2.2.1 Yield stress and continuum idealization — line 41: Liu and Mei (1989) analyzed the slow spreading of a Bingham-fluid sheet on an inclined plane. Their formulation illustrates how finite yield stress changes the relation between forcing, motion, and final shape. It also identifies a controlled setting in which a constitutive idealization can be evaluated. Transferring such…

### Liu2005 — Liu et al. 2005

Liu PL-F, Wu T-R, Raichlen F, Synolakis CE, Borrero JC (2005) Runup and rundown generated by three-dimensional sliding masses. Journal of Fluid Mechanics 536:107–144. https://doi.org/10.1017/S0022112005004799

Access level: F. Decision: revise.

Source: https://www1.udel.edu/kirby/landslide/problems/benchmark_3/liu-etal-jfm05.pdf

Checked location: Sections 2.1–2.2 and numerical/laboratory comparisons; 38-page original article

LES/VOF free-surface numerical lineage; experimental program has wedges and a hemisphere but numerical comparisons reported are for wedges.

Retain source-generation lineage and specify wedge-only numerical validation in dissertation. Do not imply all experimental bodies were numerically validated.

- Chapter_02_Literature_Review.md — 2.2.2 Source motion and observable deposits — line 57: Liu et al. (2005) describe an experimental program with wedges and a hemisphere, but their published numerical comparisons are for wedge-shaped slides. Their Section 2.2 documents the VOF/PLIC and moving-boundary lineage. Later publications report two-way moving-solid coupling (Wu et al., 2014a) and RFM (Huang et al., 2024). These…

- Chapter_03_Methods.md — 3.2.2 Finite volumes and geometric reconstruction — line 43: The VOF approach represents an interface through partial cell occupancy (Hirt and Nichols, 1981). The later PLIC implementation in this numerical lineage is described by Liu et al. (2005, Sect. 2.2). In a geometrical PLIC reconstruction, an interface cell contains a plane whose orientation is inferred from the…

- Chapter_05_Guishan.md — 5.1 Introduction — line 11: Laboratory wave-generation work provides controlled comparisons for three-dimensional sliding masses (Liu et al., 2005). Those rigid-slide cases are useful hydrodynamic benchmarks, whereas the present source experiments concern deformable material.…

- Chapter_05_Guishan.md — 5.2.2 Three-dimensional flow and material representation — line 43: Here u is velocity, p is pressure, ρ is mixture density, τ is the modeled stress tensor, g is gravitational acceleration, and fₘ is the volume fraction of material m. The fractional-volume interface description follows the VOF concept of Hirt and Nichols (1981). The later PLIC reconstruction is…

### Lovholt2015 — Løvholt et al. 2015

Løvholt F, Pedersen G, Harbitz CB, Glimsdal S, Kim J (2015) On the characteristics of landslide tsunamis. Philosophical Transactions of the Royal Society A 373:20140376. https://doi.org/10.1098/rsta.2014.0376

Access level: B. Decision: revise.

Source: https://ngi.brage.unit.no/ngi-xmlui/bitstream/11250/2374680/3/20140376.full.pdf

Checked location: Indexed author-hosted review; kinematic synthesis and abstract; complete-file fetch failed

Acceleration and velocity roles depend on slide type; one deformable example has only a weak deformation effect.

Avoid a universal claim that deformation controls generation; identify the conditional nature and distinguish synthesis from a new field validation.

- Chapter_02_Literature_Review.md — 2.2.3 Interfaces and near-source surface diagnostics — line 67: The kinematic review of Løvholt et al. (2015) distinguishes acceleration- and velocity-related controls by movement type and does not establish a universal dominance of deformation. Source assessment therefore requires both material-motion histories and the generated surface response; a final deposit outline alone cannot identify the wave-generation history.…

- Chapter_05_Guishan.md — 5.1 Introduction — line 7: The 2018 Anak Krakatau collapse demonstrates the value of combining pre- and post-failure geometry with coastal wave observations (Grilli et al., 2019). Offshore northern Sumatra, geophysical mapping and slope-stability analysis inform conditional source scenarios, with some subsurface properties assumed (Haridhi et al., 2023). The kinematic synthesis of Løvholt…

### Melville1999 — Melville and Chiew 1999

Melville BW, Chiew Y-M (1999) Time scale for local scour at bridge piers. Journal of Hydraulic Engineering 125:59–65. https://doi.org/10.1061/(ASCE)0733-9429(1999)125:1(59)

Access level: A. Decision: retain.

Source: https://ascelibrary.org/doi/10.1061/%28ASCE%290733-9429%281999%29125%3A1%2859%29

Checked location: Publisher abstract; publisher/PDF and author-repository searches

Duration dependence is explicitly limited to cylindrical piers in uniform sand under clear-water conditions.

Only the qualitative duration point is retained; no time-scale equation or quantitative application to Guandu is made.

- Chapter_02_Literature_Review.md — 2.1.3 Cohesive beds and protection systems — line 33: Chapter 2 of the SRICOS report describes an erosion-rate-versus-hydraulic-shear measurement using the Erosion Function Apparatus (Briaud et al., 1999). This observable differs from bulk rheometry. Clear-water scour duration also depends on the test setting (Melville and Chiew, 1999); its uniform-sand, cylindrical-pier scope prevents direct adoption of a time-scale…

- Chapter_04_Guandu.md — 4.4.1 Boundary realism and the meaning of validation — line 153: The tidal versus unidirectional comparison of Yu et al. (2023) concerns a different foundation and sediment setup, but supports treating forcing history as part of a scour comparison. Melville and Chiew (1999) likewise identify duration dependence for clear-water cylindrical-pier scour in uniform sand. The present fixed-direction runs do…

### Microsoft2026 — Microsoft 2026

Microsoft (2026) Comparing WSL Versions. Microsoft Learn. Accessed 24 October 2026. https://learn.microsoft.com/en-gb/windows/wsl/compare-versions

Access level: D. Decision: retain.

Source: https://learn.microsoft.com/en-gb/windows/wsl/compare-versions

Checked location: Comparing WSL 1 and WSL 2; features and lightweight utility VM description

WSL2 uses an actual Linux kernel inside a managed lightweight VM.

Architecture only; preserve measured-platform benchmark qualifications.

- Chapter_02_Literature_Review.md — 2.3.3 Containerized environments — line 91: Microsoft's WSL documentation distinguishes WSL1's translation-based architecture from WSL2's Linux kernel within a lightweight utility virtual machine (Microsoft, 2026). LXD documentation distinguishes system containers, which share the host kernel, from virtual machines with their own kernels (Canonical, 2026). In a WSL2/LXD arrangement, these mechanisms are layered. It is…

- Chapter_06_Infrastructure.md — 6.1 Deployment problem and design rationale — line 7: The migration strategy packages a compatible Linux userspace in LXD and operates it within WSL2. WSL2 supplies a Linux kernel in a utility virtual machine, while an LXD system container shares that kernel and isolates its userspace (Microsoft, 2026; Canonical, 2026). This arrangement allows Linux execution alongside a…

### Peng2026 — Peng et al. 2026

Peng C, Liu J, Qi W-G, Chen H-B, Hu C-Q (2026) Combined effects of altered hydrodynamics and skew angles on scour around a complex cap pile group foundation. Ocean Engineering 354:125007. https://doi.org/10.1016/j.oceaneng.2026.125007

Access level: B. Decision: revise.

Source: https://www.sciencedirect.com/science/article/pii/S0029801826008413

Checked location: Publisher preview introduction, abstract and conclusions; complete article not obtained

Combined hydraulic changes and skew of 0 and 5 degrees in a cap–pile-group configuration above the cap lower edge.

Retain a qualitative example with its specific geometry/exposure scope. Do not derive an angle correction or universal worst angle.

- Chapter_02_Literature_Review.md — 2.1.2 Tidal boundaries and field assessment — line 23: Yu et al. (2023) use foundation geometry and tidal observations from the Hong Kong–Zhuhai–Macao Bridge to define flume experiments. Peng et al. (2026) examine changes in depth, velocity and skew for a cap–pile-group foundation under a particular cap-exposure condition. These study designs motivate retaining forcing history and foundation…

- Chapter_04_Guandu.md — Chapter 4 Guandu Bridge Flow and Local Scour — line 5: The DBM precedent of Vuong et al. (2024) concerns Shuang-Yuan Bridge. This chapter assesses Guandu-specific observations and scenarios, with site-informed tidal experiments (Yu et al., 2023) and geometry–hydrodynamics comparisons (Peng et al., 2026) providing external context.…

### Roulund2005 — Roulund et al. 2005

Roulund A, Sumer BM, Fredsøe J, Michelsen J (2005) Numerical and experimental investigation of flow and scour around a circular pile. Journal of Fluid Mechanics 534:351–401. https://doi.org/10.1017/S0022112005004507

Access level: B. Decision: retain.

Source: https://electronicsandbooks.com/edt/manual/Magazine/J/Journal%20of%20Fluid%20Mechanics/2005%20Volume%20534/S0022112005004507.pdf

Checked location: Indexed original-paper Section 5.1, rigid-bed validation and Figure 10; publisher metadata

Separate comparisons of velocity, pressure and bed shear stress around a circular pile; model does not capture every measured circulation feature.

Supports assessing flow and scour separately, not direct validation of a complex estuarine foundation.

- Chapter_02_Literature_Review.md — 2.1.1 Foundation geometry and flow structure — line 7: Local scour is a coupled response of the flow and the bed around an obstruction. Downflow, separation, and wake motion redistribute the forcing near a foundation, while the developing hole changes the subsequent flow. Roulund et al. (2005) combined numerical and experimental investigation around a circular pile, providing…

### Sandve2013 — Sandve et al. 2013

Sandve GK, Nekrutenko A, Taylor J, Hovig E (2013) Ten simple rules for reproducible computational research. PLOS Computational Biology 9:e1003285. https://doi.org/10.1371/journal.pcbi.1003285

Access level: F. Decision: retain.

Source: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285

Checked location: Rules 1–7, including exact inputs, versions, intermediate results and raw data

Supports workflow provenance and reproducibility practices.

These are methodological recommendations, not evidence that the local records already meet them.

- Chapter_02_Literature_Review.md — 2.3.2 Preserving the computational experiment — line 81: Sandve et al. (2013) emphasize tracking the steps that produce a computational result, including software versions, parameters, and transformations. Wilson et al. (2014) discuss practices such as version control, modular organization, and automated checks that improve scientific software development. The common implication for this dissertation is that the…

### Smagorinsky1963 — Smagorinsky 1963

Smagorinsky J (1963) General circulation experiments with the primitive equations. I. The basic experiment. Monthly Weather Review 91:99–164. https://doi.org/10.1175/1520-0493(1963)091%3C0099:GCEWTP%3E2.3.CO;2

Access level: F. Decision: revise.

Source: https://gibbs.science/les/handouts/smagorinsky_1963.pdf

Checked location: Section 4, Small-Scale Eddy Diffusion; printed pp.103 onward; grid-scale deformation discussion on p.150

Original strain-related subgrid diffusion in an atmospheric model.

Keep historical origin; cite the later Splash3D papers for the actual three-dimensional closure notation and coefficient.

- Chapter_03_Methods.md — 3.3.1 Large eddy simulation — line 51: The closure has its historical origin in strain-related subgrid diffusion (Smagorinsky, 1963). The three-dimensional Splash3D notation below follows the later formulation in Wu et al. (2020) and Vuong et al. (2024), rather than attributing the complete current implementation to the atmospheric paper. The eddy viscosity is written as…

- Chapter_04_Guandu.md — 4.2.1 Hydrodynamics and rheology — line 33: The model uses the laboratory-developed Splash3D framework, derived from Truchas, to solve three-dimensional incompressible flow. Finite-volume discretization is combined with volume-of-fluid tracking of the material interfaces (Hirt and Nichols, 1981). The project formulation includes large-eddy simulation with a Smagorinsky closure (Smagorinsky, 1963). The governing equations can be written…

- Chapter_05_Guishan.md — 5.2.2 Three-dimensional flow and material representation — line 43: Here u is velocity, p is pressure, ρ is mixture density, τ is the modeled stress tensor, g is gravitational acceleration, and fₘ is the volume fraction of material m. The fractional-volume interface description follows the VOF concept of Hirt and Nichols (1981). The later PLIC reconstruction is…

### Suaznabar2017 — Suaznabar et al. 2017

Suaznabar O, Bojanowski C, Lottes SA, Shen J, Kerenyi K, Kilgore R (2017) Advanced Methodology to Assess Riprap Rock Stability at Bridge Piers and Abutments. FHWA-HRT-17-054, Federal Highway Administration. https://www.fhwa.dot.gov/publications/research/infrastructure/structures/bridge/17054/index.cfm

Access level: F. Decision: retain.

Source: https://www.fhwa.dot.gov/publications/research/infrastructure/structures/bridge/17054/001.cfm

Checked location: Full report HTML Chapter 1 and stated CFD/CSM coupling objectives

Riprap movement is an FSI problem distinct from erosion around an immobile protective shape.

Supports that distinction; it does not establish movement thresholds for the fixed P7 geometry.

- Chapter_02_Literature_Review.md — 2.1.3 Cohesive beds and protection systems — line 29: Protection adds another class of mechanics. Suaznabar et al. (2017) developed a computational approach to assess riprap-rock stability using fluid–structure interaction and laboratory assessment. This addresses a different observable from scour around a fixed protective shape. The latter can diagnose how the prescribed shape redirects flow, but cannot…

- Chapter_04_Guandu.md — 4.4.3 Implications for protection and monitoring — line 169: The fixed-riprap experiments indicate a local redistribution of exposure. They support examining the interaction between protection geometry and the surrounding foundation rather than assessing protection solely by its footprint. They do not resolve porous flow or armour movement. Assessment of rock stability requires an additional mechanical problem, as…

### Vuong2024 — Vuong et al. 2024

Vuong T-H-N, Wu T-R, Huang Y-X, Chu C-R, Wang C-Y, Le T-L (2024) Numerical study of local scour and hydrodynamic pressure of complex bridge piers. Results in Engineering 24:103533. https://doi.org/10.1016/j.rineng.2024.103533

Access level: F. Decision: revise.

Source: https://www.researchgate.net/publication/386097143_Numerical_Study_of_Local_Scour_and_Hydrodynamic_Pressure_of_Complex_Bridge_Piers

Checked location: Author-uploaded article Sections 2.2, 3, 4.1; equation 5 and Figures 5–9

DBM law; pipeline-scour laboratory benchmark; six-/ten-pile Shuang-Yuan Bridge scenarios with an initial bed at −13 m and inflow 8 m/s.

Name the actual bridge and distinguish the benchmark from a Guandu cohesive-bed calibration. Remove the earlier abstract-only uncertainty over the site identity.

- Chapter_01_Introduction.md — 1.1 Physical modeling and computational continuity — line 13: The physical modeling builds on published rheological landslide work (Wu et al., 2020; Vuong et al., 2020), DBM scour applications (Vuong et al., 2023, 2024; Lin et al., 2024), and the rigid-fluid method (Huang et al., 2024). These establish the platform capabilities that the dissertation applies and preserves.…

- Chapter_02_Literature_Review.md — 2.1.1 Foundation geometry and flow structure — line 13: For complex foundations, Vuong et al. (2024) compare original six-pile and extended ten-pile arrangements of Shuang-Yuan Bridge. Their DBM implementation is first compared with a pipeline-scour experiment, then applied to the bridge scenarios. These are separate tests of a formulation and an application. They establish prior complex-foundation DBM…

- Chapter_03_Methods.md — 3.1 Model lineage and scope — line 7: Wu et al. (2020) document the laboratory adaptation from Truchas to Splash3D and its rheological extensions. Later DBM applications include offshore-foundation scour (Vuong et al., 2023) and Shuang-Yuan Bridge scenarios (Vuong et al., 2024). Moving-solid publications provide a separate branch of that lineage (Wu et al., 2014a; Huang…

- Chapter_03_Methods.md — 3.3.1 Large eddy simulation — line 51: The closure has its historical origin in strain-related subgrid diffusion (Smagorinsky, 1963). The three-dimensional Splash3D notation below follows the later formulation in Wu et al. (2020) and Vuong et al. (2024), rather than attributing the complete current implementation to the atmospheric paper. The eddy viscosity is written as…

- Chapter_03_Methods.md — 3.4.1 Bingham and bi-viscous models — line 87: This branch structure is described as MBM in Wu et al. (2020) and as DBM in Eq. (5) of Vuong et al. (2024). The transition convention, parameter units, and treatment at the threshold remain part of the case specification. A very large μ_A approximates resistance but does not…

- Chapter_04_Guandu.md — Chapter 4 Guandu Bridge Flow and Local Scour — line 5: The DBM precedent of Vuong et al. (2024) concerns Shuang-Yuan Bridge. This chapter assesses Guandu-specific observations and scenarios, with site-informed tidal experiments (Yu et al., 2023) and geometry–hydrodynamics comparisons (Peng et al., 2026) providing external context.…

- Chapter_04_Guandu.md — 4.2.1 Hydrodynamics and rheology — line 49: Mobile sediment is represented by the discontinuous bi-viscous model, abbreviated DBM. Below the threshold rate the material has viscosity μ_A. Above it, the yielded branch has viscosity μ_B + τ₀/γ̇. The high-viscosity branch approximates strongly resistant material using a finite numerical viscosity. It permits small deformation and should…

- Chapter_04_Guandu.md — 4.4.2 Limits of a rheological bed description — line 165: The six-/ten-pile comparison at Shuang-Yuan Bridge (Vuong et al., 2024) illustrates sensitivity to foundation exposure and arrangement under that study’s forcing. Its initial bed and foundation geometry differ from Guandu. This is a methodological precedent for resolving geometric differences, rather than a direct calibration dataset for the present…

### Vuong2023 — Vuong et al. 2023

Vuong T-H-N, Wu T-R, Huang Y-X, Hsu T-W (2023) Numerical analysis of local scour of the offshore wind turbines in Taiwan. Journal of Marine Science and Engineering 11:936. https://doi.org/10.3390/jmse11050936

Access level: F. Decision: retain.

Source: https://www.researchgate.net/publication/370390092_Numerical_Analysis_of_Local_Scour_of_the_Offshore_Wind_Turbines_in_Taiwan

Checked location: Author-uploaded original article Sections 2–5; distinguish duplicated reviewer-copy snippets

Splash3D/PLIC-VOF/DBM study of monopile/tripod/jack-up foundations under waves and current.

Method precedent only; wave/current findings are not transferred to steady Guandu scenarios.

- Chapter_01_Introduction.md — 1.1 Physical modeling and computational continuity — line 13: The physical modeling builds on published rheological landslide work (Wu et al., 2020; Vuong et al., 2020), DBM scour applications (Vuong et al., 2023, 2024; Lin et al., 2024), and the rigid-fluid method (Huang et al., 2024). These establish the platform capabilities that the dissertation applies and preserves.…

- Chapter_02_Literature_Review.md — 2.1.3 Cohesive beds and protection systems — line 35: DBM has been applied to offshore turbine foundations under waves and current (Vuong et al., 2023). Its use across geometries should not be equated with uniform quantitative accuracy. Lin et al. (2024, Sect. 3.2) report similar scour patterns around a sphere but overestimate several local depths in a…

- Chapter_03_Methods.md — 3.1 Model lineage and scope — line 7: Wu et al. (2020) document the laboratory adaptation from Truchas to Splash3D and its rheological extensions. Later DBM applications include offshore-foundation scour (Vuong et al., 2023) and Shuang-Yuan Bridge scenarios (Vuong et al., 2024). Moving-solid publications provide a separate branch of that lineage (Wu et al., 2014a; Huang…

### Vuong2020 — Vuong et al. 2020

Vuong T-H-N, Wu T-R, Wang C-Y, Chu C-R (2020) Modeling the Slump-Type Landslide Tsunamis Part II: Numerical Simulation of Tsunamis with Bingham Landslide Model. Applied Sciences 10:6872. https://doi.org/10.3390/app10196872

Access level: F. Decision: revise.

Source: https://mdpi-res.com/d_attachment/applsci/applsci-10-06872/article_deploy/applsci-10-06872-v2.pdf

Checked location: Sections 2–5, equations 10–11, benchmark and rheological sensitivity

Part II uses a Bingham-type slump configuration, compares a laboratory benchmark and tests rheological/scaling effects.

Do not imply Part II tested the independently prescribed threshold-rate DBM branch used in the later bridge case.

- Chapter_01_Introduction.md — 1.1 Physical modeling and computational continuity — line 13: The physical modeling builds on published rheological landslide work (Wu et al., 2020; Vuong et al., 2020), DBM scour applications (Vuong et al., 2023, 2024; Lin et al., 2024), and the rigid-fluid method (Huang et al., 2024). These establish the platform capabilities that the dissertation applies and preserves.…

- Chapter_02_Literature_Review.md — 2.2.1 Yield stress and continuum idealization — line 43: Wu et al. (2020) compare Bingham, conventional bi-viscosity and modified bi-viscosity descriptions using analytical/laboratory mud-flow comparisons and the FGT66 tailings case. Their modified model prescribes a resistant low-rate branch independently. Vuong et al. (2020) subsequently examine a Bingham-type slump–wave benchmark, material sensitivity and scaling; that Part II configuration…

- Chapter_05_Guishan.md — 5.1 Introduction — line 9: Deformable landslides introduce uncertainty beyond source volume and position. A material can deform, spread, and settle during motion, changing its coupling with the surrounding water. Bingham-type formulations provide a continuum description of this behavior. Three-dimensional developments within the Splash3D framework have examined rheological flows and slump-generated waves against…

### Wilson2014 — Wilson et al. 2014

Wilson G, Aruliah DA, Brown CT, Chue Hong NP, Davis M, Guy RT, Haddock SHD, Huff KD, Mitchell IM, Plumbley MD, Waugh B, White EP, Wilson P (2014) Best practices for scientific computing. PLOS Biology 12:e1001745. https://doi.org/10.1371/journal.pbio.1001745

Access level: F. Decision: retain.

Source: https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745

Checked location: Best-practice list and Make Incremental Changes/Do Not Repeat Yourself

Supports version control, modularization and automated checks.

No inference that an automated execution validates physical correctness.

- Chapter_02_Literature_Review.md — 2.3.2 Preserving the computational experiment — line 81: Sandve et al. (2013) emphasize tracking the steps that produce a computational result, including software versions, parameters, and transformations. Wilson et al. (2014) discuss practices such as version control, modular organization, and automated checks that improve scientific software development. The common implication for this dissertation is that the…

### Wu2014a — Wu et al. 2014a

Wu T-R, Chu C-R, Huang C-J, Wang C-Y, Chien S-Y, Chen M-Z (2014a) A two-way coupled simulation of moving solids in free-surface flows. Computers & Fluids 100:347–355. https://doi.org/10.1016/j.compfluid.2014.05.010

Access level: B. Decision: revise.

Source: https://www.sciencedirect.com/science/article/pii/S0045793014002023

Checked location: Publisher preview abstract, introduction/conclusion; author-institution repository has metadata

Two-way moving-solid coupling, partial-cell treatment and DEM movement/rotation.

Keep concise dissertation lineage only; no detailed benchmark performance claim without the full paper.

- Chapter_02_Literature_Review.md — 2.2.2 Source motion and observable deposits — line 57: Liu et al. (2005) describe an experimental program with wedges and a hemisphere, but their published numerical comparisons are for wedge-shaped slides. Their Section 2.2 documents the VOF/PLIC and moving-boundary lineage. Later publications report two-way moving-solid coupling (Wu et al., 2014a) and RFM (Huang et al., 2024). These…

- Chapter_03_Methods.md — 3.1 Model lineage and scope — line 7: Wu et al. (2020) document the laboratory adaptation from Truchas to Splash3D and its rheological extensions. Later DBM applications include offshore-foundation scour (Vuong et al., 2023) and Shuang-Yuan Bridge scenarios (Vuong et al., 2024). Moving-solid publications provide a separate branch of that lineage (Wu et al., 2014a; Huang…

- Chapter_03_Methods.md — 3.4.3 Moving bodies and mixed failure — line 103: Huang et al. (2024) report RFM coupled to Splash3D, following earlier two-way moving-solid work by Wu et al. (2014a). These provide the moving-body background for a possible mixed-failure model. The qualification presentation identifies combined RFM–DBM simulation as planned work; separate published modules do not by themselves establish the…

### Wu2020 — Wu et al. 2020

Wu T-R, Vuong T-H-N, Lin C-W, Wang C-Y, Chu C-R (2020) Modeling the Slump-Type Landslide Tsunamis Part I: Developing a Three-Dimensional Bingham-Type Landslide Model. Applied Sciences 10:6501. https://doi.org/10.3390/app10186501

Access level: F. Decision: revise.

Source: https://videleaf.com/wp-content/uploads/2022/11/Modeling-the-Slump-Type-Landslide-Tsunamis-Part-I-Developing-a-Three-Dimensional-Bingham-Type-Landslide-Model.pdf

Checked location: Explicit 2022 republication of the 2020 article: methods equations 1–3, validation, FGT66 and sensitivity sections

Part I names BM/CBM/modified bi-viscosity (MBM); modified low-rate branch and implicit viscosity are documented.

Identify MBM terminology in 2020 and DBM terminology in later papers; do not claim the labels or test configurations are identical.

- Chapter_01_Introduction.md — 1.1 Physical modeling and computational continuity — line 13: The physical modeling builds on published rheological landslide work (Wu et al., 2020; Vuong et al., 2020), DBM scour applications (Vuong et al., 2023, 2024; Lin et al., 2024), and the rigid-fluid method (Huang et al., 2024). These establish the platform capabilities that the dissertation applies and preserves.…

- Chapter_02_Literature_Review.md — 2.2.1 Yield stress and continuum idealization — line 43: Wu et al. (2020) compare Bingham, conventional bi-viscosity and modified bi-viscosity descriptions using analytical/laboratory mud-flow comparisons and the FGT66 tailings case. Their modified model prescribes a resistant low-rate branch independently. Vuong et al. (2020) subsequently examine a Bingham-type slump–wave benchmark, material sensitivity and scaling; that Part II configuration…

- Chapter_03_Methods.md — 3.1 Model lineage and scope — line 7: Wu et al. (2020) document the laboratory adaptation from Truchas to Splash3D and its rheological extensions. Later DBM applications include offshore-foundation scour (Vuong et al., 2023) and Shuang-Yuan Bridge scenarios (Vuong et al., 2024). Moving-solid publications provide a separate branch of that lineage (Wu et al., 2014a; Huang…

- Chapter_03_Methods.md — 3.3.1 Large eddy simulation — line 51: The closure has its historical origin in strain-related subgrid diffusion (Smagorinsky, 1963). The three-dimensional Splash3D notation below follows the later formulation in Wu et al. (2020) and Vuong et al. (2024), rather than attributing the complete current implementation to the atmospheric paper. The eddy viscosity is written as…

- Chapter_03_Methods.md — 3.3.2 Pressure projection and viscous stiffness — line 71: Large constitutive viscosities make an explicit diffusion step restrictive because its stable time increment decreases with increasing viscosity and decreasing squared cell size. The rheological development of Wu et al. (2020) adopts implicit viscous treatment to address this stiffness. Implicit treatment changes the stability constraint but does not…

- Chapter_03_Methods.md — 3.4.1 Bingham and bi-viscous models — line 87: This branch structure is described as MBM in Wu et al. (2020) and as DBM in Eq. (5) of Vuong et al. (2024). The transition convention, parameter units, and treatment at the threshold remain part of the case specification. A very large μ_A approximates resistance but does not…

- Chapter_04_Guandu.md — 4.2.1 Hydrodynamics and rheology — line 49: Mobile sediment is represented by the discontinuous bi-viscous model, abbreviated DBM. Below the threshold rate the material has viscosity μ_A. Above it, the yielded branch has viscosity μ_B + τ₀/γ̇. The high-viscosity branch approximates strongly resistant material using a finite numerical viscosity. It permits small deformation and should…

- Chapter_05_Guishan.md — 5.1 Introduction — line 9: Deformable landslides introduce uncertainty beyond source volume and position. A material can deform, spread, and settle during motion, changing its coupling with the surrounding water. Bingham-type formulations provide a continuum description of this behavior. Three-dimensional developments within the Splash3D framework have examined rheological flows and slump-generated waves against…

- Chapter_05_Guishan.md — 5.2.2 Three-dimensional flow and material representation — line 43: Here u is velocity, p is pressure, ρ is mixture density, τ is the modeled stress tensor, g is gravitational acceleration, and fₘ is the volume fraction of material m. The fractional-volume interface description follows the VOF concept of Hirt and Nichols (1981). The later PLIC reconstruction is…

- Chapter_05_Guishan.md — 5.2.2 Three-dimensional flow and material representation — line 55: The strain-rate invariant must be defined consistently with the stress tensor when implementing this relation. The discontinuous model permits the unyielded viscosity μ_A to be specified independently of the yielded-branch parameters. It should therefore be distinguished from a conventional bi-viscous regularization with a prescribed branch connection. Wu et…

### Wu2014b — Wu et al. 2014b

Wu T-R, Wang H, Ko Y-Y, Chiou J-S, Hsieh S-C, Chen C-H, Lin C, Wang C-Y, Chuang M-H (2014b) Forensic diagnosis on flood-induced bridge failure. II: Framework of quantitative assessment. Journal of Performance of Constructed Facilities 28:85–95. https://doi.org/10.1061/(ASCE)CF.1943-5509.0000393

Access level: A. Decision: retain.

Source: https://doi.org/10.1061/(ASCE)CF.1943-5509.0000393

Checked location: Publisher abstract and author-institution repository; full article not obtained

Shuang-Yuan forensic framework includes hydraulics, skew, debris and structural stability.

Broad assessment sequence only, with no transfer of thresholds or calibrated parameters to Guandu.

- Chapter_02_Literature_Review.md — 2.1.3 Cohesive beds and protection systems — line 35: DBM has been applied to offshore turbine foundations under waves and current (Vuong et al., 2023). Its use across geometries should not be equated with uniform quantitative accuracy. Lin et al. (2024, Sect. 3.2) report similar scour patterns around a sphere but overestimate several local depths in a…

- Chapter_04_Guandu.md — 4.4.3 Implications for protection and monitoring — line 173: The Shuang-Yuan Bridge investigation of Wu et al. (2014b) connected reconstructed hydraulics, skewed flow, foundation conditions and structural assessment. Its relevance is the assessment sequence: a Guandu warning criterion likewise requires hydraulic and geotechnical evidence beyond the maximum erosion in one modeled case. It does not supply a…

### Xu2025 — Xu et al. 2025

Xu Z, Wang L, Wang C, Chen Y, Luo Q, Yao H-D, Wang S, He G (2025) CFDAgent: A language-guided, zero-shot multi-agent system for complex flow simulation. Physics of Fluids 37:117124. https://doi.org/10.1063/5.0294696

Access level: F. Decision: revise.

Source: https://arxiv.org/html/2507.23693v1

Checked location: Author preprint Sections 2.1/Table 1 and 4.1; published-version metadata cross-checked; journal PDF exceeded size limit

User is asked for direction, run duration, CFL, time step and confirmations; canonical sphere-flow checks are provided.

Describe interactive orchestration rather than unqualified autonomy. The full text read is a preprint; journal metadata and indexed published first page are separate checks.

- Chapter_02_Literature_Review.md — 2.4.1 Execution graphs and model assistance — line 105: Xu et al. (2025) describe separate preprocessing, solver and post-processing roles in CFDAgent. In the accessible author preprint, Table 1 and Section 4.1 show the user supplying or confirming flow direction, duration, CFL and other settings. Its canonical sphere-flow checks support a particular interactive workflow, rather than unrestricted…

- Chapter_07_Agent_Workflows.md — 7.7 Comparison with published CFD assistance — line 91: CFDAgent provides an example of language-guided preprocessing, solver execution and post-processing (Xu et al., 2025). The accessible author preprint includes explicit user choices and confirmations of numerical settings, so the relevant comparison is interactive orchestration and demonstrated task coverage. Its sphere-flow checks do not establish autonomous recovery for…

### Yao2023 — Yao et al. 2023

Yao S, Zhao J, Yu D, Du N, Shafran I, Narasimhan K, Cao Y (2023) ReAct: Synergizing Reasoning and Acting in Language Models. International Conference on Learning Representations. https://arxiv.org/abs/2210.03629

Access level: F. Decision: retain.

Source: https://arxiv.org/html/2210.03629v3

Checked location: Sections 2–4, action/observation setup and task evaluations

Interleaves reasoning/action in retrieval and interactive-decision tasks, not CFD.

Conceptual workflow origin only; no borrowed CFD success rates.

- Chapter_02_Literature_Review.md — 2.4.1 Execution graphs and model assistance — line 101: Yao et al. (2023) investigated language models that interleave reasoning and actions through external tools. This provides conceptual background for a simulation assistant that reads a task, invokes parameter-editing functions, observes logs, and decides whether to continue. The published results do not establish performance for Truchas. That performance…

- Chapter_07_Agent_Workflows.md — 7.3.1 Task state and tool boundaries — line 31: The architecture note describes a stateful graph with stages for intent parsing, input generation, simulation execution, diagnosis, and post-processing. Shared state contains the task specification, mesh settings, simulation status, retry count, and results. Conditional routing determines whether to continue, retry, skip a stage, or terminate. This design resembles…

### Yu2023 — Yu et al. 2023

Yu P, Chen J, Zhou J, Li J, Yu L (2023) Experimental investigation of local scour around complex bridge pier of sea-crossing bridge under tidal currents. Ocean Engineering 290:116374. https://doi.org/10.1016/j.oceaneng.2023.116374

Access level: B. Decision: revise.

Source: https://www.sciencedirect.com/science/article/pii/S0029801823027580

Checked location: Publisher preview introduction and abstract; full-text/publisher/repository search did not retrieve the complete article

HZMB/ Jiuzhou Waterway foundation experiments use site-informed tidal forcing and compare tidal with unidirectional scour.

Retain study design and qualitative distinction only; avoid extracting calibration constants or attributing a backfilling mechanism without its full result section.

- Chapter_02_Literature_Review.md — 2.1.2 Tidal boundaries and field assessment — line 23: Yu et al. (2023) use foundation geometry and tidal observations from the Hong Kong–Zhuhai–Macao Bridge to define flume experiments. Peng et al. (2026) examine changes in depth, velocity and skew for a cap–pile-group foundation under a particular cap-exposure condition. These study designs motivate retaining forcing history and foundation…

- Chapter_04_Guandu.md — Chapter 4 Guandu Bridge Flow and Local Scour — line 5: The DBM precedent of Vuong et al. (2024) concerns Shuang-Yuan Bridge. This chapter assesses Guandu-specific observations and scenarios, with site-informed tidal experiments (Yu et al., 2023) and geometry–hydrodynamics comparisons (Peng et al., 2026) providing external context.…

- Chapter_04_Guandu.md — 4.4.1 Boundary realism and the meaning of validation — line 153: The tidal versus unidirectional comparison of Yu et al. (2023) concerns a different foundation and sediment setup, but supports treating forcing history as part of a scour comparison. Melville and Chiew (1999) likewise identify duration dependence for clear-water cylindrical-pier scour in uniform sand. The present fixed-direction runs do…

## Remaining limits

Four retained sources remain abstract-only and their use is limited to the broad supported scope stated above. Body excerpts are distinguished from complete versions. Numerical results retained in the source-domain analysis have not been replaced or rerun. Word text, formula, table and image checks are separate from page rendering; the bundled Office renderer remains unavailable.
