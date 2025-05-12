from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import sys
import shutil
from typing import List
import uuid
import tempfile

# Adicionar o diretório raiz ao path para importar o processador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pdf_processor.processor import extract_text_from_pdf, search_keywords

app = FastAPI(title="Processador de Currículos", 
              description="API para processar múltiplos currículos em PDF e buscar palavras-chave")

@app.get("/")
async def root():
    return {"message": "API de Processamento de Múltiplos Currículos em PDF"}

@app.post("/process-resumes/") 
async def process_resumes(
    files: List[UploadFile] = File(...),
    keywords: str = Form(...)
):
    results_list = []
    keyword_list = [k.strip() for k in keywords.split(",")]


    # Verificar se o arquivo é um PDF
    for file in files:
        if not file.filename.endswith(".pdf"):

            results_list.append({
                "filename": file.filename,
                "error": "Apenas arquivos PDF são aceitos"
            })
            continue 
        

        with tempfile.TemporaryDirectory() as temp_dir:

            file_id = str(uuid.uuid4())
           
            file_path = os.path.join(temp_dir, f"{file_id}.pdf")
            

            try:

                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

            except Exception as e:
                results_list.append({
                    "filename": file.filename,
                    "error": f"Erro ao salvar o arquivo temporário: {str(e)}"
                })
                continue 
            

            try:
                text = extract_text_from_pdf(file_path)
                
                keyword_results = search_keywords(text, keyword_list)
                
                results_list.append({
                    "filename": file.filename,
                    "keywords_found": keyword_results
                })
            except Exception as e:
                 
                 results_list.append({
                    "filename": file.filename,
                    "error": f"Erro ao processar o PDF: {str(e)}"
                })
                 continue 

    
    if not any("error" not in r for r in results_list):
        raise HTTPException(status_code=500, detail="Nenhum arquivo pôde ser processado com sucesso.")

    return JSONResponse(content={"results": results_list})

