# pyfoggl
python developer client for foggl
# Foggl Python Client

The Foggl Python Client is a lightweight package that interacts with the Foggl feature toggling tool's API, allowing users to retrieve feature states and values dynamically.

## Installation

You can install the Foggl Python Client using pip:

```bash
pip install pyfoggl
```

## Usage

### Fetching Feature State and Value

The Foggl Python Client provides convenience functions to fetch feature states and values directly without explicit object instantiation.

- **Fetching Feature State:**

  ```python
  from pyfoggl import foggl_state

  auth_token = 'your-auth-token'
  foggl_name = 'your-feature-name'

  your_feature_state = foggl_state(auth_token, foggl_name)
  
  if your_feature_state:
    do_something()
  else:
    do_something_else()

  ```

- **Fetching Feature Value:**

  ```python
  from pyfoggl import foggl_value

  auth_token = 'your-auth-token'
  foggl_name = 'your-feature-name'

  your_feature_value = foggl_value(auth_token, foggl_name)
  
  do_something(foggl_value)

  ```
