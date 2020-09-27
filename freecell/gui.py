import tkinter as tk
from pathlib import Path
from freecell.deck import Deck
from freecell.game import placeholder, blank_card

card_width = 49
card_height = 64
width_gap = 5
height_gap = 20
root = tk.Tk()
assets_path = Path(__file__).parent / ".." / "assets"
card_to_img = {
    card: tk.PhotoImage(file=assets_path / f"{card.symbol.name.lower()}_{card.value}.png")
    for card in Deck.create_full()
}
canvas = tk.Canvas(root,
    width=8 * (card_width + width_gap) + width_gap,
    height=16 * (height_gap) + 2 * card_height)
canvas.pack()

def refresh(game):
    canvas.delete("all")
    for i, card in zip(range(len(game.freecells)), game.freecells):
        canvas.create_image(i * (width_gap + card_width), 0, anchor=tk.NW, image=card_to_img[card])

    for i, card in zip(range(4, 8), game.foundations):
        if card is placeholder:
            continue
        canvas.create_image(2 * width_gap + i * (width_gap + card_width), 0, anchor=tk.NW, image=card_to_img[card])

    for i, column in enumerate(game.columns):
        for j, card in enumerate(column):
            if card in {placeholder, blank_card}:
                continue
            canvas.create_image(width_gap + i * (width_gap + card_width), card_height + (j + 1) * height_gap, anchor=tk.NW, image=card_to_img[card])


def main(game, debug=False):
    refresh(game)
    root.mainloop()
