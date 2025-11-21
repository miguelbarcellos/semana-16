from threading import Thread
from flask import current_app, render_template
import requests

def send_async_sendgrid(app, to, subject, html):
    with app.app_context():
        api_key = app.config['SENDGRID_API_KEY']
        from_email = app.config['SENDGRID_FROM']

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "personalizations": [{
                "to": [{"email": to}],
                "subject": subject
            }],
            "from": {"email": from_email},
            "content": [{
                "type": "text/html",
                "value": html
            }]
        }

        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers=headers,
            json=data
        )

        print("STATUS DO SENDGRID:", response.status_code, flush=True)
        print("RESPOSTA:", response.text, flush=True)

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()

    subject = f"{app.config['FLASKY_MAIL_SUBJECT_PREFIX']} {subject}"

    html = render_template(template + '.html', **kwargs)

    thr = Thread(target=send_async_sendgrid, args=[app, to, subject, html])
    thr.start()
    return thr

