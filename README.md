# SISCOF: Contador de Colônias Bacterianas 🦠

![SISCOF Logo](https://img.shields.io/badge/SISCOF-Contador-de-Colonias-Bacterianas-brightgreen)

Bem-vindo ao repositório **SISCOF-Contador-de-Colonias-Bacterianas**! Este projeto utiliza Python e Streamlit para detectar automaticamente colônias bacterianas em imagens de placas de Petri. Através de técnicas de visão computacional, otimização bayesiana e validação manual, esta aplicação se torna uma ferramenta poderosa para laboratórios e ambientes educacionais.

## Tabela de Conteúdos

- [Visão Geral](#visão-geral)
- [Recursos](#recursos)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Uso](#uso)
- [Contribuição](#contribuição)
- [Licença](#licença)
- [Contato](#contato)
- [Links Úteis](#links-úteis)

## Visão Geral

O SISCOF é uma aplicação que visa facilitar a contagem de colônias bacterianas, um processo crucial na microbiologia. A detecção precisa dessas colônias pode ajudar na análise de microbiomas e em estudos de saúde pública. A aplicação utiliza a transformada de Hough para identificar círculos, otimizando parâmetros através de técnicas bayesianas. Além disso, oferece a possibilidade de validação manual dos resultados, permitindo que os usuários exportem imagens para documentação e análise.

### Imagem de Exemplo

![Exemplo de Detecção](https://via.placeholder.com/800x400?text=Exemplo+de+Detecção+de+Colônias)

## Recursos

- **Detecção Automática**: Identifica colônias bacterianas em imagens.
- **Otimização Bayesiana**: Ajusta parâmetros para melhorar a precisão da detecção.
- **Validação Manual**: Permite que os usuários revisem e confirmem os resultados.
- **Exportação de Imagens**: Salva imagens com anotações para futuras referências.
- **Interface Amigável**: Desenvolvida com Streamlit para fácil uso.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Streamlit**: Framework para construção de aplicações web.
- **OpenCV**: Biblioteca para visão computacional.
- **scikit-image**: Ferramenta para processamento de imagens.
- **Bayesian Optimization**: Técnica para ajuste de hiperparâmetros.
- **Transformada de Hough**: Método para detecção de formas.

## Instalação

Para instalar o SISCOF, siga os passos abaixo:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/minizeraa/SISCOF-Contador-de-Colonias-Bacterianas.git
   ```

2. **Navegue até o diretório do projeto**:
   ```bash
   cd SISCOF-Contador-de-Colonias-Bacterianas
   ```

3. **Crie um ambiente virtual (opcional, mas recomendado)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate  # Para Windows
   ```

4. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Baixe e execute a aplicação**: Acesse a seção de [Releases](https://github.com/minizeraa/SISCOF-Contador-de-Colonias-Bacterianas/releases) para obter a versão mais recente. 

## Uso

Após a instalação, você pode iniciar a aplicação com o seguinte comando:

```bash
streamlit run app.py
```

A aplicação abrirá em seu navegador padrão. Você poderá carregar imagens de placas de Petri e observar a detecção de colônias em tempo real.

### Passos para Uso

1. **Carregar Imagem**: Clique no botão para carregar uma imagem de uma placa de Petri.
2. **Ajustar Parâmetros**: Use os controles deslizantes para otimizar a detecção.
3. **Visualizar Resultados**: Veja as colônias detectadas na interface.
4. **Validação**: Revise os resultados e faça ajustes manuais, se necessário.
5. **Exportar Imagem**: Salve a imagem com as anotações.

### Exemplo de Interface

![Interface do Usuário](https://via.placeholder.com/800x400?text=Interface+do+Usuário)

## Contribuição

Contribuições são bem-vindas! Se você deseja contribuir para o SISCOF, siga os passos abaixo:

1. **Fork o repositório**.
2. **Crie uma nova branch**:
   ```bash
   git checkout -b feature/nome-da-sua-feature
   ```
3. **Faça suas alterações e commit**:
   ```bash
   git commit -m "Descrição das alterações"
   ```
4. **Envie para o repositório remoto**:
   ```bash
   git push origin feature/nome-da-sua-feature
   ```
5. **Abra um Pull Request**.

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Para perguntas ou sugestões, entre em contato:

- **Autor**: [Seu Nome](mailto:seuemail@example.com)
- **GitHub**: [minizeraa](https://github.com/minizeraa)

## Links Úteis

Para mais informações e downloads, visite a seção de [Releases](https://github.com/minizeraa/SISCOF-Contador-de-Colonias-Bacterianas/releases). 

Explore a aplicação e descubra como ela pode ajudar na análise de colônias bacterianas em seu laboratório ou ambiente educacional.