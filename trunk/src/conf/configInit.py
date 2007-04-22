import confManager
import os

main_config = confManager.config()

def grab_class_config():
    number_of_classes = main_config.confParser.getint("Classes", "number_of_classes")
    classList = []
    hrClassList = []
    for number in range(1, number_of_classes+1):
        hrClassList.append(main_config.get_option("Classes", str(number)))
    return hrClassList

def grab_file_locations():
    taskFile = main_config.get_option("Files", "taskFile")
    classesFile = os.path.expanduser(main_config.get_option("Files", "classesFile"))
    return [taskFile, classesFile]