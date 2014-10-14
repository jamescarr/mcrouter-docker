from os import environ as env
import json
from flask import Flask, request, jsonify, Response
from pymemcache.client import Client

MCROUTER_ADDR = 'MCROUTER_PORT_5000_TCP_ADDR'
MCROUTER_PORT = 'MCROUTER_PORT_5000_TCP_PORT'
app = Flask(__name__)

###
# Logging
###
import logging
import graypy

log = logging.getLogger('mcrouter-rest-api')
log.setLevel(logging.INFO)

if env.has_key('GRAYLOG2_HOST'):
    handler = graypy.GELFHandler(env.get('GRAYLOG2_HOST'), 12201)
    log.addHandler(handler)


client = None
def create_client():
    global client
    if not client:
        if env.has_key(MCROUTER_ADDR) and env.has_key(MCROUTER_PORT):
            client = Client((
                env.get(MCROUTER_ADDR),
                int(env.get(MCROUTER_PORT))
            ))
        else:
            raise Error("{} and {} are required environment variables. Please ensure these are set")
    
    return client




@app.route("/")
def root():
    return jsonify(version='0.0.0')

@app.route("/config", methods=["POST"])
def put_config():
    f = open('/etc/mcrouter/mcrouter.conf', 'r+')
    
    old = json.load(f)
    f.seek(0)
    f.write(request.get_data())
    f.close()
    
    new = json.load(f)

    log.info("mcrouter configuration changed!", 
            extra={
                'new':new,
                'old':old
    })
    return jsonify(message='configuration saved', config=new)

@app.route("/config", methods=["GET"])
def get_config():
    return serve_stat('__mcrouter__.preprocessed_config')
    
@app.route("/options", methods=["GET"])
def get_options():
    res = create_client().get('__mcrouter__.options')
    retr_options = {}

    options = res.split("\n")
    for option in options:
        (key, value) = option.split(" ")
        retr_options[key] = value

    return jsonify(**retr_options)


@app.route("/options/<option>", methods=["GET"])
def get_option(option):
    res = create_client().get('__mcrouter__.options({})'.format(option))

    return jsonify(**{option: res})

@app.route("/route/<key>")
def get_route(key):
    res = create_client().get('__mcrouter__.route(set,{})'.format(key))
    
    return jsonify(
            key=key, 
            routes=res.split('\n')
    )

@app.route("/config/sources", methods=["GET"])
def get_config_sources():
    return serve_stat('__mcrouter__.config_sources_info')

@app.route("/stats", methods=["GET"])
def get_stats():
    print(create_client().stats())

    res = create_client()._misc_cmd(b'stats\r\n', 'stats', False)
    print(res)
    retr_options = {}

    options = res.split("\n")

    return jsonify(options=options)

def serve_stat(key):
    res = create_client().get(key)
    return Response(res, mimetype='application/json')

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=int(env.get('FLASK_PORT', '5000')),
        debug=True
   )
