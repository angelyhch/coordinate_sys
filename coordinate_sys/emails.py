from threading import Thread
from flask import url_for, current_app
from flask_mail import Message

from coordinate_sys.extensions import mail


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, html=None, body=None):
    app = current_app._get_current_object()
    message = Message(subject, recipients=to)
    message.html = html
    message.body = body
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr
