"""
Pytest configuration and fixtures for CodeCrafter AI tests
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '..'))


@pytest.fixture
def sample_user_story():
    """Provide sample user story for tests"""
    return "Users should be able to register, login, view products, add items to cart, and checkout with payment processing."


@pytest.fixture
def supported_languages():
    """Provide list of supported languages"""
    return ["Java", "NodeJS", ".NET", "Python", "Go", "Ruby", "PHP", "Kotlin"]


@pytest.fixture
def sample_state():
    """Provide sample CodeCrafterState for tests"""
    from state import CodeCrafterState

    return {
        "user_story": "Users should register and login",
        "language": "Python",
        "features": ["User Registration", "User Login"],
        "services": ["UserService"],
        "architecture_hints": {"pattern": "rest"},
        "architecture_config": {"database": "postgresql"},
        "code_output": {},
        "swagger_output": "",
        "test_output": "",
        "output_dir": "./output"
    }


@pytest.fixture
def planning_result():
    """Provide sample planning result"""
    return {
        "features": ["User Registration", "User Login", "Product Viewing"],
        "services": ["UserService", "ProductService"],
        "architecture_hints": {
            "pattern": "rest",
            "database": "postgresql",
            "caching": "redis"
        },
        "architecture_config": {
            "api_gateway": "nginx",
            "service_discovery": "consul"
        }
    }
