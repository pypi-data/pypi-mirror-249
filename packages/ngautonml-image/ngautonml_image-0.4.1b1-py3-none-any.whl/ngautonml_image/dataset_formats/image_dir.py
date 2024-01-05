'''Dataset format for image classification.

Images are stored in subdirectories whose names indicate thier class.
'''
from typing import Any, Dict, List, Optional

import tensorflow as tf

from ngautonml.wrangler.constants import Defaults
from ngautonml.wrangler.dataset import Column
from ngautonml.dataset_formats.impl.dataset_config import DatasetConfig
from ngautonml.dataset_formats.impl.dataset_format_catalog import (DatasetFormat,
                                                                   DatasetFormatCatalog)
from ngautonml.problem_def.config_component import ValidationErrors
from ngautonml.problem_def.output_config import ConfigError
from ngautonml.wrangler.dataset import Dataset, RoleName


class ImageDirDatasetConfig(DatasetConfig):
    '''Holds information about an image classification dataset.

    Images are stored in subdirectories whose names indicate thier class.
    '''

    def _build_roles(self) -> Dict[RoleName, List[Column]]:
        retval = super()._build_roles()
        if RoleName.TARGET not in retval:
            # TODO(Merritt): plugins should have thier own defaults & constants
            retval[RoleName.TARGET] = [Column(name=Defaults.IMAGE_CLF_TARGET_NAME)]

        return retval

    def validate(self, **kwargs) -> None:
        errors: List[ConfigError] = []

        try:
            super().validate(**kwargs)
        except ValidationErrors as err:
            errors.extend(err.errors)

        if not self._exists('train_dir'):
            errors.append(ConfigError('a config type of `image_dir` requires a `train_dir`'))

        if len(errors) > 0:
            raise ValidationErrors(errors=errors)

    def load_train(self) -> Dataset:
        train_ds = tf.keras.utils.image_dataset_from_directory(
            self._get('train_dir'),
            validation_split=float(self._get_with_default('validation_split', dflt=0.2)),
            subset="training",
            seed=self._get_with_default('seed', dflt=123),
            image_size=(int(self._get_with_default('img_height', dflt=128)),
                        int(self._get_with_default('img_width', dflt=128))),
            batch_size=int(self._get_with_default('batch_size', dflt=32)))

        val_ds = tf.keras.utils.image_dataset_from_directory(
            self._get('train_dir'),
            validation_split=float(self._get_with_default('validation_split', dflt=0.2)),
            subset="validation",
            seed=int(self._get_with_default('seed', dflt=123)),
            image_size=(int(self._get_with_default('img_height', dflt=128)),
                        int(self._get_with_default('img_width', dflt=128))),
            batch_size=int(self._get_with_default('batch_size', dflt=32)))

        dataset = Dataset(
            metadata=self.metadata,
            keras_ds=train_ds,
            keras_validate=val_ds
        )

        return dataset

    def load_test(self) -> Optional[Dataset]:
        test_ds = tf.keras.utils.image_dataset_from_directory(
            self._get('test_dir'),
            labels=None,
            seed=int(self._get_with_default('seed', dflt=123)),
            image_size=(int(self._get_with_default('img_height', dflt=128)),
                        int(self._get_with_default('img_width', dflt=128))),
            batch_size=int(self._get_with_default('batch_size', dflt=32)),
            shuffle=False)

        dataset = Dataset(
            metadata=self.metadata,
            keras_ds=test_ds
        )
        return dataset

    def dataset(self, data: Any, **kwargs) -> Dataset:
        # TODO(Merritt): implement this
        raise NotImplementedError


class ImageDirDatasetFormat(DatasetFormat):
    '''Dataset format for image classification.

    Images are stored in subdirectories whose names indicate thier class.
    '''
    _builder = ImageDirDatasetConfig
    _name = 'image_dir'
    _tags = {}


def register(catalog: DatasetFormatCatalog, *args, **kwargs):
    '''Register all the objects in this file.'''
    catalog.register(ImageDirDatasetFormat(*args, **kwargs))
