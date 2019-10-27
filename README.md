# Bioinf

Python Implementation of the Needleman-Wunsch algorithm for bioinformatics classes at the Warsaw University of Technology.

# Instructions
The package provides a CLI tool for aligning dna sequence using the Needleman-Wunch algorithm. Install the package using the following instructions:

```
git clone www.github.com/szymanskir/bioinf
cd bioinf
python3.7 -m venv .env
source .env/bin/activate
make install
```

Sample files have been included in the repository. Run the following command for an example usage of the tools:
```
bioinf align -a a.txt -b b.txt -c config.ini
```

# Credits
This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

* Cookiecutter: https://github.com/audreyr/cookiecutter
* `audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
