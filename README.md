MyFonts Web Scraper - Análise de Lançamentos de Fontes

Este repositório contém um script em Python desenvolvido para coletar dados sobre lançamentos recentes de fontes no marketplace MyFonts. O projeto faz parte de um estudo sobre métodos quantitativos aplicados ao marketing digital, demonstrando como técnicas de web scraping podem gerar insights estratégicos para profissionais do setor tipográfico.

Com este scraper, você pode extrair informações como nome da fonte, fundidora, designer, preços, quantidade de estilos, tags, data de estreia e imagens das amostras. Os dados são salvos em uma planilha Excel (.xlsx) para análises posteriores.

🎯 Objetivos

Coletar automaticamente dados de novas fontes lançadas no MyFonts (seção "What's New").
Estruturar as informações em um formato tabular para facilitar análises de mercado.
Fornecer uma base para responder perguntas como:

Qual é o preço médio dos lançamentos?
Existe sazonalidade nos lançamentos?
Quais fundidoras estão mais ativas?
A presença de fontes variáveis influencia o preço?
Respeitar boas práticas de raspagem de dados (ética, baixo impacto no servidor).
🛠️ Tecnologias Utilizadas

Python 3.8+
Selenium – automação de navegador para sites dinâmicos
Pandas – manipulação e exportação dos dados para Excel
Requests – download de imagens
WebDriver Manager (opcional) – gerenciamento automático do ChromeDriver
📋 Pré-requisitos

Antes de executar o script, certifique-se de ter instalado:

Python (versão 3.8 ou superior)
Google Chrome (navegador utilizado para automação)
ChromeDriver compatível com sua versão do Chrome (ou use webdriver-manager para instalação automática)
🚀 Instalação e Configuração

Clone este repositório:

bash
git clone https://github.com/seu-usuario/myfonts-scraper.git
cd myfonts-scraper
Crie e ative um ambiente virtual (recomendado):

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Instale as dependências:

bash
pip install -r requirements.txt
Se o arquivo requirements.txt não existir, instale manualmente:

bash
pip install selenium pandas requests webdriver-manager
Verifique o ChromeDriver:

Opção 1 (manual): Baixe o ChromeDriver do site oficial e coloque-o no PATH ou na pasta do projeto.
Opção 2 (automática): O script pode usar o webdriver-manager para baixar a versão correta automaticamente (veja a seção de configuração).
▶️ Como Usar

Ajuste as configurações iniciais (opcional):
No arquivo principal (ex.: scraper.py), você pode modificar:

O intervalo de páginas a serem percorridas (variável range(1, 6) para páginas 1 a 5).
O fatiamento dos links (subset = cards[16:40]).
Os tempos de espera (time.sleep) para simular navegação humana.
Execute o script:

bash
python scraper.py
Acompanhe a execução:

O navegador Chrome será aberto e começará a navegar pelas páginas de novidades.
Para cada link de fonte, o script extrairá os dados e, se disponível, baixará a imagem da amostra.
Mensagens no terminal indicarão o progresso e eventuais pausas.
Resultados:

Ao final, um arquivo Excel será gerado com o nome Myfonts_Whats-New_Fonts_DD-MM.xlsx (ex.: Myfonts_Whats-New_Fonts_17-03.xlsx).
As imagens baixadas serão salvas na pasta imagens/, com nomes baseados no título da fonte.
⚙️ Funcionamento Detalhado

O script opera em duas etapas principais:

1. Coleta dos links das coleções

Acessa a URL https://www.myfonts.com/pt/collections/whats-new?page={page} para cada página definida.
Aguarda o carregamento dos elementos âncora que contenham /pt/collections/ no atributo href.
Filtra os links para remover aqueles que apontam para outras páginas de novidades (evita links de paginação).
Seleciona apenas os links dentro de um intervalo específico ([16:40]) para evitar banners e menus.
2. Extração de dados de cada fonte

Para cada link coletado, o script acessa a página detalhada da fonte.
Utiliza localizadores (By.CLASS_NAME, By.XPATH, By.ID) para extrair:

Nome da fonte (about-trademark-text-block)
Designer (primeiro link dentro de //p//a[@class='font_info_name'])
Fundidora (terceiro link no mesmo conjunto)
Preço individual (subheader_right1) – via regex para capturar valores em R$
Preço da família completa (completefamily) – extrai quantidade de estilos e o valor
Data de estreia (elemento span após o label "Estreia")
Tags (related_tags_visibility) – coletadas como lista e convertidas em string
Indicador de fonte variável (presença da tag "variable")
URL da imagem de amostra (a partir de um elemento .owl-item img)
As imagens são baixadas em resolução aumentada (modificando os parâmetros width e height na URL).
Pausas aleatórias são inseridas para evitar sobrecarga no servidor.
3. Geração da planilha

Os dados são armazenados em uma lista de dicionários e convertidos para um DataFrame pandas.
Uma coluna calculada (PreçoMin/Font) é adicionada (fórmula Excel).
O DataFrame é exportado para Excel sem índice.
📁 Estrutura dos Dados Coletados

Coluna	Descrição
Nome da fonte	Nome comercial da família tipográfica
Fundidora	Empresa ou foundry responsável pela publicação
Designer	Nome do(s) designer(s)
Preço Individual	Preço para licenciar um único estilo (ex.: "R$ 54,04")
Preço Completo	Preço para licenciar toda a família
Quantidade de Fonts	Número de estilos que compõem a família
PreçoMin/Font	Fórmula Excel: preço completo dividido pela quantidade de estilos
Estreia MyFonts	Data de lançamento da fonte no site
Imagem	Caminho local para a imagem baixada
Link	URL da página da fonte no MyFonts
Tags	Lista de tags separadas por vírgula (ex.: "Sans serif, Display, Variable")
Variable	"Sim" se a fonte for variável, "Não" caso contrário
📊 Possíveis Análises com os Dados

Com a planilha gerada, você pode realizar diversas análises de marketing e inteligência de mercado:

Distribuição de preços: média, mediana, faixas de preço mais comuns.
Sazonalidade: quantos lançamentos por dia da semana/mês.
Concentração de mercado: fundidoras e designers com mais lançamentos.
Impacto de tags: correlação entre tags (ex.: "variable") e preço.
Benchmarking: comparação de preços entre diferentes categorias.
Evolução temporal: tendências ao longo do período coletado.
🤝 Ética e Boas Práticas

Este projeto segue as recomendações éticas para web scraping:

Respeita o arquivo robots.txt do MyFonts (as áreas bloqueadas, como /account, não são acessadas).
Utiliza pausas aleatórias (time.sleep) para não sobrecarregar os servidores.
Simula comportamentos humanos (rolagem suave da página, tempos variados).
Coleta apenas dados publicamente acessíveis, sem autenticação.
Os dados são destinados a fins educacionais e de pesquisa.
Aviso: Verifique os termos de uso do site antes de executar o script em larga escala. O uso comercial dos dados pode exigir autorização prévia.

🧩 Personalização

Você pode adaptar o script para outras seções do MyFonts ou para outros sites, alterando:

As URLs iniciais e os seletores CSS/XPath.
Os campos extraídos.
O intervalo de páginas e o fatiamento dos links.
Os parâmetros de imagem (largura/altura desejados).
📝 Contribuição

Contribuições são bem-vindas! Siga os passos:

Faça um fork do projeto.
Crie uma branch para sua feature (git checkout -b feature/nova-funcionalidade).
Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade').
Push para a branch (git push origin feature/nova-funcionalidade).
Abra um Pull Request.
📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.
