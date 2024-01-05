import setuptools

with open("README.md", "r") as arq:
    readme = arq.read()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='lifemanapy',
    version="0.0.12",
    author='Ítalo Pereira Barbosa',
    author_email="pradishbijukchhe@gmail.com",
    description=u'Módulo criado para auxiliar na captura de vida e mana do personagem no jogo tibia.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_dir={"lifemanapy": "lifemanapy"},
    python_requires=">=3",
    install_requires=['opencv-python', 'pyautogui', 'numpy', 'pillow'],
)