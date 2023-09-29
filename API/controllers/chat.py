from ..models.chat_model import Message
from flask import request, jsonify, session
from ..models.exception import NotFound, ForbiddenAction


class MessageController:
    @classmethod
    def get_message(cls, id_msg):
        if not Message.exist(id_msg):
            raise NotFound(id_msg, "message")

        msg = Message.get_message(id_msg)
        return jsonify(msg.serialize()), 200

    @classmethod
    def get_messages(cls):
        id_msg = request.args.get('id_msg')
        msgs = Message.get_messages(id_msg)
        response = {}

        if msgs:
            msgs_list = []
            for msg in msgs:
                msgs_list.append(msg.serialize())

            response["messages"] = msgs_list
            response["total"] = len(msgs_list)
            return jsonify(response), 200
        else:
            return jsonify(response), 200

    @classmethod
    def delete_message(cls, id_msg):
        if not Message.exist(id_msg):
            raise NotFound(id_msg, "message")

        msg = Message.get_message(id_msg)

        if session['id_user'] == msg.id_user:
            Message.delete_message(id_msg)
            return jsonify({'message': 'Message deleted successfully'}), 204
        else:
            raise ForbiddenAction()

    @classmethod
    def create_message(cls):
        msg_data = request.json

        new_msg = Message.validate_data([
            msg_data.get('content'),
            session['id_user'],
            msg_data.get('id_channel')
        ])

        Message.create_message(new_msg)
        return jsonify({'message': 'Message created successfully'}), 201

    @classmethod
    def update_message(cls, id_msg):
        if not Message.exist(id_msg):
            raise NotFound(id_msg, "message")

        og_msg = Message.get_message(id_msg)

        if session['id_msg'] == og_msg.id_user:
            update_data = request.json

            Message.update_message((
                update_data.get('message_body', og_msg.content),
                id_msg
            ))
            return jsonify({'message': 'Message updated successfully'}), 200
        else:
            raise ForbiddenAction()