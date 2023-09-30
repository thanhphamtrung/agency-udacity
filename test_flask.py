import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie

MOCK_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ii1iNEx2bXNoaGJYOXllSDhOWFpPQSJ9.eyJpc3MiOiJodHRwczovL3RoYW5ocGhhbXRydW5nLmpwLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTE3ZWYyZWY0YzAwZTk0YmYyMjFmZGMiLCJhdWQiOiJhZ2VuY3kiLCJpYXQiOjE2OTYwODM3MzYsImV4cCI6MTY5NjE3MDEzNiwiYXpwIjoiQVQxYWlXeUw5bmNNM2RINlZGdFZUbEpxV0NnSEVMOGsiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.keQu244P_x-j-LKEMSxcvDVRJDlELhe7awF_QV_6heRwCxlX-U4ulWM_UrETS_q5wSd7zoCZd2afq_TLZzXHrczZ8d5sAAPZFOA1jNtG15q6ModWc7prPJ5VQdR1LmRFVlQrnjFy_qSJgFKz0PjNDEkLbh68kBJPQDQSCAI-SS8kzMTja3-XffdoQJo1q8infjR6vGfMkWkoJZxtgym2RGBMS3DZ7Sk4iSm7olnldMNEBTG5RW0xNY_07Y637gpd594Lqgi16BVLJZGeaxt5IuRVsFT_v1R-3B98uIsTT3_Wuhf4Ymorj-sLUgikebisJTm2f9s1yKjjU5J3AlFWlg'

class AgencyTestCase(unittest.TestCase):
    """This class represents the agency's test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            # create all tables
            self.db.create_all()

            # Insert dummy movie data into the database
            movie = Movie(title="Dummy Movie 1", release_date="2022-01-01")
            movie.insert()

            movie = Movie(title="Dummy Movie 2", release_date="2022-02-01")
            movie.insert()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def get_headers(self):
        return {'Authorization': 'Bearer ' + MOCK_TOKEN}
    
    def test_should_return_all_actors(self):
        actor = Actor(name="Leonardo Di Caprio", age="45", gender="male")
        actor.insert()

        res = self.client().get('/actors', headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_get_movies_not_found(self):
        res = self.client().get('/movies/999', headers=self.get_headers())

        self.assertEqual(res.status_code, 404)


    def test_create_movie(self):
        new_movie = {
            'title': 'New Movie',
            'release_date': '2022-01-01'
        }
        res = self.client().post('/movies', json=new_movie, headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertTrue(data['movie'])

    def test_update_movie(self):
        movie_id = Movie.query.first().id
        updated_data = {
            'title': 'Updated Movie Title'
        }
        res = self.client().patch(f'/movies/{movie_id}', json=updated_data, headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_movie_not_found(self):
        movie_id = 999
        updated_data = {
            'title': 'Updated Movie Title'
        }
        res = self.client().patch(f'/movies/{movie_id}', json=updated_data, headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

    def test_delete_movie(self):
        movie_id = Movie.query.first().id
        res = self.client().delete(f'/movies/{movie_id}', headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_movie_id'], movie_id)

    def test_delete_movie_not_found(self):
        movie_id = 999
        res = self.client().delete(f'/movies/{movie_id}', headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_get_actors_not_found(self):
        res = self.client().get('/actors/999', headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

    def test_create_actor(self):
        new_actor = {
            'name': 'New Actor',
            'age': 30,
            'gender': 'Male'
        }
        res = self.client().post('/actors', json=new_actor, headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertTrue(data['actor'])

    def test_update_actor(self):
        actor_id = Actor.query.first().id
        updated_data = {
            'name': 'Updated Actor Name'
        }
        res = self.client().patch(f'/actors/{actor_id}', json=updated_data, headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_update_actor_not_found(self):
        actor_id = 999
        updated_data = {
            'name': 'Updated Actor Name'
        }
        res = self.client().patch(f'/actors/{actor_id}', json=updated_data, headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

    def test_delete_actor(self):
        actor_id = Actor.query.first().id
        res = self.client().delete(f'/actors/{actor_id}',headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted_actor_id'], actor_id)

    def test_delete_actor_not_found(self):
        actor_id = 999
        res = self.client().delete(f'/actors/{actor_id}', headers=self.get_headers())
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)

if __name__ == "__main__":
    unittest.main()
