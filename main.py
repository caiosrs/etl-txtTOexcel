import re
import pandas as pd

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

    uf_ctps_match = re.search(r'UF CTPS\s*(.*?)(?:Sexo)', pag, re.DOTALL)

    if uf_ctps_match:
        uf_ctps = uf_ctps_match.group(1).strip()
        print(f"UF CTPS = {uf_ctps if uf_ctps else ''}")
    else:
        print("UF CTPS =")

    def capturar_cpf(pag):
        # Função para tentar capturar o CPF dentro de um trecho específico
        def verificar_cpf(texto):
            # Expressão regular para capturar o CPF no formato XXX.XXX.XXX-XX
            cpf_list = re.findall(r'\d{3}\.\d{3}\.\d{3}-\d{2}', texto)
            if cpf_list:
                return cpf_list[0]  # Retorna o primeiro CPF encontrado
            return None

        # Primeira tentativa: entre "Seção" e "Salário"
        trecho_1 = re.search(r'Seção(.*?)Salário', pag, re.DOTALL)
        if trecho_1:
            cpf = verificar_cpf(trecho_1.group(1))
            if cpf:
                return cpf

        # Segunda tentativa: entre "Horário de Trabalho" e "Data de Admissão"
        trecho_2 = re.search(r'Horário de Trabalho(.*?)Data de Admissão', pag, re.DOTALL)
        if trecho_2:
            cpf = verificar_cpf(trecho_2.group(1))
            if cpf:
                return cpf

        # Terceira tentativa: entre "Seção" e "Data de Admissão"
        trecho_3 = re.search(r'Seção(.*?)Data de Admissão', pag, re.DOTALL)
        
        if trecho_3:
            # Pega o conteúdo entre "Seção" e "Data de Admissão"
            conteudo = trecho_3.group(1)
            
            # Buscar CPFs no formato XXX.XXX.XXX-XX dentro do conteúdo
            cpfs = re.findall(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b', conteudo)
            if cpfs:
                return cpfs[0]  # Retorna o primeiro CPF encontrado
            return ""

        # Quarta tentativa: entre "Data de Admissão" e "Seção"
        trecho_4 = re.search(r'Data de Admissão(.*?)Seção', pag, re.DOTALL)
        if trecho_4:
            cpf = verificar_cpf(trecho_4.group(1))
            if cpf:
                return cpf

        # Se nenhuma das verificações encontrar o CPF, retorna vazio
        return ""

    cpf = capturar_cpf(pag)
    print(f"CPF = {cpf}")

    def capturar_doc_militar(pag):
        palavras_chave = ['Preta', 'Parda', 'Branca', 'Amarela', 'Indígena']
        # Procurando a parte do texto após "Grau de instrução"
        grau_match = re.search(r'Grau de instrução\s*[:\s]*(.*)', pag)
        
        if grau_match:
            grau_instrução = grau_match.group(1).strip()
            
            # Procurando por palavras-chave (raça/cor)
            cor_match = next((palavra for palavra in palavras_chave if palavra in grau_instrução), "")
            
            # Procurando números para "Doc. militar"
            doc_militar_match = re.search(r'Doc\.\s*militar\s*[:\s]*(\d+)', pag)
            
            if doc_militar_match:
                doc_militar = doc_militar_match.group(1)
            else:
                doc_militar = ""  # Se não houver número, doc_militar será em branco

            return doc_militar
        else:
            return ""
    doc_militar = capturar_doc_militar(pag)
    print(f"Doc. Militar = {doc_militar}")

    def capturar_cor(pag):
        # Expressões para capturar o trecho entre "Horário de Trabalho" e "Seção"
        trecho = re.search(r'Autenticar\s+(\w+)', pag)
        #trecho = re.search(r'Horário de Trabalho(.*?)Seção', pag, re.DOTALL)
        
        if trecho:
            # Pega o conteúdo entre "Horário de Trabalho" e "Seção"
            conteudo = trecho.group(1)
            
            # Lista de palavras a procurar
            palavras_cor = ['Preta', 'Parda', 'Branca', 'Amarela', 'Indígena']
            
            # Verificar se alguma das palavras está presente no conteúdo
            for cor in palavras_cor:
                if cor in conteudo:
                    return cor  # Retorna a primeira palavra encontrada
            
        # Se nenhuma das palavras for encontrada, retorna vazio
        return ""

    cor = capturar_cor(pag)
    print(f"Cor = {cor}")

    def capturar_sexo(pag):
        fichas = re.split(r'(?=Ficha do Empregado)', pag)

        # Processa cada ficha para buscar "Masculino" ou "Feminino"
        for i, ficha in enumerate(fichas):
            sexos = re.findall(r'\b(Masculino|Feminino)\b', ficha, re.IGNORECASE)
            
            if sexos:
                for sexo in sexos:
                    print(f"Sexo = {sexo}")
            else:
                print("Sexo =")

    sexo = capturar_sexo(pag)

    def capturar_grau_instrucao(pag):
        fichas = re.split(r'(?=Ficha do Empregado)', pag)

        for i, ficha in enumerate(fichas):
            grau_instrucaos = re.findall(r'\b(Ensino Fundamental 5º Completo|Ensino Fundamental 6º ao 9º|Ensino Fundamental Completo|Ensino Médio Incompleto|Ensino Médio Completo|Superior Incompleto|Superior Completo|Pós-Graduação Incompleto|Pós-Graduação)\b', ficha, re.IGNORECASE)
            
            if grau_instrucaos:
                for grau_instrucao in grau_instrucaos:
                    print(f"Grau de Instrução = {grau_instrucao}")
            else:
                print("Grau de Instrução =")

    grau_instrucao = capturar_grau_instrucao(pag)

    def capturar_deficiencia(pag):
        trecho = re.search(r'Cart. Nac. Habilitação(.*?)Cor', pag, re.DOTALL)
        
        if trecho:
            conteudo = trecho.group(1)
            
            palavras_deficiencia = ['Sim', 'Não']
            
            for deficiencia in palavras_deficiencia:
                if deficiencia in conteudo:
                    return deficiencia
            
        return ""

    deficiencia = capturar_deficiencia(pag)
    print(f"Deficiência = {deficiencia}")

    def capturar_telefone(pag):
        # Encontra o trecho entre "Telefone Celular" e "Telefone Residencial"
        trecho_celular = re.search(r'Telefone Celular(.*?)Telefone Residencial', pag, re.DOTALL)
        telefone_celular = ""
        telefone_residencial = ""

        if trecho_celular:
            # Captura números de telefone no formato permitido
            telefones = re.findall(r'\b\d{2}-\d{6,10}\b', trecho_celular.group(1))
            if telefones:
                telefone_celular = telefones[0]  # Captura o primeiro telefone celular encontrado

        # Encontra telefones após "Telefone Celular" (para o telefone residencial)
        trecho_residencial = re.search(r'Telefone Residencial(.*)', pag, re.DOTALL)
        if trecho_residencial:
            telefones = re.findall(r'\b\d{2}-\d{6,10}\b', trecho_residencial.group(1))
            if telefones:
                telefone_residencial = telefones[0]  # Captura o primeiro telefone residencial encontrado

        # Imprime os resultados
        if telefone_celular:
            print(f"Telefone Celular = {telefone_celular}")
        else:
            print("Telefone Celular =")

        if telefone_residencial:
            print(f"Telefone Residencial = {telefone_residencial}")
        else:
            print("Telefone Residencial =")
    capturar_telefone(pag)

    def capturar_cargo(pag):
        # Tenta capturar o trecho entre "Função" e "Opção em"
        match_opcao = re.search(r'Função(.*?)Opção em', pag, re.DOTALL)
        # Tenta capturar o trecho entre "Função" e uma data no formato dd/mm/aaaa
        match_data = re.search(r'Função(.*?)(\d{2}/\d{2}/\d{4})', pag, re.DOTALL)

        cargo = ""

        if match_opcao:
            cargo = match_opcao.group(1).strip()
        elif match_data:
            cargo = match_data.group(1).strip()

        # Imprime o resultado
        print(f"Cargo = {cargo}")
    capturar_cargo(pag)

    print("Função =")

    def capturar_cbo(pag):
        # Busca o texto entre "C.B.O. " e "Horário de Trabalho"
        match = re.search(r'C\.B\.O\.\s+(.*?)Horário de Trabalho', pag, re.DOTALL)
        
        cbo = ""
        if match:
            cbo = match.group(1).strip()
        
        # Imprime o resultado
        print(f"CBO = {cbo}")
    capturar_cbo(pag)

    def capturar_data_admissao(pag):
        # Busca o trecho entre "Conta vinculada no banco" e "Data da Retificação"
        trecho = re.search(r'Conta vinculada no banco(.*?)Data da Retificação', pag, re.DOTALL)
        
        data_admissao = ""
        if trecho:
            # Busca a primeira data no formato dd/mm/aaaa no trecho encontrado
            data = re.search(r'\b\d{2}/\d{2}/\d{4}\b', trecho.group(1))
            if data:
                data_admissao = data.group(0)
        
        # Se nenhuma data foi encontrada, busca a primeira data após "Data da Retificação"
        if not data_admissao:
            data_retificacao = re.search(r'Data da Retificação.*?\b(\d{2}/\d{2}/\d{4})\b', pag, re.DOTALL)
            if data_retificacao:
                data_admissao = data_retificacao.group(1)
        
        # Imprime o resultado
        print(f"Data de Admissão = {data_admissao}")
    capturar_data_admissao(pag)

    def capturar_salario(pag):
        # Procura a palavra "Por" seguida por qualquer texto e, depois, o primeiro valor monetário
        match = re.search(r'\bPor\b.*?(\d{1,3}(?:\.\d{3})*,\d{2})', pag, re.DOTALL)
        
        salario = ""
        if match:
            salario = match.group(1).strip()
        
        # Imprime o resultado
        print(f"Salário = {salario}")
    capturar_salario(pag)

    print("Por = Mês")

    def capturar_horarios(pag):
        # Localiza o texto "Horário de Intervalo" e pega os próximos 8 conjuntos separados por espaço
        match = re.search(r'Horário de Intervalo((?:\s+\S+){8})', pag)
        if match:
            # Divide os 8 conjuntos em uma lista
            proximos = match.group(1).strip().split()
            if len(proximos) >= 8:
                # Pega os 4 primeiros como horário_trabalho e os 4 últimos como horário_intervalo
                horario_trabalho = " ".join(proximos[:4])
                horario_intervalo = " ".join(proximos[4:])
                print(f"Horário de Trabalho = {horario_trabalho}")
                print(f"Horário de Intervalo = {horario_intervalo}")
            else:
                print("Dados insuficientes após 'Horário de Intervalo'")
        else:
            print("Texto 'Horário de Intervalo' não encontrado")
    capturar_horarios(pag)