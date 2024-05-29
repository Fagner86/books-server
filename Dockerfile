# Usar uma imagem base que tem Node.js e Python
FROM node:20

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm install

# Copia o código fonte do Node.js
COPY . .

# Instala as dependências do Python
RUN apt-get update && \ 
    apt-get install -y python3 python3-pip && \
    python3 -m pip install --upgrade pip && \
    pip3 install --no-cache-dir scikit-learn

# Exponha a porta que a aplicação vai rodar
EXPOSE 4000

# Define variáveis de ambiente
ENV PORT=4000

# Comando para rodar a aplicação

CMD ["node", "index.js"]
