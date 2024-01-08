from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'Test task for the Junior Python Developer position.'
LONG_DESCRIPTION = 'Test task for the Junior Python Developer position.'

# Setting up
setup(
    name="forager_task",
    version=VERSION,
    author="amato789 (Maksym Sydorchuk)",
    author_email="<maximsidorchuk@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'python-dotenv'],
    keywords=['python', 'test task', 'forager'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
