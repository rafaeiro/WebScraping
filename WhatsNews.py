from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
import os
from datetime import datetime
import time
import pandas as pd
import random

# Inicializar Chrome
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Data da coleta (para nome do arquivo e coluna)
data_coleta = datetime.now().strftime("%d-%m")

# Lista para armazenar os links finais
hrefs = []
contLinha = 1
# Loop pelas páginas 1 até 30 26
for page in range(1, 3):
    url = f"https://www.myfonts.com/pt/collections/whats-new?page={page}"
    driver.get(url)
    time.sleep(random.uniform(0.8, 1.8))

    # Rolar suavemente até o fim da página em até 15 segundos
    start_time = time.time()
    while True:
        driver.execute_script("window.scrollBy(300, 600);")  # desce 400px por vez
        time.sleep(random.uniform(0.4, 1.2))

        new_height = driver.execute_script("return window.pageYOffset + window.innerHeight")
        total_height = driver.execute_script("return document.body.scrollHeight")

        if new_height >= total_height or (time.time() - start_time) > 10:
            break

    # Esperar os cards carregarem
    wait = WebDriverWait(driver, 9)
    cards = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/pt/collections/']")))

    # 🔑 AQUI entra o fatiamento dentro de cada página
    subset = cards[16:40]  # exemplo: 17º até 40º link da página

    # Extrair só os hrefs válidos e acumular
    page_hrefs = [
        link.get_attribute("href")
        for link in subset
        if "whats-new?page=" not in link.get_attribute("href")
    ]

    hrefs.extend(page_hrefs)  # acumula no global

print(f"Total de links coletados (com fatiamento por página): {len(hrefs)}")
for h in hrefs:
    print(h)

# --- Aqui entra a parte de coleta de dados ---
dados = []

for i, link in enumerate(hrefs, start=1):
    # Pausa de 4 segundos a cada 5 links
    if i % 5 == 0:
        print("⏳ Pausa estratégica de 4 segundos...")
        time.sleep(random.uniform(1.2, 3.2))
    driver.get(link)
    time.sleep(random.uniform(1.8, 6.2))

    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, "//p//a[@class='font_info_name']"))
        )
    except:
        continue

    links = driver.find_elements(By.XPATH, "//p//a[@class='font_info_name']")
    # tags = driver.find_elements(By.ID, "related_tags_visibility")

    try:
        nome_font = driver.find_element(By.CLASS_NAME, "about-trademark-text-block").text.strip()
    except:
        nome_font = "nd"

    try:
        designer = links[0].text.strip()
    except:
        designer = "nd"

    try:
        foundry = links[2].text.strip()
    except:
        foundry = "nd"

    try:
        precoInd_text = driver.find_element(By.CLASS_NAME, "subheader_right1").text.strip()
        match = re.search(r'R\$ ?[\d\.,]+', precoInd_text)
        if match:
            precoInd = match.group(0)  # exemplo: "R$ 54,04"
        else:
            precoInd = "nd"
    except:
        precoInd = "nd"

    try:
        precoComp_text = driver.find_element(By.CLASS_NAME, "completefamily").text.strip()
        # Procurar todos os números (inteiros e com R$)
        numeros = re.findall(r'\d+', precoComp_text)  # captura só números (ex.: ["16", "210", "00"])
        valores = re.findall(r'R\$ ?[\d\.,]+', precoComp_text)

        if numeros:
            qtd_fonts = int(numeros[0])  # primeiro número encontrado (quantidade de estilos)
        else:
            qtd_fonts = 1

        if valores:
            precoComp = valores[-1]  # último valor R$ encontrado
        else:
            precoComp = precoInd
    except:
        qtd_fonts = 1
        precoComp = precoInd

    try:
        release = driver.find_element(
            By.XPATH, "//span[@class='font-info-label' and contains(text(),'Estreia')]/following-sibling::span"
        ).text.strip()
    except:
        release = "nd"

    try:
        owl_items = driver.find_elements(By.CLASS_NAME, "owl-item")
        if owl_items:
            # Dentro do primeiro .owl-item pega a <img>
            first_img = owl_items[0].find_element(By.TAG_NAME, "img")
            img_url = first_img.get_attribute("src")

            # Pasta onde salvar
            os.makedirs("imagens", exist_ok=True)

            # Nome do arquivo com base no nome da fonte
            safe_name = nome_font.replace(" ", "_").replace("/", "_")  # evita problemas em nomes
            file_path = os.path.join("imagens", f"{safe_name}.png")

            # Baixar a imagem com requests
            response = requests.get(img_url)
            with open(file_path, "wb") as f:
                f.write(response.content)

            img_path = file_path  # guarda o caminho salvo
        else:
            img_path = ""
    except:
        print("Nenhum elemento com .owl-item encontrado")
        img_path = ""
    try:
        # Coleta todos os elementos de tags (cada tag é um <a> dentro da div #related_tags_visibility)
        tag_container = driver.find_element(By.ID, "related_tags_visibility")
        tag_elements = tag_container.find_elements(By.TAG_NAME, "a")

        # Extrai o texto de cada tag
        Tags = [t.text.strip() for t in tag_elements if t.text.strip()]
        Tags_str = ", ".join(Tags)  # string única para o Excel

        # Verifica se contém "variable" (case insensitive)
        if any("variable" in t.lower() for t in Tags):
            is_variable = "Sim"
        else:
            is_variable = "Não"

    except:
        Tags = []
        Tags_str = "nd"
        is_variable = "Não"
    contLinha += 1
    dados.append({
        "Nome da fonte": nome_font,
        "Fundidora": foundry,
        "Designer": designer,
        "Preço Individual": precoInd,
        "Preço Completo": precoComp,
        "Quantidade de Fonts": qtd_fonts,
        "PreçoMin/Font": "=E{}/F{}".format(contLinha, contLinha),
        "Estreia MyFonts": release,
        "Imagem": img_path,
        "Link": link,
        "Tags": Tags_str,
        "Variable": is_variable
    })

# Salvar em Excel
df = pd.DataFrame(dados)
arquivo = f"Myfonts_Whats-New_Fonts_{data_coleta}.xlsx"
df.to_excel(arquivo, index=False)

driver.quit()
print(f"✅ Coleta finalizada. {len(dados)} registros válidos salvos em {arquivo}")
