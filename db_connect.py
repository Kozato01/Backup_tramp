import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_DATABASE')
}

class MySQLConnection:
    def __init__(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None

    def connect(self):
        """Estabelece a conexão com o banco de dados MySQL"""
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            print('Conexão bem-sucedida ao banco de dados MySQL') if self.connection.is_connected() else None
        except Error as e:
            print(f'Erro ao conectar ao MySQL: {e}')
            self.connection = None

    def close(self):
        """Fecha a conexão com o banco de dados MySQL"""
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print('Conexão encerrada')

    def read_consult(self, query, values=None):
        """Executa uma consulta SELECT no banco de dados MySQL e retorna os resultados"""
        results = None
        if self.connection and self.connection.is_connected():
            try:
                with self.connection.cursor(dictionary=True) as cursor:
                    cursor.execute(query, values) if values else cursor.execute(query)
                    results = cursor.fetchall()
                    #print('Consulta de leitura executada com sucesso\n', results)
            except Error as e:
                print(f'Erro ao executar a consulta de leitura: {e}')
        else:
            print('Conexão não está aberta')
        return results

db_connection = MySQLConnection(**db_config)