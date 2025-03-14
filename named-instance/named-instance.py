import marimo

__generated_with = "0.11.19"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    class InstanceNamer:
        def __init__(self):
            self._instances = {}
        def __call__(self, factory):
            def new_instance(name, *args, **kwargs):
                try:
                    return self._instances[name]
                except KeyError:
                    print(f'InstanceNamer: new instance `{name}`')
                    inst = factory(*args, **kwargs)
                    self._instances[name] = inst
                    return inst
            return new_instance

    named_instance = InstanceNamer()

    @named_instance
    class named_button(mo.ui.button):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._ctx = None
        @property
        def value(self):
            """The element's current value."""
            if self._ctx is None:
                return self._value
            return self._value

    @named_instance
    class named_refresh(mo.ui.refresh):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._ctx = None
        @property
        def value(self):
            """The element's current value."""
            if self._ctx is None:
                return self._value
            return self._value

    @named_instance
    class Incrementer:
        def __init__(self):
            self._val = 0
        def up(self):
            self._val += 1
            return self._val
    return (
        Incrementer,
        InstanceNamer,
        named_button,
        named_instance,
        named_refresh,
    )


@app.cell
def _(Incrementer, mo, named_button):
    state1 = Incrementer('state1')

    button = named_button('button')

    ([
        mo.md('`button` still does not update this cell.'),
        button,
        mo.md(f'state1.up() returns {state1.up()}'),
    ])
    return button, state1


@app.cell
def _(Incrementer, button, mo, named_refresh, state1):
    state2 = Incrementer('state2')

    refresh = named_refresh('refresh', label='refresh')
    mo.vstack([
        mo.md('and refreshing from this cell does nothing,'),
        mo.md('but state2 is no longer recreated.'),
        refresh,
        button,
        mo.md(f'state1.up() returns {state1.up()}'),
        mo.md(f'state2.up() returns {state2.up()}'),
    ])
    return refresh, state2


@app.cell
def _(button, mo, refresh, state1, state2):
    mo.vstack([
        mo.md('state1 still refers to the original variable,'),
        mo.md('and state2 is still not recreated.'),
        refresh,
        button,
        mo.md(f'state1.up() returns {state1.up()}'),
        mo.md(f'state2.up() returns {state2.up()}'),
    ])
    return


@app.cell
def _(mo, state1, state2):
    mo.vstack([
        mo.md('stat1 and state2 are updated as original'),
        mo.md(f'state1.up() returns {state1.up()}'),
        mo.md(f'state2.up() returns {state2.up()}'),
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
