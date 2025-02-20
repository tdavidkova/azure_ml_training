# --------------------------------------------------------------------
# Create and run an AutoML Experiment using SDK
# The steps required are,
#
# 1. Access the workspace
# 2. Get the input data either from the workspace or other data source
# 3. Create or access the compute cluster
# 4. Configure the AutoML
# 5. Submit the AutoML experiment
# --------------------------------------------------------------------

# --------------------------------------------------------------------
# Connect and access the workspace
# --------------------------------------------------------------------

# Import the Workspace class
from azureml.core import Workspace

import json
with open ("./config.json") as file:
    data = json.load(file)

# Access the workspace from the config.json 
print("Accessing the workspace...")
# ws = Workspace.from_config(path="./config")
# AVOID CONFUSION WITH OTHER CONFIG FILES THAT MIGHT BE SAVED SOMEWHERE IN PARENT/CHILD DIRECTORIES
ws = Workspace(subscription_id=data['subscription_id'],
               workspace_name=data['workspace_name'],
               resource_group=data['resource_group'])
print(ws.name)

# Get the input data from the workspace
print("Accessing the dataset...")
input_ds = ws.datasets.get('Defaults')



# --------------------------------------------------------------------
# Create the compute Cluster 
# --------------------------------------------------------------------
# Specify the cluster name
cluster_name = "my-cluster-001"

# Provisioning configuration using AmlCompute
from azureml.core.compute import AmlCompute

print("Accessing the compute cluster...")

if cluster_name not in ws.compute_targets:
    print("Creating the compute cluster with name: ", cluster_name)
    compute_config = AmlCompute.provisioning_configuration(
                                     vm_size="STANDARD_D11_V2",
                                     max_nodes=2)

    cluster = AmlCompute.create(ws, cluster_name, compute_config)
    cluster.wait_for_completion()
else:
    cluster = ws.compute_targets[cluster_name]
    print(cluster_name, ", compute cluster found. Using it...")



# --------------------------------------------------------------------
# Configure the AutoML run
# --------------------------------------------------------------------

from azureml.train.automl import AutoMLConfig

print("Creating the AutoML Configuration...")

automl_config = AutoMLConfig(task='classification',
                             compute_target=cluster,
                             training_data=input_ds,
                             validation_size=0.3,
                             label_column_name='Default Next Month',
                             primary_metric='norm_macro_recall',
                             iterations=10,
                             max_concurrent_iterations=2,
                             experiment_timeout_hours=0.25,
                             featurization='auto')

# --------------------------------------------------------------------
# Create and submit the experiment
# --------------------------------------------------------------------

from azureml.core.experiment import Experiment

new_exp = Experiment(ws, 'azureml-sdk-exp-001')

print("Submitting the experiment....")

new_run = new_exp.submit(automl_config)
new_run.wait_for_completion(show_output=True)


# Retrieve the best model
new_run.get_best_child(metric='accuracy')


# Get the metrics for all the runs
for run in new_run.get_children():
    print("")
    print("Run ID : ", run.id)
    print(run.get_metrics('accuracy'))
    print(run.get_metrics('norm_macro_recall'))










