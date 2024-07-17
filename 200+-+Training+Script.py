# ------------------------------------------------------------------
# Predict the Loan Status using Logistic Regression in scikit-learn
# ------------------------------------------------------------------
# use service principal
# az ad sp create-for-rbac --name td_principal --role Contributor --scopes //subscriptions/'9d1e7df0-a4cd-45d3-94d0-9c9208ce45ee'
# note the double slash //, one slash doesn't work

# Import required classes from Azureml
from azureml.core import Workspace, Run, Datastore, Dataset

from azureml.core.authentication import ServicePrincipalAuthentication

# Define the service principal credentials

import json
# Load the configuration file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
tenant_id = config.get('tenant_id') #"your-tenant-id"
service_principal_id = config.get('tenant_id') #"your-app-id"
service_principal_password = config.get('tenant_id')


# Authenticate using the service principal
sp_auth = ServicePrincipalAuthentication(
    tenant_id=tenant_id,
    service_principal_id=service_principal_id,
    service_principal_password=service_principal_password
)


# Access the Workspace
ws = Workspace.get(name="AzureMLWS01",
                   subscription_id="9d1e7df0-a4cd-45d3-94d0-9c9208ce45ee",
                   resource_group="teodora.davidkova-rg",
                   auth=sp_auth)
# ws = Workspace.from_config(".")

# Get the context of the experiment run
new_run = Run.get_context()


# -----------------------------------------------------
# Do your stuff here
# -----------------------------------------------------
import pandas as pd

# -----------------------------------------------------
# Access the Workspace, Datastore and Datasets
# -----------------------------------------------------
# ws                = Workspace.from_config(".")
az_store          = Datastore.get(ws, 'cont01')
az_dataset        = Dataset.get_by_name(ws, 'Loan Applications Using SDK')
az_default_store  = ws.get_default_datastore()

# -----------------------------------------------------
# Load the Azureml Dataset into the pandas dataframe
# -----------------------------------------------------
df = az_dataset.to_pandas_dataframe()
print(ws.datasets.get('Defaults'))
print(az_default_store)

# Load the data from the local files
df = pd.read_csv("./data/Loan+Data.csv")

# Select columns from the dataset
LoanPrep = df[["Married", 
             "Education",
             "Self_Employed",
             "ApplicantIncome",
            #  "LoanAmount",
            #  "Loan_Amount_Term",
            #  "Credit_History",
             "Loan_Status"
             ]]

# Clean Missing Data - Drop the columns with missing values
LoanPrep = LoanPrep.dropna()
print(len(LoanPrep))


# Create Dummy variables - Not required in designer
LoanPrep = pd.get_dummies(LoanPrep, drop_first=True)
print(LoanPrep.columns)
print(LoanPrep['Loan_Status_Y'].value_counts())
print("Check freqs")

# Create X and Y - Similar to "edit columns" in Train Module
Y = LoanPrep[['Loan_Status_Y']]
X = LoanPrep.drop(['Loan_Status_Y'], axis=1)


# Split Data - X and Y datasets are training and testing sets
from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 1253, stratify=Y)
print("Random seed 1253")


# Build the Logistic Regression model
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()


# Fit the data to the LogisticRegression object - Train Model
lr.fit(X_train, Y_train)


# Predict the outcome using Test data - Score Model 
# Scored Label
Y_predict = lr.predict(X_test)

# Get the probability score - Scored Probabilities
Y_prob = lr.predict_proba(X_test)[:, 1]

# Get Confusion matrix and the accuracy/score - Evaluate
from sklearn.metrics import confusion_matrix
cm    = confusion_matrix(Y_test, Y_predict)
score = lr.score(X_test, Y_test)


# -----------------------------------------------------
# Log metrics and Complete an experiment run
# -----------------------------------------------------

# Create the confusion matrix dictionary
cm_dict = {"schema_type": "confusion_matrix",
           "schema_version": "v1",
           "data": {"class_labels": ["N", "Y"],
                    "matrix": cm.tolist()}
           }

new_run.log("TotalObservations", len(df))
new_run.log_confusion_matrix("ConfusionMatrix", cm_dict)
new_run.log("Score", score)


# Create the Scored Dataset and upload to outputs
# -----------------------------------------------
# Test data - X_test
# Actual Y - Y_test
# Scored label
# Scored probabilities

X_test = X_test.reset_index(drop=True)
Y_test = Y_test.reset_index(drop=True)

Y_prob_df    = pd.DataFrame(Y_prob, columns=["Scored Probabilities"]) 
Y_predict_df = pd.DataFrame(Y_predict, columns=["Scored Label"]) 

scored_dataset = pd.concat([X_test, Y_test, Y_predict_df, Y_prob_df],
                           axis=1)


# Upload the scored dataset
scored_dataset.to_csv("./outputs/loan_scored.csv",
                      index=False)


# Complete the run
new_run.complete()

















