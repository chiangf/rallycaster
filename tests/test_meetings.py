import unittest
from mock import patch
from flask.ext.pymongo import PyMongo
import rallycaster
from tests import utilities


class MeetingsTestCase(unittest.TestCase):
    def setUp(self):
        rallycaster.mongo = PyMongo(rallycaster.app, config_prefix="MONGOTEST")
        rallycaster.app.config['TESTING'] = True
        self.app = rallycaster.app.test_client()

        self.patcher = patch("rallycaster.interfaces.authentication.get_user_from_session")
        self.mocker = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_get_meetings(self):
        response = self.app.get('/api/meetings/')
        meetings = utilities.get_response_data(response)['meetings']

        self.assertGreater(len(meetings), 0)


if __name__ == '__main__':
    unittest.main()
