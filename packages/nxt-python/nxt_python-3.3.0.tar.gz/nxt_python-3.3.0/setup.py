# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nxt', 'nxt.backend', 'nxt.sensor']

package_data = \
{'': ['*']}

install_requires = \
['pyusb>=1.2.1,<2.0.0']

extras_require = \
{'bluetooth': ['pybluez>=0.23,<0.24']}

setup_kwargs = {
    'name': 'nxt-python',
    'version': '3.3.0',
    'description': 'LEGO Mindstorms NXT Control Package',
    'long_description': '# ![NXT-Python](./logo.svg)\n\nNXT-Python is a package for controlling a LEGO NXT robot using the Python\nprogramming language. It can communicate using either USB or Bluetooth.\n\nNXT-Python for Python 2 is no longer supported.\n\nNXT-Python repository is on [sourcehut][] with a mirror on [Github][].\n\n[sourcehut]: https://sr.ht/~ni/nxt-python/ "NXT-Python repository on sourcehut"\n[Github]: https://github.com/schodet/nxt-python "NXT-Python repository on Github"\n\n## Requirements\n\n- [Python 3.x](http://www.python.org)\n- USB communication:\n    - [PyUSB](https://github.com/pyusb/pyusb)\n- Bluetooth communication:\n    - [PyBluez](https://github.com/pybluez/pybluez)\n\n## Installation\n\nInstall NXT-Python with pip:\n\n    python3 -m pip install --upgrade nxt-python\n\nSee [installation][] instructions in the documentation for more informations.\n\n[installation]: https://ni.srht.site/nxt-python/latest/installation.html\n\n## Next steps\n\nYou can read the [documentation][], or start directly with the [tutorial][].\n\n[documentation]: https://ni.srht.site/nxt-python/latest/\n[tutorial]: https://ni.srht.site/nxt-python/latest/handbook/tutorial.html\n\n## Upgrading your code\n\nIf you used previous version of NXT-Python with Python 2, the documentation\nincludes an [migration guide][].\n\n[migration guide]: https://ni.srht.site/nxt-python/latest/migration.html\n\n## Contact\n\nThere is a [mailing list][] for questions.\n\nNXT-Python repository maintainer is Nicolas Schodet, since 2021-11-06. You can\ncontact him on the mailing list.\n\nYou can use the [Github issues page][] to report problems, but please use the\nmailing list for questions.\n\n[mailing list]: https://lists.sr.ht/~ni/nxt-python\n[Github issues page]: https://github.com/schodet/nxt-python/issues\n\n## Thanks\n\n- Doug Lau for writing NXT\\_Python, our starting point.\n- rhn for creating what would become v2, making lots of smaller changes, and\n  reviewing tons of code.\n- Marcus Wanner for maintaining NXT-Python up to v2.2.2, his work has been\n  amazing!\n- Elvin Luff for taking over the project after Marcus, making a lot of work\n  for the port to Python 3.\n- mindsensors.com (esp. Ryan Kneip) for helping out with the code for a lot of\n  their sensors, expanding the sensors covered by the type checking database,\n  and providing hardware for testing.\n- HiTechnic for providing identification information for their sensors. I note\n  that they have now included this information in their website. ;)\n- Linus Atorf, Samuel Leeman-Munk, melducky, Simon Levy, Steve Castellotti,\n  Paulo Vieira, zonedabone, migpics, TC Wan, jerradgenson, henryacev, Paul\n  Hollensen, and anyone else I forgot for various fixes and additions.\n- Goldsloth for making some useful changes and keeping the tickets moving\n  after the migration to Github.\n- All our users for their interest and support!\n\n## License\n\nNXT-Python is free software: you can redistribute it and/or modify it under\nthe terms of the GNU General Public License as published by the Free Software\nFoundation, either version 3 of the License, or (at your option) any later\nversion.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT\nANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS\nFOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with\nthis program. If not, see <http://www.gnu.org/licenses/>.\n',
    'author': 'Nicolas Schodet',
    'author_email': 'nico@ni.fr.eu.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://sr.ht/~ni/nxt-python/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
