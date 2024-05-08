from email_sender import send_email

from flask import request
import logging

from flask import Flask, render_template
from gunicorn.app.base import BaseApplication

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template("email_form.html")

@app.route("/send-email", methods=['POST'])
def send_email_route():
    subject = request.form['subject']
    body = request.form['body']
    recipient = "vendor@example.com"  # TODO: Make recipient email dynamic
    send_email(subject, body, recipient)
    return "Email sent successfully!"


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.application = app
        self.options = options or {}
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


# Do not remove the main function while updating the app.
if __name__ == "__main__":
    options = {"bind": "%s:%s" % ("0.0.0.0", "8080"), "workers": 4, "loglevel": "info", "accesslog": "-"}
    StandaloneApplication(app, options).run()
