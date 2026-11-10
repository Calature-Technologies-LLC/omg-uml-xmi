"""
Distribution tests for omg-uml-xmi package.

Tests verify that the package can be built as a wheel/sdist and installed correctly
in a clean virtual environment.
"""

import subprocess
import sys
import os
import glob
import tempfile


def test_wheel_build_creates_valid_wheel():
    """Test that pip wheel creates a valid wheel file."""
    result = subprocess.run(["pip", "wheel", ".", "-w", "dist/"], capture_output=True, text=True)
    assert result.returncode == 0, f"Wheel build failed: {result.stderr}"

    wheels = glob.glob("dist/omg_uml_xmi-*.whl")
    assert len(wheels) == 1, f"Expected 1 wheel, got {len(wheels)}"

    wheel_path = wheels[0]
    assert os.path.exists(wheel_path), "Wheel file should exist"
    assert wheel_path.endswith(".whl"), "Should be a .whl file"


def test_wheel_install_in_clean_env():
    """Test that wheel installs correctly in a clean virtual environment."""
    import subprocess
    import os
    import glob
    import sys

    # Build wheel first
    result = subprocess.run(["pip", "wheel", ".", "-w", "dist/"], capture_output=True, text=True)
    assert result.returncode == 0, f"Wheel build failed: {result.stderr}"

    wheels = glob.glob("dist/omg_uml_xmi-*.whl")
    assert len(wheels) == 1, f"Expected 1 wheel, got {len(wheels)}"
    wheel_path = wheels[0]

    # Create temporary virtual environment
    with tempfile.TemporaryDirectory() as tmpdir:
        venv_path = os.path.join(tmpdir, "venv")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

        # Determine pip and python paths
        if sys.platform == "win32":
            pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
            python_path = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            pip_path = os.path.join(venv_path, "bin", "pip")
            python_path = os.path.join(venv_path, "bin", "python")

        # Install wheel in clean environment
        result = subprocess.run([pip_path, "install", wheel_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Install failed: {result.stderr}"

        # Verify import works
        result = subprocess.run(
            [python_path, "-c", "import omg_uml_xmi; print(omg_uml_xmi.__version__)"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "0.1.0" in result.stdout


def test_sdist_build_creates_valid_sdist():
    """Test that python -m build --sdist creates a valid sdist."""
    import subprocess
    import glob
    import os

    result = subprocess.run(["python", "-m", "build", "--sdist"], capture_output=True, text=True)
    assert result.returncode == 0, f"SDist build failed: {result.stderr}"

    sdists = glob.glob("dist/omg_uml_xmi-*.tar.gz")
    assert len(sdists) == 1, f"Expected 1 sdist, got {len(sdists)}"

    sdist_path = sdists[0]
    assert os.path.exists(sdist_path)
    assert sdist_path.endswith(".tar.gz")


def test_sdist_install_in_clean_env():
    """Test that sdist installs correctly in a clean virtual environment."""
    import subprocess
    import tempfile
    import os
    import glob
    import sys

    # Build sdist
    result = subprocess.run(["python", "-m", "build", "--sdist"], capture_output=True, text=True)
    assert result.returncode == 0, f"SDist build failed: {result.stderr}"

    sdists = glob.glob("dist/omg_uml_xmi-*.tar.gz")
    assert len(sdists) == 1
    sdist_path = sdists[0]

    with tempfile.TemporaryDirectory() as tmpdir:
        venv_path = os.path.join(tmpdir, "venv")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

        if sys.platform == "win32":
            pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
            python_path = os.path.join(venv_path, "Scripts", "python.exe")
        else:
            pip_path = os.path.join(venv_path, "bin", "pip")
            python_path = os.path.join(venv_path, "bin", "python")

        result = subprocess.run([pip_path, "install", sdist_path], capture_output=True, text=True)
        assert result.returncode == 0, f"SDist install failed: {result.stderr}"

        result = subprocess.run(
            [python_path, "-c", "import omg_uml_xmi; print(omg_uml_xmi.__version__)"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Import failed: {result.stderr}"
        assert "0.1.0" in result.stdout