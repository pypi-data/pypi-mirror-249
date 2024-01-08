# Installation

## Pip Command

```
pip install skydataplanelibs --index-url https://__token__:<your_personal_token>@gitlab.com/api/v4/projects/42839027/packages/pypi/simple
```

You will need a personal access token.

## Registry setup

If you haven't already done so, you will need to add the below to your .pypirc file.

```
[gitlab]
repository = https://gitlab.com/api/v4/projects/42839027/packages/pypi
username = __token__
password = <your personal access token>
```

For more information on the PyPi registry, see the documentation.