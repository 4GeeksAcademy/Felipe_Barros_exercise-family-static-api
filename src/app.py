"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#Obtener todos los usuarios
@app.route('/members', methods=['GET'])
def all_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "msg": "Users retrieved succesfully",
        "family": members
    }

    return jsonify(response_body), 200

#Obtener un usuario
@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_user(member_id):
    member = jackson_family.get_member(member_id)
    
    if not member:
        return jsonify({"msg": "Member not found"}), 404
    response_body = {
        "msg": "Member found succesfully",
        "id": member['id'],
        "first_name": member['first_name'],
        "age": member['age'],
        #Necesario use de list() ya que JSON no puede serializar conjuntos directamente
        "lucky_numbers": list(member['lucky_numbers'])
    }
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_new_member():
    request_body = request.get_json()
    #Verificación de datos
    if not request_body:
        return jsonify({"msg": "Missing request body"}), 400
    #Verifica de que los datos requeridos estén en la request_body
    if "first_name" not in request_body or "age" not in request_body or "lucky_numbers" not in request_body:
        return jsonify({"msg": "Missing required fields"}), 400
    
    try:
        #Intenta agregar el nuevo miembro
        new_member = jackson_family.add_member(request_body)
        #En caso de respuesta exitosa
        return jsonify({"msg": "Member added successfully"}), 201
    except (TypeError, ValueError) as error:
        return jsonify({"msg": str(error)}), 400

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    deleted_member = jackson_family.delete_member(member_id)
    if deleted_member:
        return jsonify({"done": True, "msg": "Member deleted successfully"}), 200
    else:
        return jsonify({"done": False, "msg": "Member not found"}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
