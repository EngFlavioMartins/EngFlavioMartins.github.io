"""Regression checks for the requested conceptual geometry and phone detail budget."""
import unittest
from unittest.mock import patch
import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection
from matplotlib.patches import Rectangle
import generate_research_art as research
import generate_findings_art as findings
import generate_hybrid_art as hybrid
from apply_art_palettes import original


class FinalPolishTests(unittest.TestCase):
    def tearDown(self):
        plt.close('all')

    def test_postprocessing_samples_and_light_line_roles(self):
        with patch.object(research, 'save') as save:
            research.postprocessing()
        ax = save.call_args.args[0].axes[0]
        points = [c for c in ax.collections if isinstance(c, PathCollection)]
        self.assertEqual(len(points), 1)
        self.assertEqual(len(points[0].get_offsets()), 36)
        self.assertGreaterEqual(points[0].get_sizes().min(), 60)
        # INK is deliberately mapped to light foreground in the dark edition.
        self.assertTrue(all(line.get_color() == research.INK for line in ax.lines))

    def test_hybrid_six_staggered_vortices_no_overlap_box(self):
        fig, ax = research.canvas()
        hybrid.draw_hybrid(ax)
        clouds = [c for c in ax.collections if isinstance(c, PathCollection)]
        self.assertEqual(len(clouds), 6)
        self.assertTrue(all(len(c.get_offsets()) == 26 for c in clouds))
        self.assertTrue(all(c.get_sizes().min() >= 30 for c in clouds))
        self.assertEqual(len([p for p in ax.patches if isinstance(p, Rectangle)]), 2)
        self.assertFalse(any(p.get_linestyle() == '--' for p in ax.patches))

    def test_momentum_wakes_touch_next_turbine_without_blanket(self):
        with patch.object(findings, 'save') as save:
            findings.momentum()
        ax = save.call_args.args[0].axes[0]
        self.assertFalse(any(isinstance(p, Rectangle) for p in ax.patches))
        wakes = ax.patches[:4]
        for wake, start, end in zip(wakes, [1.2,3.5,5.8,8.1], [3.5,5.8,8.1,9.65]):
            self.assertAlmostEqual(wake.get_xy()[:,0].min(), start)
            self.assertAlmostEqual(wake.get_xy()[:,0].max(), end)
        self.assertIn('Wake', [text.get_text() for text in ax.texts])
        self.assertEqual(len(ax.patches), 8)  # four wakes plus four tapered arrows

    def test_removed_and_replaced_figure_labels(self):
        cavity = original('cavity-flow')
        self.assertNotIn('<!-- Re -->', cavity)
        self.assertNotIn('<!-- 100 -->', cavity)
        actuator = original('openfoam-actuator-surface')
        self.assertNotIn('<!-- Thrust -->', actuator)
        self.assertIn('Multirotor', actuator)


if __name__ == '__main__':
    unittest.main()
