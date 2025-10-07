FROM node:20-alpine

ENV NODE_ENV=production

WORKDIR /usr/src/app

# Install dependencies first (better layer caching)
COPY package*.json ./
RUN npm ci --omit=dev || npm install --omit=dev

# Copy application source
COPY . .

EXPOSE 8081

CMD ["node", "index.js"]


