import fiftyone as fo
import fiftyone.zoo as foz

name = "coco-2017"
dataset = foz.load_zoo_dataset(name, split="validation")
session = fo.launch_app(dataset)

session.wait()