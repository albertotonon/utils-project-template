# Experiments
This is the experiments folder, it contains "experiment" code and experiment assets. **No dataset or credential is stored here!** Code can be in the form of python scripts, Jupyter notebooks, etc. Assets can be, for example, configurations files used to run the experiments. The structure of this folder is up to the engineer, it can be organised by experiment topic (e.g. "coverage" or "granularity"), by dataset (e.g. "Dump-20201008"), by ticket name (e.g. "S24DU-1559"), etc. 

## Python environments

It's up to the engineer to organise the Python environments and make sure that they are reproducible. We suggest to use [poetry](https://python-poetry.org/) to organise the environment of the whole repo, however, we are aware that in some cases the engineer might opt for creating an ad-hoc environment for just one experiment in order not to pollute too much the repo's environment. This is very good and in this case we suggest to have a `requirements.txt` file at the root of the experiment folder or any other information needed to make the environment reproducible. Folders called `venv` are git-ignored, thus are good candidates for containing virtual environments. In this case, libraries contained in the `Libs/` folder can be installed, for example, with `pip install -e ../Libs/<libname>`.


## Experiment data
**Experiment data, sensitive information (e.g. credentials) must _not_ be saved here**.

Data should be saved in the data directory corresponding to this project. See the README.md at the root of the repo. Use `paths.get_create_data_dir` in your code to access such a directory.

Credentials can be saved either in a `credentials.sh` file at the root of the repo (see `credentials_template.sh`), or in a file contained in the experiment directory that is **not pushed to git**. In this case we strongly recommend to use direnv and an ".envrc" file similarly to what is done at the root of this repo. The `source_up` direnv command might be useful in this case.