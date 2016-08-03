# -*- coding: utf-8 -*-

import uno   # module libreoffice-uno
import json  # module parse json
import flask # flask module

# return http status error
def respError(status=200, indent=2, sort_keys=False, **kwargs):
    resp = flask.make_response(json.dumps(dict(**kwargs), ensure_ascii=False, indent=indent, sort_keys=sort_keys).encode('utf8'))
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    resp.headers['mimetype'] = 'application/json'
    resp.headers['Content-Disposition'] = 'filename=Error.json'
    resp.status_code = status
    return resp
    
# return report file
def respReport(root, new_file):
    resp = flask.send_from_directory(root, new_file, as_attachment=True)
    return resp