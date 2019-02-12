from app import app

import unittest


class RouteTest(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_api_play_game(self):
        tester = app.test_client(self)
        response = tester.post('/api/play_game', data=dict(
            iterations=1,
            username='Arastorn',
            password='testBot',
            teamfile="overpowered.txt",
            challenge="ArastornChal"
        ), follow_redirects=True)
        self.assertEqual(response.status_code,200)


if __name__ == '__main__':
    unittest.main()
