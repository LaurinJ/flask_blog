# from mdblog.factory import create_flask_app
from mdblog.factory import create_flask_app
from mdblog.models import db
import sys

flask_app = create_flask_app()


def start():
    host = "0.0.0.0"
    debug = True
    flask_app.run(host, debug=debug)

def init():
    with flask_app.app_context():
        db.create_all()
        print("DB created")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        commad = sys.argv[1]
        if commad == "start":
            start()
        elif commad == "init":
            init()
        else:
            print("start or init")
    else:
        print("start or init")