FROM node:12-alpine
WORKDIR /to-do-list
COPY . .
RUN yarn install --production
CMD ["node", "/to-do-list/src/index.js"]