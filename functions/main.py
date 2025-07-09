from flask import Flask, request, jsonify, render_template
from firebase_functions import https_fn
from linebot import line_bp
from hplicense import lp_bp

import requests
import json
import os

app = Flask(__name__)

app.register_blueprint(line_bp)

@https_fn.on_request()
def flask_service(req: https_fn.Request) -> https_fn.Response:
    with app.request_context(req.environ):
        return app.full_dispatch_request()
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
    