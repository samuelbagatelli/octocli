import os


path = os.path.dirname(__file__)
path = f"{path}/templates/models"

stdpath = f"{path}/standard.py"

with open(stdpath) as f:
    content = f.read()

    content = content.replace("{{ class_name }}", "ClassName")
    content = content.replace("{{ model_name }}", "model_name")

    print(content)
