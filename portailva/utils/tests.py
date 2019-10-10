from django.test import TestCase
from django.core.exceptions import ValidationError

from portailva.utils.validators import validate_siren


class ValidatorSIRENTestCase(TestCase):
    """This class defines the test suite for the SIREN Validator."""

    def validator_fail_with(self, siren):
        with self.assertRaises(ValidationError):
            validate_siren(siren)

    def test_validator_success_with_valid_SIREN(self):
        valid_SIREN = "380438358"
        validate_siren(valid_SIREN)

    def test_validator_fail_with_wrong_SIREN_format(self):
        space_SIREN = "380 438 358"
        underbar_SIREN = "380-438-358"
        alphanumeric_SIREN = "A3843V858"
        too_long_SIREN = "350124850213548"
        self.validator_fail_with(space_SIREN)
        self.validator_fail_with(underbar_SIREN)
        self.validator_fail_with(alphanumeric_SIREN)
        self.validator_fail_with(too_long_SIREN)

    def test_validator_fail_with_corrupted_SIREN(self):
        corrupt_SIREN = "380438351"
        self.validator_fail_with(corrupt_SIREN)
