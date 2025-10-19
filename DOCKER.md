# Docker Deployment Guide

This document provides detailed instructions for deploying JobApplicationFlow using Docker.

## Prerequisites

- Docker Engine 20.10 or later
- Docker Compose V2 (comes with Docker Desktop)
- At least 4GB of free disk space
- OpenAI API key
- Serper API key

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rafacalassara/JobApplicationFlow.git
   cd JobApplicationFlow
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Start the services:**
   ```bash
   # Option A: Use the convenience script
   ./start.sh
   
   # Option B: Use docker compose directly
   docker compose up -d
   ```

## Service Architecture

### Gradio Web Application
- **Container Name:** `job-application-gradio`
- **Port:** 7860
- **Purpose:** Web interface for interactive job application processing
- **Access:** http://localhost:7860

### MCP Server
- **Container Name:** `job-application-mcp`
- **Port:** None (uses stdio for communication)
- **Purpose:** Model Context Protocol server for LLM integration
- **Access:** Through MCP client configuration

## Docker Images

### Building Individual Images

**Gradio Application:**
```bash
docker build -f Dockerfile.gradio -t job-application-flow-gradio .
```

**MCP Server:**
```bash
docker build -f Dockerfile.mcp -t job-application-flow-mcp .
```

### Running Individual Containers

**Gradio Application:**
```bash
docker run -d \
  --name job-application-gradio \
  -p 7860:7860 \
  --env-file .env \
  -v $(pwd)/outputs:/usr/src/app/outputs \
  -v $(pwd)/inputs:/usr/src/app/inputs \
  job-application-flow-gradio
```

**MCP Server (for testing):**
```bash
docker run -i --rm \
  --env-file .env \
  -v $(pwd)/outputs:/usr/src/app/outputs \
  -v $(pwd)/inputs:/usr/src/app/inputs \
  job-application-flow-mcp
```

## Environment Variables

All services require the following environment variables:

### Required
- `OPENAI_API_KEY` - Your OpenAI API key
- `SERPER_API_KEY` - Your Serper API key for web search

### Optional
- `GRADIO_SERVER_NAME` - Server bind address (default: 0.0.0.0)
- `GRADIO_SERVER_PORT` - Server port (default: 7860)
- `OPENAI_MODEL_NAME` - OpenAI model to use (default: gpt-4o-mini)
- `OPENAI_API_BASE` - OpenAI API base URL (default: https://api.openai.com/v1)

## Volume Mounts

Both services use the following volumes:

- `./outputs` - Stores generated resumes, reports, and emails
- `./inputs` - Source location for uploaded resumes

These directories are automatically created if they don't exist.

## Managing Services

### Start Services
```bash
docker compose up -d
```

### Stop Services
```bash
docker compose down
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f gradio-app
docker compose logs -f mcp-server
```

### Restart Services
```bash
docker compose restart
```

### Rebuild and Restart
```bash
docker compose up -d --build
```

## Troubleshooting

### Port Already in Use
If port 7860 is already in use, you can change it:

```bash
# Set in .env file
GRADIO_SERVER_PORT=8080

# Or in docker-compose.yml
ports:
  - "8080:7860"
```

### Missing API Keys
Ensure your `.env` file contains valid API keys:
```bash
cat .env | grep -E "OPENAI_API_KEY|SERPER_API_KEY"
```

### Container Logs Show Errors
Check the logs for specific error messages:
```bash
docker compose logs gradio-app
```

### Output Files Not Persisting
Ensure volume mounts are correct:
```bash
docker compose config | grep -A 5 volumes
```

### Rebuilding After Code Changes
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

## Production Considerations

### Security
1. Never commit your `.env` file to version control
2. Use Docker secrets for sensitive data in production
3. Consider using a reverse proxy (nginx, traefik) for HTTPS
4. Restrict network access using Docker networks

### Performance
1. Allocate sufficient resources to Docker:
   - Minimum 2 CPU cores
   - Minimum 4GB RAM
2. Monitor disk space for output files
3. Consider implementing log rotation

### Scaling
The current setup is designed for single-instance deployment. For production scaling:
1. Use orchestration tools (Kubernetes, Docker Swarm)
2. Implement load balancing for the Gradio app
3. Consider separating the MCP server into its own deployment

## Cleanup

To remove all containers, networks, and images:
```bash
# Stop and remove containers
docker compose down

# Remove images
docker rmi job-application-flow-gradio job-application-flow-mcp

# Clean up volumes (WARNING: This deletes output files)
docker compose down -v
```

## Support

For issues related to:
- Docker setup: Check Docker documentation
- Application functionality: Open an issue on GitHub
- MCP integration: Refer to Anthropic's MCP documentation
