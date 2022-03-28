from flask import Flask
from bp import user, restaurant, review
import config

app = Flask(__name__)
app.register_blueprint(user.user, url_prefix="/api/user")
app.register_blueprint(restaurant.restaurant, url_prefix="/api/restaurant")
app.register_blueprint(review.review, url_prefix="/api/review")



@app.route("/", methods=["POST"])
def test():
    return "123"

if __name__ == "__main__":
    # app.run("0.0.0.0", 80)
    listen_ip = config.Server.IP
    listen_port = config.Server.PORT
    app.run(listen_ip, listen_port, debug=True)