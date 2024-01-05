from setuptools import setup, find_packages

setup(
    name='dbgian',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Aquí puedes agregar las dependencias si las tienes
    ],
    entry_points={
        'console_scripts': [
            'dbgian = mimodulo:main',  # Reemplaza 'mimodulo' con el nombre real de tu módulo y 'main' con la función principal si la tienes
        ],
    },
)

