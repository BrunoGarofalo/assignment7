import os
import docker
import pytest

IMAGE_NAME = "legioxi/qr_codemaker"
QR_CODES_DIR = "./qr_codes"

client = docker.from_env()


def test_container_runs_and_creates_qr():
    """
    Test that the Docker container runs successfully and generates a QR code.
    This confirms that the image, dependencies, and entrypoint all work correctly.
    """
    # Run the container and capture logs
    logs = client.containers.run(
        IMAGE_NAME,
        remove=True,
        volumes={os.path.abspath(QR_CODES_DIR): {"bind": "/app/qr_codes", "mode": "rw"}},
    )

    # Verify the log output contains success message
    assert b"QR code successfully saved" in logs

    # Verify that a QR code file exists in the qr_codes directory
    qr_files = [f for f in os.listdir(QR_CODES_DIR) if f.endswith(".png")]
    assert len(qr_files) > 0, "No QR code file found — the app may not have run correctly."
