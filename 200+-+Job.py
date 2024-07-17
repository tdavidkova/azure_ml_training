# ------------------------------------------------------------
# Run a script in an Azureml environment
# ------------------------------------------------------------
# This code will submit the script provided in ScriptRunConfig
# and create an Azureml environment on the local machine
# including the docker for Azureml
# ------------------------------------------------------------


# Import the Azure ML classes
from azureml.core import Workspace, Experiment, ScriptRunConfig
from azureml.core.compute import ComputeTarget
from azureml.core.authentication import ServicePrincipalAuthentication


# Access the workspace using config.json
ws = Workspace.from_config(".")


# Create/access the experiment from workspace 
new_experiment = Experiment(workspace=ws,
                            name="Training_Job")


# -------------------------------------------------
# Create custom environment
from azureml.core import Environment
from azureml.core.environment import CondaDependencies

# Create the environment
myenv = Environment(name="MyEnvironment")

# Create the dependencies object
myenv_dep = CondaDependencies.create(conda_packages=['scikit-learn', 'pandas', 'numpy'])
myenv.python.conda_dependencies = myenv_dep

# Register the environment
myenv.register(ws)

# 2. Create or Get a Compute Target
compute_target_name = "my-cluster-001"
compute_target = ComputeTarget(workspace=ws, name=compute_target_name)
# -------------------------------------------------

# Create a script configuration for custom environment of myenv
script_config = ScriptRunConfig(source_directory=".",
                                script="200+-+Training+Script.py",
                                environment=myenv,
                                compute_target=compute_target 
                                )


# Submit a new run using the ScriptRunConfig
new_run = new_experiment.submit(config=script_config)


# Create a wait for completion of the script
new_run.wait_for_completion()















