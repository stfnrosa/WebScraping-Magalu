# WebScraping Notbooks Magalu

## Projeto de Raspagem de Notebooks

Este projeto faz a raspagem de dados do site da Magazine Luiza para coletar informações sobre notebooks e suas avaliações, analisa os resultados e exporta para um arquivo Excel.

### Bibliotecas Utilizadas

- **`BeautifulSoup:`** Para analisar o conteúdo HTML e extrair dados.
- **`os:`** Para interagir com o sistema operacional, como criar diretórios e trabalhar com arquivos.
- **`pandas:`** Para manipulação e análise de dados, incluindo a criação de DataFrames e a escrita em Excel.
- **`re:`** Para expressões regulares, utilizadas para extrair dados do texto.
- **`requests:`** Para fazer requisições HTTP para buscar páginas da web.
- **`selenium:`** Para controlar um navegador da web e interagir com conteúdo dinâmico.
- **`time:`** Para pausar a execução e gerenciar intervalos de tempo.

## Estrutura do Projeto

O projeto consiste em vários scripts Python:

- **`main.py`:** O script principal que orquestra todo o processo.
- **`send_email.py`:** Contém a função responsavél pelo envio de email

## Como Usar

1. **Instale as Bibliotecas Necessárias:**
   ```bash
   pip install requests time re os pandas beautifulsoup4 selenium send_email

2. **Configure as credenciais:**
 - Senha de Aplicativo: A segurança é fundamental! Em vez de usar sua senha normal do Gmail, você deve gerar uma "Senha de Aplicativo" específica para este projeto. Veja como:
 - Acesse sua conta do Google: https://myaccount.google.com/
 - Clique em "Segurança".
 - Na seção "Aplicativos com acesso à sua conta", clique em "Senha de aplicativo".
 - Selecione "Criar senha de aplicativo".
 - Dê um nome descritivo à senha (por exemplo, "Raspagem de Notebooks") e clique em "Criar".
 - Copie a senha gerada (é uma senha única e temporária) e guarde-a em um local seguro. Não compartilhe essa senha com ninguém!
 - Preencha o arquivo config_email.py:
    - EMAIL = "seu_email@gmail.com"  -> Substitua pelo seu email
    - PASSWORD = "sua_senha_de_aplicacao"  -> Substitua pela senha de aplicativo gerada
    - SMTP_SERVER = "smtp.gmail.com"  -> Substitua pelo servidor de email desejado e a porta do servidor
    - SMTP_PORT = 587

3. **Execute o Script**:
   ```bash
    python main.py
   
## Como Funciona
- Verificação de Conexão: O script primeiro verifica se o site da Magazine Luiza está acessível.
- Raspagem de Dados: Usando o Selenium, o script navega até a página de destino e extrai informações do produto, incluindo títulos, links e contagem de avaliações.
- Processamento de Dados: Os dados raspados são processados usando pandas para criar DataFrames e analisar as contagens de avaliações.
- Exportação para Excel: Os dados processados são exportados para um arquivo Excel com duas planilhas: 'Melhores' para produtos com pelo menos 100 avaliações e 'Piores' para produtos com menos de 100 avaliações.
- Envio por E-mail: Um email é enviado com a propria planinha gerada.



*O script depende da estrutura do site e dos nomes das classes. Se o site mudar, o script pode precisar ser ajustado.*
## Contribuindo
Contribuições são bem-vindas! Se você encontrar algum problema ou tiver sugestões de melhoria, sinta-se à vontade para abrir um problema ou enviar uma solicitação de pull.
