import PyPDF2
import re
import os
from typing import List, Dict

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extrai o texto de um arquivo PDF.
    
    Args:
        pdf_path: Caminho para o arquivo PDF
        
    Returns:
        Texto extraído do PDF
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Verificar se o PDF está protegido
            if reader.is_encrypted:

                raise ValueError("PDF protegido por senha. Não é possível processar.")
            
            # Extrair texto de todas as páginas
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
                
        if not text:

             raise ValueError("Nenhum texto pôde ser extraído do PDF. Pode ser um PDF baseado em imagem.")
             
        return text
    except ValueError as ve:

        raise ve
    except Exception as e:
        raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")

def search_keywords(text: str, keywords: List[str]) -> Dict[str, int]:
    """
    Busca palavras-chave no texto extraído do PDF (case-insensitive).
    
    Args:
        text: Texto extraído do PDF
        keywords: Lista de palavras-chave para buscar
        
    Returns:
        Dicionário com as palavras-chave encontradas e suas contagens
    """
    results = {}
    
    # Converter texto para minúsculas para busca case-insensitive
    text_lower = text.lower()
    
    for keyword in keywords:

        if not keyword:
            continue
            

        keyword_lower = keyword.lower()
        

        try:
            count = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', text_lower))
        except re.error as re_err:

            print(f"Erro de regex ao buscar '{keyword_lower}': {re_err}")
            count = 0
            

        results[keyword] = count
    
    return results
