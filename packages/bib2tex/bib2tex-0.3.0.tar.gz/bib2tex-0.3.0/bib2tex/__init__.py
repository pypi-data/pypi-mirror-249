from configparser import ConfigParser
import os


def get_package_version():
    """Returns the version number from the pyproject.toml file."""
    # Get the path to pyproject.toml
    pyproject_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")
    )

    # Read the version number using ConfigParser
    config = ConfigParser()
    config.read(pyproject_path)
    return config.get("tool.poetry", "version").strip('"')


# Store package name and version
package_name = __name__
__version__ = get_package_version()
