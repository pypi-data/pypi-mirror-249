import re
import os
import subprocess

import requests

import biolib.api
from biolib import biolib_errors
from biolib.typing_utils import Optional
from biolib.biolib_api_client.auth import BearerAuth
from biolib.biolib_api_client import BiolibApiClient, AppGetResponse
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger


def _get_git_branch_name() -> str:
    try:
        github_actions_branch_name = os.getenv('GITHUB_REF_NAME')
        if github_actions_branch_name:
            return github_actions_branch_name

        gitlab_ci_branch_name = os.getenv('CI_COMMIT_REF_NAME')
        if gitlab_ci_branch_name:
            return gitlab_ci_branch_name

        result = subprocess.run(['git', 'branch', '--show-current'], check=True, stdout=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except BaseException:
        return ''


def _get_git_repository_url() -> str:
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], check=True, stdout=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except BaseException:
        return ''


class BiolibAppApi:

    @staticmethod
    def get_by_uri(uri: str) -> AppGetResponse:
        # Replace protocol with @ (if supplied)
        uri = re.sub(r'^http(s)?://', '@', uri)
        # Replace frontend version path with app_uri compatible version (if supplied)
        uri = re.sub(r'/version/(?P<version>(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*))(/)?$', r':\g<version>', uri)

        try:
            response = biolib.api.client.get(path='/app/', params={'uri': uri})
            app_response: AppGetResponse = response.json()
            return app_response

        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise biolib_errors.NotFound(f'Application {uri} not found.') from None

            if error.response.status_code == 400:
                raise biolib_errors.BioLibError(error.response.content.decode()) from None

            raise error

    @staticmethod
    def push_app_version(
            app_id,
            zip_binary,
            author,
            app_name,
            set_as_active,
            app_version_id_to_copy_images_from: Optional[str],
    ):
        response = requests.post(
            f'{BiolibApiClient.get().base_url}/api/app_versions/',
            files={
                'source_files_zip': zip_binary,
            },
            data={
                'app': app_id,
                'set_as_active': 'true' if set_as_active else 'false',
                'state': 'published',
                'app_version_id_to_copy_images_from': app_version_id_to_copy_images_from,
                'git_branch_name': _get_git_branch_name(),
                'git_repository_url': _get_git_repository_url(),
            },
            auth=BearerAuth(BiolibApiClient.get().access_token)
        )
        if not response.ok:
            logger.error(f'Push failed for {author}/{app_name}:')
            raise BioLibError(response.text)

        # TODO: When response includes the version number, print the URL for the new app version
        logger.info(f'Initialized new app version for {author}/{app_name}.')
        return response.json()
