import torch
from torchvision.models.detection import (
    fasterrcnn_resnet50_fpn,
    FasterRCNN_ResNet50_FPN_Weights,
)
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)


class FasterRCNNModel:
    '''
    Wraps torchvision's Faster R-CNN ResNet-50 FPN and adapts its
    prediction head for a custom number of classes.

    Usage:
        wrapper = FasterRCNNModel(num_classes=2, device="cuda")
        model   = wrapper.model   # the raw nn.Module ready for training
    '''

    def __init__(self, num_classes: int, device: str):
        self.num_classes = num_classes
        self.device      = device
        self.model       = self._build().to(device)
        logger.info(
            f"FasterRCNNModel ready | num_classes={num_classes} | device={device}"
        )

    def _build(self):
        '''
        Load COCO-pretrained weights, then swap the RoI box predictor
        head so output dimensionality matches num_classes.
        '''
        try:
            weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
            model   = fasterrcnn_resnet50_fpn(weights=weights)

            # Only the final head is replaced; backbone stays frozen initially
            in_features = model.roi_heads.box_predictor.cls_score.in_features
            model.roi_heads.box_predictor = FastRCNNPredictor(
                in_features, self.num_classes
            )

            logger.info("Faster R-CNN head replaced for custom classes.")
            return model

        except Exception as e:
            logger.error(f"Model build failed: {e}")
            raise CustomException("Failed to build Faster R-CNN model", e)