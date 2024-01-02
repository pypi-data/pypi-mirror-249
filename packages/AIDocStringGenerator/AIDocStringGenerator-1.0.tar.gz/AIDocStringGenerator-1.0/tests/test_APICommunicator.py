import json
import unittest
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(f"{parent}")
from DocStringGenerator.DocstringProcessor import DocstringProcessor
from DocStringGenerator.CodeProcessor import CodeProcessor
from DocStringGenerator.CommunicatorManager import CommunicatorManager
from DocStringGenerator.BaseBotCommunicator import BaseBotCommunicator
from DocStringGenerator.DocstringProcessor import DocstringProcessor
from pathlib import Path
from DocStringGenerator.ConfigManager import ConfigManager
from DocStringGenerator.DependencyContainer import DependencyContainer
dependencies = DependencyContainer()

from dotenv import load_dotenv


# Import other necessary modules...
load_dotenv()
@unittest.skipIf(os.environ.get('RUNNING_IN_CI') == 'true', "Skipping this test in CI environment")
class DocStringGeneratorTest(unittest.TestCase):
    bot_communicator = None

    def setUp(self):
        if self.__class__ == DocStringGeneratorTest:
            self.skipTest("Skipping tests in base class")
        self.code_processor: CodeProcessor = dependencies.resolve("CodeProcessor")
        self.communicator_manager: CommunicatorManager = dependencies.resolve("CommunicatorManager") 
        self.docstring_processor: DocstringProcessor = dependencies.resolve("DocstringProcessor") 

        self.config = ConfigManager().config


    def test_docstring_generation(self):
        # Test generating docstrings for a sample Python code
        sample_code = "class MyClass:\n    def my_method(self):\n        print('Ok')"
        response = self.code_processor.process_code(sample_code)
        json_response = response.content
        # Assert response is not None or empty
        self.assertIsNotNone(json_response)
        self.assertEqual(response.error_message, "")
        self.assertTrue(response.is_valid)

        # Further assertions to check the response format, content, etc.

    def test_length_limit_enforcement(self):
        # Configuring a short max_line_length for testing
        ConfigManager().set_config('max_line_length', 50)
        sample_code = "class MyClass:\n    def my_method(self):\n        pass"
        response = self.code_processor.process_code(sample_code)

        self.assertEqual(response.error_message, "")
        self.assertTrue(response.is_valid)
        self.assertNotEqual(response.content, "")

        # Assuming response is a JSON string; parse it

        #response_data = json.loads(response.content)
        #docstrings = response_data.get('docstrings', {})
        extract_docstrings_response = dependencies.resolve("DocstringProcessor").extract_docstrings(response.content)

        self.assertEqual(extract_docstrings_response.error_message, "")
        self.assertTrue(extract_docstrings_response.is_valid)

        for class_name, class_info in response.content.items():
            if class_name != 'global_functions':
                self.assertTrue(all(len(line) <= 50 for line in class_info['docstring'].split('\n')))

            if 'methods' in class_info:
                for method, method_doc in class_info['methods'].items():
                    self.assertTrue(all(len(line) <= 50 for line in method_doc.split('\n')))


    def test_empty_code_input(self):
        # Test behavior with empty Python code input
        response = self.code_processor.process_code("")
        # Expecting an empty or specific response for empty input
        self.assertNotEqual(response, "")

    def test_json_format_compliance(self):
        # Test if the response complies with the specified JSON format
        sample_code = "class MyClass:\n    def my_method(self):\n        pass"
        response = self.code_processor.process_code(sample_code)
        self.assertEqual(response.error_message, "")
        self.assertTrue(response.is_valid)

    def test_method_docstrings_inclusion(self):
        # Test if methods within classes have their docstrings generated
        sample_code = "class MyClass:\n    def my_method(self):\n        pass"
        response = self.code_processor.process_code(sample_code)
        
        self.assertEqual(response.error_message, "")
        self.assertTrue(response.is_valid)
        self.assertIn("my_method", response.content["MyClass"]["methods"])

    def test_global_function_docstring_generation(self):
        # Test if global functions have their docstrings generated
        sample_code = "def my_function():\n    pass"
        response = self.code_processor.process_code(sample_code)
        json_response = response.content
        self.assertIn("my_function", json_response["global_functions"])

    def test_character_limit_enforcement(self):
        # Test if the character limit is enforced in the response
        sample_code = "class MyClass:\n    def my_method(self):\n        pass"
        sample_code = "class MyClass:\n    def my_method(self):\n        pass"
        response = self.code_processor.process_code(sample_code)
        json_response = response.content
        for line in json.dumps(json_response, indent=4).split("\n"):            
            self.assertLessEqual(len(line), self.config.get("max_line_length", 79))

    def test_class_with_multiple_methods(self):
        # Test generating docstrings for a class with multiple methods
        sample_code = """
class MyClass:
    def method1(self):
        pass

    def method2(self, param):
        pass
"""
        response = self.code_processor.process_code(sample_code)
        json_response = response.content
        self.assertIn("method1", json_response["MyClass"]["methods"])
        self.assertIn("method2", json_response["MyClass"]["methods"])

    def test_inheritance_handling(self):
        # Test generating docstrings for classes with inheritance
        sample_code = """
class ParentClass:
    def parent_method(self):
        pass

class ChildClass(ParentClass):
    def child_method(self):
        pass
"""
        response = self.code_processor.process_code(sample_code)
        json_response = response.content
        self.assertIn("ParentClass", json_response)
        self.assertIn("ChildClass", json_response)

    def test_docstring_for_complex_functions(self):
        # Test generating docstrings for functions with complex signatures
        sample_code = """
def complex_function(param1, param2='default', *args, **kwargs):
    pass
        """
        response = self.code_processor.process_code(sample_code)
        json_response = response.content
        self.assertIn("complex_function", json_response["global_functions"])

    def test_handling_of_decorators(self):
        # Test generating docstrings for decorated functions and methods
        sample_code = """
def my_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def decorated_function(param):
    pass
"""
        response = self.code_processor.process_code(sample_code)
        response_valid = self.code_processor.verify_code_docstrings(response.content)
        self.assertTrue(response_valid.is_valid)


    def test_docstring_format_consistency(self):
        # Test if the docstring format is consistent across various elements
        sample_code = "class MyClass:\n    def my_method(self):\n        pass"
        response = self.code_processor.process_code(sample_code)
        json_response = response.content
        self.assertTrue(self.is_consistent_format(json_response))

    def is_consistent_format(self, docstring_object):
        return dependencies.resolve("DocstringProcessor").validate_response(docstring_object)        




@unittest.skipIf(os.environ.get('RUNNING_IN_CI') == 'true', "Skipping this test in CI environment")
class AnthropicDocStringGeneratorTest(DocStringGeneratorTest):
    def setUp(self):
        super().setUp()
        ConfigManager().set_config("bot", "anthropic")
        ConfigManager().set_config("model", "claude-2.1")
        self.communicator_manager.initialize_bot_communicator()

@unittest.skipIf(os.environ.get('RUNNING_IN_CI') == 'true', "Skipping this test in CI environment")
class OpenAIDocStringGeneratorTest(DocStringGeneratorTest):
    def setUp(self):
        super().setUp()

        ConfigManager().set_config("bot", "openai")
        ConfigManager().set_config("model", "gpt-4-1106-preview")
        self.communicator_manager.initialize_bot_communicator()        

@unittest.skipIf(os.environ.get('RUNNING_IN_CI') == 'true', "Skipping this test in CI environment")
class GoogleDocStringGeneratorTest(DocStringGeneratorTest):
    def setUp(self):
        super().setUp()
        ConfigManager().set_config("bot", "google")
        ConfigManager().set_config("model", "")  
        self.communicator_manager.initialize_bot_communicator()              

@unittest.skipIf(os.environ.get('RUNNING_IN_CI') == 'true', "Skipping this test in CI environment")
class FileDocStringGeneratorTest(DocStringGeneratorTest):
    def setUp(self):
        super().setUp()
        ConfigManager().set_config("bot", "file")
        ConfigManager().set_config("model", "")
        self.communicator_manager.initialize_bot_communicator()        

if __name__ == '__main__':
    unittest.main()
