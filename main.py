#
# python main.py \
#   --phabricator-url=https://my.phabricator.com \
#   --arc-executable=/somewhere/arcanist/bin/arc changelog \
#   --since=2016-01-01
#

from datetime import datetime, timedelta
import subprocess
import click
import json
import re


@click.group()
@click.option('--arc-executable', help='Path to the ARC executable', default='arc')
@click.option('--phabricator-url', help='Phabricator URL', prompt=True)
@click.version_option(version='0.0.2')
@click.pass_obj
def cli(obj, arc_executable, phabricator_url):
    obj['arc'] = arc_executable
    obj['phabricator'] = phabricator_url


@cli.command()
@click.pass_obj
def repositories(obj):
    for repo in __repositories(obj):
        click.echo('[{: >20}] {}'.format(repo['callsign'], repo['name']))


@cli.command()
@click.option('--branch', help='Branch to analyze', default='master')
@click.option('--regexp', help='RegExp for the merge commit', default='^Merged in T([\d]+)')
@click.option(
    '--since', help='Generate since particular %Y-%m-%d',
    default=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
)
@click.pass_obj
def changelog(obj, branch, regexp, since):
    since = datetime.strptime(since, '%Y-%m-%d')
    checkpoint = int(since.strftime("%s"))

    limit = (datetime.now() - since).days * 4
    if limit > 1000:
        limit = 1000

    for repo in __repositories(obj):
        tickets = {}
        result = call_arc(obj, 'diffusion.querycommits', repositoryPHID=repo['phid'], limit=limit)

        for commit in sorted(
            result['data'].values(), reverse=True,
            cmp=lambda x, y: cmp(int(x['epoch']), int(y['epoch']))
        ):
            if int(commit['epoch']) < checkpoint:
                break

            match = re.search(regexp, commit['summary'])
            if match and match.group(1) not in tickets:
                tickets[match.group(1)] = commit['identifier']

        if not len(tickets):
            continue

        for task_id in tickets.keys():
            refs = call_arc(
                obj, 'diffusion.branchquery', callsign=repo['callsign'], contains=tickets[task_id],
                limit=100
            )
            if not len(filter(lambda e: e['shortName'] == branch, refs)):
                del tickets[task_id]

        if len(tickets):
            click.echo('##{} ({})##'.format(repo['name'], len(tickets)))

        for task_id in sorted(tickets.keys(), reverse=True):
            task = call_arc(obj, 'maniphest.info', task_id=task_id)
            click.echo(
                ' - [[ {} | {} ]]: {}'.format(
                    task['uri'], task['objectName'],
                    task['title'].encode('ascii', 'ignore').decode('utf-8')
                )
            )

    click.echo(
        '`* changelog since {:%Y-%m-%d} until {:%Y-%m-%d} ({})`'
        .format(since, datetime.now(), branch)
    )


def call_arc(obj, endpoint, **kwargs):
    p = subprocess.Popen(
        [obj['arc'], '--conduit-uri', obj['phabricator'], 'call-conduit', endpoint],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )

    result = json.loads(p.communicate(json.dumps(kwargs))[0].decode('UTF-8'))
    if result['error']:
        raise ValueError(result['errorMessage'])

    return result['response']


def __repositories(obj):
    for repo in call_arc(obj, 'repository.query', limit=1000):
        if not repo['isActive']:
            continue
        yield repo


cli(obj={})
