# Technical Design: Backend Refactor & Infrastructure

## Context
The project requires a strict directory structure for Phase 3. Current issues include hyphenated Python package names (`core-kernel`) and missing local dev infrastructure.

## Goals
1.  **Refactor**: Sanitize Python package names and imports.
2.  **Infrastructure**: Provide a robust local stack with Nginx and Docker Compose.
3.  **Automation**: Simplify developer workflows via Makefile.

## Decisions

### 1. Refactoring Strategy
We will use a shell script to automate the renaming and import updates. This reduces manual error.
**Script: `scripts/refactor_backend.sh`**
```bash
#!/bin/bash
set -e
echo "Starting Backend Refactoring..."

# Rename Directories
[ -d "libs/core-kernel" ] && mv libs/core-kernel libs/core_kernel
[ -d "libs/infra-db" ] && mv libs/infra-db libs/infra_db
[ -d "libs/infra-net" ] && mv libs/infra-net libs/infra_net

# Move Telemetry
mkdir -p libs/telemetry
if [ -f "libs/core_kernel/telemetry.py" ]; then
    mv libs/core_kernel/telemetry.py libs/telemetry/__init__.py
fi

# Update Imports (sed)
find apps libs -name "*.py" -type f -exec sed -i '' 's/from libs.core-kernel/from libs.core_kernel/g' {} +
find apps libs -name "*.py" -type f -exec sed -i '' 's/from libs.infra-db/from libs.infra_db/g' {} +
find apps libs -name "*.py" -type f -exec sed -i '' 's/from libs.infra-net/from libs.infra_net/g' {} +
find apps libs -name "*.py" -type f -exec sed -i '' 's/from libs.core_kernel.telemetry/from libs.telemetry/g' {} +
# Catch underscore variants too
find apps libs -name "*.py" -type f -exec sed -i '' 's/from libs.core_kernel.telemetry/from libs.telemetry/g' {} +
```

### 2. Infrastructure Configuration

#### Nginx (`deploy/nginx/default.conf`)
Reverse proxying `/api` and `/` with WebSocket support.
```nginx
server {
    listen 80;
    
    location /api/ {
        proxy_pass http://api_gateway:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # WebSocket Support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location / {
        proxy_pass http://web_console:5173; # Vite Dev Server
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

#### Docker Compose (`deploy/docker-compose.yml`)
Full system orchestration.
```yaml
services:
  nginx:
    image: nginx:alpine
    ports: ["80:80"]
    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on: [api_gateway, web_console]

  web_console:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - ../web-console:/app
    command: npm run dev -- --host 0.0.0.0
    ports: ["5173:5173"]

  api_gateway:
    build: { context: .., dockerfile: Dockerfile }
    volumes:
      - ../apps:/app/apps
      - ../libs:/app/libs
    # ... other services (postgres, redis, etc.)
```

### 3. Automation (`Makefile`)
Root-level `Makefile` for ease of use.
```makefile
up:
	docker compose -f deploy/docker-compose.yml up -d --build
refactor:
	bash scripts/refactor_backend.sh
```

## Risks
-   **Import Regex**: `sed` replacements might miss edge cases (e.g., dynamic imports). Verify with manual grep.
-   **Vite Host**: Vite needs `--host` to be accessible from Nginx container.
