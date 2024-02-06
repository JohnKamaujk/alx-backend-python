#!/usr/bin/env python3
"""Test module for the client module.
"""
import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Dict
from requests import HTTPError
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests the `GithubOrgClient` class."""
    @parameterized.expand([
        ("google", {'name': "episodes.dart"}),
        ("abc", {'name': "abc.github.io"})
    ])
    @patch('client.get_json')
    def test_org(self,
                 org_name: str,
                 payload: Dict,
                 mocked_get_json: MagicMock) -> None:
        """Tests the `GithubOrgClient.org` method output."""
        mocked_get_json.return_value = MagicMock(return_value=payload)
        github_client = GithubOrgClient(org_name)
        self.assertEqual(github_client.org(), payload)
        mocked_get_json.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org_name)
        )

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    def test_public_repos_url(self, org_name: str, org_payload: Dict) -> None:
        """Tests the `GithubOrgClient._public_repos_url` property."""
        # Use patch as a context manager to mock the org property
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock,
                   return_value=org_payload):
            # Create an instance of GithubOrgClient
            github_client = GithubOrgClient(org_name)
            # Access the _public_repos_url property
            result = github_client._public_repos_url

            expected_url = org_payload['repos_url']
            self.assertEqual(result, expected_url)

    @patch('client.get_json',
           return_value=[{"name": "episodes.dart"}, {"name": "kratu"}])
    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock,
           return_value='https://api.github.com/orgs/google/repos')
    def test_public_repos(self, mock_public_repos_url, mock_get_json) -> None:
        """Tests the `GithubOrgClient.public_repos` method."""
        github_client = GithubOrgClient('google')
        repos = github_client.public_repos()
        expected_repos = ["episodes.dart", "kratu"]

        self.assertEqual(repos, expected_repos)

        # Assert that the mocked property and mocked get_json were called once
        mock_public_repos_url.assert_called_once_with()
        mock_get_json.assert_called_once_with(
            'https://api.github.com/orgs/google/repos'
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self,
                         repo: Dict,
                         license_key: str,
                         expected_result: bool) -> None:
        """Tests the `GithubOrgClient.has_license` method."""
        github_client = GithubOrgClient('abc')
        result = github_client.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Performs integration tests for the `GithubOrgClient` class."""
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class fixtures before running tests."""
        url_payload_mapping = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_mock_response(url):
            if url in url_payload_mapping:
                return Mock(**{'json.return_value': url_payload_mapping[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_mock_response)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests the `public_repos` method."""
        repos = GithubOrgClient("google").public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the class fixtures after running all tests."""
        cls.get_patcher.stop()
