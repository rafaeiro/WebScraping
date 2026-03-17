from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import pandas as pd

# Inicializar Chrome
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Lista final
dados = []

# Data da coleta (para nome do arquivo e coluna)
data_coleta = datetime.now().strftime("%d-%m")

# Loop pelas páginas desejadas
for page in range(1, 3):
    url = f"https://www.myfonts.com/pt/collections/hot-new-fonts?page={page}"
    driver.get(url)
    time.sleep(1.3)

    # Rolar até o fim da página
    start_time = time.time()
    while True:
        driver.execute_script("window.scrollBy(300, 600);")
        time.sleep(0.33)
        new_height = driver.execute_script("return window.pageYOffset + window.innerHeight")
        total_height = driver.execute_script("return document.body.scrollHeight")
        if new_height >= total_height or (time.time() - start_time) > 15:
            break

    # Esperar os cards carregarem
    wait = WebDriverWait(driver, 10)
    cards = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "a[href*='/pt/collections/']")
    ))

    # 🔑 Fatiamento opcional
    subset = cards[13:69]

    for link_elem in subset:
        href = link_elem.get_attribute("href")

        # ⚠️ FILTRO: só processa links com "-font-" no endereço
        if not href or "-font-" not in href:
            continue

        # Subir até o contêiner com data-index (posição)
        try:
            parent = link_elem.find_element(By.XPATH, "./ancestor::*[@data-index][1]")
            data_index = parent.get_attribute("data-index")
        except:
            data_index = "nd"

        # Extrair nome da fonte e fundidora a partir do link
        try:
            base = href.replace("https://www.myfonts.com/pt/collections/", "")
            partes = base.split("-font-")
            nome_font = partes[0].replace("-", " ").title()
            foundry = partes[1].replace("-", " ").title() if len(partes) > 1 else "nd"
        except:
            nome_font = "nd"
            foundry = "nd"

        dados.append({
            "Nome da fonte": nome_font,
            "Posição": data_index,
            "Fundidora": foundry,
            "Data da coleta": datetime.now().strftime("%d-%m-%Y"),
            "Link": href
        })

# Criar DataFrame e salvar com data no nome
df = pd.DataFrame(dados)
arquivo = f"myfonts_hot_new_fonts_{data_coleta}.xlsx"
df.to_excel(arquivo, index=False, engine='xlsxwriter')

driver.quit()
print(f"✅ Coleta finalizada. {len(dados)} registros válidos salvos em {arquivo}")
