"""
Tests for the TeenAGI package.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from teenagi import TeenAGI, create_agent


@patch('teenagi.core.TeenAGI._initialize_client')
@patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
def test_teenagi_init(mock_init_client):
    """Test TeenAGI initialization."""
    agent = TeenAGI(name="TestAgent", provider="openai")
    assert agent.name == "TestAgent"
    assert agent.capabilities == []
    assert agent.provider == "openai"
    mock_init_client.assert_called_once()


@patch('teenagi.core.TeenAGI._initialize_client')
@patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
def test_teenagi_learn(mock_init_client):
    """Test TeenAGI learning functionality."""
    agent = TeenAGI()
    
    # Test adding a valid capability
    assert agent.learn("can search the web")
    assert len(agent.capabilities) == 1
    
    # Test adding an empty capability (should fail)
    assert not agent.learn("")
    assert len(agent.capabilities) == 1
    
    # Test adding multiple capabilities
    agent.learn("can summarize text")
    agent.learn("can translate languages")
    assert len(agent.capabilities) == 3


@patch('teenagi.core.TeenAGI._initialize_client')
@patch('teenagi.core.TeenAGI._generate_response')
@patch.dict(os.environ, {"OPENAI_API_KEY": "test_key"})
def test_teenagi_respond(mock_generate, mock_init_client):
    """Test TeenAGI response generation."""
    mock_generate.return_value = "This is a test response"
    
    agent = TeenAGI(name="ResponderAgent")
    
    # Response with no capabilities
    response = agent.respond("Hello")
    assert "ResponderAgent" in response
    assert "don't have any capabilities" in response
    assert not mock_generate.called
    
    # Add capabilities and test response
    agent.learn("can search the web")
    agent.learn("can summarize text")
    
    response = agent.respond("Find and summarize an article")
    mock_generate.assert_called_once()
    assert response == "This is a test response"


@patch('teenagi.core.TeenAGI._initialize_client')
@patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test_key"})
def test_create_agent(mock_init_client):
    """Test the create_agent factory function."""
    agent = create_agent(name="FactoryAgent", provider="anthropic")
    assert isinstance(agent, TeenAGI)
    assert agent.name == "FactoryAgent"
    assert agent.capabilities == []
    assert agent.provider == "anthropic"


@patch('os.environ.get')
def test_missing_api_key(mock_env_get):
    """Test error when API key is missing."""
    mock_env_get.return_value = None
    
    with pytest.raises(ValueError, match="OpenAI API key not found"):
        TeenAGI(provider="openai")
    
    with pytest.raises(ValueError, match="Anthropic API key not found"):
        TeenAGI(provider="anthropic") 