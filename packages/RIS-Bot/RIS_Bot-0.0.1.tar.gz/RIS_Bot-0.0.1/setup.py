import setuptools

setuptools.setup(
    name = "RIS_Bot",
    version = "0.0.1",
    author = "Tobia Ippolito",
    description = "This package contains a pytorch GPT-2 interactive calm story chatbot.",
    packages = ["RIS_bot"],
    url = "https://github.com/xXAI-botXx/RIS-Bot/tree/RIS-PyPI",
    license = "Mozilla Public License Version 2.0",
    python_requires='>=3.8, <=3.10',
    install_requires=['transformers',
                      'torch'],
    readme = "README.md",
    classifiers=[
        'Intended Audience :: Science/Research',        
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)