# Aplicativo de conversão das bases do portal DATASUS

Em meio a dificuldade no instante atual de lidar com as bases do datasus, que estão disponiveis para download de uma forma muito granularizada e em um formato não amigável,  esse app vêem com o intuito de simplificar o processo de analise de dados permitindo o download de variás bases de maneira instantanea e em um formato mais amigável. 

----

## Estrutura do projeto

O projeto está modularizado e subdividido da seguinte forma: 

tcc_datatsus_app/  
│  
├── app.py                      # Arquivo principal que inicia o Streamlit  
│  
├── config/                    # Configurações globais e constantes  
│   └── settings.py  
│  
├── database/                  # Tudo relacionado ao SQLite e outras conexões  
│   ├── db.py                  # Conexão com banco de dados  
│   └── queries.py             # Consultas SQL e lógica de acesso aos dados  
│  
├── pages/                     # No caso de usar multipáginas  
│   └── pagina_exemplo.py  
│  
├── services/                  # Regras de negócio, lógicas de manipulação  
│   └── file_service.py  
│  
├── ui/                        # Componentes de interface (Streamlit)  
│   ├── layout.py              # Layouts e organização visual  
│   └── components.py          # Componentes customizados (ex: cards, galerias)  
│  
├── utils/                     # Funções utilitárias gerais  
│   └── helpers.py  
│  
├── data/                      # Local para o CSV original ou dados temporários  
│   └── arquivos.csv  
│  
└── requirements.txt           # Dependências do projeto  
