import html


def html_p(s: str) -> str:
    new_s = '<p>{}<p>'.format(s)
    return new_s


def html_b(s: str) -> str:
    new_s = '<b>{}<b>'.format(s)
    return new_s


def html_i(s: str) -> str:
    new_s = '<i>{}<i>'.format(s)
    return new_s


def html_u(s: str) -> str:
    new_s = '<u>{}<u>'.format(s)
    return new_s


def writer(teg_arg):
    def writer_decoration(func):
        def wrapped(data):
            for teg in teg_arg:
                data = globals()['html_' + teg](data) if 'html_' + teg in globals() else data
            return func(data)

        return wrapped

    return writer_decoration


@writer('bpx')
def html_printer(s: str) -> str:
    return html.escape(s)


print(html_printer("I'll give you +++ cash for this -> stuff."))


@writer('')
def html_printer(s: str) -> str:
    return html.escape(s)


print(html_printer("I'll give you +++ cash for this -> stuff."))
