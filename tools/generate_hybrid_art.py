"""Conceptual grid/particle coupling diagram, not a numerical flow solution."""
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.colors import to_rgb
from generate_research_art import canvas, save, INK, TEAL, PAPER


def tint(colour, background, fraction):
    return tuple((1-fraction)*np.array(to_rgb(background))+fraction*np.array(to_rgb(colour)))


def draw_hybrid(ax, green=TEAL, accent='#596975', paper=PAPER, ink=INK, labels=True):
    ax.set(xlim=(0,10), ylim=(0,5.4), aspect='equal')
    ax.axis('off')
    ax.add_patch(Rectangle((.6,1),4,3,facecolor=tint(green,paper,.07),edgecolor=tint(green,paper,.4),lw=1.3))
    # The Eulerian mesh surrounds the obstacle; no mesh cells cut through it.
    for x in np.linspace(.6,4.6,13):
        segments=[(1,2),(3,4)] if 1.65 < x < 2.65 else [(1,4)]
        for lo,hi in segments: ax.plot([x,x],[lo,hi],color=tint(green,paper,.56),lw=1)
    for y in np.linspace(1,4,10):
        segments=[(.6,1.65),(2.65,4.6)] if 2 < y < 3 else [(.6,4.6)]
        for lo,hi in segments: ax.plot([lo,hi],[y,y],color=tint(green,paper,.56),lw=1)
    ax.add_patch(Rectangle((1.65,2),1,1,facecolor=ink,edgecolor=ink,lw=1.4,zorder=6))
    for y in [1.65,3.35]:
        x=np.linspace(.8,4.1,100)
        yy=y+np.sign(y-2.5)*.25*np.exp(-((x-2.15)/.7)**2)
        ax.plot(x,yy,color=green,lw=1.8)
    # Alternating rolled-up particle groups illustrate a convected wake.
    for i,(cx,cy,r) in enumerate([(4.5,2.1,.23),(5.35,2.9,.28),(6.2,2.1,.33),
                                  (7.1,2.9,.38),(8.05,2.1,.43),(9.05,2.9,.48)]):
        colour=green if i%2 else accent
        t=np.linspace(0,3.0*np.pi,26)
        radius=np.linspace(.035,r,len(t)); sign=-1 if i%2 else 1
        xx=cx+radius*np.cos(t)
        yy=cy+sign*radius*np.sin(t)
        ax.plot(xx,yy,color=colour,lw=1.1,alpha=.65)
        ax.scatter(xx,yy,s=30+i*1.5,color=colour,linewidths=0,zorder=5)
    ax.annotate('',xy=(5.45,4.5),xytext=(3.5,4.5),
                arrowprops=dict(arrowstyle='<->',color=ink,lw=2.4,mutation_scale=23))
    if labels:
        ax.text(4.5,4.92,'Two-way exchange',ha='center',size=24,color=ink)
        ax.text(2.55,.38,'Near-body grid',ha='center',size=24,color=green)
        ax.text(7.5,.38,'Vortex particles',ha='center',size=24,color=accent)


if __name__=='__main__':
    fig,ax=canvas()
    draw_hybrid(ax)
    save(fig,'hybrid-vortex-grid')
