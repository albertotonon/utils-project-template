# Utility Packages

This library contains few modules that we found useful. We encourage you to rename this library and to add here other utility packages/functions/classes that you're going to use in your experiments or in your services.

## The "notebooks" package

`lib0` contains a `notebooks` package. The idea is that you should `from <your_lib_name>.notebooks import *` so that you have everything you need in your notebooks in one import. To do that, use the `__init__.py` of that package to include things you want. 

### The "paths" module

Notice the `paths.py` module contained in `notebooks`. That's conceived to be used together with [direnv](https://direnv.net/) and the `.envrc` file at the root of the repo to load relevant paths into your environments and make them available directly in your notebooks. This is good for avoiding having long path strings everywhere in your notebook and in your shell commands. See the [Pydantic BaseSettings documentation](https://pydantic-docs.helpmanual.io/usage/settings/) for more info.

## The "data" package

The package `lib0.data` contains everything you need to read datasets and more. 

First, the module `columntypes` defines the main structure of the dataset by specifying the type of each column. Once this is done, it is possible to leverage the following methods contained in `s24io` to read your datasets:
- `read_csv_list_errors` to read a DataFrame from a CSV file and get the lines generating parse errors;
- `read_csv_cast_types` to read an AutoScout dataset and get a dataframe with the right type associated to each column;
- `cast_types` to assign the right types to an AutoScout dataset contained in a dataframe.

