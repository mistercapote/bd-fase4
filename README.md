# bd-fase4
Esse repositório contém o trabalho final da disciplina de Banco de Dados.

## Requerimentos

Para instalar as bibliotecas necessárias, execute:
```bash
  pip install -r requirements.txt
```

## Banco de dados

Entre no PostgreSQL:
```
winpty psql -U postgres
```

Crie o database:
```
DROP DATABASE IF EXISTS skoob;
CREATE DATABASE skoob WITH ENCODING 'UTF8';
\c skoob
\i DDL_create_tables_skoob.sql
\i DML_insert_skoob.SQL
```

## Configuração

No arquivo bdfase4/settings.py, altere os dados:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'skoob',
        'USER': 'SUA_USUARIO_DO_POSTGRES',
        'PASSWORD': 'SUA_SENHA_DO_POSTGRES',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=skoob,public'
        }
    }
}
````
## Rodar o servidor

Para criar o html, execute:
```bash
  python manage.py runserver
```

## Contribuições

Elisa de Oliveira Soares

Jaime Willian Carneiro

Luiz Eduardo Bravin
