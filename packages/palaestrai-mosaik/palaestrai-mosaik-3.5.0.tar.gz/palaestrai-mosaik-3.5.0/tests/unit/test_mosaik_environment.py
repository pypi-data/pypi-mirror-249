import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from palaestrai_mosaik.environment.mosaik_ifs import restore_value
from palaestrai_mosaik.mosaik_environment import MosaikEnvironment


class TestMosaikEnvironment(unittest.TestCase):
    @unittest.skip
    @patch(f"{MosaikEnvironment.__module__}.threading.Thread")
    @patch(f"{MosaikEnvironment.__module__}.MosaikWorld")
    def test_start(self, mock_world, mock_thread):
        env = MosaikEnvironment(
            "", "", 0, params={"reward": {"name": "", "params": dict()}}
        )
        mock_world.setup = MagicMock()

        env.start_environment()

    def test_restoring_values(self):
        values = [1, 2.3, 3.4]
        restored_values = restore_value(values)
        self.assertEqual(np.shape(restored_values), (3,))
        self.assertEqual(type(restored_values), list)

        restored_values = restore_value(np.array(values))
        self.assertEqual(np.shape(restored_values), (3,))
        self.assertEqual(type(restored_values), list)

        restored_values = restore_value(np.array(values[0]))
        self.assertEqual(np.shape(restored_values), ())
        self.assertEqual(type(restored_values), int)

        restored_values = restore_value(np.array(values[1]))
        self.assertEqual(np.shape(restored_values), ())
        self.assertEqual(type(restored_values), float)


if __name__ == "__main__":
    unittest.main()
