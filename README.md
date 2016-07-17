Phabricator merged tasks
========================

## How it works
- Normally, a team uses some kind of [pull request review](https://en.wikipedia.org/wiki/Distributed_version_control#Pull_requests) technique.
  The final step is an automatic merging. This step creates a new merge commit with pre-defined template (i.e. `Merged in T1234 (pull request #4321) T1234`).
- Python script finds such commits and it generates a changelog referencing the ticket.
- Also it is possible to add a project (label) to a specific ticket, just to query it later.

## Requirements
- python 2+
- [arcanist](https://secure.phabricator.com/book/phabricator/article/arcanist/)
- pip
- Optional, but preferred: [virtualenvs](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

## Install
```bash
# install arcanist Credentials
arc install-certificate

# install requirements
[sudo] pip install -r requirements.txt
```

## Run
```bash
python main.py \
  --arc-executable=/somewhere/arcanist/bin/arc changelog \
  --phabricator-url=https://my.phabricator.com \
  --branch=prod \
  --since=2016-01-01

python main.py \
  --arc-executable=/somewhere/arcanist/bin/arc repositories
```

## Wiki update script

#### Preparation (the first run only)
```bash
echo 2016-01-01 > /path/to/repository/.checkpoint
```

#### Integration example
```bash
(
  cd /path/to/repository

  # the next 2 lines are for virtualenvwrapper only
  source /usr/local/bin/virtualenvwrapper.sh
  workon my-namespace

  # create a new wiki page
  ./update-wiki.sh $WIKI_NAMESPACE $BRANCH /somewhere/arcanist/bin/arc

  # you can also apply a project if needed
  ./update-wiki.sh $WIKI_NAMESPACE $BRANCH /somewhere/arcanist/bin/arc $PHID
)
```