#!/usr/bin/env python
"""
MCP Server for Job Application Flow
Exposes the job application flow functionality as MCP tools
"""
import os
import json
import asyncio
from typing import Any, Dict, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
from main import JobApplicationFlow
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create the MCP server instance
app = Server("job-application-flow")

# Define the tool
PROCESS_JOB_APPLICATION_TOOL = Tool(
    name="process_job_application",
    description="""Process a job application by generating a tailored resume, company research report, and application email.
    
This tool automates the job application process by:
1. Converting and tailoring your resume based on the job requirements
2. Researching the company and creating a detailed report
3. Generating a professional application email

Required inputs:
- linkedin_source_resume_path: Path to your LinkedIn resume PDF
- job_posting: URL of the job posting (preferably LinkedIn)
- company: Company name
- company_url: Company website URL
- company_location: Company location (City, State)

Optional inputs:
- user_considerations_for_resume_crew: Custom instructions for resume tailoring
- user_considerations_for_companies_research_crew: Custom focus areas for company research
- user_considerations_for_email_crew: Custom instructions for email generation
""",
    inputSchema={
        "type": "object",
        "properties": {
            "linkedin_source_resume_path": {
                "type": "string",
                "description": "Path to the LinkedIn resume PDF file"
            },
            "job_posting": {
                "type": "string",
                "description": "URL of the job posting"
            },
            "company": {
                "type": "string",
                "description": "Name of the company"
            },
            "company_url": {
                "type": "string",
                "description": "Company website URL"
            },
            "company_location": {
                "type": "string",
                "description": "Company location (City, State/Region)"
            },
            "user_considerations_for_resume_crew": {
                "type": "string",
                "description": "Optional: Custom instructions for resume tailoring",
                "default": ""
            },
            "user_considerations_for_companies_research_crew": {
                "type": "string",
                "description": "Optional: Custom focus areas for company research",
                "default": ""
            },
            "user_considerations_for_email_crew": {
                "type": "string",
                "description": "Optional: Custom instructions for email generation",
                "default": ""
            }
        },
        "required": [
            "linkedin_source_resume_path",
            "job_posting",
            "company",
            "company_url",
            "company_location"
        ]
    }
)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [PROCESS_JOB_APPLICATION_TOOL]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    if name != "process_job_application":
        raise ValueError(f"Unknown tool: {name}")
    
    try:
        # Extract arguments
        inputs = {
            "linkedin_source_resume_path": arguments.get("linkedin_source_resume_path"),
            "job_posting": arguments.get("job_posting"),
            "company": arguments.get("company"),
            "company_url": arguments.get("company_url"),
            "company_location": arguments.get("company_location"),
            "user_considerations_for_resume_crew": arguments.get(
                "user_considerations_for_resume_crew", 
                "Highlight relevant skills and experience. Remove company names from resume."
            ),
            "user_considerations_for_companies_research_crew": arguments.get(
                "user_considerations_for_companies_research_crew", 
                ""
            ),
            "user_considerations_for_email_crew": arguments.get(
                "user_considerations_for_email_crew", 
                ""
            ),
        }
        
        # Run the job application flow
        job_flow = JobApplicationFlow(inputs=inputs)
        flow_inputs = job_flow.init()
        job_flow.kickoff()
        
        # Prepare the response with output file paths
        result = {
            "status": "success",
            "message": "Job application materials generated successfully",
            "outputs": {
                "resume": flow_inputs.get("crew_generated_resume_path"),
                "resume_pdf": flow_inputs.get("crew_generated_resume_path", "").replace(".md", ".pdf"),
                "company_report": flow_inputs.get("company_report_path"),
                "email": flow_inputs.get("reviewed_email_file_path")
            }
        }
        
        # Try to include content of generated files
        try:
            with open(flow_inputs.get("crew_generated_resume_path", ""), "r") as f:
                result["resume_content"] = f.read()
        except:
            pass
            
        try:
            with open(flow_inputs.get("company_report_path", ""), "r") as f:
                result["report_content"] = f.read()
        except:
            pass
            
        try:
            with open(flow_inputs.get("reviewed_email_file_path", ""), "r") as f:
                result["email_content"] = f.read()
        except:
            pass
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
        
    except Exception as e:
        error_result = {
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__
        }
        return [TextContent(
            type="text",
            text=json.dumps(error_result, indent=2)
        )]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
