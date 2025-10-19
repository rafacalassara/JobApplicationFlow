#!/usr/bin/env python
"""
MCP Server for Job Application Flow

This server exposes the Job Application Flow functionality as MCP tools
that can be used by any LLM client supporting the Model Context Protocol.
"""

import os
import json
import asyncio
from typing import Any
from datetime import datetime
from pathlib import Path

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from mcp.server.stdio import stdio_server

from dotenv import load_dotenv
from main import JobApplicationFlow

# Load environment variables
load_dotenv()

# Initialize MCP server
app = Server("job-application-flow")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="generate_job_application",
            description="""
            Generate a complete job application package including:
            - Tailored resume based on LinkedIn profile
            - Company research report
            - Draft application email
            
            This tool processes a LinkedIn resume PDF, job posting URL, and company information
            to create customized application materials.
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
                        "description": "URL of the job posting (e.g., LinkedIn job URL)"
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
                        "description": "Optional: Special instructions for resume customization",
                        "default": ""
                    },
                    "user_considerations_for_companies_research_crew": {
                        "type": "string",
                        "description": "Optional: Special instructions for company research",
                        "default": ""
                    },
                    "user_considerations_for_email_crew": {
                        "type": "string",
                        "description": "Optional: Special instructions for email writing",
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
        ),
        Tool(
            name="tailor_resume",
            description="""
            Tailor a resume for a specific job posting.
            Takes a LinkedIn resume and job posting URL to create a customized resume.
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
                    "user_considerations": {
                        "type": "string",
                        "description": "Optional: Special instructions for resume customization",
                        "default": ""
                    }
                },
                "required": ["linkedin_source_resume_path", "job_posting"]
            }
        ),
        Tool(
            name="research_company",
            description="""
            Research a company and generate a detailed report.
            Useful for preparing for interviews and understanding company culture.
            """,
            inputSchema={
                "type": "object",
                "properties": {
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
                        "description": "Company location"
                    },
                    "user_considerations": {
                        "type": "string",
                        "description": "Optional: Specific areas to focus research on",
                        "default": ""
                    }
                },
                "required": ["company", "company_url", "company_location"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""
    
    if name == "generate_job_application":
        return await generate_job_application(arguments)
    elif name == "tailor_resume":
        return await tailor_resume(arguments)
    elif name == "research_company":
        return await research_company(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def generate_job_application(arguments: dict) -> list[TextContent]:
    """Generate complete job application materials."""
    
    # Prepare inputs
    inputs = {
        "linkedin_source_resume_path": arguments["linkedin_source_resume_path"],
        "job_posting": arguments["job_posting"],
        "company": arguments["company"],
        "company_url": arguments["company_url"],
        "company_location": arguments["company_location"],
        "user_considerations_for_resume_crew": arguments.get("user_considerations_for_resume_crew", ""),
        "user_considerations_for_companies_research_crew": arguments.get("user_considerations_for_companies_research_crew", ""),
        "user_considerations_for_email_crew": arguments.get("user_considerations_for_email_crew", ""),
    }
    
    try:
        # Create and run the flow
        job_flow = JobApplicationFlow(inputs=inputs)
        flow_inputs = job_flow.init()
        job_flow.kickoff()
        
        # Read generated files
        resume_path = flow_inputs["crew_generated_resume_path"]
        report_path = flow_inputs["company_report_path"]
        email_path = flow_inputs["reviewed_email_file_path"]
        
        results = []
        
        # Read resume
        if os.path.exists(resume_path):
            with open(resume_path, 'r') as f:
                resume_content = f.read()
            results.append(TextContent(
                type="text",
                text=f"## Generated Resume\n\n{resume_content}"
            ))
        
        # Read company report
        if os.path.exists(report_path):
            with open(report_path, 'r') as f:
                report_content = f.read()
            results.append(TextContent(
                type="text",
                text=f"## Company Research Report\n\n{report_content}"
            ))
        
        # Read email
        if os.path.exists(email_path):
            with open(email_path, 'r') as f:
                email_content = f.read()
            results.append(TextContent(
                type="text",
                text=f"## Application Email\n\n{email_content}"
            ))
        
        # Add summary
        results.insert(0, TextContent(
            type="text",
            text=f"""# Job Application Generated Successfully

**Company:** {arguments['company']}
**Job Posting:** {arguments['job_posting']}

Generated files:
- Resume: {resume_path}
- Company Report: {report_path}
- Email: {email_path}

---
"""
        ))
        
        return results
        
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error generating job application: {str(e)}"
        )]


async def tailor_resume(arguments: dict) -> list[TextContent]:
    """Tailor a resume for a specific job."""
    
    inputs = {
        "linkedin_source_resume_path": arguments["linkedin_source_resume_path"],
        "job_posting": arguments["job_posting"],
        "user_considerations_for_resume_crew": arguments.get("user_considerations", ""),
        "company": "Unknown",  # Default values
        "company_url": "",
        "company_location": "",
    }
    
    try:
        from crews.tailor_resume_crew.tailor_resume_crew import TailorResumeCrew
        
        # Prepare flow inputs
        job_flow = JobApplicationFlow(inputs=inputs)
        flow_inputs = job_flow.init()
        
        # Run only the resume tailoring crew
        result = TailorResumeCrew(flow_inputs).crew().kickoff(flow_inputs)
        
        # Read the generated resume
        resume_path = flow_inputs["crew_generated_resume_path"]
        if os.path.exists(resume_path):
            with open(resume_path, 'r') as f:
                resume_content = f.read()
            
            return [TextContent(
                type="text",
                text=f"""# Tailored Resume

**Job Posting:** {arguments['job_posting']}
**Output File:** {resume_path}

---

{resume_content}
"""
            )]
        else:
            return [TextContent(
                type="text",
                text="Resume generated but file not found. Please check the outputs directory."
            )]
            
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error tailoring resume: {str(e)}"
        )]


async def research_company(arguments: dict) -> list[TextContent]:
    """Research a company and generate a report."""
    
    inputs = {
        "company": arguments["company"],
        "company_url": arguments["company_url"],
        "company_location": arguments["company_location"],
        "user_considerations_for_companies_research_crew": arguments.get("user_considerations", ""),
        "job_posting": "",  # Default values
        "linkedin_source_resume_path": "",
    }
    
    try:
        from crews.companies_research_crew.companies_research_crew import CompaniesResearchCrew
        
        # Prepare flow inputs
        job_flow = JobApplicationFlow(inputs=inputs)
        flow_inputs = job_flow.init()
        
        # Run only the company research crew
        result = CompaniesResearchCrew(flow_inputs).crew().kickoff(flow_inputs)
        
        # Read the generated report
        report_path = flow_inputs["company_report_path"]
        if os.path.exists(report_path):
            with open(report_path, 'r') as f:
                report_content = f.read()
            
            return [TextContent(
                type="text",
                text=f"""# Company Research Report

**Company:** {arguments['company']}
**URL:** {arguments['company_url']}
**Location:** {arguments['company_location']}
**Output File:** {report_path}

---

{report_content}
"""
            )]
        else:
            return [TextContent(
                type="text",
                text="Research completed but report file not found. Please check the outputs directory."
            )]
            
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error researching company: {str(e)}"
        )]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
