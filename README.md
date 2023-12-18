# Web Scraper

Este projeto é um web scraper que extrai informações de arquivos do site simpleenergy.com.br

## O que foi feito

O web scraper foi implementado em Python usando as bibliotecas `requests`, `BeautifulSoup`, `Apache Tika`, `python-dotenv` e `unittest`. O código faz uma requisição GET para o site para obter um CSRF token, e então faz uma requisição POST para cada código na lista de códigos. Para cada código, o web scraper extrai as informações de cada arquivo e salva os dados em uma lista de dicionários. As informações são então salvas em um arquivo CSV na raiz do projeto.

## Como executar o código

1. Crie um arquivo .env na raiz do seu projeto com as seguintes variáveis:
    ```
    URL=https://simpleenergy.com.br/teste
    CODES=321465,98465
    USER_AGENT=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36
    ```
2. Instale as dependências do projeto com o comando `pip install -r requirements.txt`.
3. Execute o script do projeto com o comando `python main.py`.

### Com Docker

1. No terminal, no diretório raiz do projeto execute o comando do docker-compose: `docker-compose up --build`

## Bibliotecas usadas

- `requests`: Usada para fazer requisições HTTP.
- `BeautifulSoup`: Usada para analisar o conteúdo HTML das páginas.
- `Apache Tika`: Usada para extrair texto de arquivos PDF.
- `python-dotenv`: Usada para carregar variáveis de ambiente do arquivo .env.
- `unittest`: Usada para escrever e executar testes unitários.

## Como executar os testes unitários

Execute os testes unitários com o comando `python -m unittest`.
