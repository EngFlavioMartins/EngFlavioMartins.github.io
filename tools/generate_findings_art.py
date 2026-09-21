"""Original qualitative study illustrations; no plotted values are paper data."""
import numpy as np
from matplotlib.patches import Circle, Polygon, Rectangle
from generate_research_art import canvas, save, arrow, INK, TEAL, PURPLE, PAPER, GOLD


def curl(ax, centre, radius, colour, sign=1):
    t = np.linspace(0, 2.9*np.pi, 150)
    r = np.linspace(.04, radius, len(t))
    x, y = centre[0]+r*np.cos(t), centre[1]+sign*r*np.sin(t)
    ax.plot(x, y, color=colour, lw=2)
    arrow(ax, (x[-8], y[-8]), (x[-1], y[-1]), colour, lw=1.6, scale=15)


def regenerative():
    fig, ax = canvas()
    for x, count in [(1.7, 1), (5, 2), (8.3, 4)]:
        ax.add_patch(Rectangle((x-1, .8), 2, 2, facecolor='#e5e1ee', edgecolor=PURPLE, lw=1.6))
        heights = {1: [2.8], 2: [2.8, 1.8], 4: [2.8, 2.3, 1.8, 1.3]}[count]
        for z in heights:
            ax.plot([x-1, x+1], [z, z], lw=4, color=TEAL, solid_capstyle='round')
            # Opposite circulations induce upward velocity between the tips.
            curl(ax, (x-.91, z+.25), .27, TEAL, 1)
            curl(ax, (x+.91, z+.25), .27, TEAL, -1)
        arrow(ax, (x, 3.0), (x, 3.85), TEAL, scale=25)
        ax.text(x, .22, f'{count} wing' + ('s' if count > 1 else ''), size=24, ha='center')
    ax.text(5, 4.2, 'Upward wake transport', color=TEAL, size=25, ha='center')
    save(fig, 'regenerative-wakes')


def validation():
    fig, ax = canvas()
    # An analytical silhouette explains the comparison, not its measured agreement.
    y, z = np.meshgrid(np.linspace(-1.4, 1.4, 90), np.linspace(0, 3, 90))
    deficit = np.exp(-(y/.77)**4-((z-1.3)/1.1)**4)
    for offset, sampled in [(2.25, False), (7.75, True)]:
        ax.add_patch(Rectangle((offset-1.65, .6), 3.3, 3.3, facecolor='#e9efed', edgecolor='#bdcecb', lw=1))
        if not sampled:
            ax.contourf(offset+y, .7+z, deficit, levels=[.15,.4,.7,1.1], colors=['#d4e2df','#a4c7c1','#5b9d94'])
            for t in np.linspace(-1.35, 1.35, 10):
                ax.plot([offset+t]*2, [.7,3.65], color=PAPER, alpha=.55, lw=.7)
            for t in np.linspace(.7,3.65,10):
                ax.plot([offset-1.35,offset+1.35], [t]*2, color=PAPER, alpha=.55, lw=.7)
        else:
            yy, zz = np.meshgrid(np.linspace(-1.3,1.3,13),np.linspace(.1,2.85,14))
            q = np.exp(-(yy/.77)**4-((zz-1.3)/1.1)**4)
            ax.scatter(offset+yy,.7+zz,s=19,c=q,cmap='PuBuGn',vmin=0,vmax=1,linewidths=0)
        for height in [1.2,2.35]:
            ax.plot([offset-.85, offset+.85], [height]*2, color=PURPLE, lw=3)
        ax.text(offset, .12, 'Wind tunnel' if sampled else 'CFD', size=25,ha='center')
    ax.annotate('',xy=(5.45,2.2),xytext=(4.55,2.2),
                arrowprops=dict(arrowstyle='<->',lw=2,color=INK,mutation_scale=20))
    save(fig, 'wake-validation')


def momentum():
    fig, ax = canvas()
    ax.add_patch(Rectangle((.35,.55),9.3,1.7,facecolor='#e2ebe6',edgecolor='none'))
    ax.plot([.35,9.65],[.55]*2,color='#8d9f91',lw=2)
    for x in [1.5,3.7,5.9,8.1]:
        ax.plot([x,x],[.55,1.8],color=INK,lw=2.4)
        ax.plot([x,x],[1.1,2.1],color=PURPLE,lw=4)
        ax.fill([x,x+1.5,x+1.5,x],[1.1,.95,2.25,2.1],color=PURPLE,alpha=.10)
    for z in [3.1,3.55]:
        arrow(ax,(.5,z),(9.5,z),TEAL,scale=22)
    for x in [2.4,4.6,6.8]:
        ax.annotate('',xy=(x+.45,1.75),xytext=(x-.45,3.15),
                    arrowprops=dict(arrowstyle='-|>',connectionstyle='arc3,rad=-.3',color=TEAL,lw=2.7,mutation_scale=24))
    ax.text(5,4.05,'Momentum from above',ha='center',size=25,color=TEAL)
    ax.text(5,.0,'Wind-farm layer',ha='center',size=24)
    save(fig,'vertical-momentum')


def cylinder():
    fig, ax = canvas()
    for y in [1.6,2.9]:
        ax.add_patch(Circle((2.1,y),.62,fill=False,edgecolor='#bdc9c8',lw=1.5,ls=(0,(3,4))))
    ax.add_patch(Circle((2.1,2.25),.62,facecolor='#dce9e6',edgecolor=TEAL,lw=2.4))
    ax.annotate('',xy=(.9,3.35),xytext=(.9,1.15),arrowprops=dict(arrowstyle='<->',lw=2.5,color=TEAL,mutation_scale=23))
    for i,x in enumerate([3.7,4.8,5.9,7,8.1,9.2]):
        curl(ax,(x,2.25+(.6 if i%2 else -.6)),.48,TEAL if i%2 else PURPLE,-1 if i%2 else 1)
    arrow(ax,(3.25,3.9),(9.45,3.9),INK)
    ax.text(2.0,.35,'Motion',size=24,ha='center',color=TEAL)
    ax.text(6.5,.35,'Alternating wake',size=24,ha='center')
    save(fig,'cylinder-wake')


def sizing():
    fig, ax = canvas()
    # A simply-supported, statically determinate triangular truss. Axial forces
    # set illustrative section widths, not the published optimisation result.
    points=np.array([[0,0],[1,0],[2,0],[3,0],[4,0],[.5,1],[1.5,1],[2.5,1],[3.5,1]])
    edges=[(i,i+1) for i in range(4)]+[(i,i+1) for i in range(5,8)]
    edges += [(i,i+5) for i in range(4)]+[(i+1,i+5) for i in range(4)]
    k=np.zeros((18,18)); f=np.zeros(18); f[[11,13,15,17]]=-1
    for i,j in edges:
        d=points[j]-points[i]; length=np.linalg.norm(d); b=np.r_[-d/length,d/length]; ids=[2*i,2*i+1,2*j,2*j+1]
        k[np.ix_(ids,ids)]+=np.outer(b,b)/length
    free=np.setdiff1d(np.arange(18),[0,1,9]); u=np.zeros(18)
    u[free]=np.linalg.solve(k[np.ix_(free,free)],f[free])
    assert np.max(np.abs((k@u-f)[free]))<1e-10
    forces=[]
    for i,j in edges:
        d=points[j]-points[i]; forces.append((u[2*j:2*j+2]-u[2*i:2*i+2])@d/(d@d))
    for offset,sized in [(0.35,False),(5.65,True)]:
        p=points*[1,1.55]+[offset,1.25]
        for (i,j),n in zip(edges,forces):
            ax.plot(p[[i,j],0],p[[i,j],1],color=TEAL if n>0 else PURPLE,
                    lw=(1+4*abs(n)/max(np.abs(forces))) if sized else 4,solid_capstyle='round')
        ax.scatter(p[:,0],p[:,1],s=25,facecolor=PAPER,edgecolor=INK,zorder=5)
        for i in [5,6,7,8]: arrow(ax,p[i]+[0,.75],p[i]+[0,.06],GOLD,scale=17)
        for i in [0,4]:
            x,z=p[i]; ax.add_patch(Polygon([[x,z],[x-.16,z-.3],[x+.16,z-.3]],facecolor='#b4c4bf',edgecolor=INK))
            if i == 4:
                for dx in [-.1,.1]:
                    ax.add_patch(Circle((x+dx,z-.35),.045,facecolor=PAPER,edgecolor=INK,lw=1))
        ax.text(offset+2,.38,'Sized sections' if sized else 'Uniform sections',size=23,ha='center')
    save(fig,'truss-sizing')


def sparse_tracks():
    fig, ax = canvas()
    rng=np.random.default_rng(21)
    for x,count,label in [(2.35,18,'Sparse tracks'),(7.65,55,'Denser tracks')]:
        ax.add_patch(Rectangle((x-2,.7),4,3.35,facecolor='#edf0f3',edgecolor='#c7d1d1',lw=1))
        for cx,cy,colour,sign in [(x-.72,2.15,TEAL,1),(x+.72,2.6,PURPLE,-1)]:
            for _ in range(count):
                r=rng.uniform(.18,1.03); start=rng.uniform(0,2*np.pi); theta=start+sign*np.linspace(0,.8,18)
                xx=cx+r*np.cos(theta)*.9; yy=cy+r*np.sin(theta)
                ax.plot(xx,yy,lw=1.2,color=colour,alpha=.7)
                ax.scatter(xx[-1],yy[-1],s=15,color=colour,linewidths=0)
        ax.text(x,.12,label,size=24,ha='center')
    save(fig,'sparse-lagrangian-tracks')


if __name__=='__main__':
    regenerative(); validation(); momentum(); cylinder(); sizing(); sparse_tracks()
