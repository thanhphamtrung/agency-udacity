# import os
# import unittest
# import json
# from flask_sqlalchemy import SQLAlchemy
# from app import create_app
# from models import setup_db, Movie, Actor
# from auth import AuthError

# class CastingAgencyTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app()
#         self.client = self.app.test_client

#         # Set up a test database URI (e.g., SQLite) to avoid using the production database
#         self.database_path = "sqlite:///test.db"
#         self.app.config['SQLALCHEMY_DATABASE_URI'] = self.database_path
#         self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#         with self.app.app_context():
#             setup_db(self.app)
#             # Create some initial test data
#             self.actor = Actor(name="Test Actor", age=30, gender="Male")
#             self.actor.insert()
#             self.movie = Movie(title="Test Movie", release_date="2023-12-31")
#             self.movie.insert()

#     def tearDown(self):
#         pass  # You can implement teardown logic here if needed

#     # Test the GET /actors endpoint
#     def test_get_actors(self):
#         res = self.client().get('/actors')
#         data = json.loads(res.data)

#         self.assertEqual(res.status_code, 200)
#         self.assertTrue(data['success'])
#         self.assertTrue(len(data['actors']) > 0)

#     # # Test the GET /movies endpoint
#     # def test_get_movies(self):
#     #     res = self.client().get('/movies')
#     #     data = json.loads(res.data)

#     #     self.assertEqual(res.status_code, 200)
#     #     self.assertTrue(data['success'])
#     #     self.assertTrue(len(data['movies']) > 0)

#     # Add more test methods for other endpoints...

# if __name__ == "__main__":
#     unittest.main()
