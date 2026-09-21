"""Apply the approved mixed palettes without recalculating scientific geometry.

The immutable pre-palette Git snapshot is the source, making repeated runs
idempotent. Only SVG colour/opacity styling changes: paths, points and labels
remain identical. No OpenONDA asset or companion repository is touched.
"""
import colorsys
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '270a2c61d23e85715a83b267b8c855f43efd1b2d'
HEX = re.compile(r'#[0-9a-fA-F]{6}\b')

# Retain preview definitions, but all published art uses one dark background.
PALETTES = {
    'copper': ('#006d61', '#b4471e', '#765115'),
    'blue': ('#006b50', '#175ea8', '#906000'),
    'ochre': ('#006d5b', '#8c5800', '#215c9d'),
}
DARK_BACKGROUND = '#102b32'
DARK = {
    'copper': ('#4fe0bd', '#ffae73', '#f6d66b', DARK_BACKGROUND),
    'blue': ('#4fe0bd', '#79beff', '#f6d66b', DARK_BACKGROUND),
    'ochre': ('#63e4b9', '#efc34f', '#83c9ff', DARK_BACKGROUND),
}
ART = {
    'cylinder-wake': ('copper', True),
    'truss-sizing': ('copper', True),
    'voronoi-neighbours': ('copper', True),
    'openfoam-actuator-surface': ('ochre', True),
    'regenerative-wakes': ('ochre', True),
    'wake-validation': ('blue', True),
    'vertical-momentum': ('ochre', True),
    'hybrid-vortex-grid': ('blue', True),
    'three-body-schematic': ('blue', True),
    'truss-topology-mass': ('copper', True),
    'vortex-particle-ring': ('copper', True),
    'cavity-flow': ('blue', True),
    'openfoam-postprocessing': ('blue', True),
    'sparse-lagrangian-tracks': ('copper', True),
}


def rgb(value):
    return tuple(int(value[i:i+2], 16)/255 for i in (1, 3, 5))


def blend(background, foreground, amount):
    return '#' + ''.join(f'{round(255*((1-amount)*a+amount*b)):02x}'
                         for a, b in zip(rgb(background), rgb(foreground)))


def palette(name, dark):
    if dark:
        green, accent, third, paper = DARK[name]
        return green, accent, third, paper, '#f3f9f7'
    return *PALETTES[name], '#ffffff', '#173439'


def recolour(source, name, dark, strengthen_particles=False):
    green, accent, third, paper, ink = palette(name, dark)
    exact = {
        '#f4f5f8': paper, '#ffffff': paper, '#24283e': ink,
        '#197776': green, '#288f91': green, '#126460': green,
        '#7960af': accent, '#99602f': third,
        # The hybrid preview used slate as its second vortex sign.
        '#596975': accent,
    }

    def colour(match):
        original = match.group().lower()
        if original in exact:
            return exact[original]
        hue, lightness, saturation = colorsys.rgb_to_hls(*rgb(original))
        degrees = 360*hue
        if saturation < .13 or lightness < .28:
            # Neutral meshes/supports remain neutral; brighten for dark panels.
            amount = min(1, max(.15, (1-lightness)/.72))
            return blend(paper, ink, amount)
        target = green if 120 <= degrees < 200 else third if 10 <= degrees < 85 else accent
        # Retain the ordered pale-to-strong scientific colour field, with a
        # monotonic contrast expansion rather than clipping low-valued cells.
        amount = min(1, max(0, (1-lightness)/.65)) ** .65
        return blend(paper, target, amount)

    result = HEX.sub(colour, source)
    if strengthen_particles and dark:
        # Fine particle-ring marks need stronger opacity on the deep panel.
        result = result.replace('fill-opacity: 0.6', 'fill-opacity: 1')
        result = result.replace('stroke-opacity: 0.27', 'stroke-opacity: 0.8')
    # Matplotlib math glyphs can inherit SVG's implicit black fill. Give those
    # the foreground colour as well, especially on the deep orbital panel.
    return result.replace('<svg ', f'<svg fill="{ink}" ', 1)


def original(name):
    revised = ROOT / 'tools/art-sources' / f'{name}.svg'
    if revised.exists():
        return revised.read_text()
    return subprocess.check_output(
        ['git', 'show', f'{SOURCE}:assets/work/{name}.svg'], cwd=ROOT).decode()


def main():
    for name, (family, dark) in ART.items():
        result = recolour(original(name), family, dark, name == 'vortex-particle-ring')
        (ROOT / 'assets/work' / f'{name}.svg').write_text(result)
        print(f'{name}: {family}, {"deep" if dark else "white"} background')


if __name__ == '__main__':
    main()
