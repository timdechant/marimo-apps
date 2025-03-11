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
        loser = mo.icon('game-icons:goat', size='60%', color='brown', style={'background-color':"#ff6347"})
        # loser = mo.icon('game-icons:wooden-door', size='100%', color='#777777', style={'background-color':"#ff6347"})

        @classmethod
        def to_dict(cls):
            return { key:val for key,val in cls.__dict__.items() if isinstance(val,type(cls.door)) }

        @classmethod
        def legend(cls):
            return mo.hstack(map(mo.vstack, cls.to_dict().items()), justify='center', align='center')

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
        def __init__(self, count=3, change=False):
            """
            Remember game parameters, initialize historical results,
            and set things in motion.
            """
            self._count = count
            self._change = change
            self._attempts = 0
            self._wins = 0
            self._next_step = self.start

        def start(self):
            """
            Set up the game board: show the doors and choose
            which holds the prize (without revealing anything.)
            """
            self._prize = random.randrange(self._count)
            self._icons = [Icons.door]*self._count
            self._next_step = self.step1

        def step1(self):
            """
            Simulated user randomly selects a door,
            independent of which holds the prize.
            """
            self._selected = random.randrange(self._count)
            self._icons[self._selected] = Icons.selected
            self._next_step = self.step2

        def step2(self):
            """
            Reveal all but one of the bogus prizes.
            """
            occupied = (self._prize, self._selected)
            reveal_options = [door for door in range(self._count) if door not in occupied]
            self._revealed = random.sample(reveal_options, self._count-2)
            for door in self._revealed:
                self._icons[door] = Icons.whammy
            self._next_step = self.step3

        def step3(self):
            """
            Optionally, change user selection to the remaining door.
            """
            if not self._change:
                return self.step4()

            occupied = list(self._revealed) + [self._selected]
            remaining_doors = [door for door in range(self._count) if door not in occupied]
            assert(len(remaining_doors)==1)

            self._icons[self._selected] = Icons.door
            self._selected = remaining_doors[0]
            self._icons[self._selected] = Icons.selected
            self._next_step = self.step4

        def step4(self):
            """
            Reveal the selection, hightlighting win/loss.
            """
            self._icons[self._selected] = Icons.winner if self._selected == self._prize else Icons.loser
            self._next_step = self.step5

        def step5(self):
            """
            Update the historical results.
            """
            if self._selected == self._prize:
                self._wins += 1
            self._attempts += 1
            self._next_step = self.start

        def step(self):
            self._next_step()
            return self.md

        @property
        def md(self):
            """
            Render the game board to markdown.
            """
            vstack = []
            if self._attempts > 1:
                success = 100*self._wins//self._attempts
                vstack = [mo.center(mo.md(f'## After {self._attempts} games: {success}% success'))]
            vstack.append(mo.hstack(self._icons, justify='center', align='center'))
            return mo.vstack(vstack)

    game1 = Game()
    step1 = mo.ui.refresh(label='Step:', options=[5,1], default_interval=1)

    game2 = Game(change=True)
    step2 = mo.ui.refresh(label='Step:', options=[5,1], default_interval=1)

    game3 = Game(change=True, count=6)
    step3 = mo.ui.refresh(label='Step:', options=[5,1], default_interval=1)

    return Game, game1, game2, game3, random, step1, step2, step3


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
def _(mo):
    mo.md(f"""
    # What is going on?

    ## Allow the games to run for at least 10~25 iterations; what is happening?

    ## Most people find the results surprising, or even upsetting. In fact, the dramatic history surrounding this simple puzzle is fascinating.

    ## This may tell us more about human psychology and decision making, but how do we get a handle on the probability?

    ## One way to stretch our understanding is to increase the size of the board: what if we have more doors, and still reveal all but one of the bogus prizes?

    """)
    return


@app.cell
def _(game3, mo, step3):
    mo.vstack([
        step3,
        mo.md('# More doors: Always change choice.'),
        game3.step(),
        mo.md('## Now it becomes clearer: when the selection is always changed, the contestant only loses if the intial guess was correct.  So the probability flips from $(1/N)$ to $(1 - 1/N)$!'),
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
