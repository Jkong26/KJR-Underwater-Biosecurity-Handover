# KJR Underwater Biosecurity — Handover Repository

Dataset preparation scripts for the underwater object detection project
built by Group 10 for K.J. Ross & Associates (KJR), covering a hierarchical
labelling taxonomy and object-detection pipeline for low-visibility
underwater drone footage.

This repository contains the dataset preparation scripts required to take a
labelled dataset from CVAT export through to a training-ready train /
validation / test split.

## What's in this repository

| Script | Purpose |
|---|---|
| `move_unlabelled_images.py` | Separates any training image with no matching label into an `unlabelled` folder, so the split script below only works with fully labelled data. |
| `splitting_dataset.py` | Splits the labelled dataset into train / validation / test folders at a 70% / 15% / 15% ratio, using a fixed random seed for reproducibility. |

## Run order

1. `move_unlabelled_images.py` — run first, so unlabelled images are set aside before splitting.
2. `splitting_dataset.py` — run second, on the now fully-labelled training set.

Each script has its own usage notes and required edits (mainly setting your
local dataset folder path) at the top of the file.

## Requirements

- Python 3.7+
- No third-party packages required for the two scripts currently included
  (standard library only: `os`, `shutil`, `random`, `time`)

## Dataset and model weights

The labelled dataset and trained model weight files are not included in this
repository due to size. They are hosted on the project SharePoint — see the
User & Technical Manual (in the Client Handover package) for the link and
for guidance on which model to use for which task.

## Related resources

- **User & Technical Manual** — full usage guide for non-technical and
  technical audiences, included in the Client Handover package.
- **Experiment Programme** — the full experimental log, including every
  configuration tried, results, and reasoning behind the choices made in
  this pipeline. Included in the Client Handover package as a PDF.

## Licence note

The underlying dataset (UIIS10K) is licensed under Apache 2.0 and is safe
for commercial use. Confirm any additional data sources added later carry
compatible licensing before combining them with this pipeline.

## Contact

For questions about this pipeline, contact Group 10 via the project
SharePoint, or the academic supervisor, Professor Zhe Hou, for continuity
beyond project completion.
