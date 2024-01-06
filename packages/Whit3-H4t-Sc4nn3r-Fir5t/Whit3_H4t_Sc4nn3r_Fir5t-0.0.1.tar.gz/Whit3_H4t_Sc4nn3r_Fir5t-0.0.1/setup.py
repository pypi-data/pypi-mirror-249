from setuptools import setup, find_packages

setup(
    name='Whit3_H4t_Sc4nn3r_Fir5t',
    version='0.0.1',
    description='Automation tool for scanning and analyzing vulnerabilities',
    author='Aegis0121',
    author_email='kty050121@naver.com',
    url='https://github.com/kty121/2023_Whit3_H4t_Sc4nn3r_Fir5t',
    install_requires=['requests', 'beautifulsoup4', 'python-docx', 'bs4',],
    packages=find_packages(exclude=[]),
    keywords=['Aegis0121', 'fuzzer', 'fuzzing', 'XSS', 'xss', 'Reflected', 'Cross-Site-Script', 'Cross Site Script', 'Python',],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)