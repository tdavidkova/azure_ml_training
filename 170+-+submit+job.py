# ------------------------------------------------------------
# Run a script in an Azureml environment
# ------------------------------------------------------------
# This code will submit the script provided in ScriptRunConfig
# and create an Azureml environment on the local machine
# including the docker for Azureml
# ------------------------------------------------------------

# Import the Azure ML classes
from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment
from azureml.core.runconfig import RunConfiguration
# when taking a snapshot of the project the venv folders get too large, increase limit size,
# the neater solution is to add .amlignore file in the project directory
import azureml._restclient.snapshots_client
azureml._restclient.snapshots_client.SNAPSHOT_MAX_SIZE_BYTES = 2000000000

from azureml.core.conda_dependencies import CondaDependencies


# # Define Conda dependencies
# conda_dep = CondaDependencies()
# conda_dep.add_conda_package("python=3.8.13")
# conda_dep.add_pip_package("azureml-core")
# conda_dep.add_pip_package("azureml-sdk-core")
# conda_dep.add_pip_package("pandas")

# Access the workspace using config.json
ws = Workspace.from_config(".")


# Create/access the experiment from workspace 
new_experiment = Experiment(workspace=ws,
                            name="Loan_Script")

from pathlib import Path

requirements_path = Path("./requirements.txt").resolve()
environment = Environment.from_pip_requirements(
    name="xthenv", file_path=requirements_path
)
print(environment)
environment.register(workspace=ws)

# Create an environment
# myenv = Environment(name="venv311")

# # Define dependencies properly
# dependencies = ['python=3.8.13', 
#                 'pip',
#                 {'pip': ["azureml-core", "azureml-sdk-core", "pandas"]}]

# Create a new environment
# myenv = Environment(name="nthenv")
# myenv.python.conda_dependencies
# myenv.python.conda_dependencies = conda_dep

# Create a new environment
# myenv = Environment.from_pip_requirements(name="myvenv", file_path="./requirements.txt")


# # Register the environment
# myenv.register(workspace=ws)

# print(f"Environment '{myenv.name}' registered.")

# # List all environments in the workspace to verify registration
# envs = Environment.list(workspace=ws)
# print("Available environments in the workspace:")
# for env_name in envs:
#     print(env_name)

# env_name = "nthenv"  # Replace with your environment name

# # Try to get the environment by name
# try:
#     myenv = Environment.get(workspace=ws, name=env_name)
#     print(f"Retrieved environment: {myenv.name}")
# except Exception as e:
#     print(f"Failed to retrieve environment: {e}")


# # Print the environment details
# print(f"Environment name: {myenv.name}")
# print(f"Environment version: {myenv.version}")

# # Print the Python packages and versions in the environment
# if myenv.python.conda_dependencies:
#     print("\nConda Dependencies:")
#     print(myenv.python.conda_dependencies.serialize_to_string())

# # Set user_managed_dependencies to True
# myenv.python.user_managed_dependencies = True

# # Set up the run configuration
# run_config = RunConfiguration()
# # myenv = Environment.get(workspace=ws, name="myenv")
# run_config.environment = myenv
# # run_config.environment.python.user_managed_dependencies = True


# # Create a script configuration
# script_config = ScriptRunConfig(source_directory=".",
#                                 script="180+-+Script+To+Run.py",
#                                 run_config=run_config)

Environment.build


# # Submit a new run using the ScriptRunConfig
# new_run = new_experiment.submit(config=script_config)


# # Create a wait for completion of the script
# new_run.wait_for_completion()















