import os

import cv2
import numpy as np
import torch
from torch.utils.data import Dataset

from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)


class GunDataset(Dataset):
    '''
    Custom PyTorch Dataset for gun object detection.

    Directory layout expected:
        root/
          Images/   <- .jpg / .jpeg / .png files
          Labels/   <- matching .txt files (xyxy pixel-coord format)

    Returns image tensor [3,H,W] and target dict compatible
    with torchvision Faster R-CNN.
    '''

    def __init__(self, root: str, device: str = "cpu"):
        self.image_dir  = os.path.join(root, "Images")
        self.labels_dir = os.path.join(root, "Labels")
        self.device     = device

        # Sorted lists guarantee image[i] matches label[i]
        self.img_names = sorted(os.listdir(self.image_dir))

        logger.info(
            f"GunDataset ready | {len(self.img_names)} images | device={device}"
        )

    def __len__(self) -> int:
        return len(self.img_names)

    def __getitem__(self, idx: int):
        try:
            # --- Load & normalise image ---
            img_path = os.path.join(self.image_dir, self.img_names[idx])
            bgr = cv2.imread(img_path)
            if bgr is None:
                raise FileNotFoundError(f"cv2.imread returned None for {img_path}")

            rgb   = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32)
            img_t = torch.as_tensor(rgb / 255.0).permute(2, 0, 1)  # [3,H,W]

            # --- Load bounding-box annotations ---
            stem       = os.path.splitext(self.img_names[idx])[0]
            label_path = os.path.join(self.labels_dir, stem + ".txt")

            # Default empty target (handles images with no annotations)
            target = {
                "boxes"   : torch.zeros((0, 4), dtype=torch.float32),
                "labels"  : torch.zeros(0,       dtype=torch.int64),
                "area"    : torch.zeros(0,       dtype=torch.float32),
                "image_id": torch.tensor([idx]),
            }

            if os.path.exists(label_path):
                with open(label_path, "r") as f:
                    lines     = f.read().strip().splitlines()
                    box_count = int(lines[0]) if lines else 0
                    boxes     = [
                        list(map(int, lines[i + 1].split()))
                        for i in range(box_count)
                        if i + 1 < len(lines)
                    ]

                if boxes:
                    areas = [(b[2] - b[0]) * (b[3] - b[1]) for b in boxes]
                    target["boxes"]  = torch.tensor(boxes,  dtype=torch.float32)
                    target["labels"] = torch.ones(len(boxes), dtype=torch.int64)
                    target["area"]   = torch.tensor(areas,  dtype=torch.float32)

            # Move tensors to the target device
            img_t  = img_t.to(self.device)
            target = {k: v.to(self.device) for k, v in target.items()}

            return img_t, target

        except Exception as e:
            logger.error(f"Error loading index {idx}: {e}")
            raise CustomException(f"Failed to load sample at index {idx}", e)