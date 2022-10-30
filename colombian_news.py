import os
from tkinter.tix import DisplayStyle
import requests
from lxml import html as html
from rich import print

clear = lambda: os.system('cls')

DEBUG = True
BASE_URL = 'https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLES = '//a[@class="{0}Sect"]/@href'
XPATH_NEWS_TITLES = '//a[@class="{0}Sect"]/text()' # The title showed in the news list
XPATH_NEW_TITLE = '//div[@class="mb-auto"]/h2/span/text()'
XPATH_NEW_ABSTRACT = '//div[@class="lead"]/p/text()'
XPATH_NEW_CONTENT = '//div[@class="html-content"]/p/text()'

def run():
    clear()
    print('[yellow]NOTICIERO[/yellow] [cyan]COLOMBIANO[/cyan] [red]AL INSTANTE[red]')
    print('[yellow]Qué noticias deseas explorar?[/yellow]')
    print('''
    [1]-> Finanzas
    [2]-> Economía
    [3]-> Empresas
    [4]-> Ocio
    [5]-> Globoeconomía
    [6]-> Caja fuerte
    ''')
    option = input('')

    url = BASE_URL
    section = ''

    if option == '1':
        section = 'finanzas'
    elif option == '2':
        section = 'economia'
    elif option == '3':
        section = 'empresas'
    elif option == '4':
        section = 'ocio'
    elif option == '5':
        section = 'globoeconomia'
    elif option == '6':
        section = 'caja-fuerte'
    else:
        print('[red]Opción incorrecta[/red]')
        return

    url += section

    try:
        response = requests.get(url)
        if response.status_code == 200:
            page = response.content.decode('utf-8')
            parsed = html.fromstring(page)

            links_of_news = parsed.xpath(XPATH_LINK_TO_ARTICLES.format(section))
            titles_of_news = parsed.xpath(XPATH_NEWS_TITLES.format(section))

            news = []
            print(len(links_of_news))
            print(len(titles_of_news))
            for i in range(len(links_of_news) ):
                buffer = dict(link=links_of_news[i], title=titles_of_news[i])
                news.append(buffer)
            display_news(news)
            
        else:
            raise ValueError(f'Error:{response.status_code}')
    except ValueError as ve:
        if DEBUG:
            print(f'[red]{ve}[/red]')
        else:
            print('[red]Ocurrió un error[/red]')

def display_news(news):
    clear()
    news_to_display = 15
    grouped_news = [news[i:i+news_to_display] for i in range(0,len(news), news_to_display)]
    page = 0
    selected = ''
    absolute_id = 0
    while True:
        print('[yellow]Escoge el número de la noticia que quieras leer[/yellow]')
        print('[yellow]Ingresa "<" o ">" para cambiar de página[/yellow]\n')
        print(f'[cyan]Página {page + 1}[/cyan]\n')
        for new in grouped_news[page]:
            print(f"[{absolute_id + 1}]-> {new['title']}")
            absolute_id += 1
        print('')
        selected = input('')
    
        if selected == '<':
            clear()
            page -= 1
            if page < 0:
                page = len(grouped_news) - 1
                absolute_id = len(news) - len(grouped_news[page])
            else:
                absolute_id -= (news_to_display + len(grouped_news[page + 1]))
        elif selected == '>':
            clear()
            page += 1
            if page >= len(grouped_news):
                page = 0
                absolute_id = 0
        elif selected.isnumeric():
            selected = int(selected)
            if selected > len(news) or selected <= 0:
                clear()
                print('[red]Noticia escogida fuera de rango[/red]')
            else:
                break
        else:
            print('[red]Opción inválida[/red]')
        
    show_new(news[selected - 1])

def show_new(new):
    clear()
    response = requests.get(new['link'])
    if response.status_code == 200:
        page = response.content.decode('utf-8')
        parsed = html.fromstring(page)

        title = new['title']
        abstract = parsed.xpath(XPATH_NEW_ABSTRACT)
        paragraphs = parsed.xpath(XPATH_NEW_CONTENT)

        full_content = ''
        for p in paragraphs:
            full_content += p + '\n'

        abstract = abstract[0].replace('\n', '')
        full_content = full_content.replace('\n', '\n\n')

        title = title.strip()
        abstract = abstract.strip()
        full_content.strip()

        print(f'[cyan]{title}[/cyan]\n\n')
        print(f'[green]{abstract}[/green]\n')
        print(f'[yellow]{full_content}[/yellow]\n\n')
        answer = ''
        while answer.capitalize() != 'S' and answer.capitalize() != 'N':
            print('[green]Desea ver más noticias?[/green] (S/N)')
            answer = input('')
            answer = answer.capitalize()
            if answer != 'S' and answer != 'N':
                print('[red]Opción incorrecta[/red]')
        if answer == 'S':
            clear()
            run()

    else:
        print(f'[red]Error: {response.status_code}[/red]')




if __name__ == '__main__':
    run()
