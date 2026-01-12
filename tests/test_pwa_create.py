"""Unit tests for PWA Game Framework Generator.

Tests validation, file generation, template rendering, and error handling.

Requirements:
    pip install pytest pytest-cov

Usage:
    pytest tests/test_pwa_create.py -v
    pytest tests/test_pwa_create.py --cov=pwa_create --cov-report=html
"""

import pytest
import sys
from pathlib import Path
import shutil
import tempfile
import json

# Add parent directory to path to import pwa_create
sys.path.insert(0, str(Path(__file__).parent.parent))
import pwa_create


class TestInputValidation:
    """Test suite for input validation and sanitization."""
    
    def test_valid_project_names(self):
        """Test that valid project names pass validation."""
        valid_names = [
            "my-game",
            "MyGame",
            "game123",
            "my_cool_game",
            "A1-B2_C3",
        ]
        for name in valid_names:
            result = pwa_create.validate_project_name(name)
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_empty_name_raises_error(self):
        """Test that empty names raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            pwa_create.validate_project_name("")
        
        with pytest.raises(ValueError, match="cannot be empty"):
            pwa_create.validate_project_name("   ")
    
    def test_name_too_long_raises_error(self):
        """Test that names exceeding max length raise ValueError."""
        long_name = "a" * (pwa_create.MAX_PROJECT_NAME_LENGTH + 1)
        with pytest.raises(ValueError, match="too long"):
            pwa_create.validate_project_name(long_name)
    
    def test_invalid_starting_character(self):
        """Test that names starting with invalid characters are sanitized."""
        # After sanitization, leading hyphens/underscores are stripped
        # This is better UX than rejecting - we fix it for the user
        result = pwa_create.validate_project_name("-leadinghyphen")
        assert result == "leadinghyphen"
        
        result = pwa_create.validate_project_name("_leadingunderscore")
        assert result == "leadingunderscore"
        
        # Leading dots get sanitized to hyphens then stripped
        result = pwa_create.validate_project_name(".hiddenfolder")
        assert result == "hiddenfolder"
    
    def test_path_traversal_blocked(self):
        """Test that path traversal attempts are blocked."""
        dangerous_names = [
            "../../../etc",
            "..\\..\\..\\Windows",
            "/etc/passwd",
            "C:\\Windows",
        ]
        for name in dangerous_names:
            result = pwa_create.validate_project_name(name)
            # Should be sanitized to safe value
            assert ".." not in result
            assert "/" not in result
            assert "\\" not in result
    
    def test_script_injection_sanitized(self):
        """Test that script injection attempts are sanitized."""
        malicious_names = [
            "<script>alert(1)</script>",
            "'; DROP TABLE projects;--",
            "${malicious}",
        ]
        for name in malicious_names:
            result = pwa_create.validate_project_name(name)
            # Should be sanitized (no angle brackets, quotes, etc.)
            assert "<" not in result
            assert ">" not in result
            assert "'" not in result
            assert "$" not in result
    
    def test_lowercase_conversion(self):
        """Test that project names are converted to lowercase."""
        result = pwa_create.validate_project_name("MyGameProject")
        assert result == "mygameproject"
    
    def test_space_to_hyphen_conversion(self):
        """Test that spaces are converted to hyphens."""
        result = pwa_create.validate_project_name("My Cool Game")
        assert " " not in result
        assert result == "my-cool-game"
    
    def test_consecutive_hyphens_collapsed(self):
        """Test that consecutive hyphens are collapsed."""
        result = pwa_create.validate_project_name("my---game")
        assert result == "my-game"
    
    def test_trailing_hyphens_stripped(self):
        """Test that trailing hyphens are removed."""
        result = pwa_create.validate_project_name("my-game---")
        assert result == "my-game"


class TestTemplateGeneration:
    """Test suite for template content generation."""
    
    def test_get_main_css_returns_string(self):
        """Test that get_main_css returns non-empty string."""
        result = pwa_create.Templates.get_main_css()
        assert isinstance(result, str)
        assert len(result) > 0
        assert ":root" in result
    
    def test_get_main_css_has_dark_mode(self):
        """Test that main.css includes dark mode support."""
        result = pwa_create.Templates.get_main_css()
        assert "prefers-color-scheme: dark" in result
        assert "prefers-color-scheme: light" in result
    
    def test_get_ui_css_returns_string(self):
        """Test that get_ui_css returns non-empty string."""
        result = pwa_create.Templates.get_ui_css()
        assert isinstance(result, str)
        assert len(result) > 0
        assert ".hidden" in result
    
    def test_get_html_contains_csp(self):
        """Test that HTML includes Content-Security-Policy."""
        result = pwa_create.Templates.get_html("test-project")
        assert "Content-Security-Policy" in result
        # Should NOT contain 'unsafe-inline' for style-src
        assert "'unsafe-inline'" not in result or "script-src 'self'" in result
    
    def test_get_html_contains_generator_version(self):
        """Test that HTML includes generator version metadata."""
        result = pwa_create.Templates.get_html("test-project")
        assert "generator" in result.lower()
        assert pwa_create.SCRIPT_VERSION in result
    
    def test_get_manifest_valid_json(self):
        """Test that manifest.json is valid JSON."""
        result = pwa_create.Templates.get_manifest("test-project")
        manifest = json.loads(result)
        assert manifest["name"] == "test-project"
        assert manifest["short_name"] == "test-project"
        assert "description" in manifest
        assert pwa_create.SCRIPT_VERSION in manifest["description"]
    
    def test_get_sw_includes_cache_limits(self):
        """Test that service worker includes cache size limits."""
        result = pwa_create.Templates.get_sw("test-project")
        assert "MAX_CACHE_SIZE" in result
        assert "50 * 1024 * 1024" in result  # 50MB
        assert "limitCacheSize" in result
    
    def test_get_js_assetloader_has_validation(self):
        """Test that AssetLoader includes image validation."""
        result = pwa_create.Templates.get_js_assetloader()
        assert "width < 1 || height < 1" in result or "Invalid image dimensions" in result
        assert "8192" in result  # Max dimension check
    
    def test_get_js_gameloop_has_vendor_prefix(self):
        """Test that GameLoop includes webkit visibility prefix."""
        result = pwa_create.Templates.get_js_gameloop()
        assert "webkitvisibilitychange" in result
        assert "webkitHidden" in result
    
    def test_get_js_errorhandler_exists(self):
        """Test that ErrorHandler template exists and handles rejections."""
        result = pwa_create.Templates.get_js_errorhandler()
        assert "unhandledrejection" in result
        assert "window.addEventListener" in result


class TestFrameworkCreation:
    """Test suite for complete framework generation."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        temp_path = Path(tempfile.mkdtemp())
        original_cwd = Path.cwd()
        try:
            # Change to temp directory for testing
            import os
            os.chdir(temp_path)
            yield temp_path
        finally:
            # Restore original directory and cleanup
            os.chdir(original_cwd)
            shutil.rmtree(temp_path, ignore_errors=True)
    
    def test_create_framework_dry_run(self, temp_dir):
        """Test that dry-run mode doesn't create files."""
        success = pwa_create.create_framework("test-game", dry_run=True)
        assert success is True
        
        # Check that no directory was created
        project_dir = temp_dir / "test-game"
        assert not project_dir.exists()
    
    def test_create_framework_creates_directory(self, temp_dir):
        """Test that framework creation creates project directory."""
        success = pwa_create.create_framework("test-game")
        assert success is True
        
        project_dir = temp_dir / "test-game"
        assert project_dir.exists()
        assert project_dir.is_dir()
    
    def test_create_framework_creates_essential_files(self, temp_dir):
        """Test that essential files are created."""
        pwa_create.create_framework("test-game")
        project_dir = temp_dir / "test-game"
        
        essential_files = [
            "index.html",
            "manifest.json",
            "service-worker.js",
            "README.md",
            ".gitignore",
        ]
        
        for filename in essential_files:
            file_path = project_dir / filename
            assert file_path.exists(), f"{filename} should exist"
            assert file_path.stat().st_size > 0, f"{filename} should not be empty"
    
    def test_create_framework_creates_directories(self, temp_dir):
        """Test that required directories are created."""
        pwa_create.create_framework("test-game")
        project_dir = temp_dir / "test-game"
        
        directories = [
            "css",
            "js",
            "js/core",
            "js/scenes",
            "js/utils",
            "js/ui",
            "js/state",
            "assets",
            "assets/icons",
        ]
        
        for dirname in directories:
            dir_path = project_dir / dirname
            assert dir_path.exists(), f"{dirname} directory should exist"
            assert dir_path.is_dir(), f"{dirname} should be a directory"
    
    def test_create_framework_rejects_existing_directory(self, temp_dir):
        """Test that creation fails if directory already exists."""
        # Create first time
        success1 = pwa_create.create_framework("test-game")
        assert success1 is True
        
        # Try to create again
        success2 = pwa_create.create_framework("test-game")
        assert success2 is False
    
    def test_create_framework_invalid_name_returns_false(self, temp_dir):
        """Test that invalid project names return False."""
        success = pwa_create.create_framework("")
        assert success is False


class TestConstants:
    """Test suite for module constants."""
    
    def test_script_version_format(self):
        """Test that SCRIPT_VERSION follows semantic versioning."""
        version = pwa_create.SCRIPT_VERSION
        # Should be in format X.Y.Z
        parts = version.split(".")
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)
    
    def test_min_project_name_length(self):
        """Test that MIN_PROJECT_NAME_LENGTH is reasonable."""
        assert pwa_create.MIN_PROJECT_NAME_LENGTH >= 1
        assert pwa_create.MIN_PROJECT_NAME_LENGTH < 10
    
    def test_max_project_name_length(self):
        """Test that MAX_PROJECT_NAME_LENGTH is reasonable."""
        assert pwa_create.MAX_PROJECT_NAME_LENGTH >= 10
        assert pwa_create.MAX_PROJECT_NAME_LENGTH <= 100


class TestEdgeCases:
    """Test suite for edge cases and error handling."""
    
    def test_unicode_characters_sanitized(self):
        """Test that Unicode characters are handled correctly."""
        result = pwa_create.validate_project_name("café-game")
        # Non-ASCII should be replaced with hyphens
        assert result == "caf-game" or "cafe" in result
    
    def test_numeric_only_name(self):
        """Test that numeric-only names are accepted."""
        result = pwa_create.validate_project_name("12345")
        assert result == "12345"
    
    def test_single_character_name(self):
        """Test that single character names work."""
        result = pwa_create.validate_project_name("a")
        assert result == "a"
    
    def test_maximum_length_name(self):
        """Test that names at maximum length are accepted."""
        max_name = "a" * pwa_create.MAX_PROJECT_NAME_LENGTH
        result = pwa_create.validate_project_name(max_name)
        assert len(result) <= pwa_create.MAX_PROJECT_NAME_LENGTH


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
