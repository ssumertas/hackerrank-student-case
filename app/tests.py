from django.test import TestCase

# Create your tests here.
from json import JSONDecodeError

from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import RequestsClient

HOST = 'http://127.0.0.1:8000'

student_1_params = dict(
    first_name="Scarlett",
    last_name="Evans",
    date_of_birth="2010-05-01",
    grade=8,
    phone="+11111111111",
    email="scarlet@email.com"
)

student_2_params = dict(
    first_name="Lily",
    last_name="Davies",
    date_of_birth="2010-03-15",
    grade=8,
    phone="+11222222222",
    email="lily@email.com"
)


class CreateStudentTest(TestCase):
    def setUp(self) -> None:
        self.client = RequestsClient()
        self.url = HOST + '/students/'

    def test_student_creation(self):
        r = self.client.post(self.url, data=student_1_params)
        self.assertEquals(r.status_code, status.HTTP_201_CREATED)
        data = r.json()
        self.assertIn('id', data)
        self.assertTrue(isinstance(data['id'], int))
        del data['id']
        self.assertDictEqual(student_1_params, data)


class TestGetAllStudents(TestCase):
    def setUp(self) -> None:
        self.client = RequestsClient()
        self.url = HOST + '/students/'

        students = [
            student_1_params,
            student_2_params
        ]

        try:
            self.students = [self.client.post(self.url, data=student).json() for student in students]
        except JSONDecodeError:
            self.fail('/students/ endpoint for POST request not implemented correctly')
        self.students.sort(key=lambda student: student['id'])

    def test_get_all_students(self):
        r = self.client.get(self.url)
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        data = r.json()
        self.assertListEqual(self.students, data)


class TestGetStudent(TestCase):
    def setUp(self) -> None:
        self.client = RequestsClient()
        self.url = HOST + '/students/{}/'
        try:
            self.students = [self.client.post(HOST + '/students/', data=student).json() for student in
                             [student_1_params, student_2_params]]
        except JSONDecodeError:
            self.fail('/students/ students endpoint for POST request not implemented correctly')

    def test_get_retrieve_existing_id(self):
        for student in self.students:
            student_id = student['id']
            try:
                r = self.client.get(self.url.format(student_id))
            except JSONDecodeError:
                self.fail('/students/:student_id endpoint for GET request not implemented correctly')
            self.assertEquals(r.status_code, status.HTTP_200_OK)
            data = r.json()
            self.assertDictEqual(student, data)

    def test_get_retrieve_non_existing_id(self):
        try:
            r = self.client.get(self.url.format(10000))
        except JSONDecodeError:
            self.fail('/students/:student_id endpoint for GET request not implemented correctly')
        self.assertEquals(r.status_code, status.HTTP_404_NOT_FOUND)


class TestPatchStudent(TestCase):
    def setUp(self) -> None:
        self.client = RequestsClient()
        self.url = HOST + '/students/{}/'
        try:
            self.student = self.client.post(HOST + '/students/', data=student_1_params).json()
        except JSONDecodeError:
            self.fail('/students/ students endpoint for POST request not implemented correctly')

    def test_patch_existing_student(self):
        updated_student_params = dict(
            first_name="Scarlett",
            last_name="Evans",
            date_of_birth="2010-05-01",
            grade=9,
            phone="+11111111112",
            email="scarlet.updated@email.com"
        )

        try:
            r = self.client.patch(self.url.format(self.student['id']), data=updated_student_params)
        except JSONDecodeError:
            self.fail('/students/:student_id endpoint for PATCH request not implemented correctly')
        self.assertEquals(r.status_code, status.HTTP_200_OK)
        data = r.json()
        del data['id']
        self.assertDictEqual(updated_student_params, data)

    def test_patch_non_existing_student(self):
        updated_student_params = dict(
            first_name="Scarlett",
            last_name="Evans",
            date_of_birth="2010-05-01",
            grade=9,
            phone="+11111111112",
            email="scarlet.updated@email.com"
        )

        try:
            r = self.client.patch(self.url.format(10000), data=updated_student_params)
        except JSONDecodeError:
            self.fail('/students/:student_id endpoint for PATCH request not implemented correctly')
        self.assertEquals(r.status_code, status.HTTP_404_NOT_FOUND)
