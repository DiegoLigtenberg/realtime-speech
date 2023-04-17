import argparse
import yaml

def model_parser_args():
    with open(r'utils/models.yaml') as f:
        settings = yaml.full_load(f)
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="see model_settings.yaml",default=settings)
    parser.add_argument("--model_names", help="see model_settings.yaml",default=list(settings))
    setting_list = []
    task_list = []
    for i in range(len(settings)):
        setting_list.append(list(settings[list(settings.keys())[i]].keys()))  
    for model in (list(settings.keys())):
        task = (settings[model]["task"]) 
        if task not in task_list:task_list.append(task)
        # print(model)
    setting_list = ([setting for sublist in setting_list for setting in sublist]) # generate all sublists
    setting_list = [x for i, x in enumerate(setting_list) if x not in setting_list[:i]] # remain order of sublists
    parser.add_argument("--model_settings",help="see model_settings.yaml",default=setting_list)
    parser.add_argument("--model_tasks",help="see model_settings.yaml",default=task_list)
    parser=parser.parse_args()
    return parser

if __name__ == "__main__":
    model_parser_args()

