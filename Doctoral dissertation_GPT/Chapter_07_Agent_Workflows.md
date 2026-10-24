# Chapter 7 Agent Assisted Simulation Workflows

## 7.1 Simulation management as part of the experiment

The numerical solver is only one component of the research workflow. A typical experiment also requires preparation of an input file, selection of an executable and worker count, launch and monitoring, output conversion, restart management, and extraction of figures or statistics. Repeated sensitivity studies multiply these operations. Their ordering and bookkeeping affect whether the final dataset represents the intended experiment.

The earlier laboratory procedure required manual conversion of binary outputs and manual renaming across restart segments. The automation notes describe a revised pipeline that integrates these operations. A further prototype accepts a natural-language task and invokes tools for input editing, execution, diagnosis, and post-processing. This chapter distinguishes the deterministic pipeline from the language-model-assisted layer so that the contribution of each can be assessed.

The objective is controlled assistance with an identified simulation task. It is not to transfer responsibility for constitutive choices or scientific interpretation to a model. Tool-mediated assistance is useful when it reduces operational friction while retaining the experiment definition and a record of interventions. The relevant evaluation must therefore include both execution behavior and preservation of scientific intent.

## 7.2 Deterministic execution and restart pipeline

### 7.2.1 Operations documented in the revised workflow

The automation record identifies a launch script, output-conversion routines, restart generation, and output-folder numbering. The revised sequence selects an input, launches the solver, converts available binary results, and prepares restart material when execution ends. Subsequent invocation can continue from the retained state. The reported GMV workflow also continues numbering across segments, reducing the need for manual file-name adjustment before visualization.

These changes address a concrete ambiguity in the earlier process. An output number can restart from zero even though physical time continues. Combining files solely by their local names can therefore overwrite or misorder results. An automated pipeline can enforce a monotonically ordered sequence, but it should preserve the physical time and original segment identity as well. Renaming cannot replace time provenance.

The July 2026 note also records incomplete numbering support for formats other than GMV. That limitation matters because a successful conversion in one format does not demonstrate equivalent behavior for Tecplot or EnSight. The dissertation therefore treats conversion support as format-specific until tests establish otherwise.

### 7.2.2 Checkpoints and termination

A restart file generated after abnormal termination is a candidate recovery artifact. It is not necessarily a scientifically valid state. Its usefulness depends on whether the solver completed a consistent checkpoint, whether the associated input and executable are retained, and whether restarting preserves the relevant fields. A robust workflow should test continuation against an uninterrupted reference calculation.

The same principle applies to post-processing triggered by normal termination. A process can exit without having reached the requested physical time or without writing every required field. Completion should therefore check the final time, expected outputs, log status, and selected conservation diagnostics. These checks connect automation to the numerical assessment described in Chapter 3.

## 7.3 Agent assisted architecture

### 7.3.1 Task state and tool boundaries

The architecture note describes a stateful graph with stages for intent parsing, input generation, simulation execution, diagnosis, and post-processing. Shared state contains the task specification, mesh settings, simulation status, retry count, and results. Conditional routing determines whether to continue, retry, skip a stage, or terminate. This design resembles the broader concept of interleaving model decisions with external actions discussed by Yao et al. (2023).

The prototype's actions are constrained by its tools. The demonstration notes name operations such as mesh and numerical-setting updates. The language model can propose a change only within the fields and procedures those tools support. A failure outside that coverage cannot be assumed repairable simply because its log is readable.

The architecture explanation is retained as a description of the prototype. It should be reconciled with the archived implementation before the dissertation makes claims about exact graph semantics or error handling. A conversation explaining a program is useful design documentation, but it is not equivalent to executing and inspecting every branch of that program.

### 7.3.2 Preserving the experiment definition

The requested physical configuration should remain identifiable throughout a task. Geometry, forcing, material parameters, and target duration define the experiment. Mesh and numerical tolerances may also affect the scientific result even when they are considered computational settings. An automatic repair that changes them must be recorded as an intervention rather than treated as an invisible correction.

A useful task record contains the original request, parsed parameters, original input, every changed input, invoked tool, diagnostic evidence, and output identity. The workflow should preserve the reason for each change and whether it modifies the experiment or repairs an operational defect. This record makes a successful run reviewable and enables a failed repair to be reproduced.

## 7.4 Demonstration evidence

The agent record documents mesh changes, changes involving a mesh ratio, and an automatic simulation-and-repair sequence. It also describes deriving a set of tasks from a prompt and attempting them sequentially. The documented retry ceiling is five. Once a run is judged to have ended normally, the workflow proceeds to post-processing.

The record includes a failure in Task 11 associated with MPI_Recv. The note states that this error was absent from the available diagnostic manual and could not be solved using the current tool set. This is an observed limit of coverage. The task should be classified as requiring intervention rather than silently counted as a completed simulation.

The same record places examples from different model configurations alongside one another, including Gemini and a smaller local model. These examples do not constitute a controlled comparative study. The prompts, repetition count, tool versions, and scored outcomes are not sufficient to infer relative reliability or general diagnostic capability. The supported result is feasibility of selected operations with an explicit unsupported case.

Table 7.1. Workflow capabilities and the evidence needed to assess them.

| Stage | Capability described in the records | Required acceptance evidence |
| --- | --- | --- |
| Intent parsing | Derivation of mesh settings and task list | Agreement with a predetermined structured task specification |
| Input editing | Updates to mesh and numerical fields | Valid syntax and a reviewed parameter difference |
| Execution | Sequential launch of simulation tasks | Correct executable, worker count, input identity, and final physical time |
| Diagnosis | Log-guided edits with at most five retries | Correct failure classification and permitted repair |
| Restart | Preparation and continuation through scripts | Consistent checkpoint and agreement with uninterrupted execution |
| Post-processing | Conversion after normal completion | Complete fields, correct physical times, and reproducible extraction |

## 7.5 Evaluation design

### 7.5.1 Baselines and task sets

A systematic evaluation should compare a scripted baseline, the same workflow with model assistance, and a researcher-operated reference for a defined task set. The tasks should include ordinary parameter changes, known formatting errors, supported numerical failures, and failures beyond current tool coverage. Expected outcomes should be established independently of the model's explanation.

Success should be scored at several levels. Execution success means that the intended process completed. Task success means that the requested configuration and outputs were produced. Scientific acceptance additionally requires the numerical diagnostics and comparison criteria defined for the case. Reporting these levels separately avoids giving a workflow credit for a run that executes after changing the intended experiment.

### 7.5.2 Measures and failure analysis

Useful measures include the fraction of tasks correctly completed, false repairs, unsupported failures correctly escalated, researcher interventions, elapsed time, and computing or model-service cost. Repeated trials are needed when model behavior varies. The evaluation should retain attempted tasks and failures rather than selecting only successful examples.

Repair quality deserves particular attention. A change can remove an error message without addressing its cause. For example, a smaller mesh could avoid a memory failure while no longer resolving the target geometry. A lower target duration could produce normal completion without answering the requested transient question. The assessment should therefore inspect parameter differences and final scientific outputs, not only exit status.

### 7.5.3 Practical stopping criteria

A bounded retry count prevents unlimited repetition but does not, by itself, ensure useful diagnosis. The workflow should also stop when the same unsupported failure recurs, when the proposed change exceeds the permitted scope, or when the evidence is insufficient to identify a valid repair. Stopping with a retained log and input history is a legitimate outcome that preserves the experiment for further investigation.

The five-retry prototype provides a concrete initial policy. Its optimal value has not been established. A later evaluation can compare different limits using repair success and resource consumption, while holding the task set and tool coverage fixed.

## 7.6 Findings

The scripted pipeline addresses repeated conversion, restart, and numbering tasks that previously required manual handling. The agent-assisted prototype extends this workflow to selected input edits and log-guided retries. The records support feasibility of those operations and identify a specific MPI failure beyond current coverage.

The available evidence does not quantify a general productivity gain, establish model superiority, or demonstrate autonomous scientific validation. The next contribution should be a scored evaluation with preserved task histories and explicit acceptance criteria. This would connect operational assistance to the reproducible numerical platform rather than treating normal execution as the final scientific result.
