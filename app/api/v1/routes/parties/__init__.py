"""All routes pertaining to parties"""

from flask import jsonify, request, make_response, abort

from app.api.v1 import path_1
from app.api.v1.model import PartiesModel, PARTIES

from app.api.utils import is_valid_string


@path_1.route("/parties", methods=['GET'])
def get_all_parties():
    """
    fetch_all_parties
    """
    parties = PartiesModel.get_all_parties()
    return make_response(jsonify({"status": 200, "data": parties}), 200)


@path_1.route("/parties", methods=["POST"])
def create_party():
    try:
        data = request.get_json()
        name = data['name']
        logoUrl = data['logoUrl']
    except:
        return make_response(jsonify({'status': 400,
                                      'error': "Check your json keys. Should be name and logoUrl"}), 400)

    if(is_valid_string(name) == False):
        return make_response(jsonify({'status': 400,
                                      'error': "The logoUrl and namefields are present, but they are not valid"}), 400)
    party = PartiesModel(
        name=name, logoUrl=logoUrl)
    party.save_party()
    return make_response(jsonify({"status": 201,
                                  "data": [{"id": len(PARTIES) - 1,
                                            "name": name, "logoUrl": logoUrl}]}), 201)


@path_1.route("/parties/<int:party_id>", methods=["GET"])
def get_party(party_id):
    party = PartiesModel.get_party(party_id)
    if party:
        return jsonify({"status": 200, "data": party})
    return make_response(jsonify({"status": 404, "error": "This party cannot be found"}), 404)


@path_1.route("/parties/<int:party_id>/name", methods=["PATCH"])
def update_party(party_id):
    try:
        data = request.get_json()
        name = data["name"]
    except:
        return make_response(jsonify({
            "status": 400,
            "error": "name not found"
        }), 400)
    if(is_valid_string(name) == False):
        return make_response(jsonify({
            "status": 400,
            "error": "name is present, but its not valid"
        }), 400)
    try:
        party = PartiesModel.get_party_object(party_id)[0]
    except IndexError:
        return make_response(jsonify({"status": 404, "data": "This party doesn't exist"}), 404)
    party.setname(name)
    return make_response(jsonify({"status": 200, "data": [{
        "id": party_id,
        "name": name
    }]}), 200)


@path_1.route("/parties/<int:party_id>", methods=['DELETE'])
def delete_party(party_id):
    party = PartiesModel.deleteparty(party_id)
    if party:
        return make_response(jsonify({'status': 200, 'data': "Deleted successfully"}), 200)
    return make_response(jsonify({"status": 404, "data": "This party doesn't exist"}), 404)
