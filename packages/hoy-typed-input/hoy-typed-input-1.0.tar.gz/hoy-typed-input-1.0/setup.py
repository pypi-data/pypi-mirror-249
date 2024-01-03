from setuptools import setup

with open("./README.md", "r", encoding="utf-8") as arq:
    readme = arq.read()

setup(name='hoy-typed-input',
    version='1.0',
    license='MIT License',
    author='Alan Reis Anjos',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='alanreisanjo@gmail.com',
    keywords='Hoy Typed Input',
    description='Pequena biblioteca para obrigar o usuário a digitar um tipo de dado específico',
    packages=['TypedInput']
)