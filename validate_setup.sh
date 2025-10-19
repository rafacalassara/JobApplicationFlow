#!/bin/bash
# Validation script for JobApplicationFlow setup

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}JobApplicationFlow Setup Validation${NC}"
echo "===================================="
echo ""

# Check Docker
echo -n "Checking Docker... "
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
    echo -e "${GREEN}✓ Docker installed (version $DOCKER_VERSION)${NC}"
else
    echo -e "${RED}✗ Docker not found${NC}"
    echo "  Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

# Check Docker Compose
echo -n "Checking Docker Compose... "
if docker compose version &> /dev/null; then
    COMPOSE_VERSION=$(docker compose version | awk '{print $4}')
    echo -e "${GREEN}✓ Docker Compose available (version $COMPOSE_VERSION)${NC}"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version | awk '{print $3}' | sed 's/,//')
    echo -e "${GREEN}✓ docker-compose installed (version $COMPOSE_VERSION)${NC}"
else
    echo -e "${YELLOW}⚠ Docker Compose not found${NC}"
    echo "  Docker Compose is recommended but not required"
fi

# Check .env file
echo -n "Checking .env file... "
if [ -f .env ]; then
    echo -e "${GREEN}✓ .env file exists${NC}"
    
    # Check for required variables
    if grep -q "OPENAI_API_KEY=" .env && grep -q "SERPER_API_KEY=" .env; then
        echo -e "  ${GREEN}✓ Required environment variables found${NC}"
        
        # Check if keys are set (not empty or default)
        OPENAI_KEY=$(grep "OPENAI_API_KEY=" .env | cut -d'=' -f2)
        SERPER_KEY=$(grep "SERPER_API_KEY=" .env | cut -d'=' -f2)
        
        if [ "$OPENAI_KEY" = "YOUR-KEY" ] || [ -z "$OPENAI_KEY" ]; then
            echo -e "  ${YELLOW}⚠ OPENAI_API_KEY not set${NC}"
        else
            echo -e "  ${GREEN}✓ OPENAI_API_KEY is set${NC}"
        fi
        
        if [ "$SERPER_KEY" = "YOUR-KEY" ] || [ -z "$SERPER_KEY" ]; then
            echo -e "  ${YELLOW}⚠ SERPER_API_KEY not set${NC}"
        else
            echo -e "  ${GREEN}✓ SERPER_API_KEY is set${NC}"
        fi
    else
        echo -e "  ${RED}✗ Missing required environment variables${NC}"
        echo "  Required: OPENAI_API_KEY, SERPER_API_KEY"
    fi
else
    echo -e "${RED}✗ .env file not found${NC}"
    echo "  Run: cp .env.example .env"
    echo "  Then edit .env with your API keys"
    exit 1
fi

# Check Python
echo -n "Checking Python... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo -e "${GREEN}✓ Python installed (version $PYTHON_VERSION)${NC}"
    
    # Check Python version (should be >=3.10 <=3.13)
    MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ] && [ "$MINOR" -le 13 ]; then
        echo -e "  ${GREEN}✓ Python version is compatible${NC}"
    else
        echo -e "  ${YELLOW}⚠ Python version should be >=3.10 and <=3.13${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Python not found${NC}"
    echo "  Python is needed for local development only"
fi

# Check directories
echo -n "Checking directories... "
if [ -d "outputs" ] && [ -d "inputs" ]; then
    echo -e "${GREEN}✓ outputs and inputs directories exist${NC}"
else
    if [ ! -d "outputs" ]; then
        mkdir -p outputs
        echo -e "${YELLOW}⚠ Created outputs directory${NC}"
    fi
    if [ ! -d "inputs" ]; then
        mkdir -p inputs
        echo -e "${YELLOW}⚠ Created inputs directory${NC}"
    fi
fi

# Check Dockerfiles
echo -n "Checking Dockerfiles... "
if [ -f "Dockerfile.gradio" ] && [ -f "Dockerfile.mcp" ]; then
    echo -e "${GREEN}✓ Both Dockerfiles exist${NC}"
else
    echo -e "${RED}✗ Missing Dockerfiles${NC}"
    exit 1
fi

# Check docker-compose.yml
echo -n "Checking docker-compose.yml... "
if [ -f "docker-compose.yml" ]; then
    echo -e "${GREEN}✓ docker-compose.yml exists${NC}"
    
    # Validate syntax
    if docker compose config > /dev/null 2>&1 || docker-compose config > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓ docker-compose.yml syntax is valid${NC}"
    else
        echo -e "  ${YELLOW}⚠ Could not validate docker-compose.yml syntax${NC}"
    fi
else
    echo -e "${RED}✗ docker-compose.yml not found${NC}"
    exit 1
fi

# Check MCP server file
echo -n "Checking MCP server... "
if [ -f "mcp_server.py" ]; then
    echo -e "${GREEN}✓ mcp_server.py exists${NC}"
    
    # Check Python syntax
    if python3 -m py_compile mcp_server.py 2>/dev/null; then
        echo -e "  ${GREEN}✓ mcp_server.py syntax is valid${NC}"
    else
        echo -e "  ${YELLOW}⚠ Could not validate mcp_server.py syntax${NC}"
    fi
else
    echo -e "${RED}✗ mcp_server.py not found${NC}"
    exit 1
fi

# Summary
echo ""
echo -e "${BLUE}Validation Summary${NC}"
echo "===================="
echo ""
echo -e "${GREEN}✓ All required components are present${NC}"
echo ""
echo "Next steps:"
echo "1. Ensure your .env file has valid API keys"
echo "2. Run './start.sh' to start the services"
echo "3. Access the Gradio UI at http://localhost:7860"
echo ""
echo "For MCP integration:"
echo "1. Build the MCP image: docker build -f Dockerfile.mcp -t job-application-flow-mcp ."
echo "2. Configure your MCP client (see MCP.md for details)"
echo ""
echo "For detailed documentation, see:"
echo "- README.md - General usage and setup"
echo "- DOCKER.md - Docker deployment guide"
echo "- MCP.md - MCP integration guide"
