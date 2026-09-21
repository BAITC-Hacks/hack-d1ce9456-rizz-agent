import unittest

from agent import classify, process


class ClassifierTests(unittest.TestCase):
    def test_classifies_reference_request(self):
        self.assertEqual(classify("Где парковка для гостей?")[0], "справка")

    def test_classifies_complaint_before_question(self):
        self.assertEqual(classify("Пропал Wi-Fi в корпусе B.")[0], "жалоба")

    def test_generates_russian_draft(self):
        result = process("В столовой очередь, еда холодная.")
        self.assertEqual(result.category, "жалоба")
        self.assertIn("Спасибо", result.response)


if __name__ == "__main__":
    unittest.main()
