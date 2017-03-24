from sets import Set
from collections import defaultdict


class Packager(object):
    def __init__(self):
        # Contains the installed packages and their dependencies
        self.installed_packages = Set()

        # Contains the requested installed packages
        # stores the intend, those will only be removed if
        # requested by the user
        self.manually_installed_packages = Set()

        # if foo depend on bar and baz then:
        # self.dependencies = {foo: ['bar', 'baz']}
        self.dependencies = defaultdict(list)

        # if foo depend on bar and baz then:
        # self.reverse_dependencies = {'bar': ['foo'], 'baz': ['foo']}
        self.reverse_dependencies = defaultdict(list)

    def install_once(self, name, show_warnings=True):
        """
        Only install the package if not yet installed

        When show_warnings is True already install package will
        generate a message warning the user.
        """
        if name not in self.installed_packages:
            print("\tInstalling %s" % name)
            self.installed_packages.add(name)

        elif show_warnings:
            print("\t%s is already installed." % name)

    def install(self, name):
        self._install(name)
        self.manually_installed_packages.add(name)

    def _install(self, name, show_warnings=True):
        """
        Install a package and its dependencies.

        if a dependency is already installed it wont be re-installed
        """
        for dependency_name in self.dependencies[name]:
            self._install(dependency_name, show_warnings=False)

        self.install_once(name, show_warnings=show_warnings)

    def remove(self, name):
        if self._remove(name):
            self.manually_installed_packages.remove(name)

    def _remove(self, name, show_warnings=True, is_dependency=False):
        """
        Remove a package and its dependencies.

        if a dependency is shared it wont be removed.

        returns True if the package was removed else False
        """
        # We don't want to uninstall dependencies which were also manually
        # installed
        if is_dependency and name in self.manually_installed_packages:
            return False

        if name not in self.installed_packages:
            print("\t%s is not installed." % name)
            return False

        package_was_removed = self.remove_if_not_needed(
            name, show_warnings=show_warnings)

        for dependency_name in self.dependencies.get(name, []):
            self._remove(
                dependency_name, show_warnings=False, is_dependency=True)

        if package_was_removed:
            print("\tRemoving %s" % name)
            return True
        else:
            return False

    def remove_if_not_needed(self, name, show_warnings=True):
        """
        Remove a package only if not a dependency of an installed package.

        When is_dependency is False the warning
        """
        if self.is_package_a_dependency(name):
            if show_warnings:
                print("\t%s is still needed." % name)

            return False

        self.installed_packages.remove(name)
        return True

    def is_package_a_dependency(self, name):
        for dependency_name in self.reverse_dependencies[name]:
            if dependency_name in self.installed_packages:
                return True

            if self.is_package_a_dependency(dependency_name):
                return True

        return False

    def list(self):
        """
        return a list of installed package and their dependencies
        """
        return self.installed_packages

    def print_list(self):
        """
        print a list of installed packages
        """
        for package_name in self.list():
                print("\t%s" % package_name)

    def depend(self, package_name, *dependencies):
        """
        create a set of dependencies for a package
        """
        self.dependencies[package_name] = dependencies
        for dependency_name in dependencies:
            self.reverse_dependencies[dependency_name].append(package_name)
