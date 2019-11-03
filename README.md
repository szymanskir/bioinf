![Travis CI](https://travis-ci.com/szymanskir/bioinf.svg?token=vMgapB9HzV6RFvox4Fiq&branch=master)
![codecov](https://codecov.io/gh/szymanskir/bioinf/branch/master/graph/badge.svg)


# Bioinf

Python Implementation of the Needleman-Wunsch algorithm for bioinformatics classes at the Warsaw University of Technology.

# Instructions
The package provides a CLI tool for aligning dna sequence using the Needleman-Wunch algorithm. Install the package using the following instructions:

```
git clone https://github.com/szymanskir/bioinf
cd bioinf
python3.7 -m venv .env
source .env/bin/activate
pip install -r requirements_dev.txt
make install
```

Sample files have been included in the repository. Run the following command for an example usage of the tool:
```
bioinf align -a a.txt -b b.txt -c config.ini -o output.txt
```

# Configuration file
In order to align protein sequence using the `bioinf` tool it is required to provide a configuration. The content of the example configuration file (`config.ini`) along with explanation of all fields is presented below:

```
[DEFAULT]
same = 5
diff = -5
gap_penalty = -2
max_seq_length = 10
max_number_paths = 5
```

`same` - score value for when sequence parts match

`diff` - score value for when sequence parts do not match

`gap_penalty` - score value when gap is insterted into one of the sequences

`max_seq_length` - maximum length of a processed sequence

`max_number_paths` - maximal number of path alignemnts to retrieve

# Credits
This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

* Cookiecutter: https://github.com/audreyr/cookiecutter
* `audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
