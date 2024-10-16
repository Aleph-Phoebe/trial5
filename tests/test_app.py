import unittest
from app import create_app, db
from flask_jwt_extended import create_access_token # type: ignore

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_signup(self):
        response = self.client.post('/signup', json={'username': 'testuser', 'email': 'test@example.com', 'password': 'testpass'})
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        self.client.post('/signup', json={'username': 'testuser', 'email': 'test@example.com', 'password': 'testpass'})
        response = self.client.post('/login', json={'email': 'test@example.com', 'password': 'testpass'})
        self.assertEqual(response.status_code, 200)

    def test_get_remedies(self):
        response = self.client.get('/remedies')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
