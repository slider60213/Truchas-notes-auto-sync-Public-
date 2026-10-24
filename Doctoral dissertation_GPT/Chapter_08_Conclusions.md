# Chapter 8 Conclusions and Future Work

## 8.1 Integrated findings

This dissertation examines a specialized CFD platform through physical applications, environment preservation, and simulation management. The common requirement is a traceable connection between the experiment definition and the reported result. Each component contributes evidence, but none can substitute for the others. A physically useful model needs an executable workflow, and a convenient workflow still needs physical and numerical assessment.

At Guandu Bridge, retaining layered approach velocities improves the representation of measured tidal structure. The recalculated non-boundary ebb comparison gives MAE = 0.0359 m/s for eight section–layer pairs. The interior flood comparison gives MAE = 0.0525 m/s for nine pairs and retains a positive-U bias. These values support a qualified assessment of the hydrodynamic setup and make its limitations more explicit than a general statement of good agreement.

The local bed experiments show substantial sensitivity to forcing and foundation configuration. Across the selected angles, additional scour ranges from 1.36–2.17 m at 5 m/s to 1.95–2.71 m at 6 m/s and 4.41–5.75 m at 8 m/s. The two selected approach angles reproduce different parts of historical bed-change patterns. The larger observed changes near P5 remain underpredicted, and the fixed-riprap representation redistributes exposure without evaluating stone stability. These results support conditional scenario analysis, not a complete reconstruction of past floods or a structural warning criterion.

At Guishan Island, the broad MTD3 footprint is compatible with both a sample-based rheological configuration and a low constant-viscosity experiment under the adopted reconstruction. Their similar final extent and different settling histories demonstrate the non-uniqueness of a footprint-only constraint. Density changes the stages of motion differently, and the diffuse-interface comparison exposes sensitivity in both dynamics and the extracted observable. Regional maxima approaching 1.5 m at selected Yilan stations remain conditional on the source field and transfer assumptions.

The infrastructure record demonstrates execution in the WSL2/LXD workflow and provides a timing baseline. The 3.17 ratio between the legacy four-worker run and the ten-worker 32-bit WSL run measures their combined configuration difference. Reported field statistics show close agreement over much of a selected surface, while the local 15 m discrepancy remains unresolved. The evidence supports continued use and assessment of the migrated environment, with case-specific acceptance criteria.

The workflow record demonstrates selected input editing, sequential execution, conversion, and bounded retries. The unsupported MPI_Recv failure defines a current limit. Normal completion alone cannot establish that an agent preserved the experiment or produced scientifically acceptable output. The reproducible record must include interventions and failures as well as successful runs.

## 8.2 Contributions and their scope

The physical contribution is an integrated, material-based examination of two applications using different observational constraints. The Guandu reassessment quantifies available layer-mean comparisons and retains an important spatial mismatch. The Guishan interpretation separates deposit consistency from unique source reconstruction and distinguishes source-region responses from regional scenarios.

The computational contribution is preservation and assessment of the customized workflow across recorded environments. The timing and field comparisons establish specific observations rather than universal claims about containers or architectures. The workflow contribution is a structured account of deterministic automation and tool-bounded model assistance, with criteria for evaluating future developments.

The proposed continuous viscosity treatment remains a contribution to be established through a reproducible constitutive specification and controlled comparisons. The present evidence does not justify claiming that it eliminates all yield-related numerical instability. Similarly, mixed RFM–DBM simulation, complete regional-source coupling, and general autonomous diagnosis remain extensions rather than completed results.

## 8.3 Priorities for completion

The first priority is to resolve configuration identity. The constitutive equation, unyielded viscosity, mesh, time controls, extraction thresholds, and exact binary must be linked to each reported experiment. The printed Guishan fit discrepancy and the inconsistent flood-domain dimensions must be resolved from original inputs. A shared manifest and field archive would make subsequent checks possible without relying on descriptive labels.

The second priority is targeted numerical and physical testing. At Guandu Bridge, event-matched measurements, realistic bank geometry, sediment variability, and protection permeability should be assessed separately. At Guishan Island, source-geometry ensembles, deposit-thickness residuals, conservation, interface diagnostics, and the timing and momentum of the regional transfer require attention. These tests address the largest uncertainties exposed by the present results.

The third priority is controlled infrastructure and workflow evaluation. Matched builds on the same hardware, repeated timings, and comparisons at identical physical times would clarify platform effects. A predefined agent task set with independent outcomes would quantify assistance, false repairs, and intervention needs. Both evaluations should preserve complete histories so that successful and unsuccessful results remain interpretable.

## 8.4 Longer term development

Further development can examine mixed rigid and deformable failures, improved sediment and protection mechanics, and alternative computing architectures. Such extensions should enter through the same assessment hierarchy rather than being justified by technological availability alone. GPU execution, a new solver framework, or a larger language model would each change part of the computational experiment and require its own verification.

The enduring result of modernization should be a research platform whose physical assumptions, numerical behavior, and operational history can be examined by another researcher. The present synthesis establishes that framework and identifies the evidence needed to turn its remaining provisional elements into completed doctoral results.
