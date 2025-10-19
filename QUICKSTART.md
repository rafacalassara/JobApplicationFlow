# Quick Start Guide

## For End Users

### Option 1: Use the Gradio Web Interface

```bash
# Clone the repository
git clone https://github.com/rafacalassara/JobApplicationFlow.git
cd JobApplicationFlow

# Set up environment
cp .env.example .env
# Edit .env and add your API keys

# Install dependencies
pip install -r requirements.txt

# Run the Gradio app
python app.py

# Open http://localhost:7860 in your browser
```

### Option 2: Use MCP Server with Claude Desktop

```bash
# 1. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone the repository
git clone https://github.com/rafacalassara/JobApplicationFlow.git
cd JobApplicationFlow

# 3. Set up your Claude Desktop config
# Edit: ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)
# Or: %APPDATA%\Claude\claude_desktop_config.json (Windows)

# Add this configuration:
{
  "mcpServers": {
    "job-application-flow": {
      "command": "uv",
      "args": [
        "run",
        "--quiet",
        "--script",
        "/absolute/path/to/JobApplicationFlow/mcp_server_standalone.py"
      ],
      "env": {
        "OPENAI_API_KEY": "your-openai-key",
        "SERPER_API_KEY": "your-serper-key"
      }
    }
  }
}

# 4. Restart Claude Desktop

# 5. You can now ask Claude to help with job applications!
```

### Option 3: Use Docker

```bash
# Clone and set up
git clone https://github.com/rafacalassara/JobApplicationFlow.git
cd JobApplicationFlow
cp .env.example .env
# Edit .env with your API keys

# Start services
docker-compose up -d

# Access Gradio UI at http://localhost:7860
# MCP server runs as background service
```

## For Developers

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests (if available)
pytest

# Lint code
ruff check .
```

### Modifying the MCP Server

1. Edit `mcp_server.py` to add or modify tools
2. Update tool schemas in the `list_tools()` function
3. Implement tool logic in the `call_tool()` function
4. Test locally:
   ```bash
   python mcp_server.py
   ```

### Building Docker Images

```bash
# Build Gradio app image
docker build -t job-application-gradio .

# Build MCP server image
docker build -f Dockerfile.mcp -t job-application-mcp .

# Or build both with docker-compose
docker-compose build
```

## Environment Variables Reference

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for GPT models | - |
| `SERPER_API_KEY` | Yes | Serper API key for web search | - |
| `INPUT_PATH` | No | Path for input files | `inputs` |
| `OUTPUT_PATH` | No | Path for output files | `outputs` |
| `GRADIO_SERVER_NAME` | No | Gradio server host | `0.0.0.0` |
| `GRADIO_SERVER_PORT` | No | Gradio server port | `7860` |

## Getting API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy and add to `.env`

### Serper API Key
1. Go to https://serper.dev/
2. Sign up for a free account
3. Get your API key from the dashboard
4. Copy and add to `.env`

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Docker permission errors
```bash
# On Linux, you may need to add your user to the docker group
sudo usermod -aG docker $USER
# Log out and back in for changes to take effect
```

### MCP server not connecting in Claude Desktop
1. Check that the path in config is absolute, not relative
2. Verify API keys are correct in the config
3. Check Claude Desktop logs for error messages
4. Try running the server manually: `uv run mcp_server_standalone.py`

### Port already in use (Gradio)
```bash
# Change the port in .env
echo "GRADIO_SERVER_PORT=8080" >> .env
```

## More Information

- Full MCP documentation: [MCP_SERVER.md](MCP_SERVER.md)
- Project README: [README.md](README.md)
- Report issues: https://github.com/rafacalassara/JobApplicationFlow/issues
