import marimo

__generated_with = "0.11.19"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    class Incrementer:
        def __init__(self):
            self._val = 0
        def up(self):
            self._val += 1
            return self._val
    return (Incrementer,)


@app.cell
def _(Incrementer, mo):
    state1 = Incrementer()

    button = mo.ui.button(label='button')

    mo.vstack([
        mo.md('`button` does not update this cell, perhaps because of the below duplication issue.'),
        mo.md('pressing button for this cell, however, does update other cells... confusing!'),
        button,
        mo.md(f'state1.up() returns {state1.up()}'),
    ])
    return button, state1


@app.cell
def _(Incrementer, button, mo, state1):
    state2 = Incrementer()

    refresh = mo.ui.refresh()
    mo.vstack([
        mo.md('refreshing from this cell does nothing,'),
        mo.md('and state2 is recreated just like state1 was previously.'),
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
        mo.md('but the button creates yet another instance of state2'),
        refresh,
        button,
        mo.md(f'state1.up() returns {state1.up()}'),
        mo.md(f'state2.up() returns {state2.up()}'),
    ])
    return


@app.cell
def _(mo, state1, state2):
    mo.vstack([
        mo.md('with no controls, the original state1 is used,'),
        mo.md('and state2 is reused from the previous cell'),
        mo.md(f'state1.up() returns {state1.up()}'),
        mo.md(f'state2.up() returns {state2.up()}'),
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
