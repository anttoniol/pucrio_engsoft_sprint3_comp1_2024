from flask import Flask,jsonify,request
from flask_swagger_ui import get_swaggerui_blueprint
import service

SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Events API'
    }
)

app = Flask(__name__)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@app.route("/healthcheck")
def health_check():
    return jsonify({
        "Message": "The Events API is running successfully"
    })


@app.route("/<id>", methods=["GET"])
def get_event(id):

    event_data = service.get(id)

    return jsonify({
        "id": id
    })


@app.route("/", methods=["POST"])
def save_event():
    data = request.get_json()
    service.save(data)

    return jsonify({
        "Message": "test"
    })


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)