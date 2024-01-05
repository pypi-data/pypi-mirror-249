from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='tibia-battle',
    version='0.0.2',
    license='MIT License',
    author='Ítalo Pereira Barbosa',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='tato361.portugal@gmail.com',
    keywords='battle',
    description=u'Módulo criado para auxiliar na captura do content battle do tibia.',
    packages=find_packages(),
    install_requires=['opencv-python', 'pyautogui', 'numpy', 'pillow'],)