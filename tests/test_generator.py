import sys
from pathlib import Path
from unittest.mock import patch
import pytest
import main  # your main.py script


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


def test_generate_qr_code_valid(tmp_path):
    """Test generating a QR code with a valid URL."""
    file_path = tmp_path / "qr.png"
    with patch("main.validators.url", return_value=True):
        main.generate_qr_code("https://example.com", file_path)
    assert file_path.exists()


def test_generate_qr_code_exception(tmp_path):
    """Simulate exception during image save."""
    file_path = tmp_path / "qr.png"

    def raise_error(*args, **kwargs):
        raise IOError("Disk full")

    with patch("main.validators.url", return_value=True), \
         patch.object(main.qrcode.image.pil.PilImage, "save", raise_error), \
         patch("main.logging.error") as mock_log:
        main.generate_qr_code("https://example.com", file_path)
        mock_log.assert_called_once()


def test_main_runs(monkeypatch):
    """Run main() end-to-end with argument mocking."""
    mock_args = ["prog", "--url", "https://example.com"]
    with patch.object(sys, "argv", mock_args):
        with patch("main.create_directory") as mock_dir, \
             patch("main.generate_qr_code") as mock_qr:
            main.main()
            mock_dir.assert_called_once()
            mock_qr.assert_called_once()
