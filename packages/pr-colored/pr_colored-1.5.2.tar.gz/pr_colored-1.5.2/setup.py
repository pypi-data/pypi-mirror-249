from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pr_colored',
    version='1.5.2',
    description='colored print() as pr()',
    author='Andrew M',
    author_email='toni25010@gmail.com',
    packages=['pr_colored'],
    install_requires=['termcolor'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
)

