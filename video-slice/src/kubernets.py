from bottle import app, run, template, get, post, request, install, response
from bottle_cors_plugin import cors_plugin
import os

class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):            
            
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors

DEPLOYMENT_NAME = "nginx-deployment"

@post('/num_replicas/<num_replicas>')
def alterar_replicas(num_replicas):
    os.system("kubectl scale deployment " + DEPLOYMENT_NAME + " --replicas=" + num_replicas + "")
    return "sucesso"

app = app()
app.install(cors_plugin('*'))

run(host='0.0.0.0', port=8082)
    