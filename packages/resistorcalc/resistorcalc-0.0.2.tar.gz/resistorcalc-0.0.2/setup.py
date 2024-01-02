from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="resistorcalc",
    version='0.0.2',
    author="Hariharan C",
    description='The ResistorCal is an tool used to find the resistor values by giving the input colors',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['resistor value calculator', 'color code resistor calculator', 'resistor color to value', 'resistor code decoder', 'Electronics', 'Resistor value finder', 'color code', 'color bands', 'numeric values', 'calculate resistor value from color bands', 'online resistor color code tool', 'how to identify resistor value by color', 'resistor value conversion tool', 'resistorcal', 'resistorcal tool', 'resistorcal color code calculator', 'electronics component calculator', 'electrical engineering tool', 'color code to resistance converter', 'electronic projects resistor tool', 'learn resistor color code', 'resistor coding guide', 'educational resistor tool', 'understanding resistor color bands', 'DIY electronics resistor tool', 'compare resistor calculators', 'best resistor value tool', 'india resistor color code tool'],
    packages=find_packages(),
    entrypoints={
        'console_script': [
            'resistorcalc = resistorcalc.resistorcalc:main',
        ]
    },
    install_requires=[
    ],
)