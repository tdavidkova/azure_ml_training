# -----------------------------------------------------------------
# Register the model from workspace using run_id and local pkl file
# -----------------------------------------------------------------
from azureml.core import Workspace, Model, Experiment


# Access the workspace using config.json
import json
# Load the configuration file
with open('./config.json', 'r') as config_file:
    config = json.load(config_file)

print(config)
# Extract the account key from the configuration
storage_account_key = config.get('storage_account_key')
ws = Workspace(subscription_id=config.get('subscription_id'),
               workspace_name=config.get('workspace_name'),
               resource_group=config.get('resource_group'))
print(ws.name)

experiment = Experiment(workspace=ws, name='Webservice-exp001')
print(list(experiment.get_runs()))

# Access the run using run_id
new_run = ws.get_run('e818887f-47de-4b29-ae0a-054b43221bf6')



# --------------------------------------------------------------------
# Register the model using the run object and uploaded pkl file
# --------------------------------------------------------------------
new_run.register_model(model_path='outputs/models.pkl', 
                       model_name='AdultIncome_models',
                       tags={'source':'SDK Run', 'algorithm':'RandomForest'},
                       properties={'Accuracy': new_run.get_metrics()['accuracy']},
                       description="Combined Models from Run")


# --------------------------------------------------------------------
# Register the model using Model Class and Local pkl file
# --------------------------------------------------------------------
from azureml.core import Model

Model.register(workspace=ws,
               model_path='./outputs/models.pkl', # local path
               model_name='AdultIncome_model_local',
               tags={'source':'SDK-Local', 'algorithm':'RandomForest'},
               properties={'Accuracy': 0.7866},
               description='AdultIncome model from Local'
               )


# --------------------------------------------------------------------
# Retrieve the registered models
# --------------------------------------------------------------------
Model.list(ws)


for model in Model.list(ws):
    
    print('\n', model.name, 'version:', model.version)
    print('\t', 'Run_ID : ', model.run_id)
    for prop_name in model.properties:
        prop = model.properties[prop_name]
        print ('\t',prop_name, ':', prop)
    
    for tags in model.tags:
        tag = model.tags[tags]
        print ('\t',tags, ':', tag)





