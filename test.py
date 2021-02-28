from flask import Flask
from flask_testing import TestCase
import unittest
import main
import json

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


class TestDeleteValue(NITestCase):

    def test_delete_value_existent(self):
        self.fixtures()
        response = self.client.delete("/keys/key1")
        self.assertEqual(response.json, "Database entry succesfully deleted")
        self.assert200(response)
        response = self.client.get("/keys")
        self.assertEqual(response.json, [{"key2": "bar"}])

    def test_delete_value_unexistent(self):
        response = self.client.delete("/keys/key1")
        self.assertEqual(response.json, "Not Found")
        self.assert404(response)


class TestCheckValue(NITestCase):

    def test_check_value_existent(self):
        self.fixtures()
        response = self.client.head("/keys/key1")
        self.assert200(response)

    def test_check_value_unexistent(self):
        response = self.client.head("/keys/key1")
        self.assert404(response)


class SetValue(NITestCase):
    my_data = {"key1": "baz"}
    my_headers = {'content-type': 'application/json'}

    def test_set_new_key_value(self):
        response = self.client.put(
                "/keys",
                data=json.dumps(self.my_data),
                headers=self.my_headers
                )
        self.assert200(response)
        self.assertEqual(response.json, "Setting value")
        response = self.client.get("/keys/key1")
        self.assertEqual(response.json, "baz")

    def test_set_existing_key_new_value(self):
        self.fixtures()
        response = self.client.get("/keys/key1")
        self.assertEqual(response.json, "foo")
        response = self.client.put(
                "/keys",
                data=json.dumps(self.my_data),
                headers=self.my_headers
                )
        self.assert200(response)
        self.assertEqual(response.json, "Setting value")
        response = self.client.get("/keys/key1")
        self.assertEqual(response.json, "baz")

    def test_set_no_json_content_type(self):
        response = self.client.put(
                "/keys",
                data=json.dumps(self.my_data)
                )
        self.assert400(response)
        self.assertEqual(response.json, "json expected as Content-Type")
        response = self.client.get("/keys")
        self.assertEqual(response.json, [])

    def test_set_no_dict(self):
        response = self.client.put(
                "/keys",
                data=json.dumps("I am not a dict"),
                headers=self.my_headers
                )
        self.assert400(response)
        self.assertEqual(response.json,
                "Expected a dictionary with a string as a key and a string as its value")
        response = self.client.get("/keys")
        self.assertEqual(response.json, [])

    def test_set_val_is_not_str(self):
        response = self.client.put(
                "/keys",
                data=json.dumps({"key1": [1, 2, 3]}),
                headers=self.my_headers
                )
        self.assert400(response)
        self.assertEqual(response.json,
                "Expected a dictionary with a string as a key and a string as its value")
        response = self.client.get("/keys")
        self.assertEqual(response.json, [])


if __name__ == '__main__':
    unittest.main()
