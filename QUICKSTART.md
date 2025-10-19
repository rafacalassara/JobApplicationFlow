# Quick Start Guide

Get JobApplicationFlow running in 5 minutes or less!

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- OpenAI API key ([Get key](https://platform.openai.com/api-keys))
- Serper API key ([Get key](https://serper.dev/))

## Setup in 3 Steps

### 1. Clone and Configure

```bash
# Clone the repository
git clone https://github.com/rafacalassara/JobApplicationFlow.git
cd JobApplicationFlow

# Create environment file
cp .env.example .env

# Edit .env with your favorite editor and add your API keys
nano .env  # or vim, code, etc.
```

### 2. Validate Setup (Optional but Recommended)

```bash
./validate_setup.sh
```

This will check that everything is configured correctly.

### 3. Start the Application

```bash
./start.sh
```

Choose option 1 for Gradio UI or option 3 for both services.

## Access the Application

Open your browser and go to:
```
http://localhost:7860
```

## Using the Web Interface

1. **Upload** your resume PDF
2. **Enter** job details:
   - Job posting URL
   - Company name and URL
   - Company location
3. **Customize** (optional) the generation instructions
4. **Click** "Generate Application Materials"
5. **Download** your tailored resume, company report, and email

## Using as MCP Server (for LLMs like Claude)

### Build the MCP Image

```bash
docker build -f Dockerfile.mcp -t job-application-flow-mcp .
```

### Configure Claude Desktop

Edit your Claude Desktop config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add:

```json
{
  "mcpServers": {
    "job-application-flow": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "--env-file", "/FULL/PATH/TO/.env",
        "-v", "/FULL/PATH/TO/outputs:/usr/src/app/outputs",
        "-v", "/FULL/PATH/TO/inputs:/usr/src/app/inputs",
        "job-application-flow-mcp"
      ]
    }
  }
}
```

**Replace** `/FULL/PATH/TO/` with the actual path to your JobApplicationFlow directory.

### Restart Claude Desktop

The `process_job_application` tool will now be available in Claude!

## Example MCP Usage

Tell Claude:

```
Please help me apply for a Software Engineer position at TechCorp.
My resume is at inputs/john_resume.pdf
Job posting: https://www.linkedin.com/jobs/view/123456/
Company website: https://techcorp.com
Location: San Francisco, CA
```

Claude will use the MCP tool to generate your application materials!

## Common Commands

### View Logs
```bash
docker compose logs -f
```

### Stop Services
```bash
docker compose down
```

### Restart Services
```bash
docker compose restart
```

### Rebuild After Updates
```bash
docker compose up -d --build
```

## File Locations

- **Inputs:** Place your resume PDFs in `./inputs/`
- **Outputs:** Find generated files in `./outputs/`
  - `crew_generated_resume.md` - Your tailored resume
  - `crew_generated_resume.pdf` - Resume as PDF
  - `company_report.md` - Company research
  - `reviewed_email.md` - Application email

## Troubleshooting

### Port Already in Use
Change the port in `.env`:
```bash
GRADIO_SERVER_PORT=8080
```

### API Key Errors
Verify your keys in `.env`:
```bash
cat .env | grep API_KEY
```

### Container Won't Start
Check logs:
```bash
docker compose logs gradio-app
```

### Need Help?
1. Check the logs for error messages
2. Run `./validate_setup.sh` to verify your setup
3. See the full documentation:
   - `README.md` - General documentation
   - `DOCKER.md` - Docker-specific help
   - `MCP.md` - MCP integration details

## Tips for Best Results

1. **Resume Quality:** Use a well-formatted PDF resume
2. **LinkedIn URLs:** Job posting URLs from LinkedIn work best
3. **Customization:** Use the customization fields to highlight specific skills
4. **Multiple Applications:** Process them one at a time for best results
5. **Review Output:** Always review and customize generated materials

## What's Next?

- Read `README.md` for detailed features
- Check `MCP.md` for advanced MCP usage
- See `DOCKER.md` for production deployment
- Review `CHANGELOG.md` for recent updates

## Support

Need help? 
- Check the troubleshooting section above
- Review the full documentation
- Open an issue on GitHub

---

**Ready to apply?** Get started now! 🚀
