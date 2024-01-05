"""Extension for FastAPI to make HTMX easier to use."""
import inspect
import logging
from collections.abc import Callable, Mapping
from functools import wraps
from typing import Optional

from fastapi import Request
from fastapi.templating import Jinja2Templates


class MissingFullPageTemplateError(Exception):
    """Fullpage request not a corresponding template configured for url rewriting and history to work."""

    pass


class MissingHTMXInitError(Exception):
    """FastAPI-HTMX was not initialized."""

    pass


class HXRequest(Request):
    """FastAPI Request Object with HTMX additions."""

    hx_request: bool = False


class htmx:  # noqa: D101, N801
    templates: Optional[Jinja2Templates] = None

    def __init__(
        self,
        partial_template_name: str,
        full_template_name: Optional[str] = None,
        partial_template_constructor: Optional[Callable] = None,
        full_template_constructor: Optional[Callable] = None,
        template_extension: str = "jinja2",
    ):
        """Decorator for FastAPI routes to make HTMX easier to use.

        Args:
            partial_template_name (str): A Template for the partial to use.
            full_template_name (Optional[str], optional): The full page template name. Defaults to None.
            partial_template_constructor (Optional[Callable], optional): A Callable returning the needed variables for the
                                                                      template. Defaults to None.
            full_template_constructor (Optional[Callable], optional): A Callable returning the needed variables for the
                                                                   template. Defaults to None.
            template_extension (str, optional): The template extension to use. Defaults to "jinja2".

        Raises:
            MissingFullPageTemplateError: If a full page is required bu no template is specified.
            MissingHTMXInitError: FastAPI-HTMX needs to be initialized for templates to work.

        Returns:
            Callable: The decorated function.
        """  # noqa: D401
        self.partial_template_name = partial_template_name
        self.full_template_name = full_template_name
        self.partial_template_constructor = partial_template_constructor
        self.full_template_constructor = full_template_constructor
        self.template_extension = template_extension

    def __call__(self, func):  # noqa: C901, D102
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs) -> Callable:  # noqa: C901
            request_is_fullpage_request = _is_fullpage_request(request=request)
            # hint: use `HXRequest` instead of `Request` for typing when using `request.hx_request`
            request.hx_request = not request_is_fullpage_request  # type: ignore

            # convenient history support if kwargs match in the endpoint and constructor
            if request_is_fullpage_request and self.full_template_constructor is not None:
                if inspect.iscoroutinefunction(self.full_template_constructor):
                    response = await self.full_template_constructor(**kwargs)
                else:
                    response = self.full_template_constructor(**kwargs)
            elif not request_is_fullpage_request and self.partial_template_constructor is not None:
                if inspect.iscoroutinefunction(self.partial_template_constructor):
                    response = await self.partial_template_constructor(**kwargs)
                else:
                    response = self.partial_template_constructor(**kwargs)
            else:
                if inspect.iscoroutinefunction(func):
                    response = await func(*args, request=request, **kwargs)
                else:
                    response = func(*args, request=request, **kwargs)

            # in case no constructor function or return dict was supplied, assume a template not needing variables
            if response is None:
                logging.debug("No data provided for endpoint, providing an empty dict.")
                response = {}

            # in case of RedirectResponse or similar
            if not isinstance(response, Mapping):
                return response

            template_name = self.partial_template_name
            if request_is_fullpage_request:
                if self.full_template_name is None:
                    raise MissingFullPageTemplateError()
                template_name = self.full_template_name

            if htmx.templates is None:
                raise MissingHTMXInitError(
                    "FASTAPI-HTMX was not initialized properly. "
                    "Please call 'htmx.init(templates=Jinja2Templates(directory=Path('templates')))' in your app "
                    "before using the '@htmx(...)' decorator"
                )

            return htmx.templates.TemplateResponse(
                f"{template_name}.{self.template_extension}",
                {
                    "request": request,
                    **response,
                },
            )

        return wrapper

    @staticmethod
    def init(templates: Jinja2Templates):
        """Initialize the HTMX extension.

        Args:
            templates (Jinja2Templates): The configured template instance to use.
        """
        htmx.templates = templates


def _is_fullpage_request(request: Request) -> bool:
    return "HX-Request" not in request.headers or request.headers["HX-Request"].lower() != "true"


def htmx_init(templates: Jinja2Templates):  # noqa: D103
    logging.warning("DEPRECATED: htmx_init(...) is deprecated, use 'htmx.init(...)' instead.")
    htmx.init(templates=templates)
