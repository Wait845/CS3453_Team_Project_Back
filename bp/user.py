from flask import Blueprint, request, jsonify
from response import *
from dao import DataAccess
from utils import utils


user = Blueprint("user", __name__)

@user.route("/login", methods=["POST"], strict_slashes=False)
def user_login():
    request_json = request.get_json()
    name = request_json.get("name", None)
    password = request_json.get("password", None)

    if (name and password) == None:
        return jsonify(ResMsg(data="", code=ResponseCode.FAIL, msg=ResponseMessage.FAIL).data)

    sql_veri_user = "\
        SELECT *\
        FROM user \
        WHERE name = '{}' \
            AND password = '{}'".format(
                name, password
            )

    dao = DataAccess()
    result_veri_user = dao.execute(sql_veri_user)
    if result_veri_user != None \
            and len(result_veri_user) == 1:
        session = utils.get_uuid()
        sql_update_session = "\
            UPDATE user \
            SET session = '{}'\
            WHERE name = '{}'".format(
                session, name
            )
        dao.execute(sql_update_session)

        result = jsonify(ResMsg(data="", code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS).data)
        result.set_cookie("session", session, max_age=86400)
        return result
    else:
        return jsonify(ResMsg(data="", code=ResponseCode.FAIL, msg=ResponseMessage.FAIL).data)


@user.route("/register", methods=["POST"], strict_slashes=False)
def user_register():
    request_json = request.get_json()
    name = request_json.get("name", None)
    password = request_json.get("password", None)
    if (name and password) == None:
        return jsonify(ResMsg(data="", code=ResponseCode.FAIL, msg=ResponseMessage.FAIL).data)

    # check whether user exist
    sql_get_user = "\
        SELECT name \
        FROM user \
        WHERE name = '{}'".format(
            name
        )

    dao = DataAccess()
    result_get_user = dao.execute(sql_get_user)
    if result_get_user == None:
        return jsonify(ResMsg(data="", code=ResponseCode.FAIL, msg=ResponseMessage.FAIL).data)
    elif len(result_get_user) != 0:
        return jsonify(ResMsg(data="", code=ResponseCode.NAME_EXITS, msg=ResponseMessage.NAME_EXITS).data)
    # register
    user_session = utils.get_uuid()
    sql_record_user = "\
        INSERT INTO user \
        SET name = '{}', \
            password = '{}', \
            session = '{}'".format(
                name, password, user_session
            )

    dao = DataAccess()
    result_record_user = dao.execute(sql_record_user)
    if result_record_user == None:
        return jsonify(ResMsg(data="", code=ResponseCode.FAIL, msg=ResponseMessage.FAIL).data)
    else:
        result = jsonify(ResMsg(data="", code=ResponseCode.SUCCESS, msg=ResponseMessage.SUCCESS).data)
        result.set_cookie("session", user_session, max_age=86400)
        return result
