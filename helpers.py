from flask_mail import Message


def send_mail(subject, recipient, body):
    from app import mail
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)

def send_message_received_notification(body):
    from app import mail
    msg = Message("Contact form message received", recipients=["support@cogni-bridge.studio"])
    msg.html = body
    mail.send(msg)