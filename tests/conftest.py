"""Pytest configuration and shared fixtures.

This file is automatically loaded by pytest and provides
common configuration and fixtures for all tests.
"""

import pytest
import sys
from pathlib import Path

# Ensure parent directory is in path for importing pwa_create
sys.path.insert(0, str(Path(__file__).parent.parent))


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


@pytest.fixture(scope="session")
def script_version():
    """Provide script version for testing."""
    import pwa_create
    return pwa_create.SCRIPT_VERSION


@pytest.fixture(scope="session")
def constants():
    """Provide module constants for testing."""
    import pwa_create
    return {
        "MIN_LENGTH": pwa_create.MIN_PROJECT_NAME_LENGTH,
        "MAX_LENGTH": pwa_create.MAX_PROJECT_NAME_LENGTH,
        "VERSION": pwa_create.SCRIPT_VERSION,
    }
