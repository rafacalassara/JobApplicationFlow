
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class JobAppState(BaseModel):
    base_resume: str = Field(
        default="inputs/base_resume.md",
        description="Caminho padrão para o arquivo base do currículo em Markdown (fixo).",
    )
    linkedin_md_target_resume_path: str = Field(
        default="outputs/linkedin_md_target_resume.md",
        description="Caminho padrão de saída para o currículo convertido de PDF do LinkedIn para MD (fixo).",
    )
    crew_generated_resume_path: str = Field(
        default="outputs/crew_generated_resume.md",
        description="Caminho padrão de saída para o currículo gerado/adaptado pela crew (fixo).",
    )
    company_report_path: str = Field(
        default="outputs/company_report.md",
        description="Caminho padrão de saída para o relatório de empresa (fixo).",
    )
    email_file_path: str = Field(
        default="outputs/email.md",
        description="Caminho padrão de saída para o e-mail inicial (fixo).",
    )
    reviewed_email_file_path: str = Field(
        default="outputs/reviewed_email.md",
        description="Caminho padrão de saída para o e-mail revisado (fixo).",
    )
    linkedin_source_resume_path: str = Field(
        default="inputs/Profile.pdf",
        description="Caminho padrão do PDF exportado do LinkedIn (pode ser sobrescrito pela UI).",
    )
    current_date: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d"),
        description="Data corrente no formato YYYY-MM-DD (gerado automaticamente).",
    )

    # Campos dinâmicos (opcionais) fornecidos pela UI/execução
    job_posting: Optional[str] = Field(
        default=None,
        description="URL da vaga (opcional). Ex.: link da vaga no LinkedIn.",
    )
    company: Optional[str] = Field(
        default=None,
        description="Nome da empresa alvo (opcional).",
    )
    company_url: Optional[str] = Field(
        default=None,
        description="URL do site da empresa (opcional).",
    )
    company_location: Optional[str] = Field(
        default=None,
        description="Localização da empresa (opcional).",
    )
    resume_language: Optional[str] = Field(
        default=None,
        description="Idioma desejado para o currículo (opcional). Ex.: 'en', 'pt'.",
    )
    user_considerations_for_resume_crew: Optional[str] = Field(
        default=None,
        description="Observações do usuário para a crew de currículo (opcional).",
    )
    user_considerations_for_companies_research_crew: Optional[str] = Field(
        default=None,
        description="Observações do usuário para a crew de pesquisa de empresas (opcional).",
    )
    user_considerations_for_email_crew: Optional[str] = Field(
        default=None,
        description="Observações do usuário para a crew de e-mail (opcional).",
    )
