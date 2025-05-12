from django.shortcuts import render
import requests
import json

API_URL = "http://api:8000/process-resumes/"

def upload_form(request):
    """View para exibir o formulário e processar o upload de múltiplos currículos."""
    
    if request.method == 'POST':
        # Obter a lista de arquivos PDF e as palavras-chave do formulário
        pdf_files = request.FILES.getlist('pdf_files') # Alterado para getlist
        keywords = request.POST.get('keywords', '')

        if not pdf_files:
            return render(request, 'processor_interface/upload_form.html', {
                'error': 'Por favor, selecione pelo menos um arquivo PDF.'
            })
        
        if not keywords:
            return render(request, 'processor_interface/upload_form.html', {
                'error': 'Por favor, insira pelo menos uma palavra-chave.' 
            })
        
        valid_files_for_api = []
        validation_errors = []

        for pdf_file in pdf_files:
            
            if not pdf_file.name.endswith('.pdf'):

                validation_errors.append(f"Arquivo '{pdf_file.name}' não é um PDF válido.")
            
            else:
               
                valid_files_for_api.append(('files', (pdf_file.name, pdf_file.read(), pdf_file.content_type)))

        if validation_errors:
             
             return render(request, 'processor_interface/upload_form.html', {
                'error': " ".join(validation_errors)
            })

        if not valid_files_for_api:
             
             return render(request, 'processor_interface/upload_form.html', {
                'error': 'Nenhum arquivo PDF válido foi selecionado para processamento.'
            })

        try:
    
            data = {'keywords': keywords}
            
            response = requests.post(API_URL, files=valid_files_for_api, data=data)
            
            if response.status_code == 200:
                
                api_response = response.json()
                results_list = api_response.get('results', []) 
                
                processed_results = []
                all_keywords = [k.strip() for k in keywords.split(',')]
                total_keywords = len(all_keywords)

                for result in results_list:

                    filename = result.get('filename')
                    error = result.get('error')
                    keywords_found_data = result.get('keywords_found', {})
                    
                    if error:

                        processed_results.append({
                            'filename': filename,
                            'error': error
                        })

                    else:

                        keywords_found = {k: count for k, count in keywords_found_data.items() if count > 0}
                        missing_keywords = [k for k, count in keywords_found_data.items() if count == 0]
                        found_keywords_count = len(keywords_found)
                        
                        match_percentage = 0

                        if total_keywords > 0:

                            match_percentage = (found_keywords_count / total_keywords) * 100
                        
                        processed_results.append({
                            'filename': filename,
                            'keywords_found': keywords_found,
                            'missing_keywords': missing_keywords,
                            'match_percentage': match_percentage,
                            'error': None
                        })

                

                return render(request, 'processor_interface/upload_form.html', {
                    'processed_results': processed_results 
                })
            else:

                error_message = f"Erro ao comunicar com a API: {response.status_code}"
                try:

                    error_detail = response.json().get('detail', '')

                    if error_detail:

                        error_message += f" - {error_detail}"

                except json.JSONDecodeError:
                     error_message += f" - Resposta não JSON: {response.text}"
                except Exception:
                    pass 
                
                return render(request, 'processor_interface/upload_form.html', {
                    'error': error_message
                })
                
        except requests.RequestException as e:

            return render(request, 'processor_interface/upload_form.html', {
                'error': f"Erro ao conectar com a API: {str(e)}"
            })
        except Exception as e:

            return render(request, 'processor_interface/upload_form.html', {
                'error': f"Erro inesperado durante o processamento: {str(e)}"
            })
    
    return render(request, 'processor_interface/upload_form.html')

