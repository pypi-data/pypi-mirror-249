from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='e2e_similarity',
    version='0.1',
    description='This is a package that utilizes OpenAI\'s powerful davinci-003 model to run Cypress tests, gather and parse the logs, and generate a comprehensive report. Users can specify their test directory when running the command. The package is designed to help developers automate their testing process and gain insights from the test logs.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'openai',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'check-similarity=e2e_similarity.run_commands:main'
        ]
    }
)