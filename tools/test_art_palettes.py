"""Palette regression tests: geometry/data preservation and label contrast."""
import unittest
import re
import xml.etree.ElementTree as ET
from apply_art_palettes import ART, HEX, ROOT, original, palette, recolour, rgb


def luminance(value):
    linear = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in rgb(value)]
    return sum(v*w for v, w in zip(linear, [.2126, .7152, .0722]))


class PaletteTests(unittest.TestCase):
    def test_colours_only_and_reproducible(self):
        for name, (family, dark) in ART.items():
            source = original(name)
            output = (ROOT / 'assets/work' / f'{name}.svg').read_text()
            with self.subTest(art=name):
                ET.fromstring(output)
                normalised = output.replace(f'<svg fill="{palette(family, dark)[4]}" ', '<svg ', 1)
                if name == 'vortex-particle-ring' and dark:
                    normalised = normalised.replace('fill-opacity: 1', 'fill-opacity: 0.6')
                    normalised = normalised.replace('stroke-opacity: 0.8', 'stroke-opacity: 0.27')
                self.assertEqual(HEX.sub('COLOUR', source), HEX.sub('COLOUR', normalised))
                self.assertEqual(output, recolour(source, family, dark, name == 'vortex-particle-ring'))
                self.assertNotIn('#7960af', output)
                self.assertNotIn('#f4f5f8', output)

    def test_label_contrast(self):
        for family, dark in set(ART.values()):
            green, accent, third, paper, ink = palette(family, dark)
            for foreground in [green, accent, third, ink]:
                high, low = sorted([luminance(paper), luminance(foreground)], reverse=True)
                self.assertGreaterEqual((high+.05)/(low+.05), 4.5)

    def test_protected_exclusion_and_variety(self):
        self.assertFalse(any('openonda' in name.lower() for name in ART))
        self.assertEqual({family for family, _ in ART.values()}, {'copper', 'blue', 'ochre'})
        self.assertTrue(all(dark for _, dark in ART.values()))
        self.assertEqual(len({palette(family, dark)[3] for family, dark in ART.values()}), 1)

    def test_site_palette_bindings(self):
        html = (ROOT / 'index.html').read_text()
        figures = re.findall(r'<figure\b.*?</figure>', html, re.S)
        for figure in figures:
            asset = re.search(r'/assets/work/([a-z-]+)\.svg', figure)
            if not asset:
                continue  # OpenONDA keeps its original raster and styling.
            family, dark = ART[asset[1]]
            self.assertIn('.svg?v=20260921-dark', figure)
            if dark:
                self.assertIn(f'data-art-tone="{family}"', figure)
            else:
                self.assertNotIn('data-art-tone', figure)


if __name__ == '__main__':
    unittest.main()
