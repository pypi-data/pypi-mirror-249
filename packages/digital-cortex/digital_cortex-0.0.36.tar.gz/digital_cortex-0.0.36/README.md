# digital-cortex

Python Client package for Digital Cortex

[# https://packaging.python.org/en/latest/tutorials/packaging-projects/]()

Aug-22-2023

### How to use:

``
pip install digital-cortex
``

```
import digital_cortex as dc

token = "get token from your digital-cortex account"

client = dc.client(token)

response = client.execute_function(......)
all_models_of_users = client.get_all_user_models()
dataset_details = client.get_particuler_dateset(dataset_id="data_set_id")
```