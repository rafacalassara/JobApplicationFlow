# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   Job Application Flow System                    │
└─────────────────────────────────────────────────────────────────┘

┌───────────────────────────┐    ┌───────────────────────────────┐
│    Deployment Options     │    │      User Interfaces          │
└───────────────────────────┘    └───────────────────────────────┘

   ┌─────────────────┐              ┌──────────────────┐
   │  UV Standalone  │              │   Gradio Web UI  │
   │   (No venv!)    │              │  localhost:7860  │
   └────────┬────────┘              └────────┬─────────┘
            │                                │
   ┌────────┴────────┐              ┌───────┴──────────┐
   │  Docker Image   │              │  Claude Desktop  │
   │  (MCP Server)   │              │   Zed Editor     │
   └────────┬────────┘              │   Other MCP      │
            │                       │    Clients       │
   ┌────────┴────────┐              └───────┬──────────┘
   │ Docker Compose  │                      │
   │  (Both Services)│                      │
   └────────┬────────┘                      │
            │                               │
            └───────────────┬───────────────┘
                           │
            ┌──────────────▼──────────────┐
            │                              │
            │     MCP Server / Gradio      │
            │         (main.py)            │
            │                              │
            └──────────────┬───────────────┘
                          │
            ┌─────────────▼─────────────┐
            │                            │
            │   JobApplicationFlow       │
            │     (Flow Engine)          │
            │                            │
            └──────────────┬─────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼─────┐    ┌─────▼──────┐   ┌─────▼──────┐
   │  Tailor  │    │  Company   │   │   Email    │
   │  Resume  │    │  Research  │   │   Writer   │
   │   Crew   │    │    Crew    │   │    Crew    │
   └────┬─────┘    └─────┬──────┘   └─────┬──────┘
        │                │                 │
        └────────────────┼─────────────────┘
                        │
            ┌───────────▼───────────┐
            │                        │
            │   External Services    │
            │                        │
            │  • OpenAI GPT         │
            │  • Serper (Search)    │
            │  • Web Scraping       │
            │                        │
            └────────────────────────┘
```

## Component Descriptions

### Entry Points

1. **UV Standalone** (`mcp_server_standalone.py`)
   - Direct execution with UV
   - Automatic dependency management
   - No virtual environment needed
   - Perfect for quick starts

2. **Docker Images**
   - `Dockerfile`: Gradio web interface
   - `Dockerfile.mcp`: MCP server
   - Isolated, reproducible environments

3. **Docker Compose** (`docker-compose.yml`)
   - Orchestrates both services
   - Shared network and volumes
   - Easy multi-service deployment

### User Interfaces

1. **Gradio Web UI**
   - Interactive web interface
   - File upload and download
   - Real-time processing feedback
   - Accessible via browser

2. **MCP Clients**
   - Claude Desktop integration
   - Zed editor integration
   - Any MCP-compatible client
   - Natural language interaction

### Core Engine

**JobApplicationFlow** (`main.py`)
- Orchestrates the entire workflow
- Manages crew execution
- Handles file I/O
- Configurable via environment variables

### Crew System

Three specialized crews work together:

1. **Tailor Resume Crew**
   - Analyzes LinkedIn resume
   - Scrapes job posting
   - Generates tailored resume
   - Converts to PDF

2. **Company Research Crew**
   - Web search via Serper
   - Website scraping
   - Report generation
   - Key insights extraction

3. **Email Writer Crew**
   - Uses resume and company info
   - Crafts personalized email
   - Professional tone
   - Ready to send

### External Services

- **OpenAI GPT**: AI reasoning and generation
- **Serper API**: Web search capabilities
- **Web Scraping**: Content extraction

## Data Flow

```
Input Files (inputs/)
    ↓
User Request (Gradio/MCP)
    ↓
JobApplicationFlow
    ↓
Parallel Crew Execution
    ↓
Generated Files (outputs/)
    ↓
User (Download/View)
```

## Environment Variables

```
┌───────────────────────────────────────┐
│         Environment Variables         │
├───────────────────────────────────────┤
│ Required:                             │
│  • OPENAI_API_KEY                     │
│  • SERPER_API_KEY                     │
├───────────────────────────────────────┤
│ Optional:                             │
│  • INPUT_PATH (default: inputs)       │
│  • OUTPUT_PATH (default: outputs)     │
│  • GRADIO_SERVER_NAME (default: 0.0.0.0)│
│  • GRADIO_SERVER_PORT (default: 7860) │
└───────────────────────────────────────┘
```

## File Structure

```
JobApplicationFlow/
├── mcp_server.py              # MCP server implementation
├── mcp_server_standalone.py   # UV standalone script
├── main.py                    # Core flow engine
├── app.py                     # Gradio interface
├── pyproject.toml             # Python package config
├── requirements.txt           # Dependencies
│
├── Dockerfile                 # Gradio Docker image
├── Dockerfile.mcp             # MCP Docker image
├── docker-compose.yml         # Multi-service orchestration
│
├── crews/                     # AI agent crews
│   ├── tailor_resume_crew/
│   ├── companies_research_crew/
│   └── email_writer_crew/
│
├── tools/                     # Utility tools
│   ├── convert_resume_to_pdf.py
│   └── ...
│
├── inputs/                    # Input files
│   └── (User PDF resumes)
│
├── outputs/                   # Generated files
│   ├── crew_generated_resume.md
│   ├── crew_generated_resume.pdf
│   ├── company_report.md
│   └── reviewed_email.md
│
└── docs/                      # Documentation
    ├── README.md
    ├── MCP_SERVER.md
    ├── QUICKSTART.md
    └── MIGRATION_SUMMARY.md
```

## Deployment Scenarios

### Scenario 1: Personal Use (UV)
```bash
uv run mcp_server_standalone.py
# Configure in Claude Desktop
```
**Best for**: Individual users, quick testing

### Scenario 2: Development (Python)
```bash
python app.py
# Open http://localhost:7860
```
**Best for**: Development, customization

### Scenario 3: Production (Docker)
```bash
docker-compose up -d
```
**Best for**: Stable deployments, team use

### Scenario 4: LLM Integration (MCP)
```
Claude Desktop → MCP Server → Crews → Results
```
**Best for**: Natural language interaction, automation

## Security Considerations

- API keys stored in environment variables
- No credentials in code or Git
- Docker secrets support available
- Network isolation in Docker
- Input validation on all user data

## Performance

- **Parallel crew execution** where possible
- **Caching** for repeated requests
- **Async I/O** for MCP server
- **Docker layer caching** for fast rebuilds
- **Volume mounts** for persistent data

## Scalability

Current architecture supports:
- Single user: Direct Python/UV execution
- Small team: Docker Compose
- Large scale: Kubernetes ready (Docker images)
- API access: MCP server protocol

Future scaling options:
- Load balancing
- Distributed crew execution
- Queue-based processing
- Caching layer
