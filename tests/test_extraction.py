"""Tests for the Groq LLM extraction layer.

These tests verify:
- Import functionality
- Extraction prompt structure
- Retry logic
- Sample email extraction (requires GROQ_API_KEY)
- DeadlineType classification
"""

import os
import pytest
from datetime import date
from unittest.mock import Mock, patch, MagicMock

from src.models import Opportunity, DeadlineType, OpportunityType


# Skip tests that require actual API calls if no API key
requires_groq = pytest.mark.skipif(
    not os.environ.get("GROQ_API_KEY"),
    reason="GROQ_API_KEY not set"
)


class TestExtractionImports:
    """Test that extraction module imports work."""

    def test_extraction_imports(self):
        """Verify extraction module imports successfully."""
        from src.extraction import (
            get_groq_client,
            get_groq_client_safe,
            extract_from_email,
            classify_opportunity,
            extract_opportunities_batch,
            retry_with_backoff,
            EXTRACTION_PROMPT
        )
        assert EXTRACTION_PROMPT is not None

    def test_utils_imports(self):
        """Verify utils module imports successfully."""
        from src.utils import (
            parse_date_fuzzy,
            is_relative_deadline,
            extract_deadline_type,
            clean_email_text,
            calculate_days_left
        )
        assert True


class TestDeadlineTypeExtraction:
    """Test DeadlineType classification from text."""

    def test_extract_hard_deadline(self):
        """Test extracting hard deadline type."""
        from src.utils import extract_deadline_type

        # Hard deadlines with specific dates
        assert extract_deadline_type("March 15, 2025") == DeadlineType.HARD
        assert extract_deadline_type("2025-03-15") == DeadlineType.HARD
        assert extract_deadline_type("03/15/2025") == DeadlineType.HARD
        assert extract_deadline_type("15 March 2025") == DeadlineType.HARD

    def test_extract_rolling_deadline(self):
        """Test extracting rolling deadline type."""
        from src.utils import extract_deadline_type

        assert extract_deadline_type("rolling basis") == DeadlineType.ROLLING
        assert extract_deadline_type("on a rolling basis") == DeadlineType.ROLLING
        assert extract_deadline_type("continuous review") == DeadlineType.ROLLING
        assert extract_deadline_type("applications reviewed continuously") == DeadlineType.ROLLING

    def test_extract_soft_early_deadline(self):
        """Test extracting soft early deadline type."""
        from src.utils import extract_deadline_type

        assert extract_deadline_type("early applications encouraged") == DeadlineType.SOFT_EARLY
        assert extract_deadline_type("priority deadline") == DeadlineType.SOFT_EARLY
        assert extract_deadline_type("early decision") == DeadlineType.SOFT_EARLY

    def test_extract_relative_deadline(self):
        """Test extracting relative deadline type."""
        from src.utils import extract_deadline_type

        assert extract_deadline_type("next Friday") == DeadlineType.RELATIVE
        assert extract_deadline_type("end of month") == DeadlineType.RELATIVE
        assert extract_deadline_type("two weeks from now") == DeadlineType.RELATIVE

    def test_extract_unknown_deadline(self):
        """Test extracting unknown deadline type."""
        from src.utils import extract_deadline_type

        assert extract_deadline_type(None) == DeadlineType.UNKNOWN
        assert extract_deadline_type("") == DeadlineType.UNKNOWN
        assert extract_deadline_type("   ") == DeadlineType.UNKNOWN


class TestDateParsing:
    """Test date parsing utilities."""

    def test_parse_date_fuzzy_valid(self):
        """Test parsing valid dates."""
        from src.utils import parse_date_fuzzy

        result = parse_date_fuzzy("March 15, 2025")
        assert result is not None
        assert result.year == 2025

    def test_parse_date_fuzzy_invalid(self):
        """Test parsing invalid dates returns None."""
        from src.utils import parse_date_fuzzy

        assert parse_date_fuzzy("rolling basis") is None
        assert parse_date_fuzzy("next Friday") is None

    def test_is_relative_deadline(self):
        """Test relative deadline detection."""
        from src.utils import is_relative_deadline

        assert is_relative_deadline("next Friday") is True
        assert is_relative_deadline("end of month") is True
        assert is_relative_deadline("March 15, 2025") is False

    def test_calculate_days_left(self):
        """Test days left calculation."""
        from src.utils import calculate_days_left
        from datetime import timedelta

        future = date.today() + timedelta(days=10)
        assert calculate_days_left(future) == 10

        past = date.today() - timedelta(days=5)
        assert calculate_days_left(past) == -5


class TestRetryLogic:
    """Test retry functionality."""

    def test_retry_success_first_try(self):
        """Test function succeeds on first try."""
        from src.extraction import retry_with_backoff

        mock_func = Mock(return_value="success")
        result = retry_with_backoff(mock_func)

        assert result == "success"
        assert mock_func.call_count == 1

    def test_retry_eventual_success(self):
        """Test function succeeds after retries."""
        from src.extraction import retry_with_backoff

        mock_func = Mock(side_effect=[Exception("fail"), Exception("fail"), "success"])
        result = retry_with_backoff(mock_func, max_retries=3)

        assert result == "success"
        assert mock_func.call_count == 3

    def test_retry_max_retries_exceeded(self):
        """Test function fails after max retries."""
        from src.extraction import retry_with_backoff

        mock_func = Mock(side_effect=Exception("persistent failure"))

        with pytest.raises(Exception):
            retry_with_backoff(mock_func, max_retries=3)

        assert mock_func.call_count == 3


class TestMockedExtraction:
    """Test extraction with mocked Groq API."""

    def test_classify_opportunity(self):
        """Test opportunity classification."""
        from src.extraction import classify_opportunity

        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"is_opportunity": true, "confidence": 0.95, "reason": "Real scholarship opportunity"}'))]
        mock_client.chat.completions.create.return_value = mock_response

        is_opp, confidence, reason = classify_opportunity("scholarship email text", mock_client)

        assert is_opp is True
        assert confidence == 0.95
        assert "scholarship" in reason.lower() or "opportunity" in reason.lower()

    def test_extract_from_email_mock(self):
        """Test email extraction with mocked response."""
        from src.extraction import extract_from_email

        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='''
        {
            "is_opportunity": true,
            "confidence": 0.95,
            "title": "Test Scholarship",
            "organization": "Test Corp",
            "opportunity_type": "scholarship",
            "deadline_type": "hard",
            "deadline_date": "2025-03-15",
            "deadline_text": "March 15, 2025",
            "eligibility_criteria": ["CS students"],
            "required_documents": ["transcript"],
            "application_link": "https://example.com",
            "contact_email": "test@example.com",
            "benefits": "$10000",
            "location": "Remote",
            "raw_excerpts": ["Apply by March 15"],
            "classification_reason": "Real opportunity"
        }
        '''))]
        mock_client.chat.completions.create.return_value = mock_response

        result = extract_from_email("scholarship email", mock_client)

        assert isinstance(result, Opportunity)
        assert result.is_opportunity is True
        assert result.title == "Test Scholarship"
        assert result.deadline_type == DeadlineType.HARD


class TestSampleEmails:
    """Test against sample email dataset."""

    def test_sample_emails_load(self):
        """Verify sample emails are accessible."""
        from src.sample_emails import get_sample_emails, get_opportunity_emails, get_spam_emails

        all_emails = get_sample_emails()
        assert len(all_emails) == 12

        opp_emails = get_opportunity_emails()
        assert len(opp_emails) == 10

        spam_emails = get_spam_emails()
        assert len(spam_emails) == 2

    @requires_groq
    def test_extract_google_scholarship(self):
        """Test extraction on Google Scholarship email (HARD deadline)."""
        from src.extraction import extract_from_email, get_groq_client_safe
        from src.sample_emails import get_opportunity_emails

        client = get_groq_client_safe()
        if not client:
            pytest.skip("No Groq client available")

        emails = get_opportunity_emails()
        # First email is Google Scholarship with HARD deadline
        desc, email_text = emails[0]

        result = extract_from_email(email_text, client)

        assert isinstance(result, Opportunity)
        assert result.is_opportunity is True
        assert result.confidence > 0.5
        assert "scholarship" in result.title.lower() or "google" in result.title.lower()

    @requires_groq
    def test_extract_microsoft_internship(self):
        """Test extraction on Microsoft Internship email (ROLLING deadline)."""
        from src.extraction import extract_from_email, get_groq_client_safe
        from src.sample_emails import get_opportunity_emails

        client = get_groq_client_safe()
        if not client:
            pytest.skip("No Groq client available")

        emails = get_opportunity_emails()
        # Second email is Microsoft Internship with ROLLING deadline
        desc, email_text = emails[1]

        result = extract_from_email(email_text, client)

        assert isinstance(result, Opportunity)
        assert result.is_opportunity is True
        assert result.deadline_type == DeadlineType.ROLLING

    @requires_groq
    def test_spam_classification(self):
        """Test that spam emails are correctly classified."""
        from src.extraction import classify_opportunity, get_groq_client_safe
        from src.sample_emails import get_spam_emails

        client = get_groq_client_safe()
        if not client:
            pytest.skip("No Groq client available")

        spam_emails = get_spam_emails()
        desc, email_text = spam_emails[0]

        is_opp, confidence, reason = classify_opportunity(email_text, client)

        # Spam should be classified as not an opportunity
        assert is_opp is False or confidence < 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
