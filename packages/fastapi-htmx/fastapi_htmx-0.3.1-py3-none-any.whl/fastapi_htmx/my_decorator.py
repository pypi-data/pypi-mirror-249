class htmx:  # noqa: N801, D101
    shared_value = None  # Class variable to store the shared value

    def __init__(self, mandatory_arg=None, optional_arg=None):
        # Set default values for the arguments if not provided
        self.mandatory_arg = mandatory_arg if mandatory_arg is not None else 0
        self.optional_arg = optional_arg

    @staticmethod
    def init(shared: int):
        htmx.shared_value = shared

    def __call__(self, func):  # to enable backwards compatible class
        # print("deprecated, use 'htmx.template(...) now.")  # FIXME: is always called
        def wrapper(*args, **kwargs):
            print(f"Shared value: {htmx.shared_value * self.mandatory_arg}")
            print(f"Optional argument: {self.optional_arg}")
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def template(mandatory_arg, optional_arg=None):  # actually a factory
        return htmx(mandatory_arg, optional_arg)

    @staticmethod
    def component(some_arg):  # actually a factory
        return htmx(some_arg)


def htmx_init(shared: int):
    print("deprecated, use 'htmx.init(shared=2)' now.")
    htmx.init(shared=shared)
