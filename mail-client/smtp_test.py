import unittest
import smtp_client
import configparser


class TestSMTPClient(unittest.TestCase):
    def test_parse_config(self):
        sender, _ = smtp_client.parse_config('./user.conf')
        self.assertEqual(sender, 'flyingicefr@163.com')

    def test_parse_config_exception(self):
        with self.assertRaises(OSError):
            smtp_client.parse_config('./nonexist.conf')

        with self.assertRaises(KeyError):
            smtp_client.parse_config('./invalid_key.conf')

        with self.assertRaises(configparser.MissingSectionHeaderError):
            smtp_client.parse_config('./missing_header.conf')

    def test_validate_email(self):
        self.assertTrue(smtp_client.validate_email('abc.def@gmail.com'))
        self.assertFalse(smtp_client.validate_email('abc'))
        self.assertFalse(smtp_client.validate_email('@163.com'))
        self.assertFalse(smtp_client.validate_email('xyz@123@hotmail.com'))


if __name__ == '__main__':
    unittest.main()
