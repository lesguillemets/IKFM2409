#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
from datetime import datetime
from pathlib import Path

EMOTIONS = ["anger_cl", "excite", "happy", "relax", "sad"]
def plot(dat_dir: Path = Path('./dat')):
    dat_files = list(filter(lambda f: f.is_file(),
                            dat_dir.glob('*.tsv')))
    datasets = list(map(lambda f: pd.read_csv(f, delimiter='\t'), dat_files))
    print(f"processing {dat_files} with {sum((d.shape[0] for d in datasets))} trials total")
    for (i,dat) in enumerate(datasets):
            dat['emot_str'] = dat['emotion'].map(emot_index_to_name)
            dat['setnum'] = i
            dat['valence'] = dat['x']
            dat['arousal'] = dat['y']
    dat_all = data = pd.concat(datasets, ignore_index=True)
    plot_everything(dat_all)


def plot_everything(df: pd.DataFrame):
    # colors = plt.cm.tab10(range(len(va.columns)))
    fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(24,24))
    for (emot, ax) in zip(EMOTIONS, axes.ravel()):
        em_dat = (df[df['emot_str'] == emot])
        # print(type(em_dat)) --> dataframe
        em_dat.plot(
                ax=ax, kind="scatter", x ="valence", y="arousal",
                figsize=(10,10),
                title=f"{emot}",
                label=f"{emot}",
                alpha=0.1,
                s=200
                )
        ax.set_aspect('equal')
        ax.axis([-4.5,4.5,-4.5,4.5])
        ax.axhline(color='grey', lw=0.2)
        ax.axvline(color='grey', lw=0.2)
        # ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=1, fontsize=18)
    axes[-1,-1].axis('off')
    plt.show()
    fig.savefig(f'plot_{format_datetime(datetime.now())}.png',  bbox_inches='tight')


def format_datetime(d:datetime) -> str:
    return f"{d.year}-{d.month:02}-{d.day:02}-{d.hour:02}{d.minute:02}{d.second:02}"

def emot_index_to_name(i: int) -> str:
    try:
        return EMOTIONS[i]
    except IndexError as e:
        print(i, e, file=sys.stderr)
        return "UnExpectedEmotion"


def main():
    try:
        d_name = Path(sys.argv[1])
    except IndexError as e:
        d_name = Path("./dat")
    plot(d_name)

if __name__ == "__main__":
    main()
