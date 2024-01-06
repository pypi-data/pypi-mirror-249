import unittest
from pathlib import Path

from linky.config import read_conf
from linky.utils import path_utils
from linky.utils.path_utils import (
    BASE_NAME, get_dir_prefix, get_first_dir, get_path_in_base,
    get_paths_in_root, get_prefixed_path, is_path_in_base,
)
from tests import TEST_DATA_PATH


# pylint: disable=missing-function-docstring
class GetPathInBaseTest(unittest.TestCase):
    """
    Make sure path_utils.get_path_in_base is working well
    """

    def setUp(self) -> None:
        self.base_path = Path("/home/lol/videos/.base")

    def _test_bad_path(self, target_path, error_message):
        with self.assertRaises(ValueError) as ass:
            get_path_in_base(self.base_path, Path(target_path))
        self.assertEqual(ass.exception.args[0], error_message)

    def _test_good_path(self, target_path, expected_result, categories=None, relative=False):
        self.assertEqual(
            get_path_in_base(
                self.base_path, Path(target_path),
                categories=categories, relative=relative),
            Path(expected_result)
        )

    def test_path_normal(self):
        self._test_good_path(
            "/home/lol/videos/comedian/wonderboy/jokes/on/you/test.avi",
            "/home/lol/videos/.base/jokes/on/you/test.avi",
            categories=["comedian"]
        )

    def test_path_normal_relative(self):
        self._test_good_path(
            "/home/lol/videos/comedian/wonderboy/jokes/on/you/test.avi",
            "jokes/on/you/test.avi",
            categories=["comedian"],
            relative=True
        )

    def test_path_root(self):
        self._test_bad_path(
            "/home/lol/videos/",
            "Cannot target the link root"
        )

    def test_path_no_common_path(self):
        self._test_bad_path(
            "/home/lol/music/nothing",
            "Cannot target path outside of root"
        )

    def test_path_within_base(self):
        path_in_base = "/home/lol/videos/.base/somewhere/else/in/base"
        self._test_good_path(path_in_base, path_in_base)

    def test_path_within_base_relative(self):
        self._test_good_path(
            "/home/lol/videos/.base/somewhere/else/in/base",
            "somewhere/else/in/base", relative=True
        )

    def test_path_is_base(self):
        self._test_bad_path(
            self.base_path,
            "Cannot target the base path"
        )

    def test_path_with_relative_links(self):
        self._test_bad_path(
            "./videos/watched/somewhere/else/bah.mkv",
            "Paths have to be absolute"
        )


class GetDirPrefixTest(unittest.TestCase):
    """
    Tests for path_utils.get_dir_prefix
    """

    def test_long_name(self):
        self.assertListEqual(
            get_dir_prefix("Avadakedavra"),
            ["A", "Ava"]
        )

    def test_short_names(self):
        for name in ["Lol", "Lo"]:
            self.assertListEqual(
                get_dir_prefix(name),
                ["L"]
            )

    def test_no_prefix_names(self):
        for name in ["B", ""]:
            self.assertListEqual(
                get_dir_prefix(name),
                []
            )


class GetPrefixedTest(unittest.TestCase):
    """
    Tests for path_utils.get_prefixed_path
    """

    def test_simple(self):
        self.assertEqual(
            get_prefixed_path(Path("/mnt/Videos/Gazing Stars")),
            Path("/mnt/Videos/G/Gaz/Gazing Stars")
        )


class FindBaseTest(unittest.TestCase):
    """
    Tests for path_utils.find_base
    """

    def test_find_base(self):
        expected_base = TEST_DATA_PATH / "simple_base" / path_utils.BASE_NAME
        base = path_utils.find_base(TEST_DATA_PATH / "simple_base" / "dir1" / "dir2")
        self.assertEqual(base, expected_base)

    def test_find_from_file(self):
        expected_base = TEST_DATA_PATH / "simple_base" / path_utils.BASE_NAME
        base = path_utils.find_base(TEST_DATA_PATH / "simple_base" / "dir1" / ".gitkeep")
        self.assertEqual(base, expected_base)

    def test_find_base_max_iteration(self):
        self.assertRaises(
            StopIteration,
            path_utils.find_base, TEST_DATA_PATH / "simple_base" / "dir1" / "dir2", 1
        )

    def test_find_base_no_base(self):
        self.assertRaises(
            (ValueError, FileNotFoundError),
            path_utils.find_base, Path("/usr/lib/dpkg/methods")
        )


class FirstDirTest(unittest.TestCase):
    """
    Tests for path_utils.get_first_dir
    """

    def test_category(self):
        first_dir = path_utils.get_first_dir(TEST_DATA_PATH / "simple_base" / "dir1" / "dir2")
        self.assertEqual(first_dir, "dir1")


class GetPathsInRoot(unittest.TestCase):
    """
    Tests for path_utils.get_paths_in_root
    """

    def setUp(self) -> None:
        self.test_dir = TEST_DATA_PATH / "movies"
        self.base_path = self.test_dir / BASE_NAME
        self.config = read_conf(self.test_dir)

    def test_valid_path_in_base(self):
        path = self.base_path / "The Hurt Locker (2008)" / "The.Hurt.Locker.2008.1080p.BRrip.mkv"

        self._test_valid_path(path, 5)

    def _test_valid_path(self, path, expected_count, category=None):
        paths = get_paths_in_root(path, self.config, category)
        path_count = len(paths)
        self.assertEqual(path_count, expected_count)
        for path_in_root in paths:
            self.assertFalse(
                is_path_in_base(path_in_root, self.base_path),
                "Returned path is in base: %s" % path_in_root
            )

    def test_valid_path_outside_base(self):
        path = self.test_dir / \
               "Watched" / "Watched" / \
               "The Hurt Locker (2008)" / "The.Hurt.Locker.2008.1080p.BRrip.mkv"
        self._test_valid_path(path, 5)

    def test_should_pass_with_same_category_limited_to_category(self):
        path = self.test_dir / \
               "Actors" / "Jeremy Renner" / \
               "The Hurt Locker (2008)" / "The.Hurt.Locker.2008.1080p.BRrip.mkv"
        self._test_valid_path(path, 3, "Actors")

    def test_should_pass_with_different_category_limited_to_category(self):
        path = self.test_dir / \
               "Watched" / "Watched" / \
               "The Hurt Locker (2008)" / "The.Hurt.Locker.2008.1080p.BRrip.mkv"
        self._test_valid_path(path, 3, "Actors")

    def test_with_base(self):
        path = self.test_dir / path_utils.BASE_NAME
        self.assertRaisesRegex(
            ValueError, "Can't target base",
            get_paths_in_root, path, self.config, self.base_path
        )

    def test_with_link_root(self):
        path = self.test_dir
        self.assertRaisesRegex(
            ValueError, "Can't target linked root",
            get_paths_in_root, path, self.config, self.base_path
        )

    def test_with_tag(self):
        self.assertRaisesRegex(
            ValueError, "Path cannot be tag group or tag",
            get_paths_in_root, self.test_dir / "Actors", self.config
        )

    def test_with_tag_group(self):
        self.assertRaisesRegex(
            ValueError, "Path cannot be tag group or tag",
            get_paths_in_root, self.test_dir / "Actors" / "Emilia Clarke", self.config
        )

    def test_invalid_path_in_base(self):
        path = self.base_path / "I don't exist"

        self.assertRaisesRegex(
            ValueError, "Path doesn't exist",
            get_paths_in_root, path, self.config, self.base_path
        )


class GetFirstDir(unittest.TestCase):
    """
    Tests for path_utils.get_first_dir
    """

    def test_should_pass_with_base(self):
        base_path = Path("/mnt/storage/") / BASE_NAME
        self.assertEqual(
            get_first_dir(base_path, base_path),
            BASE_NAME
        )

    def test_should_fail_with_root(self):
        base_path = Path("/mnt/storage/.base")
        self.assertRaisesRegex(
            ValueError, "Can't get first directory from root",
            get_first_dir, base_path.parent, base_path,
        )


if __name__ == "__main__":
    unittest.main()
