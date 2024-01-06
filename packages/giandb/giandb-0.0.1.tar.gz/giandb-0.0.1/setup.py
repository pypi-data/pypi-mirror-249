from setuptools import setup, find_packages

setup(
    name='giandb',
    version='0.0.1',  # Cambia la versión a la nueva
    license='MIT',
    description="paquete gian de insertar data dba",
    author="Gianacarlos Cardenas Galarza",
    install_requires=['math', 'numpy'],
    author_email="alex10estadistica@gmail.com",
    packages=find_packages(),
    url="https://github.com/CardenasGalarza/GIANDB",
    entry_points={
        'console_scripts': [
            'dbgian = mimodulo:main',  # Reemplaza 'mimodulo' con el nombre real de tu módulo y 'main' con la función principal si la tienes
        ],
    },
)
