FROM node:18 as deps

WORKDIR /usr/src/app

COPY package.json package-lock.json* ./
RUN npm install

FROM node:18 as builder

WORKDIR /usr/src/app

COPY --from=deps /usr/src/app/node_modules ./node_modules
COPY . .

ARG REACT_APP_BACKEND_URL
ENV REACT_APP_BACKEND_URL=${REACT_APP_BACKEND_URL}
ARG PORT 
ENV PORT=${PORT}

RUN npm run build