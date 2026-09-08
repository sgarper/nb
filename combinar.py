import xml.etree.ElementTree as ET
import urllib.request
import gzip

# URLs individuales sacadas de tu lista IPTV
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
                if elem.tag in ['channel', 'programme']:
                    root_unificado.append(elem)
    except Exception as e:
        print(f"Error descargando {url}: {e}")

tree = ET.ElementTree(root_unificado)
tree.write("epg.xml", encoding="utf-8", xml_declaration=True)
