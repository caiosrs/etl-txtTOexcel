import re

# Caminho para o arquivo
caminho = r'C:\Reviant\Documentos\Codes\Python\Ficha de Registro - ETL\ANDRE_PIRES-FichaRegistro.txt'

# Abrindo o arquivo no modo de leitura com a codificação utf-8
with open(caminho, 'r', encoding='utf-8') as arquivo:
    # Lendo o conteúdo completo do arquivo
    conteudo = arquivo.read()

# Utilizando expressão regular para dividir o conteúdo em páginas ou fichas (opcional)
paginas = re.split(r'Autenticar', conteudo)  # Divide o texto em partes entre a palavra "Autenticar"

# Imprimindo as fichas encontradas
for i, pag in enumerate(paginas, 1):
    if not pag.strip():
        continue
    
    print(f"\n--- Ficha {i} ---")
    
    # Capturando o trecho entre "Beneficiários" e "Residência"
    empregado_match = re.search(r'Beneficiários(.*?)Residência', pag, re.DOTALL)
    
    if empregado_match:
        empregado_conteudo = empregado_match.group(1).strip()  # Captura o conteúdo e remove espaços extras

        # Dividindo o conteúdo por quebras de linha
        linhas = [linha.strip() for linha in empregado_conteudo.split('\n') if linha.strip()]

        # Verificando se há mais de uma linha
        if len(linhas) > 1:
            beneficiario = linhas[0]  # Primeira linha como beneficiário
            empregado = linhas[1]  # Segunda linha como empregado
            print("Empregado =", empregado)

            # Separando beneficiários por vírgula e imprimindo individualmente
            beneficiarios = [b.strip() for b in beneficiario.split(',')]
            for idx, nome in enumerate(beneficiarios, 1):
                print(f"Beneficiario{idx} =", nome)

        elif len(linhas) == 1:
            empregado = linhas[0]  # Se houver apenas uma linha, é o empregado
            print("Empregado =", empregado)
        else:
            print("Nenhuma linha encontrada.")
    else:
        print("Empregado =")

    # Capturando o trecho entre "Residência" e "Data de nascimento"
    endereco_match = re.search(r'Residência(.*?)Data de nascimento', pag, re.DOTALL)
    
    if endereco_match:
        endereco_conteudo = endereco_match.group(1).strip()
        
        # Separando o endereço por vírgulas
        partes_endereco = [p.strip() for p in endereco_conteudo.split(',')]
        
        if len(partes_endereco) == 6:
            logradouro = partes_endereco[0]
            numero = partes_endereco[1]
            bairro = partes_endereco[2]
            cidade = partes_endereco[3]
            estado = partes_endereco[4]
            cep = partes_endereco[5]

            # Removendo o "- CEP:" do campo CEP
            cep = re.sub(r'- CEP:', '', cep).strip()

            # Imprimindo as variáveis de endereço
            print("Logradouro =", logradouro)
            print("Número =", numero)
            print("Bairro =", bairro)
            print("Cidade =", cidade)
            print("Estado =", estado)
            print("CEP =", cep)
        else:
            print("Endereco = ")
    else:
        print("Endereco =")

    # Capturando a data de nascimento
    data_nascimento_match = re.search(r'Local do nascimento(.*?)Estado civil', pag, re.DOTALL)

    if data_nascimento_match:
        data_nascimento_conteudo = data_nascimento_match.group(1).strip()
        
        # Procurando a primeira data no formato dd/mm/aaaa ou dd-mm-aaaa
        primeira_data_match = re.search(r'\b\d{2}[/-]\d{2}[/-]\d{4}\b', data_nascimento_conteudo)

        if primeira_data_match:
            data_nascimento_conteudo = primeira_data_match.group()
        else:
            data_nascimento_conteudo = ""  # Se não encontrar uma data, define como string vazia

        print("Data de Nascimento =", data_nascimento_conteudo)

    # Inicializa a variável como uma string vazia antes de usar
    cidade_nascimento_conteudo = ""

    cidade_nascimento_match = re.search(r'País da nacionalidade(.*?)-', pag, re.DOTALL)

    if cidade_nascimento_match:
        cidade_nascimento_conteudo = cidade_nascimento_match.group(1).strip()

        # Verificando se o conteúdo começa com "BRASIL"
        if cidade_nascimento_conteudo.startswith("BRASIL"):
            cidade_nascimento_conteudo = ""  # Define como string vazia se for Brasil

    print("Cidade de Nascimento =", cidade_nascimento_conteudo)

    uf_nascimento_match = re.search(r'País da nacionalidade.*?-(\s*\w{2})', pag, re.DOTALL)

    # Verifica se `cidade_nascimento_conteudo` é uma string vazia
    if cidade_nascimento_conteudo == "":
        uf_nascimento = ""
    elif uf_nascimento_match:
        uf_nascimento = uf_nascimento_match.group(1).strip()  # Captura as duas letras e remove espaços extras
    else:
        uf_nascimento = ""  # Se não encontrar o hífen ou as duas letras, define como string vazia

    print("UF de Nascimento =", uf_nascimento)

    # Procurando o texto "País da nacionalidade" e capturando os 10 primeiros conjuntos de caracteres após ele
    match = re.search(r'País da nacionalidade\s+((\S+\s+){1,10})', pag)

    if match:
        # Dividindo o resultado em um array de palavras
        palavras = match.group(1).strip().split()
        
        # Lista de palavras a serem verificadas
        palavras_chave = ["casado", "solteiro", "união estável", "divorciado", "viúvo"]
        
        # Verificando se alguma das palavras chave está no vetor
        estado_civil = ""
        for palavra in palavras:
            if palavra.lower() in palavras_chave:
                estado_civil = palavra
                break  # Para a verificação após encontrar a primeira correspondência
        
        print("Estado Civil =", estado_civil)
    else:
        print("Estado Civil =")

    pai_match = re.search(r'FILIAÇÃO\s*(.*?)(?:Mãe)', pag, re.DOTALL)

    if pai_match:
        pai = pai_match.group(1).strip()  # Captura o conteúdo e remove espaços extras
        print(f"Pai = {pai if pai else ''}")
    else:
        print("Pai =")

    # Capturando o trecho entre "Mãe" e "Cédula de Identidade" para cada ficha individualmente
    mae_match = re.search(r'Mãe\s*(.*?)(?:Cédula de Identidade)', pag, re.DOTALL)

    if mae_match:
        mae = mae_match.group(1).strip()  # Captura o conteúdo e remove espaços extras
        print(f"Mãe = {mae if mae else ''}")
    else:
        print("Mãe =")

    cedula_identidade_match = re.search(r'Data de emissão\s*(.*?)(?:CTPS)', pag, re.DOTALL)

    if cedula_identidade_match:
        cedula_identidade = cedula_identidade_match.group(1).strip()

        # Verificando se o resultado é composto de 8 ou 9 dígitos numéricos ou 8 dígitos seguidos por 'X/x'
        numero_valido_match = re.match(r'^\d{8,9}$|^\d{8}[Xx]$', cedula_identidade)

        if numero_valido_match:
            print(f"Cédula de Identidade = {cedula_identidade}")
        else:
            # Se não for válido, definir como string vazia
            cedula_identidade = ""
            print(f"Cédula de Identidade = {cedula_identidade}")
    else:
        print("Cédula de Identidade =")

    data_emissao_match = re.search(r'Órgão/UF emissor\s*(.*?)(?:Série)', pag, re.DOTALL)

    if data_emissao_match:
        data_emissao = data_emissao_match.group(1).strip()
        
        # Verificando se o resultado é uma data no formato dd/mm/aaaa ou dd-mm-aaaa
        data_valida_match = re.match(r'\b\d{2}[/-]\d{2}[/-]\d{4}\b', data_emissao)
        
        if data_valida_match:
            print(f"Data de emissão = {data_emissao}")
        else:
            # Se não for uma data, definir como string vazia
            data_emissao = ""
            print(f"Data de emissão = {data_emissao}")
    else:
        print(f"Data de emissão =")

    orgao_emissor_match = re.search(r'Título Eleitoral\s*(.*?)(?:UF CTPS)', pag, re.DOTALL)
    if orgao_emissor_match is None:
        # Tenta encontrar a correspondência de uma forma alternativa
        orgao_emissor_match = re.search(r'Título Eleitoral\s*(.*?)(?:C.B.O.)', pag, re.DOTALL)

    if orgao_emissor_match:
        orgao_emissor = orgao_emissor_match.group(1).strip()
        uf_emissor = ""

        # Verifica se o resultado não é vazio
        if orgao_emissor:
            # Verifica se há uma barra ("/") no resultado
            if "/" in orgao_emissor:
                partes = orgao_emissor.split("/")
                orgao_emissor = partes[0].strip()  # Pega a parte antes da barra
                uf_emissor = partes[1].strip()  # Pega a parte após a barra
            # Verifica se o resultado é composto por apenas dois caracteres (UF)
            elif len(orgao_emissor) == 2:
                uf_emissor = orgao_emissor
                orgao_emissor = ""  # Deixa órgão emissor vazio

        # Exibe os resultados
        print(f"Órgão emissor = {orgao_emissor}")
        print(f"UF emissor = {uf_emissor}")
    else:
        # Se não houver correspondência
        print("Órgão emissor =")
        print("UF emissor =")

    titulo_eleitoral_match = re.search(r'Zona\s*(.*?)(?:Horário de Intervalo)', pag, re.DOTALL)

    if titulo_eleitoral_match:
        # Extrai apenas os números do resultado encontrado
        titulo_eleitoral = ''.join(filter(str.isdigit, titulo_eleitoral_match.group(1).strip()))
        
        # Verifica se o resultado contém 10, 11 ou 12 números
        if len(titulo_eleitoral) in [10, 11, 12]:
            print(f"Título Eleitoral = {titulo_eleitoral}")
        else:
            # Se não atender aos critérios, faz uma segunda tentativa
            titulo_eleitoral_match = re.search(r'Zona\s*(.*?)(?:UF CTPS)', pag, re.DOTALL)
            if titulo_eleitoral_match:
                titulo_eleitoral = ''.join(filter(str.isdigit, titulo_eleitoral_match.group(1).strip()))
                if len(titulo_eleitoral) in [10, 11, 12]:
                    print(f"Título Eleitoral = {titulo_eleitoral}")
                else:
                    print("Título Eleitoral =")  # Resultado não atende aos critérios
            else:
                print("Título Eleitoral =")  # Nenhuma correspondência encontrada na segunda tentativa
    else:
        print("Título Eleitoral =")

    zona_match = re.search(r'Seção\s*(.*?)(?:CPF)', pag, re.DOTALL)

    if zona_match:
        # Extrai o resultado e separa por espaços
        zona = zona_match.group(1).strip()
        # Verifica cada conjunto de caracteres separados por espaço
        zona_validada = ' '.join(part for part in zona.split() if part.isdigit() and len(part) in [2, 3])
        
        # Imprime o resultado validado ou vazio se não atender aos critérios
        print(f"Zona = {zona_validada if zona_validada else ''}")
    else:
        print("Zona =")

    secao_match = re.search(r'Horário de Trabalho\s*(.*?)(?:Data de Admissão)', pag, re.DOTALL)

    if secao_match:
        # Extrai o resultado e separa por espaços
        secao = secao_match.group(1).strip()
        # Encontra a primeira parte que é numérica e tem 2, 3 ou 4 dígitos
        secao_validada = next((part for part in secao.split() if part.isdigit() and len(part) in [2, 3, 4]), "")
        
        # Imprime o resultado ou vazio se não atender aos critérios
        print(f"Seção = {secao_validada if secao_validada else ''}")
    else:
        print("Seção =")


    ctps_match = re.search(r'CTPS\s*(.*?)(?:Doc. militar)', pag, re.DOTALL)

    def extrair_ctps(pagina):
        # Tenta procurar e validar a CTPS no texto
        ctps_match = re.search(r'CTPS\s*(.*?)(?:Doc. militar)', pagina, re.DOTALL)
        if ctps_match:
            ctps = ctps_match.group(1).strip()
            # Separa por espaços e pega o primeiro conjunto de números com 4, 5, 6 ou 7 dígitos
            ctps_numeros = [part for part in ctps.split() if part.isdigit() and len(part) in [4, 5, 6, 7]]
            if ctps_numeros:
                return ctps_numeros[0]  # Retorna o primeiro número válido encontrado
            else:
                return ""  # Se não encontrar nenhum número válido, retorna vazio
        else:
            return ""

    # Verifica o primeiro padrão
    ctps = extrair_ctps(pag)
    if ctps:
        print(f"CTPS = {ctps}")
    else:
        # Segunda tentativa se o resultado da primeira for vazio
        ctps = extrair_ctps(pag)
        if ctps:
            print(f"CTPS = {ctps}")
        else:
            print("CTPS =")


    serie_match = re.search(r'Data de expedição da CTPS(.*?)Doc\. militar', pag, re.DOTALL)

    if serie_match:
        # Captura o trecho entre os textos "Data de expedição da CTPS" e "Doc. militar"
        section = serie_match.group(1).strip()

        # Separa os conjuntos de números por espaço
        numeros = [part for part in section.split() if part.isdigit()]

        # Pega os 3 ou 4 primeiros conjuntos de números
        serie = " ".join(numeros[:4])  # Pega os 4 primeiros, ou 3 se quiser ajuste aqui

        print(f"Série = {serie}")
    else:
        # Segunda tentativa caso a primeira falhe
        segunda_tentativa_match = re.search(r'Data de expedição da CTPS(.*?)Categoria', pag, re.DOTALL)

        if segunda_tentativa_match:
            # Captura o trecho entre os textos "Data de expedição da CTPS" e "Categoria"
            section = segunda_tentativa_match.group(1).strip()

            # Separa os conjuntos de números por espaço
            numeros = [part for part in section.split() if part.isdigit()]

            # Pega os 3 ou 4 primeiros conjuntos de números
            serie = " ".join(numeros[:4])  # Pega os 4 primeiros, ou 3 se quiser ajuste aqui

            print(f"Série = {serie}")
        else:
            print("Série =")