import random
import signal
import sys
from pathlib import Path

from flask import Flask

from example.events.db_event import DBEvent
from flask_edk_threads.flask_edk_threads import FlaskEDKThreads

app = Flask(__name__)
fts = FlaskEDKThreads(config_file=Path("D:\\github\\PyPackage\\flask_edk_threads\\src\\example\\ThreadConfiguration.xml"))

fts.init_app(app)


@app.route('/event')
def event():
    devs = ["dev1", "dev2", "dev3"]
    for i in range(100):
        fts.put(DBEvent(host=devs[random.randint(0, 2)], file_size=random.randint(1, 10)))
    return "OK"


@app.route('/stop')
def stop():
    fts.stop_ft()
    return "STOP"


def handle_sigint(sig, frame):
    fts.stop_ft()
    print('Close The Flask')
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    app.run(debug=True)
