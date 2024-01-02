#!/usr/bin/env python
"""The setup and build script for the python-telegram-bot library."""
import os
import subprocess
import sys

from setuptools import setup, find_packages

UPSTREAM_URLLIB3_FLAG = '--with-upstream-urllib3'


def get_requirements(raw=False):
    """Build the requirements list for this project"""
    requirements_list = []

    with open('requirements.txt') as reqs:
        for install in reqs:
            if install.startswith('# only TeleGenic.ext:'):
                if raw:
                    break
                continue
            requirements_list.append(install.strip())

    return requirements_list


def get_packages_requirements(raw=False):
    """Build the package & requirements list for this project"""
    reqs = get_requirements(raw=raw)

    exclude = ['tests*']
    if raw:
        exclude.append('TeleGenic.ext*')

    packs = find_packages(exclude=exclude)
    # Allow for a package install to not use the vendored urllib3
    if UPSTREAM_URLLIB3_FLAG in sys.argv:
        sys.argv.remove(UPSTREAM_URLLIB3_FLAG)
        reqs.append('urllib3 = 1.26.15')
        packs = [x for x in packs if not x.startswith('TeleGenic.vendor.ptb_urllib3')]

    return packs, reqs


def get_setup_kwargs(raw=False):
    """Builds a dictionary of kwargs for the setup function"""
    packages, requirements = get_packages_requirements(raw=raw)

    raw_ext = "-raw" if raw else ""
    readme = f'README{"_RAW" if raw else ""}.rst'

    fn = os.path.join('TeleGenic', 'version.py')
    with open(fn) as fh:
        for line in fh.readlines():
            if line.startswith('__version__'):
                exec(line)

    with open(readme, 'r', encoding='utf-8') as fd:

        kwargs = dict(
            script_name=f'setup.py',
            name=f'Testfortelegenic',
            version=7.2,
            author='BLANK',
            author_email='dev.unions@gmail.com',
            license='LGPLv3',
            # Keywords supported by PyPI can be found at https://git.io/JtLIZ
            project_urls={
                "Bug Tracker": "https://github.com/Dev-Union/TeleGenic/issues",
                "Source Code": "https://github.com/Dev-Union/TeleGenic",
                "News": "https://t.me/TheDevsUnion",
            },
            download_url=f'https://pypi.org/project/TeleGenic/',
            keywords='python telegram bot api wrapper',
            description="We have made you a wrapper",
            long_description = fd.read(),
            long_description_content_type='text/x-rst',
            packages=packages,

            install_requires=requirements,
            extras_require={
                'json': 'ujson',
                'socks': 'PySocks',
                # 3.4-3.4.3 contained some cyclical import bugs
                'passport': 'cryptography!=3.4,!=3.4.1,!=3.4.2,!=3.4.3',
            },
            include_package_data=True,
            classifiers=[
                'Development Status :: 5 - Production/Stable',
                'Intended Audience :: Developers',
                'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                'Operating System :: OS Independent',
                'Topic :: Software Development :: Libraries :: Python Modules',
                'Topic :: Communications :: Chat',
                'Topic :: Internet',
                'Programming Language :: Python',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3.9',
            ],
            python_requires='>=3.6'
        )

    return kwargs


def main():
    # If we're building, build ptb-raw as well
    if set(sys.argv[1:]) in [{'bdist_wheel'}, {'sdist'}, {'sdist', 'bdist_wheel'}]:
        args = ['python', 'setup-raw.py']
        args.extend(sys.argv[1:])
        subprocess.run(args, check=True, capture_output=True)

    setup(**get_setup_kwargs(raw=False))


if __name__ == '__main__':
    main()
