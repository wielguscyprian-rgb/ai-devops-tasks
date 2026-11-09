Here are production-ready Dockerfile configurations for Node.js applications, optimized for security, small image size, and fast build caching.

### 1. Production Multi-Stage Dockerfile (Recommended)

Ideal for TypeScript or applications requiring a build step, resulting in a minimal runtime image:

```dockerfile
# --- 1. Dependencies Stage ---
FROM node:20-alpine AS deps
WORKDIR /app

COPY package*.json ./
RUN npm ci

# --- 2. Build Stage ---
FROM node:20-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Run build if TypeScript or bundler is used (ignored if script doesn't exist)
RUN npm run build --if-present

# Prune devDependencies to keep runtime modules only
RUN npm prune --production

# --- 3. Production Runner Stage ---
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Run as non-root user for security
USER node

# Copy production dependencies and application code
COPY --chown=node:node --from=builder /app/node_modules ./node_modules
COPY --chown=node:node --from=builder /app/dist ./dist
COPY --chown=node:node package*.json ./

EXPOSE 3000

CMD ["node", "dist/index.js"]

```

---

### 2. Simple Dockerfile (Single-Stage)

Suitable for standard JavaScript (Node.js) applications without a build/compilation step:

```dockerfile
FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production

# Copy package files first to leverage Docker layer caching
COPY package*.json ./

# Install production dependencies only
RUN npm ci --only=production

# Copy rest of application code
COPY . .

# Use built-in non-root user
USER node

EXPOSE 3000

CMD ["node", "index.js"]

```

---

### 3. Essential `.dockerignore`

Create a `.dockerignore` file in the same directory as your `Dockerfile` to prevent copying unnecessary files into the build context:

```text
node_modules
npm-debug.log
.git
.gitignore
Dockerfile
.dockerignore
.env
.env.*
dist
coverage

```

---

### Key Best Practices Applied

* **Alpine Base Image (`node:20-alpine`):** Reduces total image size from ~1GB to under 150MB, significantly shortening deployment time and reducing security vulnerabilities.
* **Layer Caching:** Copying `package*.json` and running `npm ci` before copying source files prevents re-installing dependencies every time source code changes.
* **`npm ci` over `npm install`:** Guarantees strict, reproducible builds based on `package-lock.json`.
* **Least Privilege (`USER node`):** Executes the Node process as a unprivileged user instead of default `root`.
* **Array Syntax for `CMD`:** Using `CMD ["node", "index.js"]` (exec form) ensures Node.js receives `SIGTERM` signals directly for graceful shutdowns.
------------ODPOWIEDŹ 2:--------------------
```dockerfile
FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]

```

Powyższa konfiguracja uwzględnia jedną dodatkową i bardzo ważną instrukcję: **`WORKDIR /app`**. Ustawia ona katalog roboczy dla wszystkich kolejnych poleceń, co zapobiega kopiowaniu plików aplikacji bezpośrednio do głównego katalogu (root) kontenera.

Zapis `COPY package*.json ./` pozwala na jednoczesne skopiowanie zarówno pliku `package.json`, jak i `package-lock.json` (jeśli ten drugi istnieje).

Dobrą praktyką jest również utworzenie w tym samym folderze pliku **`.dockerignore`**, aby zapobiec kopiowaniu lokalnego folderu z zależnościami do wewnątrz kontenera:

```text
node_modules
npm-debug.log
.git
.env

```