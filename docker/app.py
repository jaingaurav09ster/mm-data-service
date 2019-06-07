from flask import Flask
from flask import jsonify
from docker.DataAccessService import DataAccessService
import json

app = Flask(__name__)


@app.route('/')
def get_query_result():
    return jsonify(get_records())


def get_records():
        try:
            data_access_service = DataAccessService()
            rows = json.loads(data_access_service.get_queried_results())
            return rows
        except Exception as error:
            print(error)
            return "Not able to connect, connection parameters are wrong, Cause:"+str(error)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

