import requests
from bs4 import BeautifulSoup
import time

def scrape_golden_globes_nominees():
    url = 'https://goldenglobes.com/winners-nominees/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Seletores CSS específicos para os indicados e suas respectivas categorias
    nominee_selector = '.c-nomination-card__nominee'
    title_selector = '.u-type-h11'

    # Listas para armazenar os dados
    nominees_info = []

    nominee_elements = soup.select(nominee_selector)

    for nominee_element in nominee_elements:
        nominee_name = nominee_element.select_one('.c-nomination-card__name').get_text().strip() if nominee_element.select_one('.c-nomination-card__name') else None
        title = nominee_element.select_one(title_selector).get_text().strip() if nominee_element.select_one(title_selector) else None
        is_winner = 'is-active' in nominee_element.get('class', [])

        # Encontrar ou criar o registro do indicado
        nominee_record = next((item for item in nominees_info if item["name"] == nominee_name), None)
        if not nominee_record:
            nominee_record = {"name": nominee_name, "nominations": 0, "wins": 0, "titles": set()}
            nominees_info.append(nominee_record)
        
        nominee_record["nominations"] += 1
        if is_winner:
            nominee_record["wins"] += 1
        if title:
            nominee_record["titles"].add(title)

    # Convertendo conjuntos de títulos em listas para melhor visualização
    for nominee in nominees_info:
        nominee["titles"] = list(nominee["titles"])

    return nominees_info

def main():
    while True:
        nominees_info = scrape_golden_globes_nominees()

        for nominee in nominees_info:
            print(f"{nominee['name']} - Indicações: {nominee['nominations']}, Vitórias: {nominee['wins']}, Títulos: {', '.join(nominee['titles'])}")

        # Pausa de 60 segundos entre cada verificação
        time.sleep(60)

if __name__ == '__main__':
    main()
