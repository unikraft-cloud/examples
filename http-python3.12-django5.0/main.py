import bjoern
import helloworld.wsgi

bjoern.run(helloworld.wsgi.application, "0.0.0.0", 80)

