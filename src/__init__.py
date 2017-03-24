from sets import Set
from collections import defaultdict


class Packager(object):
    """
    This is a package with dependency management.

    When installed manually a package can only be uninstalled manually
    When a package is being removed its dependencies are removed too
    If a dependency is still needed by an another library it will not be
    uninstalled.

    """

    def __init__(self):
        # Contains the installed packages and their dependencies
        self.installed_packages = Set()

        # Contains packages the user manually installed
        self.manually_installed_packages = Set()

        # Contains the dependency registry, if foo depends on bar and baz then:
        # self.dependencies = {foo: ['bar', 'baz']}
        self.dependencies = defaultdict(list)

        # Reverse dependency registry, if foo depend on bar and baz then:
        # self.reverse_dependencies = {'bar': ['foo'], 'baz': ['foo']}
        self.reverse_dependencies = defaultdict(list)

    def install(self, name):
        """
        Install a package and its dependencies.
        """
        self._install(name)
        self.manually_installed_packages.add(name)

    def _install(self, name, show_warnings=True):
        """
        Install a package and its dependencies.

        if a dependency is already installed it wont be re-installed
        """
        for dependency_name in self.dependencies[name]:
            self._install(dependency_name, show_warnings=False)

        self._safe_install(name, show_warnings=show_warnings)

    def _safe_install(self, name, show_warnings=True):
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

    def remove(self, name):
        """
        Remove a package and its dependencies.
        """
        self._remove(name)
        self.manually_installed_packages.remove(name)

    def _remove(self, name, show_warnings=True, is_dependency=False):
        """
        Remove a package and its dependencies.

        If a dependency is used by an installed package it wont be removed.
        """
        # We don't want to uninstall dependencies which were manually installed
        if is_dependency and name in self.manually_installed_packages:
            return

        # If the package to remove has not been installed
        if name not in self.installed_packages:
            print("\t%s is not installed." % name)
            return

        # Remove the package
        self._safe_remove(name, show_warnings=show_warnings)

        # Remove the package dependencies and the dependencies of those
        # dependencies... recursively
        for dependency_name in self.dependencies[name]:
            self._remove(
                dependency_name, show_warnings=False, is_dependency=True)

    def _safe_remove(self, name, show_warnings=True):
        """
        Remove a package only if not a dependency of an installed package.
        """
        if self.is_package_a_dependency(name):
            if show_warnings:
                print("\t%s is still needed." % name)

            return

        print("\tRemoving %s" % name)
        self.installed_packages.remove(name)

    def is_package_a_dependency(self, name):
        """
        Returns true if the given package is a dependency to another
        installed package.
        """
        for package_name in self.reverse_dependencies[name]:
            # check if the package is a dependency
            if package_name in self.installed_packages:
                return True

            # check if the dependent has dependent package as
            # a dependency of an installed package
            if self.is_package_a_dependency(package_name):
                return True

        return False

    def list(self):
        """
        return a list of installed package and their dependencies
        """
        return self.installed_packages

    def depend(self, name, *dependencies):
        """
        create a set of dependencies for a package
        """
        self.dependencies[name] = dependencies

        # fill up the revert index of dependencies
        for dependency_name in dependencies:
            self.reverse_dependencies[dependency_name].append(name)
