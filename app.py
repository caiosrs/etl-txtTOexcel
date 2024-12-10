import re
import pandas as pd


def processar_ficha(caminho_txt, caminho_excel):
    with open(caminho_txt, 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()

    # Dividindo o conteúdo em fichas com base no separador "Autenticar"
    paginas = re.split(r'Autenticar', conteudo)

    # Inicializando lista de resultados
    todos_resultados = []

    for i, pag in enumerate(paginas, 1):
        if not pag.strip():
            continue  # Ignorar páginas vazias

        print(f"\n--- Processando Ficha {i} ---")

        empregado_match = re.search(r'Beneficiários(.*?)Residência', pag, re.DOTALL)
        if empregado_match:
            empregado_conteudo = empregado_match.group(1).strip()
            linhas = [linha.strip() for linha in empregado_conteudo.split('\n\n') if linha.strip()]

            if len(linhas) > 1:
                beneficiario = linhas[0]
                empregado = linhas[1]
                beneficiarios = [b.strip() for b in beneficiario.split(',')]
            elif len(linhas) == 1:
                empregado = linhas[0]
                beneficiarios = []
            else:
                empregado = ""
                beneficiarios = []
        else:
            empregado = ""
            beneficiarios = []

        # Beneficiários individuais (até 5)
        beneficiario1 = beneficiarios[0] if len(beneficiarios) > 0 else ""
        beneficiario2 = beneficiarios[1] if len(beneficiarios) > 1 else ""
        beneficiario3 = beneficiarios[2] if len(beneficiarios) > 2 else ""
        beneficiario4 = beneficiarios[3] if len(beneficiarios) > 3 else ""

        # Inicializando variáveis com valores padrão
        logradouro = ""
        numero = ""
        complemento = ""
        bairro = ""
        cidade = ""
        estado = ""
        cep = ""

        # Capturando o trecho entre "Residência" e "Data de nascimento"
        endereco_match = re.search(r'Residência(.*?)Data de nascimento', pag, re.DOTALL)

        if endereco_match:
            endereco_conteudo = endereco_match.group(1).strip()
            
            # Separando o endereço por vírgulas
            partes_endereco = [p.strip() for p in endereco_conteudo.split(',')]

            if len(partes_endereco) == 5:
                logradouro = partes_endereco[0]
                bairro = partes_endereco[1]
                cidade = partes_endereco[2]
                estado = partes_endereco[3]
                cep_raw = partes_endereco[4]

                # Limpando o valor do CEP para remover '- CEP:'
                cep = re.sub(r'-?\s?CEP:', '', cep_raw).strip()

                # Extraindo número e complemento
                numero = re.sub(r'\D', '', numero_raw)  # Apenas números

                if not numero:
                    numero = ""

            if len(partes_endereco) == 6:#não tem complemento
                logradouro = partes_endereco[0]
                numero_raw = partes_endereco[1]
                bairro = partes_endereco[2]
                cidade = partes_endereco[3]
                estado = partes_endereco[4]
                cep_raw = partes_endereco[5]

                # Limpando o valor do CEP para remover '- CEP:'
                cep = re.sub(r'-?\s?CEP:', '', cep_raw).strip()

                # Extraindo número e complemento
                numero = re.sub(r'\D', '', numero_raw)  # Apenas números

                if not numero:
                    numero = ""

            if len(partes_endereco) == 7:
                logradouro = partes_endereco[0]
                numero_raw = partes_endereco[1]
                complemento = partes_endereco[2]
                bairro = partes_endereco[3]
                cidade = partes_endereco[4]
                estado = partes_endereco[5]
                cep_raw = partes_endereco[6]

                # Limpando o valor do CEP para remover '- CEP:'
                cep = re.sub(r'-?\s?CEP:', '', cep_raw).strip()

                # Extraindo número
                numero = re.sub(r'\D', '', numero_raw)  # Apenas números

                if not numero:
                    numero = ""

            if len(partes_endereco) == 8:
                logradouro = partes_endereco[0]
                numero_raw = partes_endereco[1]
                complemento = partes_endereco[2]
                bairro = partes_endereco[3]
                cidade = partes_endereco[4]
                estado = partes_endereco[5]
                cep_raw = partes_endereco[6]

                # Limpando o valor do CEP para remover '- CEP:'
                cep = re.sub(r'-?\s?CEP:', '', cep_raw).strip()

                # Extraindo número
                numero = re.sub(r'\D', '', numero_raw)  # Apenas números

                if not numero:
                    numero = ""

        # Extração de informações: Data de nascimento
        data_nascimento_match = re.search(r'Local do nascimento(.*?)Estado civil', pag, re.DOTALL)

        if data_nascimento_match:
            data_nascimento_conteudo = data_nascimento_match.group(1).strip()
            
            # Procurando a primeira data no formato dd/mm/aaaa ou dd-mm-aaaa
            primeira_data_match = re.search(r'\b\d{2}[/-]\d{2}[/-]\d{4}\b', data_nascimento_conteudo)

            if primeira_data_match:
                data_nascimento_conteudo = primeira_data_match.group()
            else:
                data_nascimento_conteudo = ""  # Se não encontrar uma data, define como string vazia
        else:
            data_nascimento_conteudo = ""

        #print("Data de Nascimento =", data_nascimento_conteudo)

        cidade_nascimento_conteudo = ""

        cidade_nascimento_match = re.search(r'País da nacionalidade(.*?)(-|BRASIL)', pag, re.DOTALL)

        if cidade_nascimento_match:
            cidade_nascimento_conteudo = cidade_nascimento_match.group(1).strip()

        #print("Cidade de Nascimento =", cidade_nascimento_conteudo)

        uf_nascimento_match = re.search(r'País da nacionalidade.*?-\s*([A-Za-z]{2})\b', pag, re.DOTALL)

        # Verifica se encontrou um valor válido para UF (apenas letras)
        if uf_nascimento_match:
            uf_nascimento = uf_nascimento_match.group(1).strip()
        else:
            uf_nascimento = ""

        #print("UF de Nascimento =", uf_nascimento)

        def capturar_estado_civil(pag):
            estado_civil = ""

            # Procurando o texto "País da nacionalidade" e capturando os 10 primeiros conjuntos de caracteres após ele
            match = re.search(r'País da nacionalidade\s+((\S+\s+){1,10})', pag)

            if match:
                # Dividindo o resultado em um array de palavras
                palavras = match.group(1).strip().split()

                # Lista de palavras-chave (agora incluindo frases compostas)
                palavras_chave = ["casado", "solteiro", "divorciado", "viúvo", "união estável"]

                # Criando string única a partir das palavras para busca de frases compostas
                texto_continuo = " ".join(palavras).lower()

                # Verificando se alguma frase composta (como "união estável") aparece no texto contínuo
                for chave in palavras_chave:
                    if chave in texto_continuo:
                        estado_civil = chave
                        break

            return estado_civil
        estado_civil = capturar_estado_civil(pag)

        def extrair_pai(pag):
            # Tentativa 1: Extrair entre "FILIAÇÃO" e "Mãe"
            tentativa1 = re.search(r'FILIAÇÃO(.*?)Mãe', pag, re.DOTALL)
            pai = ""
            if tentativa1:
                pai = tentativa1.group(1).strip()
            
            # Se a tentativa 1 retornar vazio, tenta a tentativa 2
            if not pai:
                tentativa2 = re.search(r'Pai(.*?)FILIAÇÃO', pag, re.DOTALL)
                if tentativa2:
                    pai = tentativa2.group(1).strip()
            
            return pai if pai else ""
        pai = extrair_pai(pag)

        # Extração de informações: Mãe
        mae = ""  # Inicializando a variável 'mae'
        mae_match = re.search(r'Mãe\s*(.*?)(?:Cédula de Identidade)', pag, re.DOTALL)

        if mae_match:
            mae = mae_match.group(1).strip()  # Captura o conteúdo e remove espaços extras
            #print(f"Mãe = {mae if mae else ''}")
        #else:
            #print("Mãe = Não encontrada")

        # Inicializa a variável cédula_identidade com valor padrão (vazio)
        cedula_identidade = ""

        # Verificação para Cédula de Identidade
        cedula_identidade_match = re.search(r'Data de emissão\s*([\d\.\,]+)\s*CTPS', pag, re.DOTALL)

        if cedula_identidade_match:
            cedula_identidade = cedula_identidade_match.group(1).strip()

            # Verificando se o resultado é composto de 7, 8 ou 9 dígitos numéricos ou 7, 8 dígitos seguidos por 'X/x'
            numero_valido_match = re.match(r'^\d{7,9}$|^\d{7}[Xx]$', cedula_identidade.replace('.', '').replace(',', ''))

            if numero_valido_match:
                pass  # A Cédula de Identidade é válida, mas não é necessário fazer nada aqui
            else:
                # Se não for válido, definir como string vazia
                cedula_identidade = ""
        else:
            cedula_identidade = ""
            
        data_emissao=""

        data_emissao_match = re.search(r'Órgão/UF emissor\s*(.*?)(?:Série)', pag, re.DOTALL)

        if data_emissao_match:
            data_emissao = data_emissao_match.group(1).strip()
            
            # Verificando se o resultado é uma data no formato dd/mm/aaaa ou dd-mm-aaaa
            data_valida_match = re.match(r'\b\d{2}[/-]\d{2}[/-]\d{4}\b', data_emissao)
            
        #     if data_valida_match:
        #         print(f"Data de emissão = {data_emissao}")
        #     else:
        #         # Se não for uma data, definir como string vazia
        #         data_emissao = ""
        #         print(f"Data de emissão = {data_emissao}")
        # else:
        #     print(f"Data de emissão =")

        orgao_emissor=""
        uf_emissor=""

        orgao_emissor_match = re.search(r'Título Eleitoral\s*(.*?)(?:UF CTPS|C.B.O.)', pag, re.DOTALL)

        if orgao_emissor_match:
            orgao_emissor = orgao_emissor_match.group(1).strip()
            uf_emissor = ""

            # Limpa o conteúdo capturado, removendo linhas extras, espaços e duplicações
            orgao_emissor = re.sub(r'\s+', ' ', orgao_emissor)  # Substitui múltiplos espaços e quebras de linha por espaço único
            orgao_emissor = re.split(r'(Data de expedição|Doc\. militar|Órgão)', orgao_emissor)[0].strip()

            # Verifica se há uma barra ("/") no resultado
            if "/" in orgao_emissor:
                partes = orgao_emissor.split("/")
                orgao_emissor = partes[0].strip()  # Pega a parte antes da barra
                uf_emissor = partes[1].strip()  # Pega a parte após a barra

            # Verifica se o resultado é composto por apenas dois caracteres (UF)
            elif len(orgao_emissor) == 2:
                uf_emissor = orgao_emissor
                orgao_emissor = ""  # Deixa órgão emissor vazio

        #     # Exibe os resultados
        #     print(f"Órgão emissor = {orgao_emissor}")
        #     print(f"UF emissor = {uf_emissor}")

        # else:
        #     # Se não houver correspondência
        #     print("Órgão emissor =")
        #     print("UF emissor =")

        titulo_eleitoral=""

        titulo_eleitoral_match = re.search(r'Zona\s*(.*?)(?:Horário de Intervalo|Horário de Trabalho|C.B.O.|Cor)', pag, re.DOTALL)

        if titulo_eleitoral_match:
            # Extrai apenas os números do resultado encontrado
            titulo_eleitoral = ''.join(filter(str.isdigit, titulo_eleitoral_match.group(1).strip()))
            
            # Verifica se o resultado contém 10, 11 ou 12 números
            if len(titulo_eleitoral) in [10, 11, 12]:
                pass
                #print(f"Título Eleitoral = {titulo_eleitoral}")
            else:
                # Se não atender aos critérios, faz uma segunda tentativa
                titulo_eleitoral_match = re.search(r'Zona\s*(.*?)(?:UF CTPS)', pag, re.DOTALL)
                if titulo_eleitoral_match:
                    titulo_eleitoral = ''.join(filter(str.isdigit, titulo_eleitoral_match.group(1).strip()))
                    if len(titulo_eleitoral) in [10, 11, 12]:
                        pass
                        #print(f"Título Eleitoral = {titulo_eleitoral}")
        #             else:
        #                 print("Título Eleitoral =")  # Resultado não atende aos critérios
        #         else:
        #             print("Título Eleitoral =")  # Nenhuma correspondência encontrada na segunda tentativa
        # else:
        #     print("Título Eleitoral =")

        zona_validada=""

        zona_match = re.search(r'Seção\s*(.*?)(?:CPF)', pag, re.DOTALL)

        if zona_match:
            # Extrai o resultado e separa por espaços
            zona = zona_match.group(1).strip()
            # Verifica cada conjunto de caracteres separados por espaço
            zona_validada = ' '.join(part for part in zona.split() if part.isdigit() and len(part) in [2, 3])
            
            # Imprime o resultado validado ou vazio se não atender aos critérios
        #     print(f"Zona = {zona_validada if zona_validada else ''}")
        # else:
        #     print("Zona =")

        def extrair_secao(pag):
            secao_validada = ""

            # Primeira verificação: busca por "Horário de Trabalho" e validação numérica
            secao_match = re.search(r'Horário de Trabalho\s*(.*?)(?:Data de Admissão)', pag, re.DOTALL)

            if secao_match:
                # Extrai o resultado e separa por espaços
                secao = secao_match.group(1).strip()

                secao_validada = next((part for part in secao.split() if part.isdigit() and len(part) in [3, 4]), "")

                # Imprime o resultado ou vazio se não atender aos critérios
                #print(f"Seção = {secao_validada if secao_validada else ''}")
            else:
                # Segunda verificação: busca por "Inscr. Órgão de Classe" e números subsequentes
                secao_secundaria_match = re.search(r'Inscr\. Órgão de Classe\s*(\d+)', pag)
                
                if secao_secundaria_match:
                    # Se encontrar um número após "Inscr. Órgão de Classe", salva esse número
                    secao_validada = secao_secundaria_match.group(1).strip()
                    #print(f"Seção = {secao_validada}")
                else:
                    # Terceira verificação: busca por "Função" e valida números antes de "Função"
                    secao_tercearia_match = re.search(r'(.*?)(?=\s*Função)', pag)

                    if secao_tercearia_match:
                        # Extrai a parte antes da palavra "Função" e verifica se são 3 ou 4 números separados por espaços
                        secao_tercearia = secao_tercearia_match.group(1).strip()
                        secao_validada = next((part for part in secao_tercearia.split() if part.isdigit() and len(part) in [3, 4]), "")

                    # Imprime o resultado ou vazio se não atender aos critérios
                    #print(f"Seção = {secao_validada if secao_validada else ''}")

            # Quarta verificação: busca por "Categoria" e valida números subsequentes
            if not secao_validada:
                secao_quarta_match = re.search(r'Cart\. Nac\. Habilitação\s*Categoria\s*(\d{3,4})', pag, re.DOTALL)
                
                if secao_quarta_match:
                    # Se encontrar números após "Categoria", valida se são 3 ou 4 números separados por espaço
                    secao_quarta = secao_quarta_match.group(1).strip()
                    secao_validada = next((part for part in secao_quarta.split() if part.isdigit() and len(part) in [3, 4]), "")

            if not secao_validada:
                secao_quinta_match = re.search(r'Cart\. Nac\. Habilitação\s*Categoria\s*(.*?)(?=Grau de instrução)', pag, re.DOTALL)
                if secao_quinta_match:
                    secao_quinta = secao_quinta_match.group(1).strip()
                    # Busca o primeiro valor que seja 3 ou 4 números separados por espaço
                    secao_validada = next((part for part in secao_quinta.split() if part.isdigit() and len(part) in [3, 4]), "")

            if not secao_validada:
                secao_sexto_match = re.search(r'FGTS\s*Categoria\s*(\d{3,4})', pag, re.DOTALL)
                
                if secao_sexto_match:
                    # Se encontrar números após "Categoria", valida se são 3 ou 4 números separados por espaço
                    secao_sexto = secao_sexto_match.group(1).strip()
                    secao_validada = next((part for part in secao_sexto.split() if part.isdigit() and len(part) in [3, 4]), "")

            # Imprime o resultado ou vazio se não atender aos critérios
            #print(f"Seção = {secao_validada if secao_validada else ''}")

            return secao_validada
        secao_validada = extrair_secao(pag)

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
        # if ctps:
        #     print(f"CTPS = {ctps}")
        # else:
        #     # Segunda tentativa se o resultado da primeira for vazio
        #     ctps = extrair_ctps(pag)
        #     if ctps:
        #         print(f"CTPS = {ctps}")
        #     else:
        #         print("CTPS =")

        def extrair_serie(pag):
            serie = ""

            # Primeira tentativa: busca entre "Data de expedição da CTPS" e "Doc. militar"
            serie_match = re.search(r'Data de expedição da CTPS(.*?)Doc\. militar', pag, re.DOTALL)

            if serie_match:
                # Captura o trecho entre os textos "Data de expedição da CTPS" e "Doc. militar"
                section = serie_match.group(1).strip()

                # Filtra apenas os conjuntos de números que possuem 3, 4 ou 5 caracteres
                numeros = [part for part in section.split() if part.isdigit() and len(part) in [3, 4, 5]]

                serie = " ".join(numeros[:5])

            if not serie:
                # Segunda tentativa: busca entre "Data de expedição da CTPS" e "Categoria"
                segunda_tentativa_match = re.search(r'Data de expedição da CTPS(.*?)Categoria', pag, re.DOTALL)

                if segunda_tentativa_match:
                    # Captura o trecho entre os textos "Data de expedição da CTPS" e "Categoria"
                    section = segunda_tentativa_match.group(1).strip()

                    numeros = [part for part in section.split() if part.isdigit() and len(part) in [3, 4, 5]]

                    serie = " ".join(numeros[:5])

            #print(f"Série = {serie if serie else ''}")
            return serie
        serie_validada = extrair_serie(pag)

        def extrair_uf_ctps(pag):
            uf_ctps = ""
            
            # Busca por "UF CTPS" seguido de duas letras (potencialmente um estado)
            uf_ctps_match = re.search(r'UF CTPS\s*(\w{2})', pag)
            uf_ctps_match2 = re.search(r'UF CTPS\s*(Masculino|Feminino)', pag)

            if uf_ctps_match:
                uf_ctps = uf_ctps_match.group(1).strip()  # Captura as duas letras após "UF CTPS"
                
                # Verifica se a palavra seguinte é "Masculino" ou "Feminino"
                if uf_ctps_match2:
                    uf_ctps = ""  # Se "Masculino" ou "Feminino" aparecer após a UF, limpa uf_ctps

            return uf_ctps
        uf_ctps = extrair_uf_ctps(pag)

        def capturar_cpf(pag):
            # Função para tentar capturar o CPF no formato XXX.XXX.XXX-XX
            def verificar_cpf(texto):
                cpf_list = re.findall(r'\d{3}\.\d{3}\.\d{3}-\d{2}', texto)
                if cpf_list:
                    return cpf_list[0]  # Retorna o primeiro CPF encontrado
                return None

            # Definir uma lista de tentativas de busca com os respectivos padrões
            tentativas = [
                (r'Seção(.*?)Salário', "Seção a Salário"),  # entre "Seção" e "Salário"
                (r'Horário de Trabalho(.*?)Data de Admissão', "Horário de Trabalho a Data de Admissão"),  # entre "Horário de Trabalho" e "Data de Admissão"
                (r'Seção(.*?)Data de Admissão', "Seção a Data de Admissão"),  # entre "Seção" e "Data de Admissão"
                (r'Data de Admissão(.*?)Seção', "Data de Admissão a Seção"),  # entre "Data de Admissão" e "Seção"
                (r'Inscr\. Órgão de Classe(.*?)Data de Admissão', "Inscr. Órgão de Classe a Data de Admissão")  # entre "Inscr. Órgão de Classe" e "Data de Admissão"
            ]

            # Percorrer as tentativas para encontrar o CPF
            for padrao, descricao in tentativas:
                trecho = re.search(padrao, pag, re.DOTALL)
                if trecho:
                    cpf = verificar_cpf(trecho.group(1))
                    if cpf:
                        return cpf

            # Se nenhum CPF for encontrado, retorna vazio
            return ""

        cpf = capturar_cpf(pag)

        def capturar_doc_militar(pag):
            doc_militar = ""
            
            # Procurar o trecho entre "Categoria" e "Título Eleitoral"
            trecho = re.search(r'Categoria(.*?)Título Eleitoral', pag, re.DOTALL)
            
            if trecho:
                # Procurar o primeiro conjunto de números que seja separado por espaços (não incluindo datas)
                numeros = re.search(r'(\d+(?: \d+)*)', trecho.group(1).strip())  # Captura números com ou sem espaço entre eles
                
                if numeros:
                    doc_militar = numeros.group(0).replace(" ", "")  # Remove os espaços entre os números
            
            return doc_militar
    
        doc_militar = capturar_doc_militar(pag)

        def capturar_cor(pag):
            palavras_cor = ['Preta', 'Parda', 'Branca', 'Amarela', 'Indígena']
            # Procurar pelo trecho que contenha uma palavra de interesse
            for palavra in palavras_cor:
                if palavra in pag:
                    return palavra  # Retorna a primeira palavra encontrada
            return ""

        cor = capturar_cor(pag)

        def capturar_sexo(pag):
            palavras_sexo = ['Masculino','Feminino']
            # Procurar pelo trecho que contenha uma palavra de interesse
            for palavra in palavras_sexo:
                if palavra in pag:
                    return palavra  # Retorna a primeira palavra encontrada
            return ""

        sexo = capturar_sexo(pag)

        def capturar_grau_instrucao(pag):
                
            palavras_grau = ['Ensino Fundamental 5º Completo','Ensino Fundamental 6º ao 9º','Ensino Fundamental Completo','Ensino Médio Incompleto','Ensino Médio Completo','Superior Incompleto','Superior Completo','Pós-Graduação Incompleto','Pós-Graduação']
            # Procurar pelo trecho que contenha uma palavra de interesse
            for palavra in palavras_grau:
                if palavra in pag:
                    return palavra  # Retorna a primeira palavra encontrada
            return ""

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

        def capturar_telefone(pag):
            # Inicializa as variáveis de telefone como None
            telefone_celular = None
            telefone_residencial = None

            # Expressão regular para capturar qualquer telefone no formato 00-00000000 ou 00-000000000
            padrao_telefone = r'(\d{2}-\d{8,9})'

            # Captura todos os números no formato correto dentro da página
            telefones_encontrados = re.findall(padrao_telefone, pag)

            # Verifica cada telefone encontrado e classifica como celular ou residencial
            for telefone in telefones_encontrados:
                if len(telefone) == 12:
                    telefone_celular = telefone
                elif len(telefone) == 11:
                    telefone_residencial = telefone

            return telefone_celular, telefone_residencial

        telefone_celular, telefone_residencial = capturar_telefone(pag)

        def capturar_cargo1(pag):
            # Expressão regular para encontrar tudo entre "Função" e a data
            padrao = r'Função\s+([\w\s]+)\s+(\d{2}/\d{2}/\d{4})'

            # Expressão regular alternativa para "Masculino" ou "Feminino" e depois o cargo e data
            padrao2 = r'(Masculino|Feminino)([\s\S]*?)\s+\d{2}/\d{2}/\d{4}'

            # Tentativa 1: Usar o primeiro padrão
            resultado = re.search(padrao, pag, re.DOTALL)
            if resultado:
                cargo = resultado.group(1).strip()
                return cargo

            # Tentativa 2: Usar o segundo padrão
            resultado2 = re.search(padrao2, pag, re.DOTALL)
            if resultado2:
                cargo = resultado2.group(2).strip()
                return cargo


            # Caso nenhum padrão tenha capturado o cargo
            return None

        def capturar_cargo2(pag):
            # Busca o conteúdo entre "Cargo:" e "Para:"
            cargo_match = re.search(r'Cargo:(.*?)(?=Para:)', pag, re.DOTALL)

            if cargo_match:
                # Obtém o conteúdo e remove os números, mantendo apenas as letras
                cargo = cargo_match.group(1)
                cargo = re.sub(r'\d+', '', cargo)  # Remove os números
                cargo = cargo.strip()  # Remove espaços extras

                return cargo
            else:
                return None

        def verificar_e_limpar_cargo(cargo):
            # Remove tudo que está antes da palavra 'Função' ou 'Telefone Celular'
            if 'Função' in cargo or 'Telefone Celular' in cargo:
                cargo = re.sub(r'.*(Função|Telefone Celular)\s+', '', cargo, flags=re.DOTALL)

            # Remove tudo que está após a palavra 'Opção em'
            if 'Opção em' in cargo:
                cargo = re.sub(r'Opção em.*$', '', cargo, flags=re.DOTALL)

            return cargo.strip()

        # Exemplo de uso
        def processar_cargo(pag):
            # Tenta capturar o cargo com o primeiro padrão
            cargo = capturar_cargo1(pag)
            if not cargo:
                # Se não encontrou, tenta capturar com o segundo padrão
                cargo = capturar_cargo2(pag)

            if cargo:
                # Verifica e limpa o cargo antes de salvar no Excel
                cargo_verificado = verificar_e_limpar_cargo(cargo)
                return cargo_verificado
            else:
                return None
        cargo = processar_cargo(pag)

        #print("Função =")

        def capturar_cbo(pag):
            # Expressão regular para encontrar tudo entre "C.B.O." e "Horário de Trabalho"
            padrao = r'C\.B\.O\.(.*?)Horário de Trabalho'
            
            # Buscar o padrão no texto
            resultado = re.search(padrao, pag, re.DOTALL)  # re.DOTALL permite capturar quebras de linha
            
            if resultado:
                cbo = resultado.group(1).strip()  # Captura o conteúdo entre C.B.O. e Horário de Trabalho
                
                # Verifica se existe a palavra "Por" no conteúdo extraído e apaga tudo após "Por"
                if "Por" in cbo:
                    cbo = cbo.split("Por")[0].strip()  # Apaga tudo após "Por" (inclusive "Por")
                
                # Verifica se existe uma data (formato DD/MM/AAAA) no conteúdo extraído e apaga tudo após a data
                match_data = re.search(r'\d{2}/\d{2}/\d{4}', cbo)
                if match_data:
                    cbo = cbo.split(match_data.group(0))[0].strip()  # Apaga tudo após a data, incluindo a data
                
                return cbo
            else:
                return None
        cbo = capturar_cbo(pag)

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
            
            return data_admissao
        data_admissao = capturar_data_admissao(pag)

        def capturar_salario(pag):
            # Procura a palavra "Por" seguida por qualquer texto e, depois, o primeiro valor monetário
            match = re.search(r'\bPor\b.*?(\d{1,3}(?:\.\d{3})*,\d{2})', pag, re.DOTALL)
            
            salario = ""
            if match:
                salario = match.group(1).strip()
            
            return salario
        salario = capturar_salario(pag)

        #print("Por = Mês")

        def capturar_horarios(pag):
            # Expressão regular para encontrar o padrão "das 00:00 as 00:00"
            padrao = r'das\s+(\d{2}:\d{2})\s+as\s+(\d{2}:\d{2})'

            # Encontrar todos os padrões na página
            horarios_encontrados = re.findall(padrao, pag)

            if len(horarios_encontrados) >= 1:
                # O primeiro padrão encontrado é o horário de trabalho
                horario_trabalho = f"{horarios_encontrados[0][0]} as {horarios_encontrados[0][1]}"
                
                # O segundo padrão, se existir, é o horário de intervalo
                horario_intervalo = (
                    f"{horarios_encontrados[1][0]} as {horarios_encontrados[1][1]}"
                    if len(horarios_encontrados) > 1
                    else None
                )

                return horario_trabalho, horario_intervalo
            else:
                # Caso nenhum horário seja encontrado
                return None, None
        horario_trabalho, horario_intervalo = capturar_horarios(pag)

        # Salvando os resultados de uma ficha
        resultado = {
            "Empregado": empregado,
            "Beneficiario1": beneficiario1,
            "Beneficiario2": beneficiario2,
            "Beneficiario3": beneficiario3,
            "Beneficiario4":beneficiario4,
            "Logradouro": logradouro,
            "Número": numero,
            "Complemento": complemento,
            "Bairro": bairro,
            "Cidade": cidade,
            "Estado": estado,
            "CEP": cep,
            "Data de Nascimento": data_nascimento_conteudo,
            "Cidade de Nascimento":cidade_nascimento_conteudo,
            "UF de Nascimento":uf_nascimento,
            "Estado Civil":estado_civil,
            "Pai":pai,
            "Mãe":mae,
            "Cédula de Identidade":cedula_identidade,
            "Data de Emissão":data_emissao,
            "Órgão Emissor":orgao_emissor,
            "UF Emissor":uf_emissor,
            "Título Eleitoral":titulo_eleitoral,
            "Zona":zona_validada,
            "Seção":secao_validada,
            "CTPS":ctps,
            "Série":serie_validada,
            "UF Ctps":uf_ctps,
            "CPF": cpf,
            "Doc. Militar":doc_militar,
            "Cor":cor,
            "Sexo":sexo,
            "Grau de Instrução":grau_instrucao,
            "Deficiência":deficiencia,
            "Telefone Residencial":telefone_residencial,
            "Telefone Celular":telefone_celular,
            "Cargo":cargo,
            "Função":"",
            "C.B.O.":cbo,
            "Data de Admissão":data_admissao,
            "Salário":salario,
            "Por":"Mês",
            "Horário de Trabalho":horario_trabalho,
            "Horário de Intervalo":horario_intervalo,
        }
        
        todos_resultados.append(resultado)

    # Criar DataFrame e salvar em Excel
    df = pd.DataFrame(todos_resultados)
    df.to_excel(caminho_excel, index=False)
    print(f"Resultados salvos no arquivo '{caminho_excel}'.")

    # Retorna a ficha processada
    return todos_resultados


# Caminhos para os arquivos
caminho_txt = r'C:\Reviant\Documentos\Codes\Python\Ficha de Registro - ETL\MARIA_TEREZA-FichaRegistro.txt'
caminho_excel = r'C:\Reviant\Documentos\Codes\Python\Ficha de Registro - ETL\resultados.xlsx'

# Chamando a função
resultado_ficha = processar_ficha(caminho_txt, caminho_excel)

# Visualizando os resultados retornados pela função
#print("Resultados processados:", resultado_ficha)
