#!/usr/bin/env python3
"""Test module for the client module.
"""
import unittest
from unittest.mock import patch, Mock, MagicMock,PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from typing import Dict


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
    
    def test_public_repos_url(self) -> None:
        """Tests the `GithubOrgClient._public_repos_url` method."""
        with patch ("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
            self.assertEqual(GithubOrgClient("google")._public_repos_url, "https://api.github.com/orgs/google/repos")

