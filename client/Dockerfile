FROM node:13.8-slim

RUN apt-get update && apt-get -y install netcat

WORKDIR /app
COPY package.json /app/

RUN npm install

EXPOSE 3000
CMD ["npm", "start"]
