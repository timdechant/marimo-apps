import marimo

__generated_with = "0.11.13"
app = marimo.App(
    width="medium",
    layout_file="layouts/monty_hall_sim.slides.json",
)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(f"""
    # Monty Hall

    ## In probability, "Monty Hall" is a toy problem that illustrates the (sometimes counter-intuitive) power of Bayesian reasoning.

    ## This is based on a game from the show "Let's Make a Deal", hosted and produced by Monty Hall.

    """)
    return


@app.cell
def _(mo):
    mo.md(f"""
    # Game Rules

    ## Monty Hall's show had the following rules for this game:

    1. Three doors are presented:
        - one leads to a cash prize
        - ...but the others hold bogus items: whammy!
    2. The contestant chooses one door.
    3. Another door is opened, always revealing one of the whammy prizes.
    4. Now the contestant is given the option to switch to the remaining door.
    5. The prize is revealed.

    """)
    return


@app.cell
def _(mo):
    class Icons:
        door = mo.icon('game-icons:wooden-door', size='100%', color='#777777')
        selected = mo.icon('game-icons:wooden-door', size='100%', color='#777777', style={'background-color':"#50C878"})
        whammy = mo.icon('game-icons:goat', size='60%', color='brown')
        prize = mo.icon('game-icons:cash', size='60%', color='gold')
        winner = mo.icon('game-icons:cash', size='60%', color='gold', style={'background-color':"#50C878"})
        # loser = mo.icon('game-icons:goat', size='60%', color='brown', style={'background-color':"red"})
        loser = mo.icon('game-icons:wooden-door', size='100%', color='#777777', style={'background-color':"red"})

        @classmethod
        def to_dict(cls):
            return { key:val for key,val in cls.__dict__.items() if isinstance(val,type(cls.door)) }

        @classmethod
        def legend(cls):
            md = mo.hstack(
                [mo.vstack(item) for item in cls.to_dict().items()],
                justify='center',
                align='center',
            )
            return md

        @classmethod
        def test(cls):
            return # self.legend() # uncomment for visible output

    mo.vstack([
        mo.md("# Game Icons"),
        Icons.legend(),
    ])

    return (Icons,)


@app.cell
def _(Icons, mo):
    import random
    class Game(object):
        def __init__(self, change=False):
            self._change = change
            self._attempts = 0
            self._wins = 0
            self._next_step = self.start

        def choose(self, choices):
            idx = random.choice(choices)
            return idx,list(i for i in choices if i != idx)

        def start(self):
            # print('start')
            self._prize,self._whammies = self.choose(range(3))
            self._icons = [Icons.door]*3
            self._selected = None
            self._revealed = None
            self._next_step = self.step1

        def step1(self):
            # print('step1')
            self._selected,_ = self.choose(range(3))
            self._icons[self._selected] = Icons.selected
            self._next_step = self.step2

        def step2(self):
            # print('step2')
            whammy_doors = [door for door in range(3) if door not in (self._prize,self._selected)]
            self._revealed = random.choice(whammy_doors)
            self._icons[self._revealed] = Icons.whammy
            self._next_step = self.step3

        def step3(self):
            if not self._change:
                return self.step4()
            # print('step3')

            remaining_doors = [door for door in range(3) if door not in (self._selected,self._revealed)]
            assert(len(remaining_doors)==1)

            self._icons[self._selected] = Icons.door
            self._selected = remaining_doors[0]
            self._icons[self._selected] = Icons.selected
            self._next_step = self.step4

        def step4(self):
            # print('step4')
            self._icons[self._prize] = Icons.prize
            if self._selected == self._prize:
                self._icons[self._prize] = Icons.winner
                self._wins += 1
            else:
                self._icons[self._prize] = Icons.prize
                self._icons[self._selected] = Icons.loser
            self._attempts += 1
            self._next_step = self.start

        def step(self):
            self._next_step()
            return self.md

        @property
        def md(self):
            return mo.vstack([
                mo.center(
                    mo.md(f'## Experiment results: {100*self._wins//self._attempts}% success' if self._attempts else '')
                ),
                mo.hstack([]),
                mo.hstack(self._icons, justify='center', align='center'),
            ])

    game1 = Game()
    step1 = mo.ui.refresh(label='Step:', options=[5,1], default_interval=1)

    game2 = Game(change=True)
    step2 = mo.ui.refresh(label='Step:', options=[5,1], default_interval=1)

    return Game, game1, game2, random, step1, step2


@app.cell
def _(game1, mo, step1):
    mo.vstack([
        step1,
        mo.md('# Policy: Commit to initial choice.'),
        game1.step()
    ])
    return


@app.cell
def _(game2, mo, step2):
    mo.vstack([
        step2,
        mo.md('# Policy: Always change choice.'),
        game2.step()
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
