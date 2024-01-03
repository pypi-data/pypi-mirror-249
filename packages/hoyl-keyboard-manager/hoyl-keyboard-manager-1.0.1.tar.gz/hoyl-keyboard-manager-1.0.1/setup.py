from setuptools import setup

with open("./README.md", "r", encoding="utf-8") as arq:
    readme = arq.read()

setup(name='hoyl-keyboard-manager',
    version='1.0.1',
    license='MIT License',
    author='Alan Reis Anjos',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='alanreisanjo@gmail.com',
    keywords='Hoyl Keyboard Manager',
    description='Pequena biblioteca para consultar eventos do teclado',
    packages=['KeyboardManager'],
    install_requires=['keyboard']
)