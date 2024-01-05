from starlette.templating import Jinja2Templates

# Usage in user code
from fastapi_htmx.htmx2 import HTMXExtension

# Initialization with templates
HTMXExtension.init(Jinja2Templates(directory="path/to/templates"))


# Decorator usage remains the same
@HTMXExtension.htmx(partial_template_name="partial_template", full_template_name="full_template")
async def some_route():  # noqa: D103
    # ... route logic here ...
    pass
