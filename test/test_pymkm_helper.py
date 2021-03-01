"""
Python unittest
"""
import io
import unittest
import logging
import re
from unittest.mock import MagicMock, Mock, mock_open, patch

from pymkm.pymkm_helper import PyMkmHelper


class TestPyMkmHelperFunctions(unittest.TestCase):
    def setUp(self):
        self.helper = PyMkmHelper()

    def test_dict_to_cardmarket_xml_request(self):
        add_to_stock_dict = [
            {
                "idProduct": 100569,
                "idLanguage": 1,
                "comments": "Inserted through the API",
                "count": 1,
                "price": 4,
                "condition": "EX",
                "isFoil": True,
                "isSigned": False,
                "isPlayset": False,
            }
        ]

        add_to_stock_xml = """<request>
               <article>
                   <idProduct>100569</idProduct>
                   <idLanguage>1</idLanguage>
                   <comments>Inserted through the API</comments>
                   <count>1</count>
                   <price>4</price>
                   <condition>EX</condition>
                   <isFoil>true</isFoil>
                   <isSigned>false</isSigned>
                   <isPlayset>false</isPlayset>
               </article>
           </request>"""
        add_to_stock_xml = re.sub(r"[\t\s]+", "", add_to_stock_xml)

        xml_data = self.helper.dicttoxml(add_to_stock_dict)
        xml_data = re.sub(r"[\t\s]+", "", xml_data)
        self.assertEqual(xml_data, add_to_stock_xml)

    def test_string_to_float_or_int(self):
        self.assertEqual(self.helper.string_to_float_or_int("1.0"), 1)
        self.assertEqual(self.helper.string_to_float_or_int("1"), 1)
        self.assertEqual(self.helper.string_to_float_or_int("AAAAA"), "AAAAA")
        self.assertEqual(self.helper.string_to_float_or_int("11.3"), 11.3)
        self.assertEqual(self.helper.string_to_float_or_int(str(4 / 3)), 4 / 3)

    def test_calculate_average(self):
        table = [
            ["Yxskaft", "SE", "NM", 1, 1.21],
            ["Frazze11", "SE", "NM", 3, 1.3],
            ["andli826", "SE", "NM", 2, 1.82],
        ]
        self.assertEqual(self.helper.calculate_average(table, 3, 4), 1.46)

    def test_calculate_median(self):
        table = [
            ["Yxskaft", "SE", "NM", 1, 1.21],
            ["Frazze11", "SE", "NM", 3, 1.3],
            ["andli826", "SE", "NM", 2, 1.82],
        ]
        self.assertEqual(self.helper.calculate_median(table, 3, 4), 1.3)
        self.assertEqual(self.helper.calculate_average(table, 3, 4), 1.46)

    def test_calculate_lowest(self):
        table = [
            ["Yxskaft", "SE", "NM", 1, 1.21],
            ["Frazze11", "SE", "NM", 3, 1.3],
            ["andli826", "SE", "NM", 2, 1.82],
        ]
        self.assertEqual(self.helper.get_lowest_price_from_table(table, 4), 1.21)

    def test_round_up_to_limit(self):
        self.assertEqual(self.helper.round_up_to_multiple_of_lower_limit(0.25, 0.99), 1)
        self.assertEqual(self.helper.round_up_to_multiple_of_lower_limit(0.25, 0), 0)
        self.assertEqual(
            self.helper.round_up_to_multiple_of_lower_limit(0.25, 0.1), 0.25
        )

        self.assertEqual(self.helper.round_up_to_multiple_of_lower_limit(0.1, 0.99), 1)
        self.assertEqual(
            self.helper.round_up_to_multiple_of_lower_limit(0.01, 0.011), 0.02
        )
        self.assertEqual(self.helper.round_up_to_multiple_of_lower_limit(0.01, 1), 1)
        self.assertEqual(self.helper.round_up_to_multiple_of_lower_limit(1, 0.1), 1)

    def test_round_down_to_limit(self):
        self.assertEqual(
            self.helper.round_down_to_multiple_of_lower_limit(0.25, 0.99), 0.75
        )
        self.assertEqual(
            self.helper.round_down_to_multiple_of_lower_limit(0.25, 1.01), 1
        )
        self.assertEqual(
            self.helper.round_down_to_multiple_of_lower_limit(0.25, 0.1), 0.25
        )

        self.assertEqual(
            self.helper.round_down_to_multiple_of_lower_limit(0.1, 0.99), 0.9
        )
        self.assertEqual(
            self.helper.round_down_to_multiple_of_lower_limit(0.01, 0.011), 0.01
        )
        self.assertEqual(self.helper.round_down_to_multiple_of_lower_limit(0.01, 1), 1)
        self.assertEqual(self.helper.round_down_to_multiple_of_lower_limit(1, 0.1), 1)

        self.assertEqual(
            self.helper.round_down_to_multiple_of_lower_limit(0.10, 8.44), 8.4
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("builtins.input", side_effect=["y", "n", "p", "n", ""])
    def test_prompt_bool(self, mock_input, mock_stdout):
        self.assertTrue(self.helper.prompt_bool("test_y"))
        self.assertFalse(self.helper.prompt_bool("test_n"))
        self.helper.prompt_bool("test_error")
        self.assertRegex(mock_stdout.getvalue(), r"\nPlease answer with y\/n\n")
        self.assertFalse(self.helper.prompt_bool("test_empty"))

    @patch("builtins.input", side_effect=["y"])
    def test_prompt_string(self, mock_input):
        self.assertEqual(self.helper.prompt_string("test"), "y")


if __name__ == "__main__":
    unittest.main()
