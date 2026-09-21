"""Compare palettes using identical computed cells and identical vector geometry.

Outputs previews only; never overwrites published artwork or numerical arrays.
"""
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle
from generate_hybrid_art import draw_hybrid
import voronoi_coherence.plotting as voronoi

PALETTES = [
    ('A', 'Teal & copper', '#18766b', '#b6633c', '#faf8f1', '#203738'),
    ('B', 'Forest & slate blue', '#246b55', '#366c99', '#f3f7f6', '#20323b'),
    ('C', 'Sea green & ochre', '#20796f', '#ad7c1e', '#faf8ee', '#30392f'),
]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(); args.output.mkdir(parents=True,exist_ok=True)
    with np.load(args.data/'trajectories.npz',allow_pickle=False) as data:
        tracks=data['tracks']; times=data['times']
    with np.load(args.data/'coherence.npz',allow_pickle=False) as data:
        chi=data['chi']
    for key,name,green,accent,paper,ink in PALETTES:
        # Same χ values, trajectories, cells, and scale in each option.
        voronoi.CMAP=LinearSegmentedColormap.from_list(name,[accent,paper,green])
        voronoi.INK=ink; voronoi.PAPER=paper
        fig=plt.figure(figsize=(12,6.3),facecolor=paper)
        fig.text(.045,.90,f'{key}  /  {name}',color=ink,size=28,weight='medium')
        left=fig.add_axes([.035,.25,.45,.56],facecolor=paper)
        voronoi._field(left,tracks,len(times)-1,chi,(0,2,0,1),arrows=False)
        left.axis('off')
        right=fig.add_axes([.51,.25,.46,.56],facecolor=paper)
        draw_hybrid(right,green,accent,paper,ink,labels=False)
        fig.text(.26,.24,'Voronoi coherence',ha='center',size=18,color=ink)
        fig.text(.74,.24,'Grid–particle coupling',ha='center',size=18,color=ink)
        for x,colour in zip([.05,.36,.67],[green,accent,paper]):
            fig.add_artist(Rectangle((x,.07),.06,.07,transform=fig.transFigure,
                                     facecolor=colour,edgecolor=ink,lw=.5))
            fig.text(x+.075,.09,colour.upper(),size=16,color=ink)
        for suffix in ['svg','png']:
            fig.savefig(args.output/f'palette-{key.lower()}.{suffix}',dpi=130,
                        metadata={'Date':None} if suffix=='svg' else None)
        plt.close(fig)
    print(f'Palette previews: {args.output}')


if __name__=='__main__':
    main()
