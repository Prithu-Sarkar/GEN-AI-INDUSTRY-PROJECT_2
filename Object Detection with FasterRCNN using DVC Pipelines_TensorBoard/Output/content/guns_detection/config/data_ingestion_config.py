# --- Dataset ---
DATASET_NAME = "issaisasank/guns-object-detection"
TARGET_DIR   = "artifacts"   # DVC tracks artifacts/raw/ and artifacts/models/

# --- Subset size (set None to use the entire dataset) ---
# 300 samples keeps Colab free-tier training feasible (~10-20 min on T4)
NUM_SAMPLES  = 300

# --- Model hyper-parameters ---
NUM_CLASSES   = 2       # 1 foreground class (gun) + 1 background
LEARNING_RATE = 1e-4
EPOCHS        = 5
BATCH_SIZE    = 3       # small batch avoids OOM on T4 (16 GB VRAM)

# --- Paths ---
RAW_DATA_PATH  = f"{TARGET_DIR}/raw"
MODEL_SAVE_DIR = f"{TARGET_DIR}/models"
MODEL_FILENAME = "fasterrcnn.pth"