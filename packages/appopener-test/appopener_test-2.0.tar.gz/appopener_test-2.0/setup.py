from distutils.core import setup

exec(compile(open('release.py').read(), 'release.py', 'exec'))

try:
    from sphinx.setup_command import BuildDoc
    cmd_class ={'build_sphinx': BuildDoc}
except ImportError:
    cmd_class = {}

from release import *

packages = ['appopener_test']


setup(name=name,
      version          = version,
      description      = description,
      long_description_content_type="text/markdown",
      long_description = long_description,
      author           = authors["Athrv"][0],
      author_email     = authors["Athrv"][1],
      maintainer       = authors["athrvvvv"][0],
      maintainer_email = authors["athrvvvv"][1],
      license          = license,
      classifiers      = classifiers,
      url              = url,
      download_url     = download_url,
      project_urls={
        'Documentation': Documentation,
        'Source': Source,
        'Tracker': Tracker,
    },
      platforms        = platforms,
      keywords         = keywords,
      py_modules       = ['appopener_test'],
      packages         = packages,
      include_package_data=True,
      install_requires=install_requires,
      cmdclass = cmd_class
      )

