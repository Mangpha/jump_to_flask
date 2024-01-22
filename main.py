from flask import Flask
from views import main_view

app = Flask(__name__)

app.register_blueprint(main_view.bp)

app.run(debug=True)
