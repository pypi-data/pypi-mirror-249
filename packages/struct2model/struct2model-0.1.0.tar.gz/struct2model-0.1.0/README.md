# Struct2Model

Create serializable rules for your python models.

## Usage


```python
import datetime
from struct2model.main import transform_value


VALUE = {
    "id": 1323,
    "name": "Sergey",
    "email": "serger.g@gmail.com",
    "birth": "1985-05-05",
    "last_login": "2015-05-05 12:00:00",
    "blocked": "SIM",
    "created_at": "2015-05-05T12:00:00.000Z",
    "updated_at": "2015-05-05T12:00:00.000+03:00",
    "address": {
        "id": 1,
        "city": "Moscow",
        "street": "Lenina",
        "house": "1",
        "state": "1",
        "zip": "123456",
    },
    "phones": [
        {"id": 1, "number": "1234567890"},
        {"id": 2, "number": "0987654321"},
    ],
}

RAPAZ_TO_PERSON_MAPPING_RULES = {
    "id": "id",
    "nome": "name",
    "data_nascimento": "birth|date,%Y-%m-%d",
    "endereco": {
        "rua": "address.street",
        "numero": "address.house",
        "bairro": "address.state",
        "cidade": "address.city",
        "estado": "address.state",
        "cep": "address.zip",
    },
    "ultima_vez_logado": "last_login|datetime,%Y-%m-%d %H:%M:%S",
    "data_cadastro": "created_at|datetime,%Y-%m-%dT%H:%M:%S.%fZ",
    "telefones": {
        "__for__": "phones",
        "__as__": "phone",
        "numero": "phone.number",
    },
    "bloqueado": "blocked|bool,SIM",
}

result = transform_value(VALUE, RAPAZ_TO_PERSON_MAPPING_RULES)

assert result["data_nascimento"] == datetime.date(1985, 5, 5)
assert result["ultima_vez_logado"] == datetime.datetime(2015, 5, 5, 12, 0)
assert result["data_cadastro"] == datetime.datetime(2015, 5, 5, 12, 0)
assert result["telefones"][0]["numero"] == "1234567890"
assert result["telefones"][1]["numero"] == "0987654321"
assert result["bloqueado"] == True
assert result["endereco"]["rua"] == "Lenina"
assert result["endereco"]["numero"] == "1"
assert result["endereco"]["bairro"] == "1"
assert result["endereco"]["cidade"] == "Moscow"
assert result["endereco"]["estado"] == "1"
assert result["endereco"]["cep"] == "123456"

assert result["id"] == 1323

```

## Installation

```bash
pip install struct2model
```

## Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

## License

MIT License
