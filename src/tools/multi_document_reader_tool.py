from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from pypdf import PdfReader
import docx2txt
import io

class DocumentReaderInput(BaseModel):
    """Schema de entrada para a ferramenta de leitura de documentos."""
    file_path: str = Field(..., description="Caminho do arquivo a ser lido (PDF, DOCX, TXT, etc)")

class MultiDocumentReaderTool(BaseTool):
    name: str = "Leitor de Documentos Múltiplos"
    description: str = """
    Lê o conteúdo de vários tipos de documentos incluindo PDF, DOCX e TXT.
    Suporta formatos: .pdf, .docx, .txt, .md
    """
    args_schema: Type[BaseModel] = DocumentReaderInput

    def _run(self, file_path: str) -> str:
        """
        Executa a leitura do documento baseado na extensão do arquivo.
        
        Args:
            file_path: Caminho completo do arquivo
            
        Returns:
            Conteúdo extraído do documento
        """
        try:
            file_extension = file_path.lower().split('.')[-1]
            
            if file_extension == 'pdf':
                return self._read_pdf(file_path)
            elif file_extension == 'docx':
                return self._read_docx(file_path)
            elif file_extension in ['txt', 'md']:
                return self._read_txt(file_path)
            else:
                return f"Formato de arquivo não suportado: {file_extension}"
                
        except Exception as e:
            return f"Erro ao ler o arquivo: {str(e)}"
    
    def _read_pdf(self, file_path: str) -> str:
        """Extrai texto de arquivo PDF usando pypdf."""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            return f"Erro ao ler PDF: {str(e)}"
    
    def _read_docx(self, file_path: str) -> str:
        """Extrai texto de arquivo DOCX usando docx2txt."""
        try:
            text = docx2txt.process(file_path)
            return text.strip()
        except Exception as e:
            return f"Erro ao ler DOCX: {str(e)}"
    
    def _read_txt(self, file_path: str) -> str:
        """Lê arquivo de texto simples."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Erro ao ler TXT: {str(e)}"
