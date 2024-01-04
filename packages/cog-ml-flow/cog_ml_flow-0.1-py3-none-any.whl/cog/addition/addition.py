from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from mlflow.models import infer_signature


class Test:
    def findsum(self, a, b):
        s = a + b
        return s

    # def ml_flow_test(self):
    #     mlflow.set_tracking_uri("http://localhost:8080")
    #     mlflow.set_experiment("EXP1")
    #     with mlflow.start_run() as run:
    #         X, y = make_regression(n_features=4, n_informative=2, random_state=0, shuffle=False)
    #         X_train, X_test, y_train, y_test = train_test_split(
    #             X, y, test_size=0.2, random_state=42
    #         )
    #         params = {"max_depth": 2, "random_state": 42}
    #         model = RandomForestRegressor(**params)
    #         model.fit(X_train, y_train)
    #
    #         # Infer the model signature
    #         y_pred = model.predict(X_test)
    #         signature = infer_signature(X_test, y_pred)
    #
    #         # Log parameters and metrics using the MLflow APIs
    #         mlflow.log_params(params)
    #         mlflow.log_metrics({"mse": mean_squared_error(y_test, y_pred)})
    #
    #         # Log the sklearn model and register as version 1
    #         mlflow.sklearn.log_model(
    #             sk_model=model,
    #             artifact_path="sklearn-model",
    #             signature=signature,
    #             registered_model_name="sk-learn-random-forest-reg-model",
    #         )
    #         print(f"Run ID: {run.info.run_id}")
    def train_model(X, y):
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a scikit-learn model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions on the test set
        y_pred = model.predict(X_test)

        # Calculate and print the Mean Squared Error
        mse = mean_squared_error(y_test, y_pred)
        print(f"Mean Squared Error: {mse}")

        # Log the model with MLflow
        with mlflow.start_run():
            # Log model parameters and metrics
            mlflow.log_param("model_type", "LinearRegression")
            mlflow.log_metric("mse", mse)

            # Save the scikit-learn model to MLflow
            mlflow.sklearn.log_model(model, "model")

        return model

if __name__ == '__main__':
    t = Test()
    t.train_model()
