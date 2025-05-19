# Relatório Técnico - Atividades no Projeto GaiaSenses

Nome: Henrique Cazarim Meirelles Alves

Período: jun/24 - o momento

Orientadora: Artemis Moroni

Instituição: CTI Renato Archer / NICS-UNICAMP

Projeto: GaiaSenses

## Objetivos da Atividade

- Auxiliar a viabilizar o emprego de dados climáticos provenientes do satélite GOES-16 (GOES-19 após abr/25) na geração de obras audiovisuais para a plataforma GaiaSenses
    - Compreender a arquitetura dos arquivos do satélite e do servidor de hospedagem em nuvem dos mesmos (Arquivos .nc hospedados na AWS)
    - Automatizar o processo de download e análise desses arquivos de acordo com o produto de interesse (Chuvas, Raios, etc.) 

- Implementação de novas animações na plataforma GaiaSenses
    - Pesquisar animações com estética que remeta a um fenômeno climático
    - Adaptar o algoritmo da animação para que funcione de forma correta e otimizada


## Atividades Desenvolvidas

- jun/24
    - Ambientação ao projeto: leitura de artigos e exploração de diretórios compartilhados

- jul/24
    - Auxílio na implementação de interface alternativa: estudo sobre possíveis interfaces gestuais para interação com a plataforma

- ago/24
    - Ambientação com algoritmos do projeto: estudo de linguagens utilizadas para o funcionamento do projeto
    - Aquisição de dados via script: desenvolvimento de scripts mais simples para aquisição de dados -> BDQueimadas, INPE

- set/24
    - Aquisição de dados via script: pré-curso INPE para o processamento de dados de satélites geoestacionários

- out/24
    - Aquisição de dados via script: curso INPE para o processamento de dados de satélites geoestacionários

- nov/24
    - Aquisição de dados via script: início do desenvolvimento de scripts para download automatizado dos arquivos do satélite

- dez/24
    - Auxílio na implementação de sensores: utilização de sensores para instalação artística referente ao projeto
    - Aquisição de dados via script: protótipo com download dos arquivos e tratamento dos dados

- jan/25 - fev/25
    - Aquisição de dados via script: finalização dos scripts com download automatizado dos arquivos para o tratamento dos dados climáticos
    - Adição de animação na plataforma: escolha, adaptação e adição de uma animação referente ao produto de raios na plataforma GaiaSenses

- mar/25 - abr/25
    - API de acesso aos dados do satélte: auxílio na implementação de uma API de acesso aos dados do satélite com os scripts desenvolvidos anteriormente

## Resultados Obtidos

- Aprendizado em implementação de interfaces gestuais e sensores com microcontroladores através do estudo e pesquisa de artigos correlatos

- Implementação bem-sucedida do script para downloas automatizado de dados provenientes do satélite por cada produto

- Integração deste script na API satellite fetcher, viabilizando o acesso aos dados pela plataforma GaiaSenses

- Adição de nova animação referente a raios na plataforma

## Dificuldades Encontradas

- Documentação escassa sobre os arquivos baixados do satélite
    - Arquivo com estrutura muito complexa e repleto de informações, a falta de documentação sobre o arquivo dificultou o processo de aprendizado e emprego dos scripts
    - O curso do INPE foi de muita valia para o processo de automatização dos downloads de arquivos da AWS, porém o foco do curso estava mais em geração de imagens referentes a um fenômeno climático e não no tratamento dos dados propriamente ditos

- Tamanho dos arquivos
    - A maioria dos arquivos ocupam pouco espaço, cerca de 1MB a depender do produto armazenado, mas há outros arquivos que requerem até 2GB de armazenamento, tornando impraticável o download dos mesmos em toda a chamada da API por conta do tempo de download e das limitações do host da API

## Próximos Passos e Recomendações

- Próximos Passos:
    - Expandir a gama de produtos analisados com a API a fim de tornar a aquisição de dados climáticos mais rica e completa
    - Otimizar o processo de download para lidar com possíveis arquivos extensos

- Recomendações:
    - Explorar a estrutura dos arquivos NetCDF4 (.nc) desde o início do processo
        - Destrinchar o arquivo por partes, com a biblioteca NetCDF4 o arquivo é tratado como um objeto com atributos que são matrizes, listas, dicionários e valores atômicos, tais atributos guardam os dados climáticos, flags que descrevem a qualidade dos dados e informações gerais sobre o satélite
        - Utilização de extensões para visualização simplidicada dos arquivos, por exemplo a extensão H5Web no VSCode que permite a interação com os dados por meio de interface gráfica
    - Links importantes
        - Pré-curso INPE: https://geonetcast.wordpress.com/2021/02/25/vlab-processamento-de-dados-de-satelites-geoestacionarios-pre-curso/ (Processamento de dados de satélites geoestacionários)
        - Curso INPE: https://colab.research.google.com/drive/1cU2unHLGlqQLmc_gE6YhlEyv52K9lYGe?usp=sharing#scrollTo=iQgz5dMgKm19 (Vídeos, Slides, Exemplos/Exercícios)
        - Guia Introdutório NOAA: https://rammb2.cira.colostate.edu/wp-content/uploads/2024/07/POR_Guia_Introdutorio_aos_Datos_da_Serie_GOES-R_v1.1.pdf (Guia Introdutório aos dados do GOES-R - NOAA, traduzido para o português)
        - GOES-R Products: https://www.goes-r.gov/products/overview.html (Nome dos produtos e respectiva documentação de cada um deles)
        - AWS S3 Explorer: https://noaa-goes19.s3.amazonaws.com/index.html (Armazenamento dos arquivos do satélite GOES19 - ao trocar 19 por 16 é possível acessar os arquivos do GOES16)
        - Relação Produtos e Siglas: http://cimss.ssec.wisc.edu/goes/GOES_ABI_Level_2_Product_Key_update.pdf (Documento não oficial)
        - Data Names: https://edc.occ-data.org/goes16/getdata/#file-formats (Formato dos arquivos para download)

## Considerações Finais

Em suma, as atividades desenvolvidas no GaiaSenses foram de grande valia para meu crescimento acadêmico e meu aprendizado prático, proporcionando experiência em ciência de dados utilizando algumas das principais bibliotecas Python, contato com tecnologias como p5.js, React, TypeScript e Docker e uso de microcontroladores com sensores. Tais atividades contribuíram significativamente para o projeto, principalmente na automatização do processo de download dos arquivos provenientes do satélite GOES-19, aquisição e tratamento dos dados a partir deste produto e implementação de todo este script em uma API, possibilitando que a plataforma do projeto empregasse os dados quase que em tempo real na produção de obras audiovisuais.

De modo geral, a participação no GaiaSenses proporcionou uma vivência multidisciplinar, pois minhas atividades não se limitaram ao desenvolvimento tecnológico. Realizei tarefas relacionadas a arte, como adaptar uma animação para integrá-la na plataforma e assistir uma apresentação de projeto relacionado ao som, movimento e tecnologia (Corpo Sonoro Expandido). Além de tarefas com caráter mais científico, como pesquisas técnicas sobre Realidades Virtual, Mista e Aumentada, Orientação Espacial com ESP32 e Corpo Sonoro Expandido.
