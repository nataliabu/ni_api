from flask import Flask
from flask_testing import TestCase
import unittest
import main

# Child of TestCase and Parent to all Test Clases
class NITestCase(TestCase):

    def create_app(self):
        app = main.app
        # Creates a testing database(that runs in RAM)
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['TESTING'] = True
        return app

    def setUp(self):
        main.db.create_all()

    def tearDown(self):
        main.db.session.remove()
        main.db.drop_all()

    # Populates the testing database
    def fixtures(self):
        obj1 = main.DataTable(key = "key1", value = "foo")
        obj2 = main.DataTable(key = "key2", value = "bar")
        main.db.session.add(obj1)
        main.db.session.add(obj2)
        main.db.session.commit()


class TestIndex(NITestCase):

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.json, "Hello NI!")


class TestGetAll(NITestCase):

    def test_db_empty(self):
        response = self.client.get("/keys")
        self.assertEqual(response.json, [])

    def test_db_populated(self):
        self.fixtures()
        response = self.client.get("/keys")
        self.assertEqual(response.json, [{"key1": "foo"}, {"key2": "bar"}])


class TestGetValue(NITestCase):

    def test_value_existent(self):
        self.fixtures()
        response = self.client.get("/keys/key2")
        self.assertEqual(response.json, "bar")

    def test_value_unexistent(self):
        self.fixtures()
        response = self.client.get("/keys/key3")
        self.assertEqual(response.json, "Not Found")
        self.assert404(response)


class TestDeleteAll(NITestCase):

    def test_delete_all(self):
        self.fixtures()
        response = self.client.delete("/keys")
        self.assertEqual(response.json, "Deleting all database entries")
        self.assert200(response)
        response = self.client.get("/keys")
        self.assertEqual(response.json, [])


if __name__ == '__main__':
    unittest.main()
