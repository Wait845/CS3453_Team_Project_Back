from re import U
from flask import Blueprint, request, jsonify
from response import *
from dao import DataAccess
from utils import utils


review = Blueprint("review", __name__)

@review.route("/", methods=["GET", "POST"], strict_slashes=False)
def handle_review():
    if request.method == "GET":
        return get_review()
    elif request.method == "POST":
        return new_review()


def get_review():
    restaurant_id = request.args.get("id", None)
    if restaurant_id == None:
        return jsonify(ResMsg(data="", code=ResponseCode.FAIL, msg=ResponseMessage.FAIL).data)
    restaurant_id = int(restaurant_id)

    sql_get_review = "\
        SELECT name, comment, rating, post_time \
        FROM review r \
        INNER JOIN user u \
        ON r.user = u.id \
        WHERE restaurant = {}".format(
            restaurant_id
        )

    dao = DataAccess()
    result_get_review = dao.execute(sql_get_review)
    if result_get_review == None:
        return jsonify(ResMsg(data="", code=ResponseCode.FAIL, msg=ResponseMessage.FAIL).data)

    result = []
    for r in result_get_review:
        result.append({
            "author": r[0],
            "comment": r[1],
            "rating": r[2],
            "post_time": r[3]
        })

    return jsonify(ResMsg(data=result, code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS).data)


def new_review():
    user_session = request.cookies.get("session", None)
    if user_session == None:
        return jsonify(ResMsg(data="", code=ResponseCode.UNLOGIN, msg=ResponseMessage.UNLOGIN).data)

    sql_get_user = "\
        SELECT id \
        FROM user \
        WHERE session = '{}'".format(
            user_session
        )

    # query user
    dao = DataAccess()
    result_get_user = dao.execute(sql_get_user)
    if result_get_user == None:
        return jsonify(ResMsg(data="", code=ResponseCode.FAIL, msg=ResponseMessage.FAIL).data)
    if len(result_get_user) != 1:
        return jsonify(ResMsg(data="", code=ResponseCode.UNLOGIN, msg=ResponseMessage.UNLOGIN).data)

    user_id = result_get_user[0][0]
    request_json = request.get_json()
    restaurant = request_json.get("restaurant")
    rating = request_json.get("rating")
    comment = request_json.get("comment")

    # new review
    sql_new_review = "\
        INSERT INTO review \
        SET user = {}, \
            restaurant = {}, \
            rating = {}, \
            comment = '{}'".format(
                user_id, restaurant, rating, comment
            )
    result_new_review = dao.execute(sql_new_review)
    if result_new_review == None:
        return jsonify(ResMsg(data="", code=ResponseCode.FAIL, msg=ResponseMessage.FAIL).data)

    return jsonify(ResMsg(data="", code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS).data)



