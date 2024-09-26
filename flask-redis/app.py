from flask import Flask
from redis import Redis
import os

app = Flask(__name__)
redis = Redis(host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"])

@app.route('/')
def hello():
    redis.incr('hits')
    counter = str(redis.get('hits'),'utf-8')
    return "This webpage has been viewed "+counter+" time(s)\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
