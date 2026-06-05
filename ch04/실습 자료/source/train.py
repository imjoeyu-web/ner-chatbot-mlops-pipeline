import pandas as pd
from sqlalchemy import create_engine

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

from airflow.models import Variable
import bentoml
import mlflow

if(Variable.get("isProd") == "true"):
    mlflow.set_tracking_uri(uri="http://mlflow-server:5000")
    mlflow.set_experiment("fraud_detection")

def build_model(**kwargs):
    with mlflow.start_run():
        if(Variable.get("isProd") == "true"):
            mlflow.autolog()
            engine = create_engine("postgresql+psycopg2://" + Variable.get("db_username") + ":" + Variable.get("db_password") + "@" + Variable.get("db_host") + ":" + Variable.get("db_port") + "/" + Variable.get("db_name"))
            data = pd.read_sql("select * from public.sample_data", engine)
        else:
            data = pd.read_csv('/opt/airflow/dags/sample_data/Fraud.csv')

        data.head()
        data.info()
        data.describe()

        #checking for null values
        data.isna().sum()

        #checking for duplicates
        data.drop_duplicates(inplace=True)

        # creating new colums and deleting the old columns
        data['balanceOrg']=data['oldbalanceOrg']-data['newbalanceOrig']
        data['balanceDest']=data['oldbalanceDest']-data['newbalanceDest']
        data.drop(['oldbalanceDest','oldbalanceOrg','newbalanceOrig','newbalanceDest'],axis=1,inplace=True)

        # Select the independent variables of interest
        ind_col= ['step','amount', 'isFraud','isFlaggedFraud','balanceOrg','balanceDest']

        # Create a correlation matrix
        corr_matrix = data[ind_col].corr()

        # Data Preprocessing
        #checking for outliers
        numerical_columns = ['step','amount','balanceOrg','balanceDest']

        # Initialize a dictionary to store the number of outliers for each column
        outliers_count = {}
        for col in numerical_columns:
            # Calculate the IQR for each numerical column
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1

            # Identify potential outliers using the IQR method
            outliers = ((data[col] < (Q1 - 1.5 * IQR)) |
                        (data[col] > (Q3 + 1.5 * IQR)))
             # Count the number of outliers for the current column
            num_outliers = outliers.sum()

            # Store the count in the dictionary
            outliers_count[col] = num_outliers

        # Display the number of outliers for each column
        for col, count in outliers_count.items():
            print(f"Number of outliers in column '{col}': {count}")


        #  One-hot encoding
        data = pd.get_dummies(data, columns=['type'])

        from sklearn.preprocessing import LabelEncoder
        labelencoder = LabelEncoder()
        data['nameOrig'] = labelencoder.fit_transform(data['nameOrig'])
        data['nameDest'] = labelencoder.fit_transform(data['nameDest'])

        # Split the data into features (X) and target (y)
        X = data.drop('isFraud', axis=1)
        y = data['isFraud']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Feature Scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.fit_transform(X_test)

        # Initialize and train the Logistic Regression model
        model = LogisticRegression(max_iter=500)
        model.fit(X_train_scaled, y_train)

        # Make predictions on the test data
        y_pred = model.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred) *100
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)

        print(f'Accuracy: {accuracy}')
        print(f'Precision: {precision}')
        print(f'Recall: {recall}')
        print(f'F1 Score: {f1}')
        print(f'ROC AUC: {roc_auc}')
        print(f'Confusion Matrix:\n{conf_matrix}')

        train_score = model.score(X_train_scaled,y_train) * 100
        test_score = model.score(X_test_scaled,y_test) * 100

        if(Variable.get("isProd") == "true"):
            mlflow.sklearn.log_model(model, "fraud_detection")

        bento_model = bentoml.sklearn.save_model("fraud_detection",
                                        model,
                                        signatures={"predict": {"batchable": True}},
                                        )
        print(f"Model saved: {bento_model}")

        # Test running inference with BentoML runner
        test_runner = bentoml.sklearn.get("fraud_detection:latest").to_runner()
        test_runner.init_local()
        test_input = [[278, 330218.42, 5144186, 523341, 0, -330218.42, 330218.42, True, False, False, False, False]]
        assert test_runner.predict.run(test_input) == model.predict(test_input)