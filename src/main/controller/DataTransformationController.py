from flask import Flask
from src.main.service.DataAccessService import DataAccessService
# The Data Transformation controller, transforms the data from various datasources into standardised JSON format


class DataTransformationController:

    app = Flask(__name__)

    @app.route("/")
    def transform():
        return DataAccessService.get_data()

    if __name__ == "__main__":
        app.run(debug=True)
