from roboflow import Roboflow
rf = Roboflow(api_key="GthT1k7M9FgAEJOGvJnD")
project = rf.workspace("capstone-5zojy").project("detecting-pencils")
version = project.version(1)
dataset = version.download("yolov8")

# save the dataset to a folder
print("saved dataset to", dataset.location)


                
            
                