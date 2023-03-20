from flask import Blueprint, Response
import json

autocomplete_bp = Blueprint('autocomplete', __name__)

@autocomplete_bp.route('/zipcodes', methods=["GET"])
def autocomplete_zipcodes():
    f = open('./controllers/filter/zipcodes.json')
    zipcodes = json.load(f)
    return Response(json.dumps(zipcodes), mimetype='application/json')

@autocomplete_bp.route('/keywords', methods=["GET"])
def autocomplete_keywords():
    f = open('./controllers/filter/keywords.json')
    keywords = json.load(f)
    return Response(json.dumps(keywords), mimetype='application/json')