# coding: Latin-1
import codecs
import json

from flask import Flask, request, jsonify
import pyodbc
import pandas as pd
from datetime import datetime

app = Flask(__name__)


class DbConection:
    def getDbDriver(self):
        """
        Obtem o driver correto instalado
        """
        drivers = [item for item in pyodbc.drivers()]
        driver = drivers[-1]
        return driver

    def connection(self):
        """
        Cria conexão com banco de dados Bizin
        """
        return pyodbc.connect(
            driver=self.getDbDriver(),
            server='(localdb)\Local',
            database='master',
            # uid='$user',
            # pwd='$password'
        )


# db_return = pd.read_sql('SELECT * FROM Livros', DbConection().connection())
# print(db_return)

@app.route('/Livros', methods=['GET'])
def consulta_livros():
    db_param = "EXEC API_Consulta_Livros_Geral"
    db_return = pd.read_sql(db_param, DbConection().connection())
    dict_return = {"Livros": []}

    for line in db_return.index:
        dict_aux = {}
        for key, value in db_return.items():
            if key == 'Data_Recebimento':
                dict_aux.update({key: trata_data(data=value[line])})
            else:
                dict_aux.update({key: value[line]})
        dict_return['Livros'].append(dict_aux)

    dc = json.dumps(dict_return, indent=4, default=str)

    return dc


def trata_data(data):
    return datetime.strftime(data, "%d-%m-%y %H:%M")


@app.route('/Livros?<int:id_livro>', methods=['GET'])
def consulta_livro_id(id_livro):
    db_param = f"EXEC API_Consulta_Livro_ID {id_livro}"
    db_return = pd.read_sql(db_param, DbConection().connection())
    dict_aux = {}

    for line in db_return.index:
        for key, value in db_return.items():
            if key == 'Data_Recebimento':
                dict_aux.update({key: trata_data(data=value[line])})
            else:
                dict_aux.update({key: value[line]})

    return json.dumps(dict_aux, indent=4, default=str)


@app.route('/Livros/Insere', methods=['POST'])
def insere_livro():
    novo_livro = request.get_json()
    print(novo_livro['Nome_Livro'])
    if not novo_livro['Nome_Livro'] and novo_livro['Valor'] == :
        db_param = f"EXEC API_Insere_Livro {novo_livro['Nome_Livro']}, {novo_livro['Valor']}"
        db_return = pd.read_sql(db_param, DbConection().connection())

        return db_return






# consulta_livros()
app.run(port=5000, host='localhost', debug=True)
