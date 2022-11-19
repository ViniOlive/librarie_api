import pymongo
from pymongo import MongoClient
from flask import Flask, request, jsonify

app = Flask(__name__)
user_db = "Dev"
pass_db = "teste123"
db_name = "Librarie"


class DbConection:
    @staticmethod
    def connect():
        connection_string = f"mongodb+srv://{user_db}:{pass_db}@stockcontroldev.v8gl9k6.mongodb.net/?retryWrites=true"
        client = MongoClient(connection_string)

        return client[db_name]


@app.route('/Books', methods=['GET'])
def show_books():
    db = DbConection().connect()
    db_table = [item for item in db['book'].find()]

    return jsonify(db_table)


@app.route('/Book', methods=['GET'])
def show_book_id():
    db = DbConection().connect()

    if request.args.get('book_id'):
        book_id = request.args.get('book_id')
        db_table = [item for item in db['book'].find({"_id": int(book_id)})]
        return jsonify(db_table)
    else:
        return "Preencha o parametro book_id"


@app.route('/Book', methods=['PUT'])
def update_info_book():
    db = DbConection().connect()
    db_table = db['book']
    book_id = request.args.get('book_id')
    dict_up = {}

    if book_id:
        for key, value in request.args.items():
            if value and not key == 'book_id':
                if value.replace('.', '').isnumeric():
                    dict_up.update({key: float(value)})
                else:
                    dict_up.update({key: value})

        db_table.update_one({"_id": int(book_id)}, {"$set": dict_up})
        return "Update realizado"
    else:
        return "Preencha o parametro book_id"

@app.route('/Book/Insert', methods=['POST'])
def insert_book():
    db = DbConection().connect()
    db_table = db['book']
    book_id = db_table.find_one(sort=[("_id", pymongo.DESCENDING)])["_id"] + 1
    dict_in = {"_id": book_id}

    for key, value in request.args.items():
        if value:
            if value.replace('.', '').isnumeric():
                dict_in.update({key: float(value)})
            else:
                dict_in.update({key: value})
        else:
            return f"O campo {key} deve ser preenchido."

    db_table.insert_one(dict_in)
    return f"Livro ID: {book_id} inserido com sucesso"


app.run(port=5000, host='localhost', debug=True)
