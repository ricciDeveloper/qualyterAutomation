# Automação de Consulta SERP - Lojas Belgo

Este projeto automatiza a consulta de palavras-chave no Google Search (SERP) para verificar a presença de anúncios e resultados orgânicos relacionados ao site **belgo.com.br** e seus concorrentes. A automação é feita com Python, utilizando Selenium para navegar no navegador Chrome e Pandas para manipulação de dados em planilhas Excel.

---

## Funcionalidades

- Leitura de palavras-chave a partir de uma planilha Excel.
- Pesquisa automática no Google para cada palavra-chave.
- Identificação de anúncios patrocinados e resultados orgânicos que contenham URLs do domínio `belgo.com.br` e concorrentes.
- Classificação dos resultados em categorias:
  - Patrocinado Belgo e Concorrente
  - Patrocinado Belgo
  - Outros anúncios
  - Orgânico Belgo e Concorrente
  - Orgânico Belgo
  - Orgânico Concorrente
  - Outros (nenhum resultado relevante)
- Salvamento dos resultados em uma nova planilha Excel.

---

## Requisitos

- Python 3.8+
- Google Chrome instalado
- ChromeDriver compatível com a versão do Chrome (deve estar no PATH ou no mesmo diretório do script)

---

