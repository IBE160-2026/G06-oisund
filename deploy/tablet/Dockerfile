FROM node:24.19.0-alpine@sha256:d32cdf619f63fe0471182d08996dd516c6275bb5fd31ae06e55a570bd9e1ad43 AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/tsconfig.json ./tsconfig.json
COPY frontend/src/ ./src/
COPY deploy/tablet/index.html ./index.html
ENV VITE_PRIVATE_API_BASE=/private-api
RUN npm run build

FROM nginx:1.30.6-alpine-slim@sha256:dede8895648b461178c3bc604f7eed4423efe5220b2c4d839f5eb3d34ac3f8f7
COPY --from=build /app/dist /usr/share/nginx/html
COPY deploy/tablet/nginx.conf.template /etc/nginx/templates/default.conf.template
COPY deploy/tablet/nginx-main.conf /etc/nginx/nginx.conf
USER 101:101
ENTRYPOINT ["/bin/sh", "-ec"]
CMD ["envsubst '${TABLET_HOST}' < /etc/nginx/templates/default.conf.template > /tmp/tablet.conf; exec nginx -g 'daemon off;'"]
