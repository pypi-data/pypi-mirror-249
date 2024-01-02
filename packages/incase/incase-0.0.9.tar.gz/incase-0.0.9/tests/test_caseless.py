from unittest import TestCase, main

from incase import Case, Caseless


class TestCaseless(TestCase):

    test_string = "test string"

    expected = {
        "CASELESS": Caseless("test string"),
        "CAMEL": "testString",
        "DROMEDARY": "testString",
        "MEDIAL": "testString",
        "SNAKE": "test_string",
        "PASCAL": "TestString",
        "INITIAL_CAPITALS": "TestString",
        "KEBAB": "test-string",
        "DASH": "test-string",
        "UPPER_SNAKE": "TEST_STRING",
        "UPPERCASE": "TEST STRING",
        "UPPER": "TEST STRING",
        "LOWERCASE": "test string",
        "LOWER": "test string",
        "TITLE": "Test String",
        "ALTERNATING": "TeSt sTrIng",
        "SARCASM": "TeSt sTrIng",
        "ORIGINAL": "test string",
        "WORD": "test string",
        Case.CASELESS: Caseless("test string"),
        Case.CAMEL: "testString",
        Case.DROMEDARY: "testString",
        Case.MEDIAL: "testString",
        Case.SNAKE: "test_string",
        Case.PASCAL: "TestString",
        Case.INITIAL_CAPITALS: "TestString",
        Case.KEBAB: "test-string",
        Case.DASH: "test-string",
        Case.UPPER_SNAKE: "TEST_STRING",
        Case.UPPERCASE: "TEST STRING",
        Case.UPPER: "TEST STRING",
        Case.LOWERCASE: "test string",
        Case.LOWER: "test string",
        Case.TITLE: "Test String",
        Case.ALTERNATING: "TeSt sTrIng",
        Case.SARCASM: "TeSt sTrIng",
        Case.ORIGINAL: "test string",
        Case.WORD: "test string",
    }

    def test_cases(self):
        for case, value in self.expected.items():
            with self.subTest(msg=f"test {case}", case=case, value=value):
                self.assertEqual(Caseless(self.test_string)[case], value)

    def test_slice(self):
        self.assertEqual(self.test_string[1::2], Caseless(self.test_string)[1::2])

    def test_repr(self):
        self.assertEqual(repr(Caseless(self.test_string)), f'Caseless("{self.test_string}")')

    def test_hash(self):
        self.assertEqual(
            hash(Caseless(self.test_string)), hash(Caseless(self.test_string.upper()))
        )

    def test_factory(self):
        factory_func = Caseless.factory("upper")
        self.assertEqual(factory_func(self.test_string), self.test_string.upper())


if __name__ == "__main__":
    main()  # pragma: no cover
