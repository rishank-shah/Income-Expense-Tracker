import threading
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))

account_activation_token = AppTokenGenerator()


def email_register(request,user,email):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))            
    domain = get_current_site(request).domain
    link = reverse('activate',kwargs={'uidb64':uidb64,'token':account_activation_token.make_token(user)})
    activate_url = 'http://' + domain + link
    email_subject = 'Activate your Income-Expense account'
    email_body = 'Hi ' + user.username + ". We're excited to have you get started. First, you need to confirm your account. Just press the button below.\n"
    extra_info = "You are receiving this message because you registered on " + domain +". If you didn't register please contact support team on " + domain 
    fromEmail = 'noreply@income-expense.com'
    html_content = render_to_string("partials/_email_template.html",{
        'email_html_title':'Verify Account',
        'email_title':'Welcome!',
        'email_body':email_body,
        'button_text':'Confirm Account',
        'extra_info':extra_info,
        'btn_url':activate_url,
        'help_text':"If that doesn't work, copy and paste the following link in your browser:",
        'verify_email':True
    })
    text_content = strip_tags(html_content)
    EmailThread(email_subject, text_content, fromEmail,email,html_content).start()


class EmailThread(threading.Thread):

    def __init__(self,email_subject, text_content, fromEmail,to,html_content):
        self.email_subject = email_subject
        self.text_content = text_content
        self.fromEmail = fromEmail
        self.receiver = to
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.email_subject,
            self.text_content,
            self.fromEmail,
            [self.receiver],
            html_message = self.html_content
        )