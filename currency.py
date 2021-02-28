from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}')  # Использовать переданный requests
    soup = BeautifulSoup(response.content, 'xml')
    am_from = Decimal(1)
    am_to = Decimal(1)
    nom_from = 1
    nom_to = 1

    if cur_from != 'RUR':
        am_from = soup.find('CharCode', text=cur_from).find_next_sibling('Value').string
        am_from = Decimal(am_from.replace(',','.'))
        nom_from = int(soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string)
    if cur_to != 'RUR':
        am_to = soup.find('CharCode', text=cur_to).find_next_sibling('Value').string
        am_to = Decimal(am_to.replace(',','.'))
        nom_to = int(soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string)
    
    rur = amount * am_from / nom_from

    result = rur / am_to * nom_to
    return round(result, 4)  # не забыть про округление до 4х знаков после запятой
