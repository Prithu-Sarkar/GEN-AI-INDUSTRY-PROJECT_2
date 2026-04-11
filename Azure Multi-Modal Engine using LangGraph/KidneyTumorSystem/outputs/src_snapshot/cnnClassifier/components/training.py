import tensorflow as tf
from pathlib import Path
from cnnClassifier.entity.config_entity import TrainingConfig


class Training:
    """Handles model loading, data generator creation, and model fitting."""

    def __init__(self, config: TrainingConfig):
        self.config = config

    def get_base_model(self) -> None:
        self.model = tf.keras.models.load_model(
            str(self.config.updated_base_model_path)
        )
        # Recompile the model after loading to ensure optimizer is correctly initialized
        self.model.compile(
            optimizer=tf.keras.optimizers.SGD(learning_rate=self.config.params_learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=["accuracy"],
        )

    def train_valid_generator(self) -> None:
        """Build training and validation ImageDataGenerators."""
        datagenerator_kwargs = dict(rescale=1.0 / 255, validation_split=0.20)
        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],
            batch_size=self.config.params_batch_size,
            interpolation="bilinear",
        )

        # Validation generator (no augmentation)
        valid_dg = tf.keras.preprocessing.image.ImageDataGenerator(**datagenerator_kwargs)
        self.valid_generator = valid_dg.flow_from_directory(
            directory=str(self.config.training_data),
            subset="validation", shuffle=False, **dataflow_kwargs,
        )

        # Training generator (optional augmentation)
        if self.config.params_is_augmentation:
            train_dg = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range=40, horizontal_flip=True,
                width_shift_range=0.2, height_shift_range=0.2,
                shear_range=0.2, zoom_range=0.2,
                **datagenerator_kwargs,
            )
        else:
            train_dg = valid_dg

        self.train_generator = train_dg.flow_from_directory(
            directory=str(self.config.training_data),
            subset="training", shuffle=True, **dataflow_kwargs,
        )

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model) -> None:
        model.save(path)

    def train(self, callback_list: list) -> None:
        """Fit the model and save trained weights."""
        self.steps_per_epoch  = self.train_generator.samples // self.train_generator.batch_size
        self.validation_steps = self.valid_generator.samples  // self.valid_generator.batch_size
        self.model.fit(
            self.train_generator,
            epochs=self.config.params_epochs,
            steps_per_epoch=self.steps_per_epoch,
            validation_steps=self.validation_steps,
            validation_data=self.valid_generator,
            callbacks=callback_list,
        )
        self.save_model(path=self.config.trained_model_path, model=self.model)
