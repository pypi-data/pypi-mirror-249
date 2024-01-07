import pytest

import haitch as H


def test_element():
    got = str(H.div(style_="color:red;")("Hello, world!"))
    want = '<div style="color:red;">Hello, world!</div>'
    assert got == want


def test_made_up_tag():
    got = str(H.foo())
    want = "<foo></foo>"
    assert got == want


def test_no_attrs():
    got = str(H.div("Hello, world!"))
    want = "<div>Hello, world!</div>"
    assert got == want


def test_strip_reserved_word_attr():
    got = str(H.button(class_="btn")("Click me!"))
    want = '<button class="btn">Click me!</button>'
    assert got == want


def test_boolean_attr():
    got = str(H.div(autofocus=True)("Hello, world!"))
    want = "<div autofocus>Hello, world!</div>"
    assert got == want


def test_self_closing():
    got = str(H.hr())
    want = "<hr/>"
    assert got == want


def test_false_attr_value_is_filtered_out():
    got = str(H.div(autofocus=False)("Hello, world!"))
    want = "<div>Hello, world!</div>"
    assert got == want


def test_escape_attr():
    got = str(H.div(class_="<br/>"))
    want = '<div class="&lt;br/&gt;"></div>'
    assert got == want


def test_escape_child():
    got = str(H.div("<br>"))
    want = "<div>&lt;br&gt;</div>"
    assert got == want


@pytest.mark.parametrize("value", [1, 1.0, ["1"], ("1",)])
def test_bad_attr_value(value):
    exc = f"Attribute value must be `str` or `bool`, not {type(value)}"
    with pytest.raises(ValueError, match=exc):
        str(H.div(id=value))


@pytest.mark.parametrize("child", [1, 1.0, ["1"], ("1",)])
def test_bad_child_value(child):
    exc = f"Child must be `str` or `Element`, not {type(child)}"
    with pytest.raises(ValueError, match=exc):
        str(H.div(child))


def test_nested_elements():
    dom = H.p(autofocus=True)(
        H.label(for_="num")("#"),
        H.input(type="text", id="num"),
    )

    got = str(dom)
    want = '<p autofocus><label for="num">#</label><input type="text" id="num"/></p>'

    assert got == want


def test_handle_nested_iterable():
    dom = H.ul()(
        *[H.li(str(n)) for n in range(3)],
    )

    got = str(dom)
    want = "<ul><li>0</li><li>1</li><li>2</li></ul>"

    assert got == want
