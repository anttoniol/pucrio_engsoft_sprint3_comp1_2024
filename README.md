# PUC-RIO: especialização em Engenharia de Software
## Sprint 3
## Componente A: agregador de eventos

### Descrição

Este componente, com o auxílio do componente C, agrega eventos e também fornece uma breve previsão do tempo para 
a semana da data inicial do evento, desde que o evento ocorra nos próximos cinco dias a partir do dia atual. Os dados de previsão do tempo
são obtidos por meio da API da Accuweather.

### Instruções de uso

#### API: Inicialização
1. Clonar o repositório
2. Pelo terminal, acessar a pasta do repositório
3. Criar uma cópia do arquivo "model.properties.ini"
4. Renomear a cópia para "properties.ini"

#### Accuweather
1. Seguir as etapas das seções "Registration" e "App Creation" contidas em https://developer.accuweather.com/getting-started
2. Inserir a API key do Accuweather no campo "key" do arquivo "properties.ini"
   1. Caso haja algum problema, tente usar a chave "rzOq3yuphIvADhvoAzKYXtxd6kEjcFUM" (sem aspas) no "properties.ini" 

#### API: Execução
##### Com Dockerfile
1. Na pasta do componente, executar o Dockerfile usando o comando `sudo docker build -t event_app .`
2. Executar o comando `sudo docker run event_app`
3. Acessar o endereço http://localhost:8000/swagger , para utilizar os endpoints

##### Sem Dockerfile
1. Na pasta do componente, criar um ambiente virtual, conforme explicado em https://www.alura.com.br/artigos/ambientes-virtuais-em-python?gclid=Cj0KCQjw6cKiBhD5ARIsAKXUdyaJkqNkWzEWgYdNgrCXhupl1irAxb_tmcN0RmpRj1htFv8RsRSQ9KwaAvmqEALw_wcB
2. Executar o comando pip install -r requirements.txt, para instalar as bibliotecas necessárias
3. No diretório "api", rodar a aplicação: python3 predictor_controller.py
4. Acessar o link http://localhost:8000/swagger, para fazer alguma requisição à API

