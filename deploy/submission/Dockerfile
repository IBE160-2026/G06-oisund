FROM node:24.19.0-alpine@sha256:d32cdf619f63fe0471182d08996dd516c6275bb5fd31ae06e55a570bd9e1ad43
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
ENV VITE_FICTIONAL_API=http://127.0.0.1:18327
ENV VITE_PRIVATE_API=http://127.0.0.1:18328
RUN npm run build
RUN mkdir -p node_modules/.vite-temp && chown -R node:node node_modules/.vite-temp
USER node
CMD ["npm", "run", "start", "--", "--port", "15325"]
