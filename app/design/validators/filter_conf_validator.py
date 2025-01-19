"""
This file contains the implementation of the filter conf validator
"""
from app.design.exceptions.filter_config_exceptions import MissingKeysError, IncorrectTypeError
from app.design.types.fir_filter_types import FilterConf

REQUIRED_KEYS: list[str] = ['Ap', 'As', 'fp', 'fs', 'F', 'filter_type', 'filter_window']
OPTIONAL_KEYS: list[str] = ['fs2', 'fp2']

VALID_FILTER_TYPES: list[str] = ['passband', 'lowpass', 'highpass', 'bandpass']
VALID_WINDOW_TYPES: list[str] = ['hamming', 'blackman', 'kaiser']


class FilterConfTypeValidator:
    """
    Filter Configuration Type Validator
    """

    def __init__(self, filter_conf: FilterConf):
        self.filter_conf = filter_conf
        self.validate_filter_conf()

    def _validate_required_keys(self):
        missing_keys = [key for key in REQUIRED_KEYS if key not in self.filter_conf]
        if missing_keys:
            raise MissingKeysError(missing_keys)

    def _validate_correct_types(self):
        incorrect_types = []
        for key in REQUIRED_KEYS:
            if key == 'filter_type' or key == 'filter_window':
                if not isinstance(self.filter_conf[key], str):
                    incorrect_types.append(key)
                    continue
            elif key in self.filter_conf and not isinstance(self.filter_conf[key], (int, float)):
                incorrect_types.append(key)

        if incorrect_types:
            raise IncorrectTypeError(incorrect_types)

    def _validate_optional_keys(self):
        incorrect_types = [key for key in OPTIONAL_KEYS if
            key in self.filter_conf and self.filter_conf[key] is not None and not isinstance(self.filter_conf[key],
                                                                                             (int, float))]
        if incorrect_types:
            raise IncorrectTypeError(incorrect_types)

    def _validate_filter_type(self):
        """
        Validates the filter type
        :raises: ValueError if the filter type is not valid
        """
        if self.filter_conf['filter_type'] not in VALID_FILTER_TYPES:
            raise ValueError(f"Filter type must be one of {', '.join(VALID_FILTER_TYPES)}")

    def _validate_filter_window(self):
        """
        Validates the filter window
        :raises: ValueError if the filter window is not valid
        """
        if self.filter_conf['filter_window'] not in VALID_WINDOW_TYPES:
            raise ValueError(f"Filter window must be one of {', '.join(VALID_WINDOW_TYPES)}")

    def validate_filter_conf(self) -> bool:
        """
        Validates the filter configuration
        :return: True if the filter configuration is valid, False otherwise
        """
        if not self.filter_conf:
            raise TypeError("Filter configuration cannot be empty")

        if not isinstance(self.filter_conf, dict):
            raise TypeError("Filter configuration must be a dictionary")

        self._validate_required_keys()
        self._validate_correct_types()
        self._validate_optional_keys()

        self._validate_filter_type()
        self._validate_filter_window()

        return True


class FilterValuesValidator(FilterConfTypeValidator):
    """
    Filter Values Validator
    """

    def __init__(self, filter_conf: FilterConf):
        self.filter_conf = filter_conf
        super().__init__(filter_conf)

    def _validate_frequecies_grater_than(self, keys: list[str], value):
        invalid_frequency = [key for key in keys if self.filter_conf[key] >= value]
        if len(invalid_frequency) > 0:
            raise ValueError(f'{", ".join(invalid_frequency)} must be greater than {value}')

    def _validate_ripples(self):
        """
        Validates the ripples of the filter configuration
        :raises: ValueError if the ripples are not valid
        """
        if self.filter_conf['Ap'] <= 0:
            raise ValueError("Ap must be greater than 0")

        if self.filter_conf['As'] <= 0:
            raise ValueError("As must be greater than 0, usually grateter than 20")

    def _validate_frequency_values(self):
        """
        Validates the frequency values of the filter configuration
        :return: True if the values are valid, raises ValueError otherwise
        """
        REQUIRED_FREQUENCY_KEYS = ['fp', 'fs', 'F']
        OPTIONAL_FREQUENCY_KEYS = ['fp2', 'fs2']

        # Validate frequencies grater than 0
        self._validate_frequecies_grater_than(REQUIRED_FREQUENCY_KEYS, 0)

        if self.filter_conf['filter_type'] in ['bandpass', 'stopband']:
            self._validate_frequecies_grater_than(OPTIONAL_FREQUENCY_KEYS, 0)

        # Validate frequencies grater than sampling frequency
        self._validate_frequecies_grater_than(REQUIRED_FREQUENCY_KEYS, self.filter_conf['F'])

        if self.filter_conf['filter_type'] in ['bandpass', 'stopband']:
            self._validate_frequecies_grater_than(OPTIONAL_FREQUENCY_KEYS, self.filter_conf['F'])

        if self.filter_conf['filter_type'] == 'highpass':
            if self.filter_conf['fp'] >= self.filter_conf['fs']:
                raise ValueError("fp must be greater than fs")

        if self.filter_conf['filter_type'] == 'lowpass':
            if self.filter_conf['fp'] <= self.filter_conf['fs']:
                raise ValueError("fp must be greater than fs")

        if self.filter_conf['filter_type'] == 'bandpass':
            if self.filter_conf['fp'] >= self.filter_conf['fp2']:
                raise ValueError("fp must be greater than fp2")

            if self.filter_conf['fs'] <= self.filter_conf['fs2']:
                raise ValueError("fs must be greater than fs2")

            if self.filter_conf['fp'] == self.filter_conf['fs']:
                raise ValueError("fp and fs cannot be the same for highpass/lowpass.")

        if self.filter_conf['filter_type'] == 'stopband':
            if self.filter_conf['fp'] <= self.filter_conf['fp2']:
                raise ValueError("fp must be greater than fp2")

            if self.filter_conf['fs'] >= self.filter_conf['fs2']:
                raise ValueError("fs must be greater than fs2")

    def validate_values(self) -> bool:
        """
        Validates the values of the filter configuration
        :return: True if the values are valid, False otherwise
        """
        self._validate_ripples()

        self._validate_frequency_values()

        return True


class FilterConfValidator(FilterConfTypeValidator, FilterValuesValidator):
    """
    Filter Configuration Validator
    """

    def __init__(self, filter_conf: FilterConf):
        self.filter_conf = filter_conf
        FilterConfTypeValidator.__init__(self, filter_conf)
        FilterValuesValidator.__init__(self, filter_conf)
