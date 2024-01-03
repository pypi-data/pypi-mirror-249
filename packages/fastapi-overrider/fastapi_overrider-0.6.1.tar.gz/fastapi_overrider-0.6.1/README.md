# fastapi-overrider

Easy and safe dependency overrides for your [FastAPI](https://fastapi.tiangolo.com/) tests. 

## Installation

`pip install fastapi-overrider`

## Motivation

FastAPI provided a nice mechanism to override dependencies, but there are a few gotchas:

- Overrides are not cleaned up automatically after a test run
- Using `unittest.mock.Mock` is non-trivial due to the way FastAPI relies on inspection
  of signatures when calling dependencies.
- Likewise, mocking async dependencies is cumbersome.

The goal of fastapi-override is to make dependency overriding easy, safe, reusable, composable,
and extendable.

## Usage

Use it as pytest fixture to ensure every test is run with a clean set of overrides:

```python
@pytest.fixture()
def override(app: FastAPI) -> Iterator[Overrider]:
    with Overrider(app) as override:
        yield override

def test_get_item_from_value(client: TestClient, override: Overrider) -> None:
    override_item = Item(item_id=0, name="Bar")
    override.value(lookup_item, override_item)

    response = client.get("/item/0").json()

    assert Item(**response) == override_item
```

Alternatively use it as a context manager:

```python
def test_get_item_context_manager(client: TestClient, app: FastAPI) -> None:
    with Overrider(app) as override:
        override_item = Item(item_id=0, name="Bar")
        override.value(lookup_item, override_item)

        response = client.get("/item/0").json()

        assert Item(**response) == override_item
```

In both cases the overrides will be cleaned up after the test.

The above examples also show how to override a dependency with just the desired return
value. Overrider will take care of creating a matching wrapper function and setting it
as an override.

It doesn't matter if your dependency is async or not. Overrider will do the right thing.

`override.value()` returns the override value:

```python
def test_get_item_return_value(client: TestClient, override: Overrider) -> None:
    item = override.value(lookup_item, Item(item_id=0, name="Bar"))

    response = client.get("/item/0").json()

    assert Item(**response) == item
```

`override.function()` accepts a callable:

```python
def test_get_item_function(client: TestClient, override: Overrider) -> None:
    item = Item(item_id=0, name="Bar")
    override.function(lookup_item, lambda item_id: item)  # noqa: ARG005

    response = client.get("/item/0").json()

    assert Item(**response) == item
```

Use it as a drop-in replacement for `app.dependency_overrides`:

```python
def test_get_item_drop_in(client: TestClient, override: Overrider) -> None:
    item = Item(item_id=0, name="Bar")
    def override_lookup_item(item_id: int) -> Item:  # noqa: ARG001
        return item
    override[lookup_item] = override_lookup_item

    response = client.get("/item/0").json()

    assert Item(**response) == item
```

Overrider can create mocks for you:

```python
def test_get_item_mock(client: TestClient, override: Overrider) -> None:
    item = Item(item_id=0, name="Bar")
    mock_lookup = override.mock(lookup_item)
    mock_lookup.return_value = item

    response = client.get("/item/0")

    mock_lookup.assert_called_once_with(item_id=0)
    assert Item(**response.json()) == item
```

Spy on a dependency. The original dependency will still be called, but you can call assertions
and inspect it like a `unittest.mock.Mock`:

```python
def test_get_item_spy(client: TestClient, override: Overrider) -> None:
    spy = override.spy(lookup_item)

    client.get("/item/0")

    spy.assert_called_with(item_id=0)
```

You can call Overrider directly and it will guess what you want to do:

If you pass in a callable, it will act like `override.function()`:

```python
def test_get_item_call_callable(client: TestClient, override: Overrider) -> None:
    item = Item(item_id=0, name="Bar")
    override(lookup_item, lambda item_id: item)  # noqa: ARG005

    response = client.get("/item/0").json()

    assert Item(**response) == item
```

If you pass in a non-callable, it will act like `override.value()`:

```python
def test_get_item_call_value(client: TestClient, override: Overrider) -> None:
    item = override(lookup_item, Item(item_id=0, name="Bar"))

    response = client.get("/item/0").json()

    assert Item(**response) == item
```

If you don't pass in anything, it will create a mock:

```python
def test_get_item_call_mock(client: TestClient, override: Overrider) -> None:
    item = Item(item_id=0, name="Bar")
    mock_lookup = override(lookup_item)
    mock_lookup.return_value = item

    response = client.get("/item/0")

    mock_lookup.assert_called_once_with(item_id=0)
    assert Item(**response.json()) == item
```

Reuse common overrides. They are composable, you can have multiple:

```python
@pytest.fixture()
def as_dave(app: FastAPI) -> Iterator[Overrider]:
    with Overrider(app) as override:
        mock_user = override(get_user)
        mock_user.return_value.name = "Dave"
        yield override

@pytest.fixture()
def in_the_morning(app: FastAPI) -> Iterator[Overrider]:
    with Overrider(app) as override:
        mock_time_of_day = override(get_time_of_day)
        mock_time_of_day.return_value = "morning"
        yield override

def test_get_greeting(client: TestClient, as_dave: Overrider, in_the_morning: Overrider) -> None:
    response = client.get("/")

    assert response.text == '"Good morning, Dave."'
```

Extend it with your own convenience methods:

```python
class MyOverrider(Overrider):
    def user(self, *, name: str, authenticated: bool = False) -> None:
        mock_user = self(get_user)
        mock_user.return_value.name = name
        mock_user.return_value.authenticated = authenticated

@pytest.fixture()
def override(app: FastAPI):
    with MyOverrider(app) as override:
        yield override

def test_open_pod_bay_doors(client: TestClient, my_override: MyOverrider) -> None:
    my_override.user(name="Dave", authenticated=False)

    response = client.get("/open/pod_bay_doors")

    assert response.text == "\"I'm afraid I can't let you do that, Dave.\""
```
