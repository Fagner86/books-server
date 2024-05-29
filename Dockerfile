# Usando uma imagem base que já tem Node.js e Python instalados
FROM tiangolo/node-frontend:10 as build-stage

# Configura o diretório de trabalho
WORKDIR /app

# Copia os arquivos package.json e package-lock.json
COPY package*.json ./

# Instala as dependências do Node.js
RUN npm install

# Copia o código fonte do Node.js
COPY . .

# Instala as dependências do Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir scikit-learn

# Exponha a porta que a aplicação vai rodar
EXPOSE 4000

# Define variáveis de ambiente
ENV PORT=4000

# Comando para rodar a aplicação
CMD ["node", "index.js"]
