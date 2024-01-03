import setuptools
setuptools.setup(
    name='gamestoreapi',
    version='0.1',
    author='guard_games',
    author_email='sourceguy68@gmail.com',
    description='a pip package to interact with my game store',
    packages=setuptools.find_packages(),
    keywords=['python', 'game store', 'gamestore', 'api', 'achievements'],
    install_requires=[
        'requests',
    ],
     classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)