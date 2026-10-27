# Chapter 6 Containerized Deployment and Numerical Consistency

## 6.1 Deployment problem and design rationale

The laboratory workflow historically combines a customized Linux solver with Windows-based preparation and visualization. This arrangement preserves access to specialized physical modules but introduces dependencies on particular compilers, libraries, file formats, and operational knowledge. Development notes describe cross-system line-ending problems, incompatible library architectures, input-parser changes, and repeated output-conversion steps. These are concrete sources of execution friction, although their frequency and cost have not been measured systematically.

The migration strategy packages a compatible Linux userspace in LXD and operates it within WSL2. WSL2 supplies a Linux kernel in a utility virtual machine, while an LXD system container shares that kernel and isolates its userspace (Microsoft, 2026; Canonical, 2026). This arrangement allows Linux execution alongside a Windows research environment. Its practical attraction is preservation of the customized stack and access to local tools, rather than a presumption of universal speed or complete isolation from host behavior.

The alternative of adopting current upstream Truchas would require a separate reconciliation of input conventions, code changes, and laboratory extensions. The upstream project remains relevant for comparison, but a common project name does not make two code histories interchangeable. The present work therefore examines preservation and assessment of the laboratory version. It does not establish that this is the only viable modernization route.

## 6.2 Dependency and architecture issues

Build notes identify Chaco, PGSLib, Ubiksolve, an MPI implementation, and legacy compiler or parser dependencies. The migration must maintain agreement among their binary interfaces. Mixing 32-bit and 64-bit libraries can prevent linking or lead to incompatible assumptions about integer and address sizes. The label 64-bit must therefore be defined carefully: executable architecture, integer width, addressability, and floating-point precision are different properties.

The notes describe changes to source syntax, compiler handling of nested calls or overloaded operators, and input-processing routines. These records are useful for identifying a reproducible build recipe. They do not establish, by themselves, which changes are necessary or sufficient for every platform. A final recipe should contain the exact compiler versions, options, library builds, source revision, and a small verification suite. Advice retained in a troubleshooting conversation must be distinguished from changes confirmed by a successful build and test.

Container export and import can preserve an environment image. To make that image scientifically useful, its identity must be recorded together with the case manifest and executable checksum. A container that can start is an operational artifact; a container that can reproduce a specified result with documented tolerances is a stronger research artifact. These are separate milestones.

## 6.3 Recorded timing experiment

The benchmark note uses a Guishan configuration with 100 × 80 × 70 cells, or 560000 cells in total. It records material density 2000 kg/m³, constant viscosity 10⁻³ Pa s, and an output interval of 5 s. This grid differs from the 100 × 100 × 70 initial source grid described in Chapter 5. The timing record is therefore treated as a distinct benchmark configuration and is not assigned retrospectively to every physical result.

Elapsed times are recorded to output bin 25 (Table 6.1). The table includes legacy Machine 160, WSL configurations, and Machine 174. The records do not provide enough hardware and software metadata to isolate all causes of the differences. In particular, machines, worker counts, architecture labels, and possibly build settings change across entries.

Table 6.1. Recorded benchmark timings to output bin 25.

| Platform | Recorded architecture label | Workers | Elapsed time | Minutes |
| --- | --- | ---: | --- | ---: |
| Machine 160 | 32-bit | 4 | 14 h 06 min | 846 |
| Machine 160 | 32-bit | 10 | 5 h 37 min | 337 |
| WSL | 32-bit | 4 | 5 h 48 min | 348 |
| WSL | 32-bit | 10 | 4 h 27 min | 267 |
| WSL | 64-bit | 10 | 3 h 35 min | 215 |
| Machine 174 | 64-bit | 10 | 4 h 00 min | 240 |

Using the legacy four-worker entry as reference, the ten-worker 32-bit WSL entry has a recorded speed ratio of 846/267 = 3.17. The ten-worker 64-bit WSL entry gives 846/215 = 3.93. These ratios summarize the total configuration difference. They do not measure container overhead or prove that binary architecture alone caused the further reduction.

Within Machine 160, increasing the recorded worker count from four to ten gives a ratio of 846/337 = 2.51. Within 32-bit WSL, the same worker-count change gives 348/267 = 1.30. The worker-count ratio is 2.5. The legacy result is close to that nominal scaling ratio, while the WSL result shows much smaller additional benefit. Without repeated timings and confirmed identical work, neither value should be used to estimate a general scaling law. They indicate that the useful worker count depends on the configuration.

The four-worker cross-platform ratio is 846/348 = 2.43, while the ten-worker ratio is 337/267 = 1.26. Their difference further cautions against a single statement about virtualization speed. A controlled comparison would use the same hardware, equivalent builds and inputs, fixed output placement, explicit worker binding, and repeated runs. It would separately report initialization, solver, and output costs if those phases can be measured reliably.

## 6.4 Reported field comparison

The draft comparison uses the legacy four-worker field as a numerical reference. It describes 8000 horizontal samples at a selected time of approximately 125.02 s. For the ten-worker WSL comparison, the note reports MAE = 0.0204 m, RMSE = 0.3420 m, mean difference = 0.0041 m, and R² = 0.9953. It also reports 99.00% of sampled differences below 0.10 m and a maximum absolute difference of 15.0 m at approximately (1025, −875) m.

These values indicate close agreement over much of the sampled field together with a small number of potentially important outliers. RMSE is about 16.8 times MAE, consistent with a highly uneven difference distribution. This observation follows from the reported summaries; the complete distribution still needs to be recovered from matched fields. A high correlation does not eliminate the significance of the local maximum.

The notes propose wetting–drying or interface reconstruction as an explanation for the maximum. That explanation remains a hypothesis without collocated fraction profiles, timing checks, and a comparison of extraction rules. The maximum could also be affected by coordinate registration, a different wet mask, different physical times, or parallel-decomposition sensitivity. The available summaries do not distinguish among those causes. Accordingly, the dissertation does not conclude that the outlier is harmless or that numerical dissipation is negligible.

A later note labeled DBM-64bit reports R² = 0.9918 for a comparison associated with a different output index. It is not pooled with the earlier R² = 0.9953 result. Their case identities, output times, constitutive settings, and masks must be reconciled before a joint conclusion is made. The 64-bit label also does not establish that the same floating-point precision changed between the compared runs.

## 6.5 A reproducible migration assessment

The next assessment should start with a case that can be executed in every environment with exactly identified inputs. One comparison should retain worker count while changing environment; another should retain environment while changing worker count. A third can assess the architecture transition with consistent libraries and an explicit precision specification. Repeated timings would quantify variability and reveal initialization or file-system effects.

Numerical outputs should be compared at matched physical times. Comparing the same output filename or index is insufficient if adaptive stepping or output scheduling differs. The extraction method should use the same volume-fraction threshold, wet mask, interpolation, and vertical convention. Where a surface contains multiple intersections, the rule selecting an intersection must be specified.

Field differences should be evaluated globally and near the quantities of interest. For the Guishan benchmark, these include source-region extrema, spatial wave patterns, and material distribution. For rheological verification, an analytical or well-characterized material-flow case can test behavior without the geometric complexity of the island. Material-volume and momentum diagnostics would help distinguish an extraction discrepancy from a change in the solved dynamics.

Acceptance tolerances should be set according to intended use before examining all differences. A tolerance adequate for visualizing an offshore wave field may be inadequate for a threshold decision at one gauge. Numerical reproducibility is therefore best stated as agreement within a defined tolerance for a defined case and observable. Exact bitwise equality is a separate, stronger requirement and is not assumed here.

## 6.6 Findings and limitations

The deployment records demonstrate that the customized platform can execute in the recorded WSL/LXD workflow and that selected configurations reach the benchmark output faster than the legacy reference. The timing table provides a useful baseline for further controlled tests. The reported field summaries also support substantial similarity over much of one sampled surface field.

The evidence does not isolate container overhead, establish a universal speed advantage, or complete cross-platform verification. The local 15 m discrepancy and the identity of later 64-bit comparisons remain unresolved. The defensible conclusion is that the migrated environment is a viable platform for continued numerical assessment, with its physical and reproducibility claims tied to case-specific tests. This conclusion preserves the practical value of modernization without assigning it evidence that has not yet been collected.


## 6.7 Relation to reproducible workflow research

Container-based dependency preservation (Boettiger, 2015; Kurtzer et al., 2017) explains the portability objective of the migrated platform. Explicit workflow systems additionally preserve how computational steps depend on one another (Di Tommaso et al., 2017). The reported WSL2/LXD deployment addresses the environment layer; the recorded conversion, restart and extraction steps address the experiment layer. Cross-platform agreement must still be distinguished from discretization assessment (Celik et al., 2008). No container speedup or error tolerance follows from those publications alone.
