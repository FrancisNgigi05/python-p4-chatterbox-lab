from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import asc

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        all_messages = []

        for message in Message.query.order_by(asc(Message.created_at)):
            message_dict = message.to_dict()
            all_messages.append(message_dict)

        response = make_response(all_messages, 200)
        return response
    
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data['body'],
            username=data['username']
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        response = make_response(message_dict, 201)

        return response

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):

    # if request.method == 'GET':
    #     specific_message_dict = specific_message.to_dict()
    #     response = make_response(specific_message_dict, 200)

    #     return response
    specific_message = Message.query.filter(Message.id == id).first()
    
    if request.method == 'PATCH':
        data = request.get_json()
        for attr in request.form:
            setattr(specific_message, attr, data[attr])

        db.session.add(specific_message)
        db.session.commit()

        specific_message_dict = specific_message.to_dict()

        response = make_response(specific_message_dict, 200)
        
        return response
        
    elif request.method == 'DELETE':
        db.session.delete(specific_message)
        db.session.commit()

        response_body = {
            "deleted": True
        }

        response = make_response(response_body, 200)
        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
