# MCP Server Documentation

## Overview

The Job Application Flow MCP (Model Context Protocol) server exposes job application automation tools to any LLM client that supports MCP. This allows you to integrate job application generation capabilities into Claude Desktop, Zed, or any other MCP-compatible client.

## Available Tools

### 1. `generate_job_application`

Generates a complete job application package including:
- Tailored resume based on LinkedIn profile
- Company research report
- Draft application email

**Parameters:**
- `linkedin_source_resume_path` (required): Path to the LinkedIn resume PDF file
- `job_posting` (required): URL of the job posting (e.g., LinkedIn job URL)
- `company` (required): Name of the company
- `company_url` (required): Company website URL
- `company_location` (required): Company location (City, State/Region)
- `user_considerations_for_resume_crew` (optional): Special instructions for resume customization
- `user_considerations_for_companies_research_crew` (optional): Special instructions for company research
- `user_considerations_for_email_crew` (optional): Special instructions for email writing

**Example:**
```json
{
  "linkedin_source_resume_path": "/path/to/resume.pdf",
  "job_posting": "https://www.linkedin.com/jobs/view/123456789/",
  "company": "TechCorp",
  "company_url": "https://techcorp.com",
  "company_location": "San Francisco, CA"
}
```

### 2. `tailor_resume`

Tailors a resume for a specific job posting.

**Parameters:**
- `linkedin_source_resume_path` (required): Path to the LinkedIn resume PDF file
- `job_posting` (required): URL of the job posting
- `user_considerations` (optional): Special instructions for resume customization

### 3. `research_company`

Researches a company and generates a detailed report.

**Parameters:**
- `company` (required): Name of the company
- `company_url` (required): Company website URL
- `company_location` (required): Company location
- `user_considerations` (optional): Specific areas to focus research on

## Installation

### Option 1: Standalone with UV (Recommended)

No virtual environment needed! Just install UV and run:

```bash
# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run the MCP server
uv run mcp_server_standalone.py
```

### Option 2: Docker

#### Using Docker Compose (Both Gradio and MCP)

```bash
# Clone the repository
git clone https://github.com/rafacalassara/JobApplicationFlow.git
cd JobApplicationFlow

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Start both services
docker-compose up -d

# The Gradio UI will be available at http://localhost:7860
# The MCP server will be running as a background service
```

#### Using Docker (MCP Server Only)

```bash
# Build the MCP server image
docker build -f Dockerfile.mcp -t job-application-mcp .

# Run the MCP server
docker run -it \
  -e OPENAI_API_KEY=your-key \
  -e SERPER_API_KEY=your-key \
  -v $(pwd)/outputs:/usr/src/app/outputs \
  -v $(pwd)/inputs:/usr/src/app/inputs \
  job-application-mcp
```

### Option 3: Traditional Python Environment

```bash
# Clone the repository
git clone https://github.com/rafacalassara/JobApplicationFlow.git
cd JobApplicationFlow

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the MCP server
python mcp_server.py
```

## Configuration

### Environment Variables

The following environment variables are required:

- `OPENAI_API_KEY`: Your OpenAI API key for GPT models
- `SERPER_API_KEY`: Your Serper API key for web search

Optional environment variables:

- `INPUT_PATH`: Custom path for input files (default: `./inputs`)
- `OUTPUT_PATH`: Custom path for output files (default: `./outputs`)

### MCP Client Configuration

To use the MCP server with Claude Desktop or other MCP clients, add the following to your MCP configuration file:

**For Claude Desktop (macOS):** `~/Library/Application Support/Claude/claude_desktop_config.json`

**For Claude Desktop (Windows):** `%APPDATA%\Claude\claude_desktop_config.json`

**Configuration:**

```json
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
        "OPENAI_API_KEY": "your-openai-api-key-here",
        "SERPER_API_KEY": "your-serper-api-key-here"
      }
    }
  }
}
```

**Important:** Replace `/absolute/path/to/JobApplicationFlow/` with the actual absolute path to where you cloned the repository.

### Alternative Configuration (Using Python)

If you prefer not to use UV, you can run the server with Python:

```json
{
  "mcpServers": {
    "job-application-flow": {
      "command": "python",
      "args": [
        "/absolute/path/to/JobApplicationFlow/mcp_server.py"
      ],
      "env": {
        "OPENAI_API_KEY": "your-openai-api-key-here",
        "SERPER_API_KEY": "your-serper-api-key-here"
      }
    }
  }
}
```

## Usage Examples

### Example 1: Generate Complete Application

In Claude Desktop (or any MCP client), you can ask:

> "I need help applying for a Software Engineer position at Google. Can you generate a complete job application package? The job posting is at https://www.linkedin.com/jobs/view/123456789/, and my resume is at /Users/me/Documents/resume.pdf. Google is located in Mountain View, CA."

The MCP server will:
1. Research Google
2. Tailor your resume for the position
3. Generate a customized application email

### Example 2: Just Tailor Resume

> "Can you tailor my resume at /Users/me/Documents/resume.pdf for this job posting: https://www.linkedin.com/jobs/view/123456789/?"

### Example 3: Research Company

> "Can you research Microsoft? Their website is https://www.microsoft.com and they're located in Redmond, WA."

## Output Files

All generated files are saved in the `outputs` directory:

- `crew_generated_resume.md` - Tailored resume in Markdown
- `crew_generated_resume.pdf` - Tailored resume in PDF format
- `company_report.md` - Company research report
- `reviewed_email.md` - Draft application email

## Troubleshooting

### MCP Server Not Connecting

1. **Check API Keys**: Ensure your `OPENAI_API_KEY` and `SERPER_API_KEY` are set correctly
2. **Check Path**: Make sure the path to `mcp_server_standalone.py` is absolute, not relative
3. **UV Installation**: Verify UV is installed by running `uv --version`
4. **Logs**: Check Claude Desktop logs for error messages

### Docker Issues

1. **Permissions**: Ensure the `outputs` and `inputs` directories are writable
2. **Environment Variables**: Verify your `.env` file contains the correct API keys
3. **Network**: Check if the containers are running with `docker ps`

### Module Import Errors

If you get import errors, ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

## Development

To modify the MCP server:

1. Edit `mcp_server.py` to add or modify tools
2. Update `pyproject.toml` if adding new dependencies
3. Test locally before deploying:
   ```bash
   python mcp_server.py
   ```

## Support

For issues or questions:
- GitHub Issues: https://github.com/rafacalassara/JobApplicationFlow/issues
- Documentation: See README.md for general project information

## License

This project is licensed under the MIT License - see the LICENSE file for details.
