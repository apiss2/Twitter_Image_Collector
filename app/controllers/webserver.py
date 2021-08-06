import logging
from flask import Flask, request
from flask import render_template

from app.controllers import api_func
from app.models.user import User
import settings

logger = logging.Logger(__name__)

app = Flask(
    __name__,
    static_url_path="/static/",
    static_folder="../../static/",
    template_folder='../views')


@app.route('/', methods=["GET", "POST"])
def index():
    status = 200
    if request.method == 'POST':
        if request.form['order_type'] == "registration_order":
            # TODO: 不正値が入力されてたらアラート出したい(validationの実装)
            status = api_func.registration_user(request)
        elif request.form['order_type'] == "delete_order":
            status = api_func.delete_user(request)
        elif request.form['order_type'] == "registration_fromfile_order":
            status = api_func.registration_from_file(request)
        else:
            logger.error("action=rendering_index info=OrderTypeError")
    user_list = User.get_users()
    return render_template('./index.html', user_list=user_list), status


def start():
    app.run(debug=True, host='127.0.0.1', port=settings.WEB_PORT, threaded=True)
