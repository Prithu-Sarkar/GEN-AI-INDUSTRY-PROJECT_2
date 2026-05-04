# Object Detection using Faster R-CNN & DVC Pipelines

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"/>
  <img src="https://img.shields.io/badge/DVC-Pipeline-945DD6?style=for-the-badge&logo=dvc&logoColor=white"/>
  <img src="https://img.shields.io/badge/MLflow-Tracking-0194E2?style=for-the-badge&logo=mlflow&logoColor=white"/>
  <img src="https://img.shields.io/badge/DagsHub-Integrated-FF6B6B?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/TensorBoard-Logging-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white"/>
</p>

---

## Overview

This project implements an end-to-end **object detection pipeline** using **Faster R-CNN ResNet-50 FPN**, fine-tuned on a custom dataset. The entire workflow — from raw data acquisition to model training and artifact management — is orchestrated through **DVC (Data Version Control)**, enabling fully reproducible, stage-aware pipeline execution.

Experiment tracking is handled via **MLflow**, with remote logging to **DagsHub**, alongside **TensorBoard** for real-time loss visualization. The codebase follows a modular, production-grade architecture with structured logging, custom exception handling, and per-epoch model checkpointing.

---

## Architecture

```
Object Detection Pipeline
│
├── Stage 1: Data Ingestion
│   ├── Authenticated dataset download (Kaggle API)
│   ├── Recursive folder traversal & flattening
│   └── Structured output -> artifacts/raw/{Images, Labels}
│
└── Stage 2: Model Training
    ├── Faster R-CNN ResNet-50 FPN (COCO pre-trained)
    ├── Custom head replacement (N-class fine-tuning)
    ├── 80/20 train-validation split
    ├── Per-batch TensorBoard logging
    ├── Per-epoch MLflow metric tracking
    └── Checkpoint saving -> artifacts/models/
```

---

## Project Structure

```
project_root/
│
├── src/
│   ├── __init__.py
│   ├── logger.py                  # Timestamped rotating file logger + stdout stream
│   ├── custom_exception.py        # File & line-enriched exception wrapper
│   ├── data_ingestion.py          # Kaggle download, zip handling, dataset flattening
│   ├── data_processing.py         # PyTorch Dataset (YOLO xyxy annotation format)
│   ├── model_architecture.py      # Faster R-CNN builder with custom head
│   └── model_training.py          # Full training loop (TensorBoard + MLflow + checkpoints)
│
├── config/
│   ├── __init__.py
│   └── data_ingestion_config.py   # Centralized constants & hyper-parameters
│
├── artifacts/
│   ├── raw/
│   │   ├── Images/                # DVC-tracked: all image files
│   │   └── Labels/                # DVC-tracked: all annotation files
│   └── models/
│       └── fasterrcnn.pth         # DVC-tracked: final trained model
│
├── logs/                          # Timestamped log files (one per run)
├── tensorboard_logs/              # TensorBoard event files (one dir per run)
├── mlruns/                        # Local MLflow runs (when DagsHub is disabled)
│
├── dvc.yaml                       # DVC pipeline definition (stages, deps, outs)
├── dvc.lock                       # Auto-generated: hashes of all stage I/O
├── requirements.txt
└── README.md
```

---

## Model

| Component | Detail |
|-----------|--------|
| Backbone | ResNet-50 with Feature Pyramid Network (FPN) |
| Pre-training | COCO (via `torchvision` weights API) |
| Head | Replaced `FastRCNNPredictor` for custom class count |
| Optimizer | Adam |
| Loss | Faster R-CNN internal: RPN + RoI classification + box regression |
| Device | CUDA (GPU) / CPU fallback |

---

## DVC Pipeline

The pipeline is defined in `dvc.yaml` with two stages:

```yaml
stages:
  data_ingestion:
    cmd: python src/data_ingestion.py
    deps: [src/data_ingestion.py, config/data_ingestion_config.py]
    outs: [artifacts/raw/]

  model_training:
    cmd: python src/model_training.py
    deps: [src/model_training.py, artifacts/raw/, ...]
    outs: [artifacts/models/fasterrcnn.pth]
```

Run the full pipeline with a single command:

```bash
dvc repro
```

DVC automatically skips stages whose dependencies have not changed, ensuring efficient re-execution.

---

## Experiment Tracking

All training runs are tracked with **MLflow** and logged remotely to **DagsHub**.

**Logged parameters:**

- `num_classes`, `learning_rate`, `epochs`, `batch_size`, `num_samples`, `device`, `model`

**Logged metrics (per epoch):**

- `train_loss`, `val_loss`

**Logged artifacts:**

- Final model (`fasterrcnn.pth`)
- Epoch-level checkpoints

**TensorBoard scalars:**

- `Loss/train_batch` — per-batch training loss
- `Loss/train_epoch` — average training loss per epoch
- `Loss/val_epoch` — average validation loss per epoch

---

## Configuration

All hyper-parameters and paths are centralized in `config/data_ingestion_config.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DATASET_NAME` | `issaisasank/guns-object-detection` | Kaggle dataset slug |
| `TARGET_DIR` | `artifacts` | Root output directory (DVC-tracked) |
| `NUM_SAMPLES` | `300` | Training subset size (`None` = full dataset) |
| `NUM_CLASSES` | `2` | Background + foreground classes |
| `LEARNING_RATE` | `1e-4` | Adam optimizer learning rate |
| `EPOCHS` | `5` | Number of training epochs |
| `BATCH_SIZE` | `3` | Samples per training batch |

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- CUDA-capable GPU (recommended)
- Kaggle account with API credentials
- DagsHub account (for remote MLflow tracking)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Credentials

Set the following environment variables before running:

```bash
# Kaggle (dataset download)
export KAGGLE_USERNAME=your_kaggle_username
export KAGGLE_KEY=your_kaggle_api_key

# MLflow / DagsHub (experiment tracking)
export MLFLOW_TRACKING_URI=https://dagshub.com/<username>/<repo>.mlflow
export MLFLOW_TRACKING_USERNAME=your_dagshub_username
export MLFLOW_TRACKING_PASSWORD=your_dagshub_token

# MongoDB (optional metadata store)
export MONGO_DB_URL=your_mongodb_connection_string
```

### Initialise DVC

```bash
git init
dvc init
git add .
git commit -m "feat: initialise project with DVC"
```

### Run the Pipeline

```bash
dvc repro
```

---

## Logging

Every run produces a timestamped log file under `logs/`:

```
logs/log_2025-05-03_14-32-01.log
```

Log entries include module name, level, timestamp, and message — streamed simultaneously to the file and to stdout.

---

## Checkpointing

Model state dicts are saved after every epoch:

```
artifacts/models/fasterrcnn_epoch1.pth
artifacts/models/fasterrcnn_epoch2.pth
...
artifacts/models/fasterrcnn.pth   <- final model (DVC output)
```

---

## Reproducibility

This project guarantees full reproducibility through:

- **DVC** — tracks data, model artifacts, and pipeline stage hashes in `dvc.lock`
- **MLflow** — records every hyper-parameter and metric against a unique run ID
- **Git + DVC lock** — committing `dvc.lock` pins the exact dataset version and model weights used in any given experiment

To reproduce a previous experiment exactly:

```bash
git checkout <commit-hash>
dvc checkout
dvc repro
```

---

## Tech Stack

| Tool | Role |
|------|------|
| PyTorch + torchvision | Model definition & training loop |
| Faster R-CNN ResNet-50 FPN | Object detection architecture |
| DVC | Pipeline orchestration & artifact versioning |
| MLflow | Experiment tracking & model registry |
| DagsHub | Remote MLflow backend & Git hosting |
| TensorBoard | Real-time training visualization |
| kagglehub | Authenticated dataset download |
| OpenCV | Image loading & preprocessing |
| MongoDB | Optional metadata persistence |

---

## Dataset

**Source:** [Kaggle — issaisasank/guns-object-detection](https://www.kaggle.com/datasets/issaisasank/guns-object-detection)

**Annotation format:** YOLO-style plain text (pixel-coordinate xyxy bounding boxes)

```
<box_count>
<x_min> <y_min> <x_max> <y_max>
...
```

The ingestion pipeline flattens all nested subdirectories into two clean folders (`Images/`, `Labels/`) for deterministic dataset loading.

---

## License

This project is released for educational and research purposes.

---

## Author

**Prithu Sarkar**  
[GitHub](https://github.com/Prithu-Sarkar) · [DagsHub](https://dagshub.com)
