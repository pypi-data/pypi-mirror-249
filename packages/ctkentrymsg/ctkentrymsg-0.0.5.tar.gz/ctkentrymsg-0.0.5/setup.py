from setuptools import find_packages, setup

long_description = ''
change_log = ''
with open('README.md', 'r') as fh:
    long_description = fh.read()
with open('CHANGELOG.md', 'r') as fh:
    change_log = fh.read()

setup(
    name='ctkentrymsg',
    version='0.0.5',
    description='CTkEntry widget with message functionality',
    author='Shine Jayakumar',
    author_email='shinejayakumar@yahoo.com',
    packages=find_packages(),
    long_description=f'{long_description}\n\n\n{change_log}',
    long_description_content_type='text/markdown',
    url='https://github.com/shine-jayakumar/CTkEntryMsg',
    license='MIT',
    project_urls={
        'Documentation': 'https://github.com/shine-jayakumar/CTkEntryMsg',
        'Source': 'https://github.com/shine-jayakumar/CTkEntryMsg'
    },
    keywords=['ctkentrymsg', 'customtkinter', 'tkinter', 'ctkentry' ,' ctkentry-show-message'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=["customtkinter"],
    python_requires=">=3.7"
)