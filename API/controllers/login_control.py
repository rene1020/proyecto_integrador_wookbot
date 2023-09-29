from ..models.login_models import Login
from ..database import *
from flask import jsonify, request, session


class LoginController():

    @classmethod
    def login(cls):
        """Realiza el llamado al metodo para realizar el login"""
        data = request.json
        user = Login(
            email=data.get('email'),
            passwords=data.get('passwords')
        )

        if Login.is_registered(user):
            session['email'] = data.get('email')
            return {"message": "Sesion iniciada"}, 200
        else:
            return {"message": "Usuario o contraseña incorrectos"}, 401

    @classmethod
    def logout(cls):
        if 'email' in session:
            session.pop('email', None)
            return {"message": "Sesion cerrada"}, 200