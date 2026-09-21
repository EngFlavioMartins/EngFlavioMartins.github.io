"""Geometry checks for the illustrative actuator projection (not a CFD solver)."""
import unittest
import numpy as np
from generate_research_art import actuator_camera, actuator_surfaces, actuator_project, actuator_wake


class ActuatorGeometryTests(unittest.TestCase):
    def test_orthographic_camera(self):
        basis = actuator_camera()
        np.testing.assert_allclose(basis @ basis.T, np.eye(2), atol=1e-14)
        # The broad square is seen primarily face-on, not edge-on.
        normal_view = np.cross(*basis)
        self.assertGreater(abs(normal_view[0]), .8)

    def test_force_normals(self):
        rotor, strips = actuator_surfaces()
        for face, force in [(rotor, [-1, 0, 0]), *[(s, [0, 0, 1]) for s in strips]]:
            a, b = face[1]-face[0], face[3]-face[0]
            self.assertAlmostEqual(np.dot(a, force), 0)
            self.assertAlmostEqual(np.dot(b, force), 0)
            np.testing.assert_allclose(np.cross(np.cross(a, b), force), 0)
        np.testing.assert_allclose(rotor[:, 0], 0)
        for strip in strips:
            self.assertLess(strip[:, 0].min(), 0)
            self.assertGreater(strip[:, 0].max(), 0)

    def test_projected_vector_directions(self):
        origin = np.array([0., 0., 0.])
        flow = actuator_project([1, 0, 0])-actuator_project(origin)
        thrust = actuator_project([-1, 0, 0])-actuator_project(origin)
        rise = actuator_project([0, 0, 1])-actuator_project(origin)
        np.testing.assert_allclose(flow, -thrust)
        self.assertGreater(flow[0], 0)
        self.assertAlmostEqual(rise[0], 0)
        self.assertGreater(rise[1], 0)

    def test_wakes_start_at_strip_tips(self):
        _, strips = actuator_surfaces()
        for strip in strips:
            z = strip[0, 2]
            for tip, sign in [(-1.5, 1), (1.5, -1)]:
                path = actuator_wake(z, tip, sign)
                np.testing.assert_allclose(path[0], [0, tip, z])
                self.assertTrue(np.all(np.diff(path[:, 0]) > 0))
                self.assertGreater(path[-1, 2], z)


if __name__ == "__main__":
    unittest.main()
