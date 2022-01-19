from flask_script import Manager
from server import create_app

app = create_app('ProductionConfig')

manager = Manager(app)

@manager.command
def debug():
    app.config.from_object('server.config.DebugConfig')
    app.run(host='0.0.0.0')

@manager.command
def runserver():
    app.run(host='0.0.0.0')

if __name__ == '__main__' :
    manager.run()