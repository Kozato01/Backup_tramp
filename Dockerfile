# Use uma imagem base oficial do Python 3.12.2
FROM python:3.12.2-slim

# Crie um usuário não root e defina como o usuário atual
RUN useradd -m myuser

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o requirements.txt e instale as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código do seu aplicativo para o contêiner
COPY . .

# Mude a propriedade dos arquivos para o usuário não root
RUN chown -R myuser:myuser /app

# Mude para o usuário não root
USER myuser

# Exponha a porta em que a aplicação será executada
EXPOSE 8080

# Defina o comando para rodar a aplicação
CMD ["python", "webhookapp.py"]

# Nota: Ao construir a imagem, use o comando:
# docker build -t webhook_cloud:latest .
