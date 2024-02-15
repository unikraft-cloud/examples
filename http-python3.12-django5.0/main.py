import bjoern
import helloworld.wsgi
import os
from werkzeug.middleware.shared_data import SharedDataMiddleware

app = helloworld.wsgi.application
app = SharedDataMiddleware(app, {
    '/static': '/app/static',
})
bjoern.run(app, "0.0.0.0", 80)

