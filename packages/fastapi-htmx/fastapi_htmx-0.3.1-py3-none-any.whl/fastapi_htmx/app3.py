from fastapi_htmx.my_decorator import htmx, htmx_init

# htmx.init(shared=2)
htmx_init(shared=2)


@htmx.template(mandatory_arg=10, optional_arg="Hello")
def my_function():
    print("Function is executing.")


my_function()


@htmx.template(mandatory_arg=20)
def my_function2():
    print("Function is executing.")


my_function2()


@htmx(mandatory_arg=20)
def my_function3():
    print("Function is executing.")


my_function3()


@htmx.component(some_arg=100)
def my_function4():
    print("Function is executing.")


my_function4()
