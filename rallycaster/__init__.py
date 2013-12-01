from flask import Flask
app = Flask(__name__, instance_relative_config=True)

import interfaces.error_handling
import interfaces.authentication
import interfaces.meetings
