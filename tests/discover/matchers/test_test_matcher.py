from unittest import TestCase, mock
from unittest.mock import MagicMock, mock_open

from test_reader.discover.matchers.testmatcher import TestMatcher


class TestTestMatcher(TestCase):

    def test_given_test_rules_with_next_strategy_and_file_with_a_test_then_test_should_be_returned(self):
        file_path = 'path'
        test_config_name = 'Unit'

        # Arrange
        mock_test_rules = MagicMock()
        mock_test_rules.test_description_regex = "`(.+?)`"
        mock_test_rules.test_description_strategy = "NEXT_LINE"
        mock_test_rules.test_notation = "^@Test+$"

        mock_test_config = MagicMock()
        mock_test_config.name = test_config_name
        mock_test_config.test_rules = mock_test_rules
        mock_test_config.get_type_names.return_value = [test_config_name]
        mock_test_config.get_type_by_name.return_value = mock_test_config

        file_content = 'Title \n@Test \nfun `test_name`\n\n{\n\n}'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = TestMatcher(mock_test_config).matches(file_path)

            # Assert
            self.assertEqual(1, len(result))
            self.assertEqual('test_name', result[0].name)
            self.assertEqual([test_config_name], result[0].types)

    def test_given_test_rules_with_next_strategy_and_file_with_more_than_one_test_then_tests_should_be_returned(self):
        file_path = 'path'
        test_config_name = 'Unit'

        # Arrange
        mock_test_rules = MagicMock()
        mock_test_rules.test_description_regex = "`(.+?)`"
        mock_test_rules.test_description_strategy = "NEXT_LINE"
        mock_test_rules.test_notation = "^@Test+$"

        mock_test_config = MagicMock()
        mock_test_config.name = test_config_name
        mock_test_config.test_rules = mock_test_rules
        mock_test_config.get_type_names.return_value = [test_config_name]
        mock_test_config.get_type_by_name.return_value = mock_test_config

        file_content = 'Title \n@Test \nfun `test_name`\n\n{\n\n}\n\n@Test \nfun `other_test_name`\n\n{\n\n}'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = TestMatcher(mock_test_config).matches(file_path)

            # Assert
            self.assertEqual(2, len(result))
            self.assertEqual('test_name', result[0].name)
            self.assertEqual([test_config_name], result[0].types)
            self.assertEqual('other_test_name', result[1].name)
            self.assertEqual([test_config_name], result[1].types)

    def test_given_test_rules_with_next_strategy_and_file_with_a_test_without_description_then_test_should_be_returned(
            self):
        file_path = 'path'
        test_config_name = 'Unit'

        # Arrange
        mock_test_rules = MagicMock()
        mock_test_rules.test_description_regex = "`(.+?)`"
        mock_test_rules.test_description_strategy = "NEXT_LINE"
        mock_test_rules.test_notation = "^@Test+$"

        mock_test_config = MagicMock()
        mock_test_config.name = test_config_name
        mock_test_config.test_rules = mock_test_rules
        mock_test_config.get_type_names.return_value = [test_config_name]
        mock_test_config.get_type_by_name.return_value = mock_test_config

        file_content = 'Title \n@Test \nfun\n\n{\n\n}'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = TestMatcher(mock_test_config).matches(file_path)

            # Assert
            self.assertEqual(1, len(result))
            self.assertEqual('fun', result[0].name)
            self.assertEqual([test_config_name], result[0].types)

    def test_given_test_rules_with_same_strategy_and_file_with_a_test_then_test_should_be_returned(self):
        file_path = 'path'
        test_config_name = 'Unit'

        # Arrange
        mock_test_rules = MagicMock()
        mock_test_rules.test_description_regex = 'def (.+?)\('
        mock_test_rules.test_description_strategy = "SAME_LINE"
        mock_test_rules.test_notation = "def (.+?)\("

        mock_test_config = MagicMock()
        mock_test_config.name = test_config_name
        mock_test_config.test_rules = mock_test_rules
        mock_test_config.get_type_names.return_value = [test_config_name]
        mock_test_config.get_type_by_name.return_value = mock_test_config

        file_content = 'Title \n def test_name():\n\n\n\n'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = TestMatcher(mock_test_config).matches(file_path)

            # Assert
            self.assertEqual(1, len(result))
            self.assertEqual('test_name', result[0].name)
            self.assertEqual([test_config_name], result[0].types)

    def test_given_test_rules_with_same_strategy_and_file_with_more_than_one_test_then_tests_should_be_returned(self):
        file_path = 'path'
        test_config_name = 'Unit'

        # Arrange
        mock_test_rules = MagicMock()
        mock_test_rules.test_description_regex = 'def (.+?)\('
        mock_test_rules.test_description_strategy = "SAME_LINE"
        mock_test_rules.test_notation = "def (.+?)\("

        mock_test_config = MagicMock()
        mock_test_config.name = test_config_name
        mock_test_config.test_rules = mock_test_rules
        mock_test_config.get_type_names.return_value = [test_config_name]
        mock_test_config.get_type_by_name.return_value = mock_test_config

        file_content = 'Title \n def test_name():\n\n\n\ndef other_test_name():\n\n'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = TestMatcher(mock_test_config).matches(file_path)

            # Assert
            self.assertEqual(2, len(result))
            self.assertEqual('test_name', result[0].name)
            self.assertEqual([test_config_name], result[0].types)
            self.assertEqual('other_test_name', result[1].name)
            self.assertEqual([test_config_name], result[1].types)

    def test_given_test_rules_with_same_strategy_and_file_with_a_test_without_description_then_test_should_be_returned(
            self):
        file_path = 'path'
        test_config_name = 'Unit'

        # Arrange
        mock_test_rules = MagicMock()
        mock_test_rules.test_description_regex = 'def (.+?)\('
        mock_test_rules.test_description_strategy = "SAME_LINE"
        mock_test_rules.test_notation = "def (.+?)"

        mock_test_config = MagicMock()
        mock_test_config.name = test_config_name
        mock_test_config.test_rules = mock_test_rules
        mock_test_config.get_type_names.return_value = [test_config_name]
        mock_test_config.get_type_by_name.return_value = mock_test_config

        file_content = 'Title \n def a):\n\n\n\n'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = TestMatcher(mock_test_config).matches(file_path)

            # Assert
            self.assertEqual(1, len(result))
            self.assertEqual('def a):', result[0].name)
            self.assertEqual([test_config_name], result[0].types)

    def test_given_test_rules_with_same_strategy_and_file_without_tests_then_no_test_should_be_returned(self):
        file_path = 'path'
        test_config_name = 'Unit'

        # Arrange
        mock_test_rules = MagicMock()
        mock_test_rules.test_description_regex = 'def (.+?)\('
        mock_test_rules.test_description_strategy = "SAME_LINE"
        mock_test_rules.test_notation = "def (.+?)\("

        mock_test_config = MagicMock()
        mock_test_config.name = test_config_name
        mock_test_config.test_rules = mock_test_rules
        mock_test_config.get_type_names.return_value = [test_config_name]
        mock_test_config.get_type_by_name.return_value = mock_test_config

        file_content = 'Title \n\nEnd\n'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = TestMatcher(mock_test_config).matches(file_path)

            # Assert
            self.assertEqual(0, len(result))

    def test_given_test_rules_with_next_strategy_and_file_without_tests_then_no_test_should_be_returned(self):
        file_path = 'path'
        test_config_name = 'Unit'

        # Arrange
        mock_test_rules = MagicMock()
        mock_test_rules.test_description_regex = "`(.+?)`"
        mock_test_rules.test_description_strategy = "NEXT_LINE"
        mock_test_rules.test_notation = "^@Test+$"

        mock_test_config = MagicMock()
        mock_test_config.name = test_config_name
        mock_test_config.test_rules = mock_test_rules
        mock_test_config.get_type_names.return_value = [test_config_name]
        mock_test_config.get_type_by_name.return_value = mock_test_config

        file_content = 'Title \nfun `test_name`\n\n{\n\n}'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = TestMatcher(mock_test_config).matches(file_path)

            # Assert
            self.assertEqual(0, len(result))

    def test_given_more_than_one_test_rules_and_file_with_more_than_one_test_then_tests_should_be_returned(self):
        # Arrange
        file_path = 'path'
        child_test_name = 'Child'
        parent_test_name = 'Parent'

        mock_test_rules = MagicMock()
        mock_test_rules.test_description_regex = 'def (.+?)\('
        mock_test_rules.test_description_strategy = "SAME_LINE"
        mock_test_rules.test_notation = "def (.+?)\("

        parent_config_mock, child_config_mock = MagicMock(), MagicMock()
        child_config_mock.name = child_test_name
        child_config_mock.test_rules = mock_test_rules

        parent_config_mock.name = parent_test_name
        parent_config_mock.test_rules = mock_test_rules
        parent_config_mock.get_type_names.return_value = [parent_test_name, child_test_name]
        parent_config_mock.get_type_by_name.side_effect = [parent_config_mock, child_config_mock]

        file_content = 'Title \n def test_name():\n\n\n\ndef other_test_name():\n\n'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = TestMatcher(parent_config_mock).matches(file_path)

            # Assert
            self.assertEqual(2, len(result))
            self.assertEqual('test_name', result[0].name)
            self.assertEqual([parent_test_name, child_test_name], result[0].types)
            self.assertEqual('other_test_name', result[1].name)
            self.assertEqual([parent_test_name, child_test_name], result[1].types)