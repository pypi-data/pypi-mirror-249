import unittest
from datetime import datetime

from votifier import VoteV1


class TestVoteV1(unittest.TestCase):
    def test_payload(self):
        vote = VoteV1(
            service_name='TestService',
            username='foobar',
            address='127.0.0.1',
            timestamp=datetime.fromtimestamp(1620000000),
        )
        self.assertEqual(str(vote), 'VOTE\nTestService\nfoobar\n127.0.0.1\n1620000000000\n')
