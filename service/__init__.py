"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys
from flask import Flask
from .models import Order, Item, db
from service import config
from .common import log_handlers
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# Dependencies require we import the routes AFTER the Flask app is created
# pylint: disable=wrong-import-position, wrong-import-order
from service import routes         # noqa: E402, E261
# pylint: disable=wrong-import-position
from .common import error_handlers  # noqa: F401 E402

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

app.logger.info("App Root Path: {}".format(app.root_path))

try:
    routes.init_db()  # make our SQLAlchemy tables
except Exception as error:
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)


admin = Admin(app, name='order', template_mode='bootstrap3')

# Add administrative views here
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Item, db.session))

app.logger.info("Service initialized!")
