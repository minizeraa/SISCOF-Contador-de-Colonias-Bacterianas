# SISCOF-Contador-de-Colonias-Bacterianas

## 🧫 Visão Geral

O **Detector de Colônias em Placa de Petri** é uma aplicação interativa desenvolvida com **Python** e **Streamlit** para facilitar a identificação e contagem de colônias bacterianas em imagens laboratoriais. Por meio de técnicas de visão computacional e algoritmos de otimização, o sistema automatiza etapas que geralmente são feitas manualmente, tornando o processo mais rápido, preciso e confiável.

Voltado para aplicações laboratoriais, científicas e educacionais, o sistema oferece controle visual total da imagem, parâmetros ajustáveis e exportação dos dados analisados.

## 🚀 Funcionalidades Principais

- **Upload e visualização de imagem** da placa de Petri (formatos `.png`, `.jpeg`, `.jpg`);
- **Ferramenta de zoom interativo**, com seleção manual da região da placa;
- **Definição assistida da placa e de colônias pequenas e grandes** por meio de círculos desenhados na interface;
- **Detecção automática de colônias** com base em transformada de Hough Circular;
- **Otimização bayesiana** para calibrar o melhor valor de sigma na detecção (algoritmo `gp_minimize`);
- **Visualização e confirmação manual das colônias detectadas**, com recortes da imagem original e binarizada;
- **Exportação de imagens** em arquivos `.zip` separando colônias confirmadas e descartadas.

## 📷 Imagens

![2024-05-17_15-55](https://github.com/user-attachments/assets/a545707a-eaeb-4529-8cb7-2fe6b204d7cb)


## 🗂 Arquitetura & Estrutura de Código

| Arquivo/Pasta               | Descrição |
|----------------------------|-----------|
| `streamlit_app.py`         | Ponto de entrada da aplicação (upload da imagem). |
| `passo_1.py`               | Etapa de zoom e marcação da placa de Petri e colônias de referência. |
| `passo_2.py`               | Otimização de parâmetros e detecção automática de colônias. |
| `passo_3.py`               | Análise dos resultados, visualização e exportação. |
| `detectar_colonias.py`     | Função de detecção usando `skimage` (Transformada de Hough). |
| `models/Circulo.py`        | Classe base `Circulo` e especialização `Colonia` com métodos de análise. |

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **Streamlit**: para construção da interface web interativa;
- **OpenCV**: para pré-processamento de imagem e limiarização adaptativa;
- **Scikit-Image (`skimage`)**: para transformada de Hough e detecção de bordas;
- **Scikit-Optimize (`skopt`)**: para otimização bayesiana dos parâmetros de detecção;
- **Pillow**: para manipulação de imagens;
- **Matplotlib**: para gráficos e visualização;
- **Loguru**: para logging detalhado e rastreamento de eventos.

## ⚙️ Instalação e Configuração

1. **Clone o repositório**

```bash
 git clone https://github.com/GustavoGLD/colony-detector.git
 cd colony-detector
```

2. **Crie e ative um ambiente virtual**

```bash
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**

```bash
streamlit run streamlit_app.py
```

## 👨‍💻 Como Usar

1. Carregue uma imagem da placa de Petri na tela inicial.
2. Use o zoom e desenhe o círculo que define a área da placa.
3. Marque colônias pequenas e grandes como referência.
4. Avance para a etapa de detecção automática.
5. Revise e confirme visualmente as colônias detectadas.
6. Exporte as imagens confirmadas ou descartadas para análise futura.

## 📊 Resultados

Os resultados incluem:

* Imagens recortadas das colônias;
* Quantidade total e filtrada de colônias detectadas;
* Visualização da detecção sobre a imagem original;
* Exportação em `.zip`.

## 🚧 Trabalhos Futuros

* Implementar detecção por aprendizado de máquina supervisionado;
* Calcular métricas como densidade e distribuição espacial das colônias;
* Adicionar suporte a múltiplas placas por imagem;
* Internacionalização da interface (Português/Inglês).

## 🔍 Desafios & Aprendizados

* **Calibração dos parâmetros de detecção** usando otimização bayesiana aumentou significativamente a precisão.
* **Segmentação de imagem** com limiar adaptativo exigiu atenção à variação de iluminação.
* **Modularidade e orientação a objetos** foram essenciais para isolar responsabilidades.
* A **interface com Streamlit** permitiu rápido desenvolvimento com boa usabilidade para usuários não técnicos.

**Autor:** Gustavo Lídio Damaceno • [LinkedIn](https://www.linkedin.com/in/gustavo-lidio-damaceno/)

**Empresa:** Siscof
