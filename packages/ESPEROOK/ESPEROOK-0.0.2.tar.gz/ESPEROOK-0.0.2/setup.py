from setuptools import setup, find_packages

setup(
    name='ESPEROOK',
    version='0.0.2',  # Cambia la versión a la nueva
    license='MIT',
    description="paquete gian de insertar data dba",
    author="Gianacarlos Cardenas Galarza",
    install_requires=['numpy'],
    author_email="alex10estadistica@gmail.com",
    packages=find_packages(),
    url="https://github.com/CardenasGalarza/ESPEROOK",
    entry_points={
        'console_scripts': [
            'dbgian = mimodulo:main',  # Reemplaza 'mimodulo' con el nombre real de tu módulo y 'main' con la función principal si la tienes
        ],
    },
)
