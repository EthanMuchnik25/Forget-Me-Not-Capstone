_base_ = '../grounding_dino_swin-t_pretrain_obj365.py'


data_root = 'data/Detecting-Pencils/'
class_name = ('backpack', 'bed', 'bicycle', 'book', 'bottle', 'bowl', 'box', 'bus', 'car', 'card', 'cell phone', 'chair', 'couch', 'cup', ' desk', 'dining table', 'earbuds', 'glasses', 'handbag', 'keyboard', 'keys', 'lamp', 'laptop', 'marker', 'mouse', 'pen', 'pencil - v1 2022-04-21 11-44am', 'person', 'pillow', 'remote', 'scissors', 'shoes', 'spoon', 'tablet', 'tape', 'toilet-paper', 'trash-can', 'truck', 'tv', 'wallet')
palette = [(255, 97, 0), (0, 201, 87), (176, 23, 31), (138, 43, 226),
           (30, 144, 255)]
num_classes = len(class_name)
model = dict(bbox_head=dict(num_classes=num_classes))
metainfo = dict(classes=class_name, palette=palette)

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='RandomFlip', prob=0.5),
    dict(
        type='RandomChoice',
        transforms=[
            [
                dict(
                    type='RandomChoiceResize',
                    scales=[(480, 1333), (512, 1333), (544, 1333), (576, 1333),
                            (608, 1333), (640, 1333), (672, 1333), (704, 1333),
                            (736, 1333), (768, 1333), (800, 1333)],
                    keep_ratio=True)
            ],
            [
                dict(
                    type='RandomChoiceResize',
                    # The radio of all image in train dataset < 7
                    # follow the original implement
                    scales=[(400, 4200), (500, 4200), (600, 4200)],
                    keep_ratio=True),
                dict(
                    type='RandomCrop',
                    crop_type='absolute_range',
                    crop_size=(384, 600),
                    allow_negative_crop=True),
                dict(
                    type='RandomChoiceResize',
                    scales=[(480, 1333), (512, 1333), (544, 1333), (576, 1333),
                            (608, 1333), (640, 1333), (672, 1333), (704, 1333),
                            (736, 1333), (768, 1333), (800, 1333)],
                    keep_ratio=True)
            ]
        ]),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor', 'flip', 'flip_direction', 'text',
                   'custom_entities'))
]

train_dataloader = dict(
    sampler=dict(_delete_=True, type='DefaultSampler', shuffle=True),
    batch_sampler=dict(type='AspectRatioBatchSampler'),
    dataset=dict(
        _delete_=True,
        type='CocoDataset',
        data_root=data_root,
        metainfo=metainfo,
        filter_cfg=dict(filter_empty_gt=False, min_size=32),
        pipeline=train_pipeline,
        return_classes=True,
        ann_file='train/_annotations.coco.json',
        data_prefix=dict(img='train/')))

val_dataloader = dict(
    dataset=dict(
        metainfo=metainfo,
        data_root=data_root,
        return_classes=True,
        ann_file='valid/_annotations.coco.json',
        data_prefix=dict(img='valid/')))
test_dataloader = val_dataloader

val_evaluator = dict(
    type='CocoMetric',
    ann_file=data_root + 'valid/_annotations.coco.json',
    metric='bbox',
    format_only=False)
test_evaluator = val_evaluator

optim_wrapper = dict(
    _delete_=True,
    type='OptimWrapper',
    optimizer=dict(type='AdamW', lr=0.0001, weight_decay=0.0001),
    clip_grad=dict(max_norm=0.1, norm_type=2),
    paramwise_cfg=dict(custom_keys={
        'absolute_pos_embed': dict(decay_mult=0.),
        'backbone': dict(lr_mult=0.1)
    }))

# learning policy
max_epochs = 12
param_scheduler = [
    dict(
        type='MultiStepLR',
        begin=0,
        end=max_epochs,
        by_epoch=True,
        milestones=[11],
        gamma=0.1)
]
train_cfg = dict(max_epochs=max_epochs, val_interval=1)
default_hooks = dict(checkpoint=dict(max_keep_ckpts=1, save_best='auto'))

load_from = 'https://download.openmmlab.com/mmdetection/v3.0/mm_grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth'  # noqa

# _base_ = '../grounding_dino_swin-t_pretrain_obj365.py'

# data_root = 'data/Detecting-Pencils/'

# dataset_type = 'CocoDataset'
# classes = ('backpack', 'bed', 'bicycle', 'book', 'bottle', 'bowl', 'box', 'bus', 'car', 'card', 'cell phone', 'chair', 'couch', 'cup', ' desk', 'dining table', 'earbuds', 'glasses', 'handbag', 'keyboard', 'keys', 'lamp', 'laptop', 'marker', 'mouse', 'pen', 'pencil - v1 2022-04-21 11-44am', 'person', 'pillow', 'remote', 'scissors', 'shoes', 'spoon', 'tablet', 'tape', 'toilet-paper', 'trash-can', 'truck', 'tv', 'wallet')

# train_pipeline = [
#     dict(type='LoadImageFromFile'),
#     dict(type='LoadAnnotations', with_bbox=True),
#     dict(type='RandomFlip', prob=0.5),
#     dict(
#         type='RandomChoice',
#         transforms=[
#             [
#                 dict(
#                     type='RandomChoiceResize',
#                     scales=[(480, 1333), (512, 1333), (544, 1333), (576, 1333),
#                             (608, 1333), (640, 1333), (672, 1333), (704, 1333),
#                             (736, 1333), (768, 1333), (800, 1333)],
#                     keep_ratio=True)
#             ],
#             [
#                 dict(
#                     type='RandomChoiceResize',
#                     # The radio of all image in train dataset < 7
#                     # follow the original implement
#                     scales=[(400, 4200), (500, 4200), (600, 4200)],
#                     keep_ratio=True),
#                 dict(
#                     type='RandomCrop',
#                     crop_type='absolute_range',
#                     crop_size=(384, 600),
#                     allow_negative_crop=True),
#                 dict(
#                     type='RandomChoiceResize',
#                     scales=[(480, 1333), (512, 1333), (544, 1333), (576, 1333),
#                             (608, 1333), (640, 1333), (672, 1333), (704, 1333),
#                             (736, 1333), (768, 1333), (800, 1333)],
#                     keep_ratio=True)
#             ]
#         ]),
#     dict(
#         type='PackDetInputs',
#         meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
#                    'scale_factor', 'flip', 'flip_direction', 'text',
#                    'custom_entities'))
# ]

# test_pipeline = [
#     dict(
#         type='LoadImageFromFile', backend_args=None,
#         imdecode_backend='pillow'),
#     dict(
#         type='FixScaleResize',
#         scale=(800, 1333),
#         keep_ratio=True,
#         backend='pillow'),
#     dict(type='LoadAnnotations', with_bbox=True),
#     dict(
#         type='PackDetInputs',
#         meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
#                    'scale_factor', 'text', 'custom_entities',
#                    'tokens_positive'))
# ]

# train_dataloader = dict(
#     dataset=dict(
#         _delete_=True,
#         type='CocoDataset',
#         data_root=data_root,
#         ann_file='train/_annotations.coco.json',
#         data_prefix=dict(img='train/'),
#         return_classes=True,
#         filter_cfg=dict(filter_empty_gt=False, min_size=32),
#         pipeline=train_pipeline))

# # val_dataloader = dict(
# #     dataset=dict(
# #         _delete_=True,
# #         type='CocoDataset',
# #         data_root=data_root,
# #         ann_file='valid/_annotations.coco.json',
# #         data_prefix=dict(img='valid/'),
# #         return_classes=True,
# #         filter_cfg=dict(filter_empty_gt=False, min_size=32),
# #         pipeline=test_pipeline))

# val_dataloader = dict(
#     batch_size=1,
#     num_workers=2,
#     persistent_workers=True,
#     drop_last=False,
#     sampler=dict(type='DefaultSampler', shuffle=False),
#     dataset=dict(
#         type='CocoDataset',
#         data_root=data_root,
#         ann_file='valid/_annotations.coco.json',
#         data_prefix=dict(img='valid/'),
#         test_mode=True,
#         pipeline=test_pipeline,
#         return_classes=True,
#     ))


# test_dataloader = val_dataloader
# val_evaluator = dict(
#     ann_file='data/Detecting-Pencils/valid/_annotations.coco.json',
#     backend_args=None,
#     format_only=False,
#     metric='bbox',
#     type='CocoMetric')

# test_evaluator = dict(
#     ann_file='data/Detecting-Pencils/test/_annotations.coco.json',
#     backend_args=None,
#     format_only=False,
#     metric='bbox',
#     type='CocoMetric')

# optim_wrapper = dict(
#     _delete_=True,
#     type='OptimWrapper',
#     optimizer=dict(type='AdamW', lr=0.0002, weight_decay=0.0001),
#     clip_grad=dict(max_norm=0.1, norm_type=2),
#     paramwise_cfg=dict(
#         custom_keys={
#             'absolute_pos_embed': dict(decay_mult=0.),
#             'backbone': dict(lr_mult=0.1),
#             'language_model': dict(lr_mult=0.1),
#         }))
        

# # learning policy
# max_epochs = 12
# param_scheduler = [
#     dict(
#         type='MultiStepLR',
#         begin=0,
#         end=max_epochs,
#         by_epoch=True,
#         milestones=[8, 11],
#         gamma=0.1)
# ]
# train_cfg = dict(max_epochs=max_epochs, val_interval=1)

# default_hooks = dict(checkpoint=dict(max_keep_ckpts=1, save_best='auto'))

# load_from = 'https://download.openmmlab.com/mmdetection/v3.0/mm_grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth'  # noqa
