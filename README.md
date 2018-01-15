# RAMUkaka

<img src="https://raw.githubusercontent.com/agilityroots/common/master/images/ramukaka_logo.png" alt="Drawing" style="width: 200px;"/>

Ramukaka, stylized as `RAMUkaka`, is the affectionate name for the chatbot in use at Agility Roots.


**About the name:**

* `RAMU` stands for Robotic Automated Monotony Undoer.
* `kaka` is an affectionate patronymic, usually for an elderly person or sometimes, a helper that has been with you for many years.


## How to run

### Initialize

* Note: Errbot requires Python 3 so make sure you have it. [Python 3 can coexist with Python 2.](https://askubuntu.com/a/17631)
* This directory is a `pipenv` environment so `cd` to this directory and run:

```
pipenv install
```

The above command installs the dependencies mentioned in the [`Pipfile`](Pipfile). To load these dependencies you need to run:

```
pipenv shell
```

This creates a new shell process for you where you can start Errbot: just run `errbot`.

## Run Errbot

* *Run Errbot (local shell)*: Run `errbot -T`.
* *Run Errbot (connecting to Slack)*: Run `errbot`.
* *Exit Errbot console*: `Ctrl-D` or `Ctrl-C`

## References

1. Errbot: plugin development: http://errbot.io/en/latest/user_guide/plugin_development/development_environment.html
1. Errbot Getting Started: http://errbot.io/en/latest/index.html
1. http://errbot.io/en/latest/user_guide/setup.html
1. http://errbot.io/en/latest/user_guide/configuration/slack.html
1. `config.py` template: https://github.com/errbotio/errbot/blob/master/errbot/config-template.py
1. AWS plugin for errbot adapter from https://github.com/jvasallo/err-plugins/blob/master/err-aws/aws.py
