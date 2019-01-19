from app import createApp, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import *

app = createApp()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()




