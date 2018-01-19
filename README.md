# RAMUkaka

<img src="https://raw.githubusercontent.com/agilityroots/common/master/images/ramukaka_logo.png" alt="Drawing" style="width: 100px;"/>

Ramukaka, stylized as `RAMUkaka`, is the affectionate name for the chatbot in use at Agility Roots.

**About the name:**

* `RAMU` stands for Robotic Automated Monotony Undoer.
* `kaka` is an Indian vernacular term used for an [elderly uncle](http://www.shabdkosh.com/translate/%E0%A4%95%E0%A4%BE%E0%A4%95%E0%A4%BE/%E0%A4%95%E0%A4%BE%E0%A4%95%E0%A4%BE-meaning-in-Hindi-English) or sometimes, a respected helper.

## How to run

### 1. Satisfy Prerequisites

| What? | Version? | Why? |
|-|-|
| OS | Ubuntu 16.04 64-bit (_preferred_) | `RAMUkaka` has been tested only on Ubuntu. |
| Python | 3+ (_3.5.2 recommended_) | `RAMUkaka` uses [Errbot](http://errbot.io/en/latest/) as its bot framework, which supports Python 3. |
| `pipenv` | Latest ([Install Instructions](https://docs.pipenv.org/#install-pipenv-today)) | [Errbot installation](http://errbot.io/en/latest/user_guide/setup.html#installation) is recommended using a `virtualenv`, so `pipenv` was the natural option. |

**Note**

* In case you're wondering, [Python 3 can coexist with Python 2.](https://askubuntu.com/a/17631)


### 2. Configure Connectivity

`RAMUkaka` can connect to the following services, so you need accounts you can use.

| What? | What needs to be done? |
|-|-|
| Slack | Follow the instructions for [creating a Bot token for Errbot](http://errbot.io/en/latest/user_guide/configuration/slack.html). |
| AWS | Create an AWS account. It is _highly recommended_ that you create an IAM user in AWS that the Bot can use. |

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
