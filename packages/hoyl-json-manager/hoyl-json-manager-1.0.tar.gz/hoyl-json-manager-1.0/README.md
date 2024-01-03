# JSON Manager
- Pequena biblioteca para validação e manipulação de JSONs.
---
## Instalação
- Enquanto o PyPi está fora do ar, você pode instalar a biblioteca através do `git submodule add git@github.com:Hoyasumii/JsonManager.git`
- Caso queira colocar o submódulo em uma pasta específica, basta adicionar o nome da pasta após o link do repositório.
---
## Métodos disponíveis
### `checker` -> `dict`
- Retorna um dicionário com as chaves que estão: `Faltando`, `Com valor errado` e `Chaves extras`.
- Parâmetros:
    - `json`: O JSON a ser validado.
    - `schema`: O schema a ser usado na validação.
### `dropKey` -> `bool`
- Retorna `True` se a chave foi removida com sucesso, `False` caso contrário.
- Parâmetros:
    - `json`: O JSON a ser manipulado.
    - `key`: A chave a ser removida.
### `get` -> `dict`
- Retorna o `dicionário` do **JSON**.
- Parâmetros:
    - `json`: O JSON a ser manipulado.
### `update` -> `bool`
- Retorna `True` se o **JSON** foi atualizado com sucesso, `False` caso contrário.
- Parâmetros:
    - `json`: O JSON a ser manipulado.
    - `key`: A chave a ser atualizada.
    - `value`: O valor a ser atualizado.
---