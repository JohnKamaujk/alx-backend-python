#!/usr/bin/env python3
"""Test module for the client module.
"""
import unittest
from unittest.mock import patch, Mock, MagicMock
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
        """Tests the `GithubOrgClient.org` function output."""
        mocked_get_json.return_value = MagicMock(return_value=payload)
        github_client = GithubOrgClient(org_name)
        self.assertEqual(github_client.org(), payload)
        mocked_get_json.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org_name)
        )
