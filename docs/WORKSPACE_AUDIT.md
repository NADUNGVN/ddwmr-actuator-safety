# Workspace audit — 2026-09-28

## Existing layout (read only)

Workspace: `D:/Research/Teacher_Vien`.

| Path | Observed purpose/status | Isolation decision |
|---|---|---|
| `README.md` | Shared project index and creation instructions | Read only; not amended in this task |
| `templates/research-project/` | General research skeleton and `.gitignore` | Read only; copied only `.gitignore` into the new project |
| `projects/quadrotor-backstepping-control/` | Quadrotor MATLAB/Simulink research; independent Git repo; existing modified and untracked files | No edits, no cleanup, no execution, no commits |
| `projects/tcns-information-limits/` | Independent manuscript/reproducibility package awaiting advisor review according to its README | No edits or runs; `git status` reports it is not a Git repository |
| `projects/ddwmr-actuator-safety/` | Newly created DDWMR research project with a new `.git/` | Sole write boundary |

The shared README recommends a separate directory and Git repository for each new study. No applicable ancestor `AGENTS.md` was found in the checked workspace/parent locations. The new project has its own `AGENTS.md`.

## Existing changes

The quadrotor repo already had modified `.gitignore` and `README.md`, and untracked `.github/`, `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, `config/`, `data/`, several `docs/` entries, `experiments/registry/`, `hardware/`, `publications/`, `research/`, `results/`, `scripts/`, `setup_project.m`, `src/`, and `tests/`. These changes predate DDWMR work and must never be attributed to this project or reset.

## Operational boundary

All new research files and future software environments/results belong inside this repository. No shared MATLAB `savepath`, global package installation, root Git initialization, or sibling artifact reuse is part of this task. Existing unpublished research was read only at README/status level for orientation, not imported into the DDWMR study. This is an operational audit, not a full bytewise backup or checksum audit of sibling repositories.
