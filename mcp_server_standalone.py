#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = [
#   "mcp>=1.0.0",
#   "crewai>=0.86.0",
#   "crewai-tools>=0.17.0",
#   "python-dotenv>=1.0.1",
#   "beautifulsoup4>=4.12.3",
#   "pdfplumber>=0.11.4",
#   "weasyprint>=64.1",
#   "pypdfium2>=4.30.0",
# ]
# ///
"""
Standalone MCP Server for Job Application Flow (UV-based)

This script can be run directly with UV without creating a virtual environment:
    uv run mcp_server_standalone.py

It automatically manages dependencies and runs the MCP server.
"""

import os
import sys
from pathlib import Path

# Add the current directory to the path so we can import local modules
sys.path.insert(0, str(Path(__file__).parent))

# Import and run the MCP server
from mcp_server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
