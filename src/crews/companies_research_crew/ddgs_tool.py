from crewai.tools import BaseTool
from duckduckgo_search import DDGS
from typing import Type
from pydantic import BaseModel, Field

class DuckDuckGoSearchInput(BaseModel):
    """Schema de entrada para a ferramenta de busca"""
    query: str = Field(..., description="A consulta de busca a ser executada")

class DuckDuckGoSearchTool(BaseTool):
    name: str = "DuckDuckGo Search Tool"
    description: str = (
        "Ferramenta para buscar informações na internet usando DuckDuckGo. "
        "Útil para encontrar informações atualizadas, notícias, artigos e dados gerais."
    )
    args_schema: Type[BaseModel] = DuckDuckGoSearchInput
    
    def _run(self, query: str) -> str:
        """Executa a busca no DuckDuckGo"""
        ddgs = DDGS()
        results = ddgs.text(
            keywords=query,
            region='wt-wt',
            safesearch='moderate',
            timelimit=None,
            max_results=10
        )
        
        if not results:
            return "Nenhum resultado encontrado."
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result['title']}\n"
                f"   URL: {result['href']}\n"
                f"   Descrição: {result['body']}\n"
            )
        
        return "\n".join(formatted_results)

if __name__ == "__main__":
    tool = DuckDuckGoSearchTool()
    print(tool.run("Qual é o melhor time de futebol do mundo?"))