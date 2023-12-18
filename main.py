import requests
from bs4 import BeautifulSoup
from tika import parser
from dotenv import load_dotenv
import logging
import csv
import os

load_dotenv()


class WebScraper:
    def __init__(self):
        self.url = os.getenv('URL')
        self.codes = os.getenv('CODES').split(',')
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': os.getenv('USER_AGENT')})
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def get_csrf_token(self):
        logging.info('Obtendo CSRF token...')
        response_csrf = self.session.get(self.url)
        soup = BeautifulSoup(response_csrf.text, 'html.parser')
        csrf = soup.find('input', attrs={'name': 'csrf'}).get('value')
        return csrf

    def get_file_content(self, url_file):
        logging.info('Obtendo conteúdo do arquivo...')

        if url_file.endswith('.txt'):
            response_file = self.session.get(self.url + url_file)
            if response_file.status_code == requests.codes.ok:
                return response_file.text
            else:
                logging.warn(f'Não foi possível baixar o arquivo: {url_file}.')
        elif url_file.endswith('.pdf'):
            response_file = self.session.get(self.url + url_file, stream=True)
            if response_file.status_code == requests.codes.ok:
                return parser.from_buffer(response_file.content)['content']
            else:
                logging.warn(f'Não foi possível baixar o arquivo: {url_file}.')
        else:
            logging.warn(f'Tipo de arquivo desconhecido: {url_file}.')
        return None

    def scrape(self):
        csrf_token = self.get_csrf_token()
        if csrf_token is None:
            logging.error('Não foi possível encontrar o CSRF Token.')
            return None

        data_result = []
        for code in self.codes:
            logging.info(f'Fazendo requisição POST para o código {code}')
            data = {'codigo': code, 'csrf': csrf_token}

            response_post = self.session.post(self.url, data=data)
            if response_post.status_code == requests.codes.ok:
                logging.info('Requisição POST bem-sucedida.')

                soup = BeautifulSoup(response_post.text, 'html.parser')
                body = soup.find('body')
                all_div = body.children
                info_file = {'code': code, 'data': []}

                for div_file in all_div:
                    if div_file.name == 'div':
                        links = div_file.select('a[download]')
                        if links:
                            file_name = div_file.find('div').text
                            file_data = {'file_name': file_name,
                                         'file_data': []}
                            for link in links:
                                url_file = link['href']
                                file_content = self.get_file_content(url_file)
                                if file_content is not None:
                                    file_data['file_data'].append({
                                        'file': link.text,
                                        'file_content': file_content
                                    })
                            info_file['data'].append(file_data)
                data_result.append(info_file)
            else:
                logging.error(f"""Não foi possível acessar o site com o código
                              {code}.""")
        return data_result

    def to_csv(self, info_file):
        with open('data.csv', 'w', newline='') as file:
            logging.info('Criando data.csv com informações do site...')
            writer = csv.writer(file)
            writer.writerow([
                "Código", "Nome", "Nome arquivo", "Dados"])
            for info in info_file:
                code = info['code']
                for data in info['data']:
                    file_name = data['file_name']
                    for file in data['file_data']:
                        writer.writerow([
                            code,
                            file_name,
                            file['file'],
                            file['file_content']
                        ])


if __name__ == '__main__':
    scraper = WebScraper()
    info_file = scraper.scrape()
    scraper.to_csv(info_file)
