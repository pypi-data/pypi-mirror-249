from .base import Notification
from . import changelog
import logging
import requests


log = logging.getLogger(__name__)


class SlackRelease(Notification):

    def __call__(self, channel_name, token, emoji,
                 vcs_url=None, changelog_url=None):
        if not vcs_url:
            vcs_url = f'http://github.com/ZeitOnline/{self.project}/tree/{self.version}'
        if not changelog_url:
            changelog_url = f'http://github.com/ZeitOnline/{self.project}/blob/main/CHANGES.rst'

        with requests.Session() as http:
            r = http.post(
                f'http://hackbot.zon.zeit.de/{token}/deployment/{channel_name}',
                json={
                    'project': self.project,
                    'environment': self.environment,
                    'version': self.version,
                    'emoji': emoji,
                    'vcs_url': vcs_url,
                    'changelog_url': changelog_url,
                })
            log.info('%s returned %s: %s', r.url, r.status_code, r.text)


class SlackPostdeploy(Notification):

    def __call__(self, channel_id, filename, slack_token, github_token):
        t = changelog.download_changelog(
            github_token, self.project, self.version, filename)
        postdeploy = changelog.extract_postdeploy(t)
        if not postdeploy:
            log.info(
                'No postdeploy entries found in %s %s', self.project, filename)
            return

        with requests.Session() as http:
            r = http.post(
                'https://slack.com/api/chat.postMessage', json={
                    'channel': channel_id,
                    'text': f'```\n{postdeploy}\n```'
                }, headers={'Authorization': f'Bearer {slack_token}'})
            log.info('%s returned %s: %s', r.url, r.status_code, r.text)
