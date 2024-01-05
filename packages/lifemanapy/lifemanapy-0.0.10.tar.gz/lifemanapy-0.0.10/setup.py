from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='lifemanapy',
    version='0.0.10',
    license='MIT License',
    author='Ítalo Pereira Barbosa',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='tato361.portugal@gmail.com',
    keywords='life mana',
    description=u'Módulo criado para auxiliar na captura de vida e mana do personagem no jogo tibia.',
    packages=['lifemanapy', 'lifemanapy.constants', 'lifemanapy.converter', 'lifemanapy.dimensions', 'lifemanapy.configs'],
    install_requires=['opencv-python', 'pyautogui', 'numpy', 'pillow'],)