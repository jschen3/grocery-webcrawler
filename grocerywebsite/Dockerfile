FROM node:19.6 AS build
WORKDIR /frontend
COPY package.json ./package.json
COPY package-lock.json ./package-lock.json
COPY playwright.config.ts ./playwright.config.tx
COPY svelte.config.js ./svelte.config.js
COPY tsconfig.json ./tsconfig.json
COPY vite.config.js ./vite.config.js
COPY src ./src
COPY static ./static
COPY tests ./tests
RUN npm install
RUN npm run build
EXPOSE 80
CMD [ "npm", "run", "preview" ]

