from importlib.metadata import version as _get_version_fn
import os


# Store package name and version
package_name = __name__
version = _get_version_fn(package_name)

