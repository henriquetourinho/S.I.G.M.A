# 💡 S.I.G.M.A. – Sistema Inteligente de Gerenciamento e Mapeamento de Arquivos

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**Uma plataforma de exploração e mapeamento de dados locais — nascida na Bahia para o mundo.**

S.I.G.M.A. é uma aplicação de desktop avançada, escrita em Python com PySide6, que transforma a maneira como você busca, analisa e entende os arquivos em seu sistema Linux.

![Screenshot do S.I.G.M.A.](https://github.com/henriquetourinho/S.I.G.M.A/blob/main/media/sigma.gif?raw=true)

---

### Sobre o Projeto

O S.I.G.M.A. não nasceu pronto. Ele é a materialização da jornada de um desenvolvedor visionário que partiu de uma pergunta fundamental: **"Como transformar um simples script de busca em uma solução de inteligência de dados completa, robusta e inovadora?"**

O projeto começou com um humilde script em Bash e, através de uma evolução contínua e ambiciosa, foi reescrito e aprimorado em Python, ganhando uma interface gráfica moderna, funcionalidades de busca multi-critério e uma arquitetura robusta que abre as portas para o futuro da análise de dados com IA.

Cada funcionalidade do S.I.G.M.A. foi meticulosamente planejada e implementada para criar uma ferramenta que não apenas encontra arquivos, mas também revela a informação contida neles. Este é um projeto que reflete a paixão pela tecnologia e o compromisso de desenvolver software de alta qualidade no Brasil.

---

### 🚀 Instalação Rápida (.deb autossuficiente)

> **Novo!** Agora o S.I.G.M.A. pode ser instalado facilmente via pacote `.deb` autossuficiente:
>
> - Não requer Python, PySide6 ou outras bibliotecas instaladas no sistema.
> - O executável já traz tudo embutido, graças ao [PyInstaller](https://pyinstaller.org/).
> - Compatível com Debian, Ubuntu e derivados.
>
> **Passos:**
> 1. [Baixe o último pacote .deb na página de releases](https://github.com/henriquetourinho/S.I.G.M.A/releases).
> 2. Instale via terminal:
>    ```bash
>    sudo dpkg -i sigma-deb.deb
>    sudo apt-get install -f  # caso precise corrigir dependências
>    ```
> 3. Execute digitando:
>    ```bash
>    sigma
>    ```
> 4. Pronto! Não é necessário configurar ambientes Python nem instalar dependências.

---

### Principais Funcionalidades

* **🖥️ Interface Gráfica Avançada:**
    * Construída com **PySide6**, oferece uma experiência de usuário limpa, intuitiva e moderna para realizar buscas complexas sem a necessidade de memorizar comandos.

* **🔎 Busca Multi-Critério e Granular:**
    * Filtre arquivos com precisão cirúrgica por **Nome**, **Extensão**, **Classificação** (Imagens, Documentos, etc.), **Tamanho** (com unidades de KB, MB, GB), **Permissões** (Leitura, Executável), **Proprietário** (Usuário) e **Data da Última Modificação**.

* **⚡ Desempenho Assíncrono:**
    * Utiliza `threading` para executar as buscas em segundo plano. A interface **nunca congela**, mesmo ao escanear diretórios com milhões de arquivos, permitindo total interatividade e a capacidade de abortar a busca a qualquer momento.

* **📊 Visualização Detalhada de Metadados:**
    * A tabela de resultados exibe uma riqueza de informações sobre cada arquivo encontrado, permitindo uma análise rápida e completa dos dados.

* **🌐 Portabilidade e Robustez:**
    * Escrito em Python para ser compatível com diversos sistemas baseados em Debian, com tratamento de erros para garantir uma operação estável.

---

### Instalação e Uso Técnico (Método Tradicional)

> Se preferir instalar pelo código-fonte, siga o passo a passo abaixo:

1.  **Instale as dependências base do sistema:**
    ```bash
    sudo apt-get update
    sudo apt-get install git python3-venv -y
    ```

2.  **Clone o repositório do S.I.G.M.A.:**
    ```bash
    git clone https://github.com/henriquetourinho/S.I.G.M.A.git
    cd S.I.G.M.A
    ```

3.  **Crie e ative o Ambiente Virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Instale as Dependências da Interface Gráfica:**
    ```bash
    sudo apt-get install python3-pyside6 -y
    ```

5.  **Execute o S.I.G.M.A.:**
    ```bash
    python3 sigma.py
    ```
    *Nota: É recomendado executar como usuário normal, não como root.*

---

### Visão de Futuro (Roadmap)

O S.I.G.M.A. foi projetado para ser uma plataforma em constante evolução. As próximas funcionalidades planejadas incluem:

* **Análise de Espaço (Treemap):** Visualização interativa do uso de disco dos arquivos encontrados.
* **Visualização de Relações (Grafo):** Mapeamento de como os arquivos se conectam entre si (ex: um HTML e seus CSS/JS).
* **Detecção de Duplicatas Semânticas:** Uso de IA para encontrar arquivos com conteúdo similar, não apenas idênticos.
* **Indexação de Arquivos:** Criação de um índice em SQLite para buscas praticamente instantâneas.

---

### Tech Stack

* **Linguagem:** Python 3
* **Interface Gráfica:** PySide6
* **Bibliotecas Nativas Principais:** `os`, `stat`, `threading`, `pwd`, `datetime`.

---

### Requisitos

* **Sistema Operacional:** Debian ou derivados (Ubuntu, Linux Mint, etc.).
* **Dependências de Sistema:** `git`, `python3`, `python3-venv` e os pacotes do `PySide6` (apenas para instalação tradicional).

---

### Licença

Este projeto é distribuído sob a **GPL-3.0 license**. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🙋‍♂️ Desenvolvido por

**Carlos Henrique Tourinho Santana** 📍 Salvador - Bahia  
🔗 Wiki Debian: [wiki.debian.org/henriquetourinho](https://wiki.debian.org/henriquetourinho)  
🔗 LinkedIn: [br.linkedin.com/in/carloshenriquetourinhosantana](https://br.linkedin.com/in/carloshenriquetourinhosantana)  
🔗 GitHub: [github.com/henriquetourinho](https://github.com/henriquetourinho)

---

📢 **Este é um projeto vivo — colaborações, sugestões e novas ideias são muito bem-vindas!**
