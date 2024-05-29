FROM node:20

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm install
RUN pip install scikit-learn
COPY . .

EXPOSE 8080

CMD ["node", "index.js"]