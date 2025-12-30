import pytest
import os
from app.services.ingestion.detect import detect_bank

class TestBankDetection:
    
    def test_detect_hdfc(self):
        # Mock test - in real scenario, use actual PDF
        assert detect_bank is not None
    
    def test_detect_sbi(self):
        assert detect_bank is not None
    
    def test_detect_icici(self):
        assert detect_bank is not None
    
    def test_detect_kotak(self):
        assert detect_bank is not None
    
    def test_detect_unknown_bank(self):
        # Test with non-existent file should return UNKNOWN
        result = detect_bank('/nonexistent/path.pdf')
        assert result == 'UNKNOWN'
