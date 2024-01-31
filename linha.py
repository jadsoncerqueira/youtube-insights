from selenium import webdriver
from parsel import Selector
from selenium.webdriver.common.by import By
import time
import unicodedata
import csv
import os

file_path = './maiores-canais.csv'


def getByTenMoviesChannell(arroba):
    class_item_btn = "yt-chip-cloud-chip-renderer"
    class_item_card = "#dismissible"

    URL = f"https://www.youtube.com/{arroba}/videos"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    driver.get(URL)

    driver.implicitly_wait(10)

    btns = driver.find_elements(By.CLASS_NAME, class_item_btn)
    btns[len(btns) - 2].click()

    time.sleep(2)
    page_source = driver.page_source
    selector = Selector(text=page_source)

    canalName = selector.css("yt-formatted-string::text").get()
    videos = selector.css(class_item_card).getall()
    videos = videos[:10]

    vid = []

    for video in videos:
        if (len(video.strip()) > 1):
            aux = Selector(text=video)
            href = aux.css("#thumbnail a::attr(href)").get()
            link_video = f'https://www.youtube.com{href}'
            title = aux.css("h3 a::attr(title)").get()
            views = aux.css("span.ytd-video-meta-block::text").get()
            views = unicodedata.normalize("NFKD", views)
            videos_aux = [title, link_video, views]
            vid.append(videos_aux)

    driver.quit()
    return (canalName, vid)


arrobas_canais = [
    "@codigofontetv",
]

header = ['Canal', 'Titulo do Video', 'Link', "Visualizações"]

ponteiro = 1

print("-----------------------------")
print("Iniciando extração de videos!")
print("-----------------------------")

for arroba in arrobas_canais:
    file_exists = os.path.isfile(file_path)
    canal = getByTenMoviesChannell(arroba)
    with open(file_path, 'a') as csvfile:
        if not file_exists:
            csv.writer(csvfile, delimiter=',').writerow(header)

        for item in canal[1]:
            csv.writer(csvfile, delimiter=',').writerow([canal[0], *item])

    print(f'{ponteiro}/{len(arrobas_canais)} Canais extraidos')
    ponteiro += 1

print("--------------------")
print("Extração finalizada!")
print("--------------------")
