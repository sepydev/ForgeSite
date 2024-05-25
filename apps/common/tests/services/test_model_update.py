from datetime import timedelta
from unittest.mock import Mock, patch

from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from apps.common.factories import RandomModelFactory, SimpleModelFactory
from apps.common.services import model_update


class ModelUpdateTests(TestCase):
    def setUp(self):
        self.model_instance = RandomModelFactory()
        self.simple_object = SimpleModelFactory()
        self.instance = Mock(field_a=None, field_b=None, field_c=None)

    def test_model_update_does_nothing(self):
        with self.subTest("when no fields are provided"):
            instance = RandomModelFactory()

            updated_instance, has_updated = model_update(
                instance=instance, fields=[], data={}
            )

            self.assertEqual(instance, updated_instance)
            self.assertFalse(has_updated)
            self.assertNumQueries(0)

        with self.subTest("when non of the fields are in the data"):
            instance = RandomModelFactory()

            updated_instance, has_updated = model_update(
                instance=instance, fields=["start_date"], data={"foo": "bar"}
            )

            self.assertEqual(instance, updated_instance)
            self.assertFalse(has_updated)
            self.assertNumQueries(0)

    def test_model_update_updates_only_passed_fields_from_data(self):
        instance = RandomModelFactory()

        update_fields = ["start_date"]
        data = {
            "field_a": "value_a",
            "start_date": instance.start_date - timedelta(days=1),
            "end_date": instance.end_date + timedelta(days=1),
        }

        self.assertNotEqual(instance.start_date, data["start_date"])

        update_query = None

        with CaptureQueriesContext(connection) as ctx:
            updated_instance, has_updated = model_update(
                instance=instance, fields=update_fields, data=data
            )
            update_query = ctx.captured_queries[-1]

        self.assertTrue(has_updated)
        self.assertEqual(updated_instance.start_date, data["start_date"])
        self.assertNotEqual(updated_instance.end_date, data["end_date"])

        self.assertFalse(hasattr(updated_instance, "field_a"))

        self.assertNotIn("end_date", update_query)

    def test_model_update_raises_error_when_called_with_non_existent_field(self):
        instance = RandomModelFactory()

        update_fields = ["non_existing_field"]
        data = {"non_existing_field": "foo"}

        with self.assertRaises(AssertionError):
            updated_instance, has_updated = model_update(
                instance=instance, fields=update_fields, data=data
            )

    def test_model_update_updates_many_to_many_fields(self):
        instance = RandomModelFactory()
        simple_obj = SimpleModelFactory()

        update_fields = ["simple_objects"]
        data = {"simple_objects": [simple_obj]}

        self.assertNotIn(simple_obj, instance.simple_objects.all())

        original_updated_at = instance.updated_at

        updated_instance, has_updated = model_update(
            instance=instance, fields=update_fields, data=data
        )

        self.assertEqual(updated_instance, instance)
        self.assertTrue(has_updated)

        self.assertIn(simple_obj, updated_instance.simple_objects.all())
        self.assertEqual(
            original_updated_at,
            updated_instance.updated_at,
            "If we are only updating m2m fields, don't auto-bump `updated_at`",
        )

    def test_model_update_updates_standard_and_many_to_many_fields(self):
        instance = RandomModelFactory()
        simple_obj = SimpleModelFactory()

        update_fields = ["start_date", "simple_objects"]
        data = {
            "start_date": instance.start_date - timedelta(days=1),
            "simple_objects": [simple_obj],
        }

        self.assertNotIn(simple_obj, instance.simple_objects.all())

        updated_instance, has_updated = model_update(
            instance=instance, fields=update_fields, data=data
        )

        self.assertTrue(has_updated)
        self.assertEqual(updated_instance.start_date, data["start_date"])
        self.assertIn(simple_obj, updated_instance.simple_objects.all())

    def test_model_update_does_not_automatically_update_updated_at_if_model_does_not_have_it(
        self,
    ):
        instance = SimpleModelFactory()

        self.assertFalse(hasattr(instance, "updated_at"))

        update_fields = ["name"]
        data = {"name": "HackSoft"}

        with patch("apps.common.services.timezone.now") as now:
            updated_instance, has_updated = model_update(
                instance=instance, fields=update_fields, data=data
            )

            now.assert_not_called()

        self.assertTrue(has_updated)
        self.assertFalse(hasattr(instance, "updated_at"))
