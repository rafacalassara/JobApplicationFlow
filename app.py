import gradio as gr
import os
from main import JobApplicationFlow

class OutputState:
    def __init__(self):
        self.current_page = 0
        self.outputs = []

    def set_outputs(self, outputs):
        self.outputs = outputs
        self.current_page = 0

    def get_current_content(self):
        if not self.outputs:
            return ""
        return self.outputs[self.current_page]

    def get_page_info(self):
        if not self.outputs:
            return "No content"
        return f"Page {self.current_page + 1} of {len(self.outputs)}"

output_state = OutputState()

def read_file_content(path):
    with open(path, "r") as file:
        return file.read()

def process_job_application(linkedin_source_resume_path, job_posting, company, company_url, company_location,
                          user_considerations_for_resume_crew, user_considerations_for_companies_research_crew,
                          user_considerations_for_email_crew):
    inputs = {
        "linkedin_source_resume_path": linkedin_source_resume_path.name if linkedin_source_resume_path else None,
        "job_posting": job_posting,
        "company": company,
        "company_url": company_url,
        "company_location": company_location,
        "user_considerations_for_resume_crew": user_considerations_for_resume_crew,
        "user_considerations_for_companies_research_crew": user_considerations_for_companies_research_crew,
        "user_considerations_for_email_crew": user_considerations_for_email_crew,
    }

    job_flow = JobApplicationFlow(inputs=inputs)
    inputs = job_flow.init()
    job_flow.kickoff()

    # For resume, show file info instead of preview
    resume_file_info = f"""
    ### Resume File Information
    - **File Name**: {os.path.basename(inputs['crew_generated_resume_path'])}
    - **Location**: {inputs['crew_generated_resume_path']}
    - **Status**: Ready for download
    """

    # Return all updates
    return {
        # File paths for downloads
        resume_path: gr.update(value=inputs["crew_generated_resume_path"]),
        report_path: gr.update(value=inputs["company_report_path"]),
        email_path: gr.update(value=inputs["reviewed_email_file_path"]),
        
        # Preview content
        resume_preview: gr.update(value=resume_file_info),
        report_preview: gr.update(value=read_file_content(inputs["company_report_path"])),
        email_preview: gr.update(value=read_file_content(inputs["reviewed_email_file_path"])),
        
        # # File names
        # resume_name: gr.update(value=f"📄 {os.path.basename(inputs['crew_generated_resume_path'])}"),
        # report_name: gr.update(value=f"📊 {os.path.basename(inputs['company_report_path'])}"),
        # email_name: gr.update(value=f"✉️ {os.path.basename(inputs['reviewed_email_file_path'])}"),
        
        # Show the output container
        output_container: gr.update(visible=True),
        
        # Hide loading status
        loading_status: gr.update(visible=False),
        
        # Hide generate button
        generate_button: gr.update(visible=False)
    }

def show_loading():
    return {
        generate_button: gr.update(visible=False),
        loading_status: gr.update(visible=True, value="Processing your application materials..."),
        output_container: gr.update(visible=False)
    }

# Custom CSS for styling
custom_css = """
.dark-theme {
    background-color: #1a1a1a;
    color: white;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.file-row {
    border-bottom: 1px solid #eee;
    padding: 12px 0;
    margin-bottom: 16px;
}

.file-preview {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 16px;
    margin-top: 8px;
    background: #0b0f19;
    min-height: 200px;
    overflow-y: auto;
}

.download-button {
    text-align: right;
}

.preview-container {
    height: 500px;
    overflow-y: auto;
}

.tabs {
    margin-top: 20px;
}

.tab-nav {
    margin-bottom: 16px;
}

.loading-spinner {
    text-align: center;
    padding: 20px;
    font-size: 1.2em;
}

.input-section {
    margin-bottom: 24px;
    padding: 16px;
    border: 1px solid #ddd;
    border-radius: 8px;
}
"""

# Gradio UI layout
with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as demo:
    gr.Markdown("# Job Application Automation Tool")
    
    # Input Section
    with gr.Group(elem_classes=["input-section"]):
        gr.Markdown("### Resume Upload")
        linkedin_source_resume_path = gr.File(
            label="LinkedIn Resume PDF",
            file_types=[".pdf"],
            file_count="single"
        )

    with gr.Group(elem_classes=["input-section"]):
        gr.Markdown("### Job Details")
        with gr.Row():
            job_posting = gr.Textbox(
                label="Job Posting URL",
                placeholder="https://www.linkedin.com/jobs/view/...",
                scale=2
            )
            company = gr.Textbox(
                label="Company Name",
                placeholder="Company name...",
                scale=1
            )
            company_url = gr.Textbox(
                label="Company URL",
                placeholder="https://company.com",
                scale=1
            )
        
        company_location = gr.Textbox(
            label="Company Location",
            placeholder="City, State"
        )

    with gr.Group(elem_classes=["input-section"]):
        gr.Markdown("### Customization Options")
        with gr.Row():
            user_considerations_for_resume_crew = gr.Textbox(
                label="Resume Customization Notes",
                lines=3,
                placeholder="Enter specific requirements for resume customization..."
            )
            user_considerations_for_companies_research_crew = gr.Textbox(
                label="Research Focus Areas",
                lines=3,
                placeholder="Enter specific areas of company research to focus on..."
            )
            user_considerations_for_email_crew = gr.Textbox(
                label="Email Content Notes",
                lines=3,
                placeholder="Enter specific points to include in the email..."
            )

    generate_button = gr.Button(
        "Generate Application Materials",
        variant="primary"
    )
    
    loading_status = gr.Markdown(visible=False, elem_classes=["loading-spinner"])
    
    # Output Section
    with gr.Group(visible=False) as output_container:
        gr.Markdown("### Generated Materials")
        
        with gr.Tabs():
            # Resume tab
            with gr.Tab("Resume"):
                # Download section
                with gr.Row(elem_classes=["file-row"]):
                    resume_path = gr.File(
                        label="Download Resume",
                        visible=True,
                        elem_classes=["download-button"]
                    )
                # Preview section (using Markdown to show file info)
                resume_preview = gr.Markdown(
                    label="Resume Info",
                    elem_classes=["file-preview"]
                )

            # Company report tab
            with gr.Tab("Company Research"):
                # Download section
                with gr.Row(elem_classes=["file-row"]):
                    report_path = gr.File(
                        label="Download Report",
                        visible=True,
                        elem_classes=["download-button"]
                    )
                # Preview section
                report_preview = gr.Markdown(
                    label="Report Preview",
                    elem_classes=["file-preview"]
                )

            # Email tab
            with gr.Tab("Application Email"):
                # Download section
                with gr.Row(elem_classes=["file-row"]):
                    email_path = gr.File(
                        label="Download Email",
                        visible=True,
                        elem_classes=["download-button"]
                    )
                # Preview section
                email_preview = gr.Markdown(
                    label="Email Preview",
                    elem_classes=["file-preview"]
                )

    # Event handlers
    generate_button.click(
        fn=show_loading,
        outputs=[generate_button, loading_status, output_container]
    ).then(
        fn=process_job_application,
        inputs=[
            linkedin_source_resume_path, job_posting, company, company_url, company_location,
            user_considerations_for_resume_crew, user_considerations_for_companies_research_crew,
            user_considerations_for_email_crew
        ],
        outputs=[
            resume_path, report_path, email_path,
            resume_preview, report_preview, email_preview,
            output_container, loading_status, generate_button
        ]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch()