# JobApplicationFlow

Welcome to the JobApplicationFlow Crew project, powered by [crewAI](https://crewai.com) and [Gradio](https://gradio.app). 

This project is a flow of AI agents that will generate a job application report, a crew generated resume and a reviewed email for a job application based on the user LinkedIn profile resume, job posting and company information.

The information of the job application and the company will be autommatically by the crews that we use based on the informations we pass in the interface.

![app_interface](.assets/app_interface.png)

## 🚀 New: MCP Server Support

This project now includes a **Model Context Protocol (MCP) server** that exposes job application tools to any LLM client (Claude Desktop, Zed, etc.). 

### Quick Start with MCP

```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run the standalone MCP server (no venv needed!)
uv run mcp_server_standalone.py
```

For detailed MCP setup and usage instructions, see [MCP_SERVER.md](MCP_SERVER.md).

## Installation

Ensure you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) and Python >=3.10 <=3.13 installed on your system. 

Clone the repository:

```bash	
git clone https://github.com/rafacalassara/JobApplicationFlow.git
cd JobApplicationFlow
```

Create a conda environment:

```bash
conda create -n job_application_flow python=3.12
```

Next, activate the environment:

```bash
conda activate job_application_flow
```

Now install the dependencies:

```bash
pip install -r requirements.txt
```

Add the `OPENAI_API_KEY` and `SERPER_API_KEY` into the `.env` file.

## Running the Project

### Option 1: Gradio Web Interface

To kickstart the project run the following command to initialize the interface:

```bash
python app.py
```

This command initializes the Gradio interface and starts the web server on `http://127.0.0.1:7860`.

### Option 2: MCP Server (for LLM Clients)

See [MCP_SERVER.md](MCP_SERVER.md) for complete MCP server documentation.

### Option 3: Docker Compose (Both Services)

Run both the Gradio UI and MCP server with Docker:

```bash
# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Start both services
docker-compose up -d
```

This will start:
- **Gradio UI** at `http://localhost:7860`
- **MCP Server** as a background service

This example, unmodified, will create a company report, a crew generated resume and a reviewed email for the job application. The files will be saved in the outputs folder.

## How the Project Works

Based on the job application, the company and the user LinkedIn profile, the crews will work as follows:

1. The `Tailor Resume Crew` will convert the user PDF LinkedIn profile into a Markdown filecrew generated resume, scrap the job application URL and adjust the user resume accordingly.

2. The `Company Report Crew` will search for the company information using the Serper API and create a detailed report on the company main points.

3. Then the `Email Writer Crew` will create an email based on the company report, the user resume and the job application information for the user to send.
