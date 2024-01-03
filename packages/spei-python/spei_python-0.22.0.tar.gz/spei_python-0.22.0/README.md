[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

spei-python
===========

A library for accessing the SPEI API for python.


## Installation
Use the package manager [poetry](https://pypi.org/project/poetry/) to install.

    poetry install spei-python

## Usage
Use our client to send orders to SPEI.
```python
from spei.client import BaseClient

client = BaseClient(
    host='http://karpay-beta.intfondeadora.app',
    username='karpay',
    password='password',
    priv_key='private_key',
    priv_key_passphrase='passphrase',
)
```

## Methods
- [registra_orden](/spei/README.md)

## Resources
There are two main resources.

- [Orden](spei/resources/orden.py) our abstraction of order, this goes through SPEI as XML.
- [Respuesta](spei/resources/respuesta.py) our abstraction of received SPEI messages and response to SPEI orders.

## Types
- [TipoPagoOrdenPago](/spei/types.py#6) Order payment type.
- [TipoOrdenPago](/spei/types.py#33) Order type.
- [TipoCuentaOrdenPago](/spei/types.py#38) Account type.
- [PrioridadOrdenPago](/spei/types.py#58) Order priority.
- [CategoriaOrdenPago](/spei/types.py#63) Order Category.
- [EstadoOrdenPago](/spei/types.py#76) Order status.
- [ClaveOrdenanteOrdenPago](/spei/types.py#83) Root Institution Code.
- [FolioOrdenPago](/spei/types.py#87) Order invoice identifier.
- [MedioEntregaOrdenPago](/spei/types.py#91) Order transmission method.
- [TopologiaOrdenPago](/spei/types.py#107) Order notification method.

## Errors
You may use any of the generic errors in [errors](/spei/errors.py) to return as response to SPEI. (?) Need to ask karpay.

These errors are included inside respuesta.

## Test
Tested with [mamba](https://mamba-framework.readthedocs.io/en/latest/), install poetry dev packages and then run tests.

    poetry run make test

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Checksum Generator
This repo includes a utility to generate [firma digital aplicada](https://www.notion.so/fondeadoraroot/Algoritmo-de-Firma-e-Karpay-SPEI-02e6c25b7c5943bea054ae37c9605bdc)

```sh
python bin/generate_checksum.py bin/message.json
```
