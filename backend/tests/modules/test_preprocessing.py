import pytest
import pandas as pd
from app.services.preprocessing.preprocess_csv import safe_float, validate_columns

class TestPreprocessing:
    
    def test_safe_float_valid(self):
        assert safe_float('1000.50') == 1000.50
        assert safe_float('1,000.50') == 1000.50
    
    def test_safe_float_invalid(self):
        assert safe_float('invalid') is None
        assert safe_float('') is None
        assert safe_float(None) is None
    
    def test_validate_columns_success(self):
        df = pd.DataFrame({
            'Debit_Amount': [100.0],
            'Credit_Amount': [0.0],
            'Balance': [1000.0]
        })
        validate_columns(df)
    
    def test_validate_columns_missing(self):
        df = pd.DataFrame({'Debit_Amount': [100.0]})
        with pytest.raises(ValueError, match="Missing required columns"):
            validate_columns(df)
    
    def test_data_normalization(self):
        test_values = ['1,000', '500.50', 'invalid']
        assert safe_float(test_values[0]) == 1000.0
        assert safe_float(test_values[1]) == 500.50
        assert safe_float(test_values[2]) is None
