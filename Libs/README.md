# Libraries

Make one folder for each library that you're going to use in your project and, possibly, re-use in some API. You can use the content of `lib0` as a template. **Don't forget to add a `setup.py` to each lib** you write, so that you can install it in edit mode in your environment, and reuse it in your notebooks.

## Installing each library

You should install in edit mode the libraries contained in this directory, so that you can modify them, and have the modified version directly available in your Python environment. You can do that in different ways, depending on how you manage your Python environment. 

- if you use raw virtualenvs just run `pip install -e Libs/<your_lib>` from the root of the repo.

- if you use [poetry](https://python-poetry.org/), add lines like the following in the "tool.poetry.dependencies" section of your `pyproject.toml` file located at the root of this repo, and then run `poetry install`

  ```
  libname = {path = "Libs/libname", develop = true}
  ```

