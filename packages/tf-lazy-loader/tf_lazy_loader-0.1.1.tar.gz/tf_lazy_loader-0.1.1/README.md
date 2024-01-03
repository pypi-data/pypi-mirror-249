# tf-lazy-loader


## Installation

```bash
pip install tf-lazy-loader
```

## Usage

```python
from tf_lazy_loader import dynamic_import

# Lazily import the "os" module
os = dynamic_import("os")

# Trigger the actual import by referencing a name in the "os" module:
print(os.environ)
```

### Conditionally switching between lazy and eager imports

You can set the `lazy` arg of the `dynamic_import` function to `False` to eagerly import the given module. This can be useful if you only want to perform lazy imports based on a flag.

For example, if you have a Django project and you only want to enable lazy imports when in DEBUG mode, and do imports eagerly in production, you would do something like this:

```python
from django.conf import settings

DEBUG = settings.DEBUG

os = dynamic_import("os", lazy=DEBUG)
```
