# API Bank - AWS Chalice

API bancaria simple desarrollada con **AWS Chalice + Python**, pensada para practicar arquitectura serverless, lógica de negocio y despliegue sobre AWS Lambda/API Gateway.

## Stack

* Python 3.10+
* AWS Chalice
* Pydantic
* WSL2 / Ubuntu
* AWS Lambda / API Gateway

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install chalice pydantic
```

Ejecutar localmente:

```bash
chalice local
```

Base URL:

```text
http://127.0.0.1:8000
```

## Estructura

```text
.
├── .chalice/
│   └── config.json
├── chalicelib/
│   ├── repositories/
│   ├── schemas/
│   └── services/
├── app.py
├── requirements.txt
└── README.md
```

Flujo principal:

```text
Chalice Route
    ↓
Service
    ↓
Repository
```

## Lógica de negocio

La API permite gestionar cuentas bancarias simples.

Reglas principales:

* monedas permitidas: `PEN` y `USD`;
* las cuentas inician con saldo `0.00`;
* solo cuentas activas pueden operar;
* depósitos y retiros deben ser mayores que `0`;
* no se puede retirar más dinero del saldo disponible;
* los montos usan `Decimal`.

## Endpoints

### Crear cuenta

```http
POST /api/v1/accounts
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Tony Inuma",
    "currency": "PEN"
  }'
```

### Listar cuentas

```http
GET /api/v1/accounts
```

```bash
curl http://127.0.0.1:8000/api/v1/accounts
```

### Obtener cuenta

```http
GET /api/v1/accounts/{account_id}
```

```bash
curl http://127.0.0.1:8000/api/v1/accounts/1
```

### Depositar

```http
POST /api/v1/accounts/{account_id}/deposit
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/accounts/1/deposit \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "500.00"
  }'
```

### Retirar

```http
POST /api/v1/accounts/{account_id}/withdraw
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/accounts/1/withdraw \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "150.00"
  }'
```

## Próximos pasos

```text
[ ] Transfers
[ ] Transaction history
[ ] Persistencia
[ ] DynamoDB / PostgreSQL
[ ] Tests
[ ] Deploy AWS
```
