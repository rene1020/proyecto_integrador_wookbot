from flask import jsonify, request
import re
from mysql.connector import Error as mysqlErrors
from ..models.user_model import User
from ..models.exception import *


class UserController:

    @classmethod
    def create_user(cls):
        data = request.json

        params = User(
            users=data.get('users'),
            passwords=data.get('passwords'),
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            birthday_date=data.get('birthday_date'),
        )
        try:
            User.create_user(params)
        except mysqlErrors as error:
            raise DataBaseError(
                f"Se produjo un error al intentar insertar un nuevo usuario en la base de datos {error}")
        return {"Mensaje": "Se Creo el usuario con exito."}, 201

    @classmethod
    def get_all(cls):
        try:
            rta = User.get_all()
        except mysqlErrors as error:
            raise DataBaseError(
                "Se produjo un error al cargar todos los usuarios de la base de datos. {}".format(error))
        return rta, 200

    @classmethod
    def get(cls, user_id):
        """Get a user by id"""
        user = User(user_id=user_id)  # Crear una instancia de User
        # Llamar al método get de la instancia de User
        result = User.get(user)
        if result is not None:
            return result.serialize(), 200
        else:
            raise NotFound()

    @classmethod
    def update_user_endpoint(cls, user_id):
        new_data = request.json
        try:
            user = User(**new_data)
            user.user_id = user_id
            User.update_user_pr(user)
            return {"mensaje": f"Se modificaron con éxito los datos del usuario con id={user_id}."}, 200
        except mysqlErrors as error:
            raise Data_BaseError(
                f"Se produjo un error al momento de actualizar los datos del usuario con id={user_id} en la base de datos. {error}")

    @classmethod
    def delete_user(cls, user_id: int):
        try:
            User.delete(user_id)
            return jsonify({"message": "Usuario eliminado exitosamente"}), 200
        except Exception as e:
            return jsonify({"message": f"Error al eliminar el usuario: {str(e)}"}), 500

    @classmethod
    def control_existe_usuario(cls, id_usuario):
        if not (User.user_exist(id_usuario)):
            raise UsuarioNoEncontrado(
                "El usuario con id={} no se encontro en la base de datos.".format(id_usuario))