#!/bin/bash
# Start script for JobApplicationFlow

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}JobApplicationFlow Startup Script${NC}"
echo "===================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo -e "${RED}Please edit .env file with your API keys before continuing!${NC}"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}docker-compose command not found, trying 'docker compose'${NC}"
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Ask user what they want to run
echo ""
echo "What would you like to do?"
echo "1) Start Gradio UI (Web Interface)"
echo "2) Build MCP Server Image"
echo "3) Start both services (Gradio + MCP)"
echo "4) Stop all services"
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo -e "${GREEN}Starting Gradio UI...${NC}"
        $COMPOSE_CMD up -d gradio-app
        echo ""
        echo -e "${GREEN}Gradio UI is starting!${NC}"
        echo "Access it at: http://localhost:7860"
        echo ""
        echo "To view logs: $COMPOSE_CMD logs -f gradio-app"
        echo "To stop: $COMPOSE_CMD down"
        ;;
    2)
        echo -e "${GREEN}Building MCP Server Image...${NC}"
        docker build -f Dockerfile.mcp -t job-application-flow-mcp .
        echo ""
        echo -e "${GREEN}MCP Server image built successfully!${NC}"
        echo "You can now configure your MCP client to use this image."
        echo "See README.md for configuration instructions."
        ;;
    3)
        echo -e "${GREEN}Starting all services...${NC}"
        $COMPOSE_CMD up -d
        echo ""
        echo -e "${GREEN}All services are starting!${NC}"
        echo "- Gradio UI: http://localhost:7860"
        echo "- MCP Server: Running in background"
        echo ""
        echo "To view logs: $COMPOSE_CMD logs -f"
        echo "To stop: $COMPOSE_CMD down"
        ;;
    4)
        echo -e "${YELLOW}Stopping all services...${NC}"
        $COMPOSE_CMD down
        echo -e "${GREEN}All services stopped.${NC}"
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac
