from utils import base

from src import foxlator_lib as fll


class ErrorTests(base.TestBase):
    reason = "example-reason"

    def test_error_get_reason_should_return_correct_reason(self):
        self.assertEqual(fll.error.BaseError(
            self.reason).get_reason(), self.reason)

    def test_base_error_should_be_convertible_to_string(self):
        error = fll.error.BaseError(reason=self.reason)

        self.assertEqual(error.to_string(), f"BaseError - {self.reason}")
        self.assertEqual(error.to_string(), str(error))

    def test_inherited_error_should_return_correct_error_name(self):
        class SomeError(fll.error.BaseError):
            pass
        self.assertTrue(
            SomeError(self.reason).to_string().startswith("SomeError"))
