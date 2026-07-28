###############################################################################
# FILE: extrator_projeto.py
###############################################################################

import os
import sys
import glob

def find_source_file():
    """Procura automaticamente por um arquivo de texto de entrada caso o padrão não exista."""
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        return sys.argv[1]
    
    if os.path.exists("entrada.txt"):
        return "entrada.txt"
        
    # Procura por qualquer .txt na pasta atual (exceto o próprio script)
    txt_files = [f for f in glob.glob("*.txt") if f != "extrator_projeto.py"]
    if txt_files:
        print(f"[Aviso] 'entrada.txt' não especificado. Usando encontrado: '{txt_files[0]}'")
        return txt_files[0]
        
    return None

def is_just_identifier(path_str):
    """
    Verifica se a string é apenas um identificador numérico/rótulo 
    (ex: '0001', 'Arquivo 0001', 'File 1', 'Nº 01').
    """
    cleaned = path_str.lower().replace("arquivo", "").replace("file", "").replace("caminho", "").replace("path", "").strip()
    cleaned = cleaned.strip("\"'# =-*:")
    return cleaned.isdigit() or cleaned == ""

def is_valid_filepath(path_str):
    """Verifica se a string parece um caminho de arquivo válido e não apenas um ID, bloco ou frase."""
    if not path_str or len(path_str) > 250:
        return False
    
    # Ignora blocos de markdown e instruções em texto descritivo
    path_lower = path_str.lower().strip()
    if path_lower.startswith("```") or "adicionar ao" in path_lower:
        return False
        
    # No Windows, esses caracteres são estritamente proibidos em caminhos de arquivos
    invalid_win_chars = set('*?"<>|')
    if any(c in invalid_win_chars for c in path_str):
        return False
        
    if is_just_identifier(path_str):
        return False
    
    # Considera válido se tiver barra de diretório, extensão com ponto ou for palavra única (ex: Dockerfile, Makefile)
    has_ext_or_dir = "." in path_str or "/" in path_str or "\\" in path_str
    is_single_word = len(path_str.split()) == 1
    return has_ext_or_dir or is_single_word

def extract_and_save_files():
    source_filepath = find_source_file()
    if not source_filepath:
        print("Erro: Nenhum arquivo de entrada (.txt) foi encontrado nesta pasta.")
        print("Certifique-se de colocar o arquivo de texto com os códigos aqui.")
        return

    print(f"Lendo dados de: {source_filepath}")
    with open(source_filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    current_filepath = None
    current_content = []
    files_created = 0

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        stripped_lower = stripped.lower()
        
        # 1. IGNORA LINHAS INDESEJADAS (markdown, instruções em texto, etc.)
        if stripped_lower.startswith("```") or "adicionar ao " in stripped_lower:
            i += 1
            continue
        
        # Procura por variações de '# Arquivo', '# FILE', etc.
        if "# arquivo" in stripped_lower or "# file" in stripped_lower:
            # Se já havia um arquivo aberto acumulando código, salva ele antes de iniciar o próximo
            if current_filepath and current_content and is_valid_filepath(current_filepath):
                save_file(current_filepath, current_content)
                files_created += 1
                current_content = []
            
            # Tenta extrair o caminho na própria linha
            potential_path = ""
            if ":" in stripped:
                potential_path = stripped.split(":", 1)[1].strip()
            else:
                parts = stripped.split(maxsplit=1)
                potential_path = parts[1].strip() if len(parts) > 1 else ""
            
            potential_path = potential_path.strip("\"'# =-*")
            
            # Se o que foi extraído for apenas um número/rótulo ou algo inválido,
            # fazemos um "lookahead" (olhamos as próximas linhas) para achar o caminho real.
            if not is_valid_filepath(potential_path):
                found_real_path = False
                lookahead = 1
                # Inspeciona até 5 linhas para frente em busca do caminho real
                while i + lookahead < len(lines) and lookahead <= 5:
                    next_line = lines[i + lookahead].strip()
                    next_line_lower = next_line.lower()
                    
                    # Ignora linhas vazias, blocos de markdown ou frases instrucionais
                    if not next_line or set(next_line).issubset(set("#=-* ")) or next_line_lower.startswith("```") or "adicionar ao " in next_line_lower:
                        lookahead += 1
                        continue
                    
                    # Limpa possíveis prefixos na linha seguinte como "# Caminho:", "File:", etc.
                    candidate = next_line
                    if ":" in candidate:
                        candidate = candidate.split(":", 1)[1].strip()
                    candidate = candidate.strip("\"'# =-*")
                    
                    # Se encontrarmos algo que pareça um caminho de arquivo real
                    if is_valid_filepath(candidate):
                        current_filepath = candidate
                        i += lookahead  # Avança o índice para pular as linhas de cabeçalho consumidas
                        found_real_path = True
                        break
                    lookahead += 1
                
                # Se não encontrou nas linhas seguintes, ignora esse bloco ou usa nome temporário
                if not found_real_path:
                    current_filepath = None
            else:
                current_filepath = potential_path
            
            i += 1
            continue

        if current_filepath:
            # Ignora linhas decorativas ou marcações de fim de arquivo
            if stripped.startswith("###") or "fim do arquivo" in stripped_lower or "end file" in stripped_lower:
                i += 1
                continue
            current_content.append(line)

        i += 1

    # Salva o último arquivo pendente
    if current_filepath and current_content and is_valid_filepath(current_filepath):
        save_file(current_filepath, current_content)
        files_created += 1

    print(f"\nProcesso concluído! Total de arquivos extraídos e salvos: {files_created}")

def save_file(filepath, content_lines):
    # Proteção extra: se o caminho tiver caracteres proibidos ou for inválido, aborta o salvamento
    if not is_valid_filepath(filepath):
        print(f"[Ignorado] -> Caminho inválido detectado: '{filepath}'")
        return

    while content_lines and not content_lines[0].strip():
        content_lines.pop(0)
    while content_lines and not content_lines[-1].strip():
        content_lines.pop()

    # Evita criar arquivos vazios
    if not content_lines:
        return

    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(content_lines) + "\n")
    
    print(f"[Salvo] -> {filepath}")

if __name__ == "__main__":
    extract_and_save_files()

###############################################################################
# END FILE
###############################################################################