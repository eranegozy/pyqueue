#!/usr/bin/python3

from flask import Flask, request, jsonify, send_file
import random

app = Flask(__name__)

help_queue = []
checkoff_queue = []


@app.route('/')
def index():
    index_file = 'www/index.html'
    return send_file(index_file)


@app.route('/scripts.js')
def js():
    js_file = 'www/scripts.js'
    return send_file(js_file)


@app.route('/queue/help', methods=['GET', 'POST'])
def help_queue_manager():
    msg = ''
    if request.method == 'POST':
        first_name = request.values.get('first_name')
        last_name = request.values.get('last_name')
        kerberos = request.values.get('kerberos')
        remove = True if request.values.get('remove') == 'true' else False
        if kerberos and first_name and last_name:
            entry = (first_name, last_name, kerberos)
            if remove and entry in help_queue:
                help_queue.remove(entry)
                msg = 'removed from queue'
            elif entry not in help_queue:
                help_queue.append(entry)
                msg = 'added to queue'
            else:
                msg = 'already added to queue'
            return jsonify({'message': msg})
        else:
            msg = 'missing queue data'
    else:
        return jsonify({'help_queue': help_queue, 'message':msg})

    return jsonify({'error_code': 400, 'message': msg})


@app.route('/queue/checkoff', methods=['GET', 'POST'])
def checkoff_queue_manager():
    msg = ''
    if request.method == 'POST':
        first_name = request.values.get('first_name')
        last_name = request.values.get('last_name')
        kerberos = request.values.get('kerberos')
        remove = True if request.values.get('remove') == 'true' else False

        if kerberos and first_name and last_name:
            entry = (first_name, last_name, kerberos)
            if remove and entry in checkoff_queue:
                checkoff_queue.remove(entry)
                msg = 'removed from queue'
            elif entry not in checkoff_queue:
                checkoff_queue.append(entry)
                msg = 'added to queue'
            else:
                msg = 'already added to queue'
            return jsonify({'message': msg})
        else:
            msg = 'missing queue data'
    else:
        return jsonify({'checkoff_queue': checkoff_queue, 'message': msg})

    return jsonify({'error_code': 400, 'message': msg})



if __name__ == "__main__":
    port = 5000
    app.run(host='localhost', port=port)
