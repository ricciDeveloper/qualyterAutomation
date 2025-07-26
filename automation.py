import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# === CONFIGURAÇÕES DO DRIVER ===
def configurar_driver():
    print("🔧 Iniciando driver do Chrome em modo anônimo...")
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1200x800")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Driver iniciado com sucesso!")
        return driver
    except Exception as e:
        print("❌ Erro ao iniciar o driver:", e)
        raise

# === LER PLANILHA ===
def carregar_palavras_arquivo(caminho):
    print(f"📂 Lendo planilha: {caminho}")
    try:
        df = pd.read_excel(caminho, sheet_name="Página1")
        print(f"📄 {len(df)} palavras-chave carregadas.")
        return df
    except Exception as e:
        print("❌ Erro ao ler a planilha:", e)
        raise

# === VERIFICAR RESULTADO DA BUSCA ===
def analisar_resultado(driver, palavra):
    print(f"🔎 Buscando por: {palavra}")
    driver.get(f"https://www.google.com/search?q={palavra}")

    try:
        # Espera até o resultado principal aparecer
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "search")))
    except:
        print("⚠️ Timeout esperando a página carregar...")

    # Espera aleatória para evitar detecção
    espera = random.uniform(7, 12)
    print(f"⏱️ Aguardando {espera:.2f}s...")
    time.sleep(espera)

    try:
        anuncios = driver.find_elements(By.XPATH, "//div[@data-text-ad]")
        patrocinados = []

        for bloco in anuncios:
            try:
                link = bloco.find_element(By.TAG_NAME, "a").get_attribute("href")
                if link:
                    patrocinados.append(link)
            except:
                continue

        belgo_ads = [url for url in patrocinados if "belgo.com.br" in url]
        outros_ads = [url for url in patrocinados if "belgo.com.br" not in url]

        if belgo_ads and outros_ads:
            return "Patrocinado Belgo e Concorrente"
        elif belgo_ads:
            return "Patrocinado Belgo"
        elif patrocinados:
            return "Outros"

        print("ℹ️ Nenhum patrocínio detectado. Verificando resultado orgânico...")
        resultados_organicos = driver.find_elements(By.CSS_SELECTOR, "div#search a")

        encontrou_belgo = False
        encontrou_concorrente = False

        for link in resultados_organicos:
            href = link.get_attribute("href")
            if href and href.startswith("http"):
                if "belgo.com.br" in href:
                    encontrou_belgo = True
                else:
                    encontrou_concorrente = True

        if encontrou_belgo and encontrou_concorrente:
            return "Orgânico Belgo e Concorrente"
        elif encontrou_belgo:
            return "Orgânico Belgo"
        elif encontrou_concorrente:
            return "Orgânico Concorrente"

    except Exception as e:
        print("⚠️ Erro durante análise da SERP:", e)

    return "Outros"

# === PROCESSAR PALAVRAS-CHAVE ===
def processar_palavras(driver, df):
    print("🚀 Iniciando análise das palavras-chave...")
    resultados = []

    total = len(df)
    for i, palavra in enumerate(df.iloc[:, 0]):
        print(f"🔢 [{i+1}/{total}]")
        try:
            resultado = analisar_resultado(driver, palavra)
        except Exception as e:
            print(f"⚠️ Erro ao analisar '{palavra}':", e)
            resultado = "Erro"
        print(f"✅ Resultado: {palavra} → {resultado}")
        resultados.append(resultado)

    df["Resultado"] = resultados
    return df

# === SALVAR NOVA PLANILHA ===
def salvar_planilha(df, caminho_saida):
    try:
        df.to_excel(caminho_saida, index=False)
        print(f"💾 Planilha salva com sucesso em: {caminho_saida}")
    except Exception as e:
        print("❌ Erro ao salvar a planilha:", e)
        raise

# === EXECUÇÃO PRINCIPAL ===
if __name__ == "__main__":
    caminho_entrada = "Teste Automacao Consulta SERP _ Lojas Belgo.xlsx"
    caminho_saida = "Resultado_Automacao_Belgo.xlsx"
    driver = None

    try:
        driver = configurar_driver()
        df_palavras = carregar_palavras_arquivo(caminho_entrada)
        df_resultado = processar_palavras(driver, df_palavras)
        salvar_planilha(df_resultado, caminho_saida)
        print("🎉 Automação finalizada com sucesso!")
    except Exception as e:
        print("🔥 Erro crítico na execução:", e)
    finally:
        if driver:
            driver.quit()
            print("🛏️ Driver encerrado.")
