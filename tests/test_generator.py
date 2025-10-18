import os
from pathlib import Path
from unittest.mock import patch
import pytest
import main  # import your QR code script


def test_create_directory_success(tmp_path):
    """Ensure directory creation works without error."""
    dir_path = tmp_path / "test_dir"
    main.create_directory(dir_path)
    assert dir_path.exists()


def test_is_valid_url_true():
    """Valid URL should return True."""
    with patch("main.validators.url", return_value=True):
        assert main.is_valid_url("https://example.com") is True


def test_is_valid_url_false():
    """Invalid URL should log error and return False."""
    with patch("main.validators.url", return_value=False):
        with patch("main.logging.error") as mock_log:
            result = main.is_valid_url("bad_url")
            assert result is False
            mock_log.assert_called_once()


def test_generate_qr_code_invalid_url(tmp_path):
    """If URL is invalid, no file should be created."""
    file_path = tmp_path / "qr.png"
    with patch("main.validators.url", return_value=False):
        main.generate_qr_code("bad_url", file_path)
    assert not file_path.exists()
