# -------------------------------------------------------------
# Consume the service end point using workspace access.
# -------------------------------------------------------------

# Import the Azure ML classes
from azureml.core import Workspace

# Access the workspace using config file
print("Accessing the workspace....")
import json
# Load the configuration file
print("Accessing the workspace from job....")
with open('./config.json', 'r') as config_file:
    config = json.load(config_file)

print(config)
# Extract the account key from the configuration
storage_account_key = config.get('storage_account_key')
ws = Workspace(subscription_id=config.get('subscription_id'),
               workspace_name=config.get('workspace_name'),
               resource_group=config.get('resource_group'))
print(ws.name)


# Access the service end points
print("Accessing the service end-points")
service = ws.webservices['adultincome-service']


# Prepare the input data
import json

x_new = {'age':[46],
         'workclass':['Private'],
         'education':['Masters'],
         'marital_status':['Married-civ-spouse'],
         'hours per week':[60]}

# Convert the dictionary to a serializable list in json
json_data = json.dumps({"data": x_new})

# Call the web service
print("Calling the service...")
response = service.run(input_data = json_data)

# Collect and convert the response in local variable
print("Printing the predicted class...")
predicted_classes = json.loads(response)

print('\n', predicted_classes)




   
    
    