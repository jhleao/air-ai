FROM node:lts-alpine

WORKDIR /app

RUN npm install -g http-server

COPY package.json yarn.lock ./

RUN yarn

COPY . .
COPY .env .

RUN yarn build

EXPOSE 5173
CMD [ "http-server", "dist", "-p", "5173"]
