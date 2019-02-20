from urllib.parse import urlencode
from flask import request, redirect, url_for, session
import httplib2

from tunnistamo_client import app, oidc, tunnistamo_oauth

@app.route('/oidc_logout')
def oidc_logout():
    if oidc.user_loggedin:
        token = request.cookies.get(app.config['OIDC_ID_TOKEN_COOKIE_NAME'])
        extra_params = {
            'id_token_hint': token,
            'post_logout_redirect_uri': url_for('index', _external=True),
        }
        logout_url = '{url}?{extra_params}'.format(
            url=oidc.flow_for_request().revoke_uri,
            extra_params=urlencode(extra_params)
        )
        oidc.logout()
        return redirect(logout_url)
    else:
        return redirect(url_for('index'))

@app.route('/oauth2_logout')
def oauth2_logout():
    token = session.pop('tunnistamo_token', (None, None))
    if token:
        http = httplib2.Http()
        resp, content = http.request(
            tunnistamo_oauth.revoke_url,
            'POST',
            body=urlencode({
                'token': token[1] if token[1] is not None else token[0],
                'token_type_hint': 'refresh_token' if token[1] is not None else 'access_token',
                'client_id': tunnistamo_oauth.consumer_key,
                'client_secret': tunnistamo_oauth.consumer_secret
            }),
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
    return redirect(url_for('index'))
