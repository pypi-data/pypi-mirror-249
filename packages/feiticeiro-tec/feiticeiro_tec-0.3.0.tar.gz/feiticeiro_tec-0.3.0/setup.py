from setuptools import setup


import os


def listar_subpastas(diretorio):
    subpastas = [diretorio]
    for nome in os.listdir(diretorio):
        if nome == "__pycache__":
            continue
        caminho = os.path.join(diretorio, nome)
        if os.path.isdir(caminho):
            subpastas.append(caminho)
            subpastas.extend(listar_subpastas(caminho))
    return subpastas


with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="feiticeiro_tec",
    version="0.3.0",
    url="https://github.com/feiticeiro-tec/feiticeiro-tec",
    license="BSD3",
    author="Silvio Henrique Cruz Da Silva",
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email="silviohenriquecruzdasilva@gmail.com",
    keywords="python, feiticeiro_tec, utilidades, feiticeiro, tec",
    description=("pacote de utilidades para projetos python"),
    packages=listar_subpastas("feiticeiro_tec"),
    package_data={
        "feiticeiro_tec": [
            "flask/job_manager/templates/job_manager/*",
        ],
    },
    install_requires=[
        "loguru",
        "pydantic",
    ],
    extras_require={
        "dynaconf": ["dynaconf"],
        "validate": ["validate_docbr"],
        "request": ["requests"],
    },
)
