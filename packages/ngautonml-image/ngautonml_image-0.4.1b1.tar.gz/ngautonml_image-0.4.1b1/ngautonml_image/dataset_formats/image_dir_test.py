'''Tests for image_dir.py.'''

import math
from pathlib import Path

# pylint: disable=no-name-in-module
from tensorflow.python.data.ops.dataset_ops import BatchDataset  # type: ignore[import]

from .image_dir import ImageDirDatasetFormat


NUM_IMAGES = 3665

MINIMAL_CLAUSE = {
    'config': 'image_dir',
    'train_dir': str(Path(__file__).parents[4] / 'examples' / 'flowers' / 'train')
}


def test_defaults() -> None:
    '''Test that default parameters get applied when not specified.'''
    dut = ImageDirDatasetFormat().build(MINIMAL_CLAUSE)
    got = dut.load_train()['keras_ds']
    assert isinstance(got, BatchDataset)
    assert got.class_names == ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']
    for image_batch, _ in got:
        # shape tuple is (batch_size, img_height, img_width, _)
        assert image_batch.shape == (32, 128, 128, 3)
        break
    want_val_split = 1 - 0.2
    num_images_got = len([1 for _ in got.unbatch()])
    num_images_want = math.floor(NUM_IMAGES * want_val_split)
    assert num_images_got == num_images_want


OVERRIDE_CLAUSE = {
    'config': 'image_dir',
    'train_dir': str(Path(__file__).parents[4] / 'examples' / 'flowers' / 'train'),
    'validation_split': 0.6,
    'img_height': 2,
    'img_width': 8,
    'batch_size': 10
}


def test_overrides() -> None:
    '''Test that overridden parameters get properly applied.'''
    dut = ImageDirDatasetFormat().build(OVERRIDE_CLAUSE)
    got = dut.load_train()['keras_ds']
    assert isinstance(got, BatchDataset)
    for image_batch, _ in got:
        # shape tuple is (batch_size, img_height, img_width, _)
        assert image_batch.shape == (10, 2, 8, 3)
        break
    want_val_split = 1 - 0.6
    num_images_got = len([1 for _ in got.unbatch()])
    num_images_want = math.floor(NUM_IMAGES * want_val_split)
    assert num_images_got == num_images_want
