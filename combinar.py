import xml.etree.ElementTree as ET
import urllib.request
import gzip

# Diccionario ampliado de traducción / sustitución rápida
DICCIONARIO = {
    # --- TÉRMINOS Y COMPETICIONES (Ruso -> Español) ---
    "Футбол": "Fútbol",
    "Кубок России": "Copa de Rusia",
    "Бильярд": "Billar",
    "Лига Чемпионов": "Liga de Campeones",
    "Лига Европы": "Liga Europa",
    "Лига Конференций": "Liga Conferencia",
    "Трансляция из Москвы": "Retransmisión desde Moscú",
    "Обзор тура": "Resumen de la jornada",
    "Прямая трансляция": "En directo",
    "В записи": "Diferido",
    "Матч": "Partido",
    "Обзор": "Resumen",
    "Журнал": "Revista / Magazín",
    "1/16 финала": "Dieciseisavos de final",
    "1/8 финала": "Octavos de final",
    "1/4 финала": "Cuartos de final",
    "1/2 финала": "Semifinales",
    "Финал": "Final",
    "Испания": "España",
    "Италия": "Italia",
    "Англия": "Inglaterra",
    "Германия": "Alemania",
    "Франция": "Francia",

    # --- TÉRMINOS Y COMPETICIONES (Polaco -> Español) ---
    "Piłka nożna": "Fútbol",
    "Liga niemiecka": "Liga Alemana",
    "Liga hiszpańska": "Liga Española",
    "Liga włoska": "Liga Italiana",
    "Liga francuska": "Liga Francesa",
    "Liga angielska": "Liga Inglesa",
    "Liga mistrzów": "Liga de Campeones",
    "Liga europy": "Liga Europa",
    "Na żywo": "En directo",
    "Premiera": "Estreno",
    "Magazyn": "Revista / Magazín",
    "Skróty": "Resúmenes",
    "Studio": "Plató / Análisis",

    # --- ESPAÑA (LaLiga) ---
    "Реал": "Real Madrid",
    "Реал Мадрид": "Real Madrid",
    "Барселона": "Barcelona",
    "Атлетико": "Atlético de Madrid",
    "Атлетик": "Athletic Club",
    "Севилья": "Sevilla",
    "Бетис": "Real Betis",
    "Реал Сосьедад": "Real Sociedad",
    "Вильярреал": "Villarreal",
    "Валенсия": "Valencia",
    "Сельта": "Celta de Vigo",
    "Осасуна": "Osasuna",
    "Райо Вальекано": "Rayo Vallecano",
    "Мальорка": "Mallorca",
    "Хетафе": "Getafe",
    "Жирона": "Girona",
    "Лас-Пальмас": "Las Palmas",
    "Алавес": "Alavés",
    "Эспаньол": "Espanyol",
    "Вальядолид": "Real Valladolid",
    "Эльче": "Elche",
    "Сегунда": "Segunda división",
    "Леганес": "Leganés",

    # --- INGLATERRA (Premier League) ---
    "Манчестер Сити": "Manchester City",
    "Манчестер Юнайтед": "Manchester United",
    "Арсенал": "Arsenal",
    "Ливерпуль": "Liverpool",
    "Челси": "Chelsea",
    "Тоттенхэм": "Tottenham Hotspur",
    "Ньюкасл": "Newcastle United",
    "Астон Вилла": "Aston Villa",
    "Брайтон": "Brighton",
    "Вест Хэм": "West Ham",
    "Вулверхэмптон": "Wolverhampton",
    "Эвертон": "Everton",
    "Брентфорд": "Brentford",
    "Фулхэм": "Fulham",
    "Кристал Пэлас": "Crystal Palace",
    "Борнмут": "Bournemouth",
    "Ноттингем Форест": "Nottingham Forest",
    "Лестер": "Leicester City",
    "Ипсвич": "Ipswich Town",
    "Саутгемптон": "Southampton",

    # --- ITALIA (Serie A) ---
    "Интер": "Inter de Milán",
    "Милан": "AC Milan",
    "Ювентус": "Juventus",
    "Наполи": "Nápoles",
    "Рома": "AS Roma",
    "Лацио": "Lazio",
    "Аталанта": "Atalanta",
    "Фиорентина": "Fiorentina",
    "Торино": "Torino",
    "Болонья": "Bologna",
    "Монца": "Monza",
    "Дженоа": "Genoa",
    "Удинезе": "Udinese",
    "Кальяри": "Cagliari",
    "Лечче": "Lecce",
    "Верона": "Hellas Verona",
    "Эмполи": "Empoli",
    "Парма": "Parma",
    "Комо": "Como",
    "Венеция": "Venezia",

    # --- FRANCIA (Ligue 1) ---
    "ПСЖ": "PSG",
    "Пари Сен-Жермен": "Paris Saint-Germain",
    "Марсель": "Olympique de Marsella",
    "Олимпик Марсель": "Olympique de Marsella",
    "Монако": "Monaco",
    "Лион": "Olympique de Lyon",
    "Олимпик Лион": "Olympique de Lyon",
    "Lille": "Lille OS",
    "Лилль": "Lille",
    "Ренн": "Rennes",
    "Ницца": "Niza",
    "Ланс": "Lens",
    "Страсбур": "Estrasburgo",
    "Тулуза": "Toulouse",
    "Монпелье": "Montpellier",
    "Реймс": "Reims",
    "Нант": "Nantes",
    "Брест": "Brest",
    "Гавр": "Le Havre",
    "Осер": "Auxerre",
    "Сент-Этьен": "Saint-Étienne",
    "Анже": "Angers"
}

def traducir_texto(texto):
    if not texto:
        return texto
    for origen, destino in DICCIONARIO.items():
        texto = texto.replace(origen, destino)
    return texto

URLS = [
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=7631",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=465373",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=465198",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=7673",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=5755",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=538903",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=62234",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=90540",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=67504",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=6340",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=6338",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=562308",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=406566",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=406588",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=540072",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=464949",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=465329",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=6958",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=5828",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=7612",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=392147",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=392164",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=219100",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=219104",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=406806",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=6152",
    "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL01hZHJpZA%3D%3D&channel_id=6150"
]

root_unificado = ET.Element("tv")

for url in URLS:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read()
            if response.info().get('Content-Encoding') == 'gzip':
                content = gzip.decompress(content)
            
            sub_tree = ET.fromstring(content)
            for elem in sub_tree:
                if elem.tag == 'programme':
                    for sub in elem:
                        if sub.tag in ['title', 'desc'] and sub.text:
                            sub.text = traducir_texto(sub.text)
                if elem.tag in ['channel', 'programme']:
                    root_unificado.append(elem)
    except Exception as e:
        print(f"Error procesando {url}: {e}")

tree = ET.ElementTree(root_unificado)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)
