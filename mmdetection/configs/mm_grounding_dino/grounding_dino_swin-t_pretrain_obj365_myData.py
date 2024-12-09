# 1. dataset settings
_base_ = './grounding_dino_swin-t_pretrain_obj365.py'


dataset_type = 'CocoDataset'
classes = ('backpack', 'bed', 'bicycle', 'book', 'bottle', 'bowl', 'box', 'bus', 'car', 'card', 'cell phone', 'chair', 'couch', 'cup', 'dining table', 'earbuds', 'glasses', 'handbag', 'keyboard', 'keys', 'lamp', 'laptop', 'marker', 'mouse', 'pen', 'pencil - v1 2022-04-21 11-44am', 'person', 'pillow', 'remote', 'scissors', 'shoes', 'spoon', 'tablet', 'tape', 'toilet-paper', 'trash-can', 'truck', 'tv', 'wallet', )
data_root='data/Detect-Pencils'

num_classes = len(classes)

model = dict(bbox_head=dict(num_classes=num_classes))




train_dataloader = dict(
    batch_size=2,
    num_workers=2,
    dataset=dict(
        type=dataset_type,
        # explicitly add your class names to the field `metainfo`
        metainfo=dict(classes=classes),
        data_root=data_root,
        ann_file='train/_annotations.coco.json',
        data_prefix=dict(img='train/image_data')
        )
    )

val_dataloader = dict(
    batch_size=1,
    num_workers=2,
    dataset=dict(
        type=dataset_type,
        test_mode=True,
        # explicitly add your class names to the field `metainfo`
        metainfo=dict(classes=classes),
        data_root=data_root,
        ann_file='val/annotation_data',
        data_prefix=dict(img='val/image_data')
        )
    )

test_dataloader = dict(
    batch_size=1,
    num_workers=2,
    dataset=dict(
        type=dataset_type,
        test_mode=True,
        # explicitly add your class names to the field `metainfo`
        metainfo=dict(classes=classes),
        data_root=data_root,
        ann_file='test/annotation_data',
        data_prefix=dict(img='test/image_data')
        )
    )

model = dict(
    roi_head=dict(
        bbox_head=[
            dict(
                type='Shared2FCBBoxHead',
                # explicitly over-write all the `num_classes` field from default 80 to 5.
                num_classes=40),
            dict(
                type='Shared2FCBBoxHead',
                # explicitly over-write all the `num_classes` field from default 80 to 5.
                num_classes=40),
            dict(
                type='Shared2FCBBoxHead',
                # explicitly over-write all the `num_classes` field from default 80 to 5.
                num_classes=40)],
    # explicitly over-write all the `num_classes` field from default 80 to 5.
    mask_head=dict(num_classes=40)))
