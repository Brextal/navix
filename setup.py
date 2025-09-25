from setuptools import setup

setup(
    name='navix',
    version='1.0.0',
    py_modules=['main', 'core', 'actions', 'utils', 'log'],
    include_package_data=True,
    install_requires=[
        'prompt_toolkit>=3.0.0',
        'Pillow>=9.0.0',
        # Agrega otras dependencias si las usas (ej. click, rich, etc.)
    ],
    entry_points={
        'console_scripts': [
            'navix = main:main',
        ],
    },
    author='Brextal',
    description='Explorador de archivos en terminal con vista de imágenes usando Kitty',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license='MIT',
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Topic :: Utilities',
        'Topic :: System :: Shells',
        'Topic :: Software Development :: User Interfaces',
    ],
)
