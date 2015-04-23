import os
from django.test.client import Client
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'

from mock import Mock, patch
from types import DictType, ListType
import json
from django.test.testcases import TestCase

class HarpTestCase(TestCase):

    def mock(self, obj_class):
        mock = Mock(spec = obj_class)
        return mock

    def patch(self, *args):
        if len(args) == 2:
            patcher = patch.object(args[0], args[1])
        else:
            patcher = patch(args[0])
        instance = patcher.start()
        self.addCleanup(patcher.stop)
        return instance

    def assertCalled(self, instance):
        self.assertTrue(instance.called)

    def assertCalledOnce(self, instance):
        self.assertEqual(instance.call_count, 1)

    def assertIsOne(self, instance):
        self.assertEqual(instance, 1)

    def assertAsExpected(self):
        self.assertEqual(self.expected, self.actual)

    def assertEmpty(self, instance):
        self.assertEqual(len(instance), 0)

    def assertNone(self, instance):
        self.assertEqual(instance, None)

    def assertEqualDict(self, actual, expected):
        for key in expected:
            if isinstance(expected[key], DictType):
                self.assertEqualDict(self, actual[key], expected[key])
            else:
                self.assertEqual(actual[key], expected[key])

        self.assertEqual(len(actual), len(expected))

    @classmethod
    def print_json(cls, output = None):
        if not output:
            output = cls.output
        if not (isinstance(output, DictType) or isinstance(output, ListType)):
            output = json.loads(output)

        print json.dumps(output, sort_keys = True, indent = 4)
        return output

    def json_to_dict(self, content = None):
        return json.loads(content)

    @classmethod
    def run_tests(cls, module_name, test_class_name, test_methods, verbose = False, fail_fast = True):

        if module_name is None:
            raise Exception("Where's the module name, eh?")

        tests = []
        if test_class_name:
            module_path = '%s.%s' % (module_name, test_class_name)
        else:
            module_path = module_name

        if test_methods:
            tests = [
                "%s.%s" % (module_path, test_method)
                for test_method in test_methods
            ]
        else:
            tests = [module_path]

        sys.argv = ['', 'test'] + tests
        if verbose:
            sys.argv += ['-v2']
        else:
            sys.argv += ['-v0']
        if fail_fast:
            sys.argv += ['--failfast']

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)

class IntegrationTestCase(HarpTestCase):
    django_client = Client()

    def http_get(self, url = None, params = {}):
        url = url or self.endpoint
        response = self.django_client.get(url, data = params)
        try:
            return response.status_code, json.loads(response.content)
        except:
            raise
