from flask import Flask, render_template
from bp import user, restaurant, review
import config
from flask_cors import CORS


app = Flask(__name__, static_url_path="/static", static_folder="build/static", template_folder="build")
app.register_blueprint(user.user, url_prefix="/api/user")
app.register_blueprint(restaurant.restaurant, url_prefix="/api/restaurant")
app.register_blueprint(review.review, url_prefix="/api/review")

cors = CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print("Catch All")
    return render_template("index.html")

if __name__ == "__main__":
    # app.run("0.0.0.0", 80)
    listen_ip = config.Server.IP
    listen_port = config.Server.PORT
    app.run(listen_ip, listen_port, debug=True)