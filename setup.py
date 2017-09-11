import os
import sys
from distutils.sysconfig import get_python_lib

from setuptools import setup, find_packages

if "install" in sys.argv[1]:

    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib"):
        lib_paths.append(get_python_lib(prefix="/usr/local/"))
    for path in lib_paths:
        existing_path = os.path.abspath(os.path.join(path, "kcw"))
        if os.path.exists(existing_path):
            break


def getSqliteDep(version):
    """

    :param version:
    :return:
    """
    if sys.version_info[0] < 3:
        return 'pysqlite'
    else:
        return ''


# Get version of the module.
version = __import__('kcw').get_version()
symver = {"b", "a", "rc", "s"}
for s in symver:
    if s in version:
        version = version.replace(s, ".")


EXCLUDE_FROM_PACKAGES = ['']

setup(
    name="kcwallpaper",
    version=version,
    url="https://github.com/voldien/kcwallpaper",
    author="Valdemar Lindberg",
    author_email="voldiekami@gmail.com",
    description=open('README.md').read(),
    license="GNU General Public License v3 (GPLv3)",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    entry_points={'console_scripts': [
              'kcwallpaper = kcw.__main__:main'
          ]},
    install_requires=['mysql==0.0.1',
                      'mysql-connector==2.1.4',
                      getSqliteDep(sys.version_info[0]),
                      'urllib3'],
    zip_safe=False,
    data_files=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: KCW',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: SQL',
        'Topic :: Software Development :: Version Control :: Git'
    ]
)
