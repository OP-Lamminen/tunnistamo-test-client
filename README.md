# Tunnistamo Test Client

Very simple Flask app acting as a test client to Tunnistamo authentication provider. Don't use anywhere near the production.

## Prerequisites
 * flask
 * flask_oidc
 * flask_oauthlib
 * Tunnistamo test instance running somewhere, e.g. localhost:8000

## Setup
The configuration is contained in two places. OIDC configuration is located in `tunnistamo_oidc.json` and OAuth2 configuration is located in `tunnistamo_client/__init__.py`.

You need to add OIDC provider and OAuth2 provider clients to your Tunnistamo test instance and then add the respsective keys, secrets and URLs to the above files.

## Running

#### Run the test server on port 4000
```
$ FLASK_ENV=development flask run -h localhost -p 4000
```

#### If your test environment doesn't use HTTPS
```
$ OAUTHLIB_INSECURE_TRANSPORT=1 FLASK_ENV=development flask run -h localhost -p 4000
```

#### If you don't want to bother with debug PIN
```
$ WERKZEUG_DEBUG_PIN=off FLASK_ENV=development flask run -h localhost -p 4000
```
