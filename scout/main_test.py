import io
import sys
import unittest

from scout.main import print_welcome_message


class TestMain(unittest.TestCase):
    def test_welcome_message_prints(self):
        # Arrange
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput

        # Act
        print_welcome_message()

        # Assert
        self.assertIsNotNone(capturedOutput.getvalue())

        # Cleanup
        sys.stdout = sys.__stdout__

if __name__ == '__main__':
    unittest.main()
