from pprint import pformat
from flask import render_template, url_for, g, redirect, url_for, session

from tunnistamo_client import app, oidc, tunnistamo_oauth


@app.route('/oidc_login')
@oidc.require_login
def oidc_login():
    return render_template('login.html',
                           login_method='OIDC',
                           access_token=oidc.get_access_token(),
                           user_data=pformat(g.oidc_id_token),
                           logout=url_for('oidc_logout'))

@app.route('/oauth2_login')
def oauth2_login():
    if 'tunnistamo_token' not in session:
        return tunnistamo_oauth.authorize(callback=url_for('oauth2_login_callback', _external=True))
    return render_template('login.html',
                           login_method='OAuth2',
                           access_token=session['tunnistamo_token'],
                           user_data=pformat(tunnistamo_oauth.get('user').data),
                           logout=url_for('oauth2_logout'))

@app.route('/oauth2_login/callback')
def oauth2_login_callback():
    resp = tunnistamo_oauth.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return redirect(url_for('index'))
    session['tunnistamo_token'] = (resp['access_token'], resp.get('refresh_token'))
    return redirect(url_for('oauth2_login'))
