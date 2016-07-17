Phabricator merged tasks
========================

## How it works
- Normally, a team uses some kind of [pull request review](https://en.wikipedia.org/wiki/Distributed_version_control#Pull_requests) technique.
  The final step is an automatic merging. This step creates a new merge commit with pre-defined template (i.e. `Merged in T1234 (pull request #4321) T1234`).
- Python script finds such commits and it generates a changelog referencing the ticket according a branch.
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

## License
The MIT License (MIT)
Copyright (c) 2016 Kanstantsin Kamkou <2ka.by>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
