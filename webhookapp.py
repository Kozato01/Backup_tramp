from db_connect import db_connection
from flask import Flask, request, jsonify
from tools.functions import *
import time, datetime

#Instancia do banco!
db_connection.connect()
app = Flask(__name__)

#Verifica os dados la no banco
def if_user_exists(cpf):
    try:
        cpf = cpf.replace('.', '').replace('-', '')
        query = f"SELECT EXISTS (SELECT 1 FROM Webhook_Comp.CadastroOperadora WHERE cpf = '{cpf}') as return_bank"
        results = db_connection.read_consult(query)
        if results and len(results) > 0:
            return results[0]['return_bank']
        else:
            return False

    except Exception as e:
        print(f"Erro ao verificar se o usuário existe: {e}")
        return False


@app.route('/', methods=['GET'])
def home():
    return 'OK, Webhook do Google Cloud SQL', 200


#protocolo
@app.route('/dialog_protocolo', methods=['POST'])
def webhook_protocolo():
    request_json = request.get_json()
    session = request_json['sessionInfo']['session']
    user_input = request_json['text']  # Obtém o texto de entrada do usuário
       
    gerarproto = gerar_protocolo()
    parameters = {
        'Protocolo': gerarproto
    }
    response = format_response_for_dialogflow(
        texts=[f''],
        session_info={
            'session': session,
            'parameters': parameters
        }
    )
    #print(request_json)
    return jsonify(response)



@app.route('/return_bank', methods=['GET'])
def webhook_web():
    # Obtém o CPF da query string
    cpf = request.args.get('cpf')
    if not cpf:
        return jsonify({"error": "CPF is required"}), 400
    exists = if_user_exists(cpf)
    response = {
        'valor': exists,
        'frase': 'Esse é o valor retornado do banco de dados.'
    }
    return jsonify(response)

    
# Rota para protocolo e direcionar pra uma pagina
@app.route('/dialog_verific_cpbase_cloud', methods=['POST'])
def webhook_verificação_cpf_inbase():
    request_json = request.get_json()
    session = request_json['sessionInfo']['session']
    user_input = request_json['text']  # Obtém o texto de entrada do usuário
    cpf = request_json['sessionInfo']['parameters']['cpf']

    if if_user_exists(cpf):
        resposta = 'valido'
        mensagem = f'🎉 Usuário com CPF {cpf} encontrado! 😊 Aproveite nossos excelentes benefícios.'
    else:
        resposta = 'não existe'
        mensagem = f'😔 Parece que você não tem cadastro aqui com a gente, Que tal se cadastrar para aproveitar um de nossos planos depois? 🚀'


    parameters = {
        'Resposta': resposta,
        'Mensagem': mensagem
    }
    
    response = format_response_for_dialogflow(
        texts=[f'{mensagem}'],
        session_info={
            'session': session,
            'parameters': parameters    
        }
    )
    #print(request_json)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
