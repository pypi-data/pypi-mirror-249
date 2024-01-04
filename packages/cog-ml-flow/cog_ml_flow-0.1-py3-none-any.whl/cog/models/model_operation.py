import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.datasets import load_diabetes


def create_model(model_name, model_path):
    # Train a simple Linear Regression model
    model = LinearRegression()

    # Load the diabetes dataset
    diabetes = load_diabetes()
    X, y = diabetes.data, diabetes.target

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Log the model with MLflow
    mlflow.sklearn.log_model(model, model_path, registered_model_name=model_name)

    # Save the model as an artifact
    # mlflow.sklearn.save_model(model, model_path)


def search_run_id_of_reg_model(model_name):
    # Search for registered models in MLflow
    print(mlflow.search_registered_models())
    for model in mlflow.search_registered_models():
        if model_name == model.name:
            print("Registered Models:")
            print(model)
        else:
            print("Model Not Found:")


def train_model(run_name, model_name, model_path):
    # Load the diabetes dataset
    diabetes = load_diabetes()
    X, y = diabetes.data, diabetes.target

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Calculate and log the Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)
    mlflow.log_metric("mse", mse)

    # Log the trained model with MLflow
    # model_uri='models:/diabetes_model/<model_version/stage/latest'
    run_id = mlflow.active_run().info.run_id
    model_path1 = f"{run_id}/models/{model_name}"
    # with mlflow.active_run().info.run_id:
    mlflow.sklearn.log_model(model, model_name, registered_model_name=model_name)

    # Register the trained model with MLflow
    mlflow.register_model("runs:/{}/model".format(mlflow.active_run().info.run_id), name=model_name)

    # Save the model as an artifact
    # mlflow.sklearn.save_model(model, model_path)


if __name__ == "__main__":
    # Set the MLflow tracking URI (replace with your MLflow server URI)
    mlflow.set_tracking_uri("http://127.0.0.1:5000")

    # Start an MLflow run
    with mlflow.start_run(run_name="diabetes_experiment"):
        # Create and log a model
        create_model("diabetes_model", "models/diabetes_model")

        # Search for registered models
        search_run_id_of_reg_model('diabetes_model')

        # Train and log a model
        #train_model("diabetes_run", "diabetes_model", "models/diabetes_model")
