#setup.py 


"""
 * CVE-2021-20323
 * CVE-2021-20323 Bug scanner for WebPentesters and Bugbounty Hunters
 *
 * @Developed By Cappricio Securities <https://cappriciosec.com>
 */


"""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='keycloak_xss',
    version='1.1',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'click',
        'pyyaml',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'keycloak_xss=keycloak_xss.main:main',
        ],
    },
)

