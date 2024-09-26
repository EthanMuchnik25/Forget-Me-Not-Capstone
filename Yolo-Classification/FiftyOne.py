import fiftyone as fo
import fiftyone.zoo as foz

name = "coco-2017"
dataset = foz.load_zoo_dataset(name, split="validation", max_samples=100)
session = fo.launch_app(dataset)

session.wait()