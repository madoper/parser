# SEMANTIC: Multi-stage build for React frontend

# Stage 1: Build stage
FROM node:18-alpine as builder

# SEMANTIC: Set working directory
WORKDIR /app

# SEMANTIC: Copy package files for dependency installation
COPY package.json package-lock.json* ./

# SEMANTIC: Install dependencies with clean cache
RUN npm install --omit=dev && npm cache clean --force

# SEMANTIC: Copy application source
COPY . .

# SEMANTIC: Build production bundle
RUN npm run build

# Stage 2: Production stage with nginx
FROM nginx:alpine

# SEMANTIC: Copy built assets from builder
COPY --from=builder /app/build /usr/share/nginx/html

# SEMANTIC: Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# SEMANTIC: Expose HTTP port
EXPOSE 3000

# SEMANTIC: Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

# SEMANTIC: Start nginx
CMD ["nginx", "-g", "daemon off;"]
