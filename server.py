#!/usr/bin/python3

from flask import Flask, request, jsonify, send_file
import time

app = Flask(__name__)

help_queue = []

def sec_to_str(s):
    s = int(s)
    return f'{s//60}:{s%60:02d}'

def update_queue():
    now = time.time()
    for e in help_queue:
        e['elapsed'] = sec_to_str(now - e['created'])

@app.route('/')
def index():
    index_file = 'www/index.html'
    return send_file(index_file)


@app.route('/scripts.js')
def js():
    js_file = 'www/scripts.js'
    return send_file(js_file)


@app.route('/queue', methods=['GET', 'POST'])
def manage_queue():
    if request.method == 'POST':
        msg = 'error'
        name = request.values.get('name')
        kerberos = request.values.get('kerberos')
        reqtype = request.values.get('type')        
        remove = request.values.get('remove') == 'true'

        # find if entry already exists, based on kerberos:
        entry = [x for x in help_queue if x['kerberos'] == kerberos]
        entry = entry[0] if entry else None

        # remove from queue
        if remove and entry:
            help_queue.remove(entry)
            msg = 'removed from queue'

        # nothing to remove
        elif remove and not entry:
            msg = 'not in queue'

        # update entry (but leave created time as is)
        elif entry:
            entry['name'] = name
            entry['type'] = reqtype
            msg = 'updated request'

        # create new entry
        else:
            msg = 'added to queue'
            entry = { 'kerberos': kerberos, 'name': name, 'type': reqtype, 
                      'created': time.time(), 'elapsed': 0 }
            help_queue.append(entry)

        return jsonify({'message': msg})

    # request.method = 'GET'
    else:
        update_queue()
        return jsonify({'help_queue': help_queue, 'message': ''})

    return jsonify({'error_code': 400, 'message': ''})


if __name__ == "__main__":
    port = 5000
    app.run(host='localhost', port=port)
