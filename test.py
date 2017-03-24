import unittest
from sets import Set

from src import Packager


class TestSrc(unittest.TestCase):

    def setUp(self):
        self.pkg = Packager()

    def test_should_install_package(self):
        self.pkg.install('foo')
        self.assertEqual(self.pkg.list(), Set(['foo']))

    def test_should_remove_package(self):
        self.pkg.install('foo')
        self.assertEqual(self.pkg.list(), Set(['foo']))

        self.pkg.remove('foo')
        self.assertEqual(self.pkg.list(), Set())

    def test_should_install_dependencies(self):
        self.pkg.depend('foo', 'bar', 'baz')
        self.pkg.install('foo')
        self.assertEqual(self.pkg.list(), Set(['foo', 'bar', 'baz']))

    def test_should_remove_dependencies(self):
        self.pkg.depend('foo', 'bar', 'baz')
        self.pkg.install('foo')
        self.assertEqual(self.pkg.list(), Set(['foo', 'bar', 'baz']))

        self.pkg.remove('foo')
        self.assertEqual(self.pkg.list(), Set())

    def test_should_not_fail_when_removing_not_installed_package(self):
        self.pkg.remove('foo')
        self.assertEqual(self.pkg.list(), Set())

    def test_should_install_same_dependencies_once(self):
        self.pkg.depend('foo', 'bar')
        self.pkg.depend('new_foo', 'bar')
        self.pkg.install('foo')
        self.pkg.install('new_foo')
        self.assertEqual(self.pkg.list(), Set(['new_foo', 'foo', 'bar']))

    def test_should_not_remove_cross_dependencies(self):
        self.pkg.depend('foo', 'bar', 'baz')
        self.pkg.depend('new_foo', 'bar')
        self.pkg.install('foo')
        self.pkg.install('new_foo')
        self.assertEqual(
            self.pkg.list(),
            Set(['new_foo', 'foo', 'bar', 'baz'])
        )

        self.pkg.remove('foo')
        self.assertEqual(self.pkg.list(), Set(['new_foo', 'bar']))

    def test_should_not_remove_deep_cross_dependencies(self):
        # Here we defined a deep dependency where
        # - foo -> bar -> baz
        # and install new_foo which also depend on the deep dependency baz
        # - new_foo -> baz
        # baz should persist if we uninstall 'foo'
        self.pkg.depend('foo', 'bar', 'foobar')
        self.pkg.depend('bar', 'baz')
        self.pkg.depend('new_foo', 'baz')
        self.pkg.install('foo')
        self.pkg.install('new_foo')
        self.assertEqual(
            self.pkg.list(),
            Set(['new_foo', 'foo', 'bar', 'baz', 'foobar'])
        )

        self.pkg.remove('foo')
        self.assertEqual(self.pkg.list(), Set(['new_foo', 'baz']))


if __name__ == '__main__':
    unittest.main()
