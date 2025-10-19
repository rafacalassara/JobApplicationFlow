# MCP (Model Context Protocol) Integration Guide

This guide explains how to use JobApplicationFlow as an MCP server with various LLM clients.

## What is MCP?

Model Context Protocol (MCP) is an open standard developed by Anthropic that enables LLM applications to securely connect to external data sources and tools. JobApplicationFlow exposes its job application processing capabilities as an MCP tool that can be used by any MCP-compatible client.

## Available Tools

### process_job_application

Processes a job application by generating:
1. A tailored resume based on job requirements
2. A comprehensive company research report
3. A professional application email

**Required Parameters:**
- `linkedin_source_resume_path` - Path to your resume PDF file
- `job_posting` - URL of the job posting
- `company` - Company name
- `company_url` - Company website URL
- `company_location` - Company location (City, State)

**Optional Parameters:**
- `user_considerations_for_resume_crew` - Custom instructions for resume tailoring
- `user_considerations_for_companies_research_crew` - Custom focus areas for company research
- `user_considerations_for_email_crew` - Custom instructions for email generation

**Returns:**
- Status and file paths for generated documents
- Content of generated resume, report, and email

## Setup Instructions

### 1. Build the MCP Docker Image

```bash
cd JobApplicationFlow
docker build -f Dockerfile.mcp -t job-application-flow-mcp .
```

### 2. Configure Your MCP Client

#### Claude Desktop (macOS)

Edit the Claude Desktop configuration file:
```bash
# Location: ~/Library/Application Support/Claude/claude_desktop_config.json
```

Add the following configuration:

```json
{
  "mcpServers": {
    "job-application-flow": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--env-file",
        "/full/path/to/JobApplicationFlow/.env",
        "-v",
        "/full/path/to/JobApplicationFlow/outputs:/usr/src/app/outputs",
        "-v",
        "/full/path/to/JobApplicationFlow/inputs:/usr/src/app/inputs",
        "job-application-flow-mcp"
      ]
    }
  }
}
```

#### Claude Desktop (Windows)

Edit the Claude Desktop configuration file:
```
Location: %APPDATA%\Claude\claude_desktop_config.json
```

Add the following configuration (use Windows path format):

```json
{
  "mcpServers": {
    "job-application-flow": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--env-file",
        "C:\\path\\to\\JobApplicationFlow\\.env",
        "-v",
        "C:\\path\\to\\JobApplicationFlow\\outputs:/usr/src/app/outputs",
        "-v",
        "C:\\path\\to\\JobApplicationFlow\\inputs:/usr/src/app/inputs",
        "job-application-flow-mcp"
      ]
    }
  }
}
```

#### Other MCP Clients

For other MCP-compatible clients, use similar configuration with the command:

```bash
docker run -i --rm \
  --env-file /path/to/.env \
  -v /path/to/outputs:/usr/src/app/outputs \
  -v /path/to/inputs:/usr/src/app/inputs \
  job-application-flow-mcp
```

### 3. Verify the Setup

1. Restart your MCP client (e.g., Claude Desktop)
2. The `job-application-flow` server should appear in the available tools
3. You should see the `process_job_application` tool

## Usage Examples

### Example 1: Basic Job Application

Ask your LLM:

```
I need help applying for a job. Please use the process_job_application tool with:
- My resume is at /inputs/my_resume.pdf
- Job posting: https://www.linkedin.com/jobs/view/1234567/
- Company: TechCorp Inc.
- Company URL: https://techcorp.com
- Location: San Francisco, CA
```

### Example 2: Custom Instructions

```
Process my job application with custom instructions:
- Resume: /inputs/john_resume.pdf
- Job: https://www.linkedin.com/jobs/view/9876543/
- Company: DataStartup
- URL: https://datastartup.io
- Location: New York, NY
- Resume instructions: Emphasize my Python and ML experience
- Company research: Focus on their AI products and recent funding
- Email instructions: Keep it concise and mention my open source contributions
```

### Example 3: Batch Processing

You can process multiple job applications in sequence by calling the tool multiple times.

## File Management

### Input Files

Place your resume PDF in the `inputs` directory:
```bash
cp your_resume.pdf JobApplicationFlow/inputs/
```

When referencing in the MCP tool, use the path relative to the container:
```
/usr/src/app/inputs/your_resume.pdf
```

Or simply:
```
inputs/your_resume.pdf
```

### Output Files

Generated files are saved to the `outputs` directory:
- `crew_generated_resume.md` - Tailored resume in Markdown
- `crew_generated_resume.pdf` - Tailored resume in PDF
- `company_report.md` - Company research report
- `reviewed_email.md` - Application email draft

These files are returned by the tool and also available on your host machine in the `outputs` directory.

## Troubleshooting

### Tool Not Appearing in Client

1. Check that Docker is running: `docker ps`
2. Verify the image exists: `docker images | grep job-application-flow-mcp`
3. Check MCP client logs for errors
4. Ensure paths in configuration are absolute and correct

### Permission Errors

Ensure the Docker container has permission to write to the output directory:
```bash
chmod -R 755 outputs inputs
```

### API Key Errors

Verify your `.env` file contains valid API keys:
```bash
cat .env
```

### Container Startup Issues

Test the container directly:
```bash
docker run -i --rm --env-file .env job-application-flow-mcp
```

The server should start and wait for input on stdin.

### Output Files Not Saved

Check volume mounts are correct:
```bash
docker run -i --rm \
  --env-file .env \
  -v "$(pwd)/outputs:/usr/src/app/outputs" \
  -v "$(pwd)/inputs:/usr/src/app/inputs" \
  job-application-flow-mcp
```

## Advanced Configuration

### Custom Model Configuration

Add to your `.env` file:
```bash
OPENAI_MODEL_NAME=gpt-4
OPENAI_API_BASE=https://api.openai.com/v1
```

### Using with Alternative OpenAI-Compatible APIs

```bash
OPENAI_API_BASE=https://your-llm-provider.com/v1
OPENAI_API_KEY=your-provider-key
```

### Running Without Docker

You can also run the MCP server directly with Python:

```bash
cd JobApplicationFlow
python mcp_server.py
```

This is useful for development but Docker is recommended for production use.

## Integration with Other Tools

### Programmatic Access

You can interact with the MCP server programmatically using the MCP Python SDK:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="docker",
    args=[
        "run", "-i", "--rm",
        "--env-file", ".env",
        "-v", "$(pwd)/outputs:/usr/src/app/outputs",
        "-v", "$(pwd)/inputs:/usr/src/app/inputs",
        "job-application-flow-mcp"
    ]
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()
        result = await session.call_tool(
            "process_job_application",
            {
                "linkedin_source_resume_path": "inputs/resume.pdf",
                "job_posting": "https://...",
                # ... other parameters
            }
        )
```

## Best Practices

1. **Resume Management**: Keep your resumes organized in the `inputs` directory
2. **Output Organization**: Regularly backup or organize files from the `outputs` directory
3. **API Usage**: Be mindful of OpenAI and Serper API usage and costs
4. **Privacy**: Never share your `.env` file or commit it to version control
5. **Batch Processing**: For multiple applications, process them sequentially to avoid rate limits

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Claude Desktop Configuration](https://docs.anthropic.com/claude/docs/mcp)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Serper API Documentation](https://serper.dev/docs)

## Support

For MCP-specific issues:
1. Check the Docker container logs: `docker logs job-application-mcp`
2. Verify MCP client configuration
3. Test with the direct Python command to isolate Docker issues
4. Open an issue on the GitHub repository with relevant logs
