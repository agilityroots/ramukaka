[![Gitter chat](https://badges.gitter.im/agilityroots/devopsyness.png)](https://gitter.im/agilityroots/devopsyness)
[![Twitter Follow](https://img.shields.io/twitter/follow/agilityroots.svg?style=social&label=Follow)](http://twitter.com/agilityroots)
[![Website](https://raw.githubusercontent.com/agilityroots/common/master/images/agile_logo_badge_visit_us_github.png)](http://www.agilityroots.com)

# RAMUkaka

<img src="https://raw.githubusercontent.com/agilityroots/common/master/images/ramukaka_logo.png" alt="Drawing" style="width: 100px;"/>

Ramukaka, stylized as `RAMUkaka`, is the affectionate name for the chatbot in use at Agility Roots.

**About the name:**

* `RAMU` stands for Robotic Automated Monotony Undoer.
* `kaka` is an Indian vernacular term used for an [elderly uncle](http://www.shabdkosh.com/translate/%E0%A4%95%E0%A4%BE%E0%A4%95%E0%A4%BE/%E0%A4%95%E0%A4%BE%E0%A4%95%E0%A4%BE-meaning-in-Hindi-English) or sometimes, a respected helper.

## How to run

The instructions below tell you _how to get your own instance of `RAMUkaka` running_ on your own technology stack.


### 1. Satisfy Prerequisites

| What? | Version? | Why? |
|-|-|
| OS | Ubuntu 16.04 64-bit (_preferred_) | `RAMUkaka` has been tested only on Ubuntu. |
| Python | 3+ (_3.5.2 recommended_) | `RAMUkaka` uses [Errbot](http://errbot.io/en/latest/) as its bot framework, which supports Python 3. |
| `pipenv` | Latest ([Install Instructions](https://docs.pipenv.org/#install-pipenv-today)) | [Errbot installation](http://errbot.io/en/latest/user_guide/setup.html#installation) is recommended using a `virtualenv`, so `pipenv` was the natural option.<p>If you don't know what the above means, read about [Pipenv](https://docs.pipenv.org) first. |

**Note**

* In case you're wondering, [Python 3 can coexist with Python 2.](https://askubuntu.com/a/17631)
* _Some awareness of Python ecosystem_ is needed to get things running and troubleshoot.

### 2. Configure Connectivity

`RAMUkaka` can connect to the following services, so you need accounts you can use, and need to configure each service separately.

| What? | What needs to be done? |
|-|-|
| Slack | Follow the instructions for [creating a Bot token for Errbot](http://errbot.io/en/latest/user_guide/configuration/slack.html). |
| AWS | <ul><li>Create an AWS account if not already present; then create a "Bot" IAM user for `RAMUkaka`.</li><li>It is _highly recommended_ that you set a restricted policy for this user; this limits the resources available to this IAM user and prevents misuse</li><li>(for e.g. you can restrict the bot IAM user to a certain region or certain instance types).</li></ul> |

### 3. Set environment

`RAMUkaka` reads the following configuration from Environment Variables.

**AWS Connectivity**

```
ERRBOT_AWS_KEYPAIR_NAME # an AWS keypair
ERRBOT_AWS_DEFAULT_REGION # AWS region where RAMUkaka will work
ERRBOT_AWS_SECRET_KEY # AWS secret key
ERRBOT_AWS_ACCESS_KEY # AWS access key
ERRBOT_AWS_ACCOUNT_ID # account ID for AWS
```

**Slack Connectivity**

`ERRBOT_SLACK_TOKEN # Slack Token`


### 4. Initialize

* Fork or clone this repository on a laptop or server that satisfies the above requirements.
* CD to the `ramukaka` directory.
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

## About The Toolstack

We use the following toolstack to implement `RAMUkaka`.

| Tool | Why? |
|-|-|
| [Errbot](https://www.errbot.io) | The Bot framework, based on Python |
| [spaCy](https://www.spacy.io) | For NLP and ML implementation within `RAMUkaka` |
| [Apache libcloud](https://libcloud.readthedocs.io) | Python connectivity to any virtualization provider. |
| `py.test` | Test Cases for the bot. |

### Testing


## References

Errbot

1. Testing Errbot: http://errbot.io/en/latest/user_guide/plugin_development/testing.html
1. Errbot: plugin development: http://errbot.io/en/latest/user_guide/plugin_development/development_environment.html
1. Errbot Getting Started: http://errbot.io/en/latest/index.html
1. http://errbot.io/en/latest/user_guide/setup.html
1. http://errbot.io/en/latest/user_guide/configuration/slack.html
1. `config.py` template: https://github.com/errbotio/errbot/blob/master/errbot/config-template.py
1. AWS plugin for errbot adapter from https://github.com/jvasallo/err-plugins/blob/master/err-aws/aws.py

Apache libcloud

1. [API Docs and Examples](https://libcloud.readthedocs.io/en/latest/compute/index.html#examples)
