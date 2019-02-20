from flask import Flask, redirect, url_for, render_template, session
from flask_oidc import OpenIDConnect
from flask_oauthlib.client import OAuth

app = Flask('tunnistamo_client')

app.config.update({
    'SECRET_KEY': '********',
    'OIDC_CLIENT_SECRETS': 'tunnistamo_oidc.json',
    'OIDC_SCOPES': ['openid', 'profile'],
    'OIDC_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True,
})

oidc = OpenIDConnect(app)

oauth = OAuth()
tunnistamo_oauth = oauth.remote_app('tunnistamo',
    consumer_key='tunnistamo_client',
    consumer_secret='********',
    request_token_params={'scope': 'read'},
    base_url='http://localhost:8000/oauth2',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='http://localhost:8000/oauth2/token/',
    authorize_url='http://localhost:8000/oauth2/authorize/'
)
tunnistamo_oauth.revoke_url = 'http://localhost:8000/oauth2/revoke_token/'

import tunnistamo_client.login
import tunnistamo_client.logout

@app.route("/")
def index():
    if oidc.user_loggedin:
        return redirect(url_for('oidc_login'))
    if 'tunnistamo_token' in session:
        return redirect(url_for('oauth2_login'))
    return render_template('index.html',
                           oidc_login=url_for('oidc_login'),
                           oauth2_login=url_for('oauth2_login'))

@tunnistamo_oauth.tokengetter
def get_tunnistamo_token():
    return session.get('tunnistamo_token')
