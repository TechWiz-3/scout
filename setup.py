from setuptools import setup, find_packages
#from pathlib import Path

#project_dir = Path(__file__).parent
#long_description = (project_dir / "README.md").read_text()

setup(
    name="gh-scout",
    url="https://github.com/TechWiz-3/scout",
    author="Zac the Wise aka TechWiz-3",
    version='0.1.0',
    description="⭐ Find hacktoberfest repos to contribute to from your CLI",
#    long_description_content_type='text/markdown',
#    long_description=long_description,
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        scout=scout.main:cli
    ''',
    instal_requires=["rich"],
)
