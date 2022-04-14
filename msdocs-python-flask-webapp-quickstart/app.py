import os
import pprint
from datetime import datetime

from azure.identity._credentials import ManagedIdentityCredential
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


def get_token():
    # logging.info(f"Getting token for managed identity")
    # print('here', os.environ["IDENTITY_ENDPOINT"])
    #   pprint.pprint(list(os.environ.items()))
    default_credential = ManagedIdentityCredential()
    # default_credential = DefaultAzureCredential(managed_identity_client_id='dd3d6c47-2893-4054-ae9c-ef5a40aef484')
    token = default_credential.get_token(
        "https://ossrdbms-aad.database.windows.net/.default").token
    # logging.info(f"Token aquired")
    print(token)
    return token


@app.route('/')
def index():
    print('Request for index page received')
    get_token()
    return render_template('index.html')


@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('name')

    if name:
        print('Request for hello page received with name=%s' % name)
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
