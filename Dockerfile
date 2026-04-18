# ─────────────────────────────────────────────────────────────
# Ayur Narayana — Static Site
# Multi-stage: build stage (for future asset pipelines) + nginx
# ─────────────────────────────────────────────────────────────

# ---------- Stage 1: Build (placeholder – extend for bundlers) ----------
FROM node:20-alpine AS builder

WORKDIR /app

# Copy all source files
COPY . .

# If you add a package.json / bundler later, run it here:
# RUN npm ci && npm run build

# For now, the "build" is just the raw files
RUN mkdir -p /app/dist && cp -r . /app/dist

# ---------- Stage 2: Serve with nginx ----------
FROM nginx:1.25-alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom nginx config
COPY nginx.conf /etc/nginx/conf.d/ayurnarayana.conf

# Copy built static files
COPY --from=builder /app/dist /usr/share/nginx/html

# Cloud Run requires the container to listen on PORT env var (default 8080)
# nginx.conf reads $PORT via envsubst at startup
ENV PORT=8080

EXPOSE 8080

# Use envsubst to substitute $PORT in nginx config at container start
CMD ["/bin/sh", "-c", \
    "envsubst '$PORT' < /etc/nginx/conf.d/ayurnarayana.conf > /etc/nginx/conf.d/default.conf \
    && nginx -g 'daemon off;'"]
