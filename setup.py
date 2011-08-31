from distutils.core import setup


VERSION = __import__("mediaman").__version__


setup(
    name = "mimesis-mediaman",
    version = VERSION,
    author = "Midwest Communications",
    #author_email = "development@eldarion.com",
    description = "media management frontend",
    long_description = open("README").read(),
    #license = "BSD",
    url = "https://github.com/MidwestCommunications/mimesis-mediaman",
    packages = [
        "mediaman",
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)

