from re import M
from flask import Blueprint, request, jsonify
from isort import code
from response import *
from dao import DataAccess
from utils import utils

restaurant = Blueprint("restaurant", __name__)

@restaurant.route("/", methods=["GET", "POST"], strict_slashes=False)
def handle_restaurant():
    if request.method == "GET":
        return get_restaurant()
    elif request.method == "POST":
        return new_restaurant()


def get_restaurant():
    restaurant_id = request.args.get("id", None)
    # get all restaurants
    if restaurant_id == None:
        sql_get_restaurant = "\
            SELECT id, name, `desc`, img \
            FROM restaurant"

        dao = DataAccess()
        result_get_restaurant = dao.execute(sql_get_restaurant)
        if result_get_restaurant == None:
            return jsonify(ResMsg(data="", code=ResponseCode.FAIL, msg=ResponseMessage.FAIL).data)

        result = []
        for restaurant in result_get_restaurant:
            result.append({
                "id": restaurant[0],
                "name": restaurant[1],
                "desc": restaurant[2],
                "img_url": restaurant[3]
            })
        return jsonify(ResMsg(data=result, code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS).data)

    # get a restaurant
    else:
        restaurant_id = int(restaurant_id)
        # get restaurant's info
        sql_get_restaurant = "\
            SELECT id, name, `desc`, zip, tel, website, location \
            FROM restaurant \
            WHERE id = {}".format(
                restaurant_id
            )

        dao = DataAccess()
        result_get_restaurant = dao.execute(sql_get_restaurant)
        if result_get_restaurant == None \
                or len(result_get_restaurant) == 0:
            return jsonify(ResMsg(data="", code=ResponseCode.FAIL, msg=ResponseMessage.FAIL).data)

        result_get_restaurant = result_get_restaurant[0]

        # get restaurant's rating
        sql_get_rating = "\
            SELECT rating \
            FROM review \
            WHERE restaurant = {}".format(
                restaurant_id
            )
        result_get_rating = dao.execute(sql_get_rating)
        if result_get_rating == None \
                or len(result_get_rating) == 0:
            rating = 0
        else:
            rating = [r[0] for r in result_get_rating]
            rating = round(sum(rating) / len(rating), 1)

        result = {
            "id": restaurant_id,
            "name": result_get_restaurant[1],
            "desc": result_get_restaurant[2],
            "zip": result_get_restaurant[3],
            "tel": result_get_restaurant[4],
            "website": result_get_restaurant[5],
            "location": result_get_restaurant[6],
            "rating": rating
        }
        return jsonify(ResMsg(data=result, code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS).data)


def new_restaurant():
    name = request.form.get("name", None)
    desc = request.form.get("desc", None)
    zip = request.form.get("zip", None)
    tel = request.form.get("tel", None)
    website = request.form.get("website", "")
    img = request.form.get("img", None)
    location = request.form.get("location", None)

    if (name and desc and zip and tel and img and location) == None:
        return jsonify(ResMsg(data="", code=ResponseCode.FAIL, msg=ResponseMessage.FAIL).data)

    sql_new_restaurant = "\
        INSERT INTO restaurant \
        SET name = '{}', \
            `desc` = '{}', \
            zip = '{}', \
            tel = {}, \
            website = '{}', \
            img = '{}', \
            location = '{}'".format(
                name, desc, zip, tel, website, img, location
            )

    dao = DataAccess()
    result_new_restaurant = dao.execute(sql_new_restaurant)
    if result_new_restaurant == None:
        return jsonify(ResMsg(data="", code=ResponseCode.FAIL, msg=ResponseMessage.FAIL).data)

    return jsonify(ResMsg(data="", code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS).data)