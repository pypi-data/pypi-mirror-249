#!/usr/bin/env python3

# This file is part of userspacefs.

# userspacefs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# userspacefs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with userspacefs.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="userspacefs",
    version='3.0.0',
    author="Rian Hunter",
    author_email="rian@alum.mit.edu",
    description="Cross-platform user-space file systems for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://thelig.ht/code/userspacefs',
    license="GPL3",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Filesystems',
    ],
    packages=["userspacefs"],
    package_data={"userspacefs": ["py.typed"]},
    python_requires='>=3.11',
    install_requires=[
        "aiohttp>=3.9.0,<4",
        "typing_extensions>=4.9.0,<5",
        'pywin32;sys_platform=="win32"',
    ],
)
