# working script with azure compute instance, !!! add all venvs to .almignore
from azureml.core import Experiment, ScriptRunConfig, Environment, Workspace
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.compute import ComputeTarget
# from azureml.core.compute import LocalCompute

# Access the workspace using config.json
ws = Workspace.from_config(".")

# Define a local compute target
# local_compute = LocalCompute(ws, name="local-compute")

# 1. Create or Get an Environment
sklearn_env = Environment("sklearn-env1")

# Define your Conda and pip dependencies
packages = CondaDependencies.create(
    conda_packages=['python=3.8', 'scikit-learn', 'pandas'],  # Specify conda packages
    pip_packages=['azureml-defaults']  # Specify pip packages
)
sklearn_env.python.conda_dependencies = packages

# Optionally, register the environment (if you want to reuse it)
sklearn_env.register(workspace=ws)

# 2. Create or Get a Compute Target
compute_target_name = 'standard-v1'
compute_target = ComputeTarget(workspace=ws, name=compute_target_name)

# 3. Create a Script Configuration
script_config = ScriptRunConfig(
    source_directory='.',  # Directory containing the script
    script='180+-+Script+To+Run.py',  # Script to run
    environment=sklearn_env,  # Environment for the run
    compute_target=compute_target  # Compute target for running the script
    # compute_target="local"  # Compute target on local machine
)

# 4. Submit and Run the Experiment
experiment = Experiment(workspace=ws, name='training-experiment')
run = experiment.submit(config=script_config)
run.wait_for_completion()