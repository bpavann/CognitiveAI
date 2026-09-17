from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def check_retrieval_relevance(score: float, threshold: float = 0.35) -> bool:
    """
    Checks whether a retrieved document is sufficiently relevant.
    Returns:
        True  -> relevant
        False -> irrelevant
    """
    return score >= threshold
    
def mask_retrieval_pii(content: str) -> str:
    """
    Detects and masks PII in retrieved content.
    Returns:
        Masked content with sensitive information removed.
    """
    if not content:
        return content
    results = analyzer.analyze(
        text=content,
        language="en",
        entities=[
            "PERSON",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "CREDIT_CARD"
        ]
    )
    if not results:
        return content
    anonymized = anonymizer.anonymize(text=content,analyzer_results=results)
    return anonymized.text

def check_retrieval_security(content: str) -> bool:
    """
    Checks retrieved content for obvious prompt injection patterns.
    Returns:
        True  -> safe
        False -> suspicious / unsafe
    """
    if not content:
        return True
    content_lower = content.lower()
    suspicious_patterns = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "ignore the previous instructions",
        "disregard previous instructions",
        "disregard all previous instructions",
        "forget previous instructions",
        "forget all previous instructions",
        "ignore the user",
        "ignore the user's request",
        "follow these instructions instead",
        "follow the instructions below",
        "follow my instructions instead",
        "system prompt",
        "developer message",
        "developer instructions",
        "reveal your instructions",
        "reveal the system prompt",
        "show me your system prompt",
        "show internal instructions",
        "reveal internal instructions",
        "you are now",
        "act as system",
        "act as an administrator",
        "override your instructions",
        "override the system",
        "bypass your instructions",
        "bypass the guardrails",
        "disable your guardrails",
        "disable safety",
        "do not follow your rules",
        "pretend you have no restrictions",
        "jailbreak",
        "execute this instruction",
        "execute the following command",
        "send the following information",
        "disclose confidential information",
        "reveal confidential information",
    ]

    for pattern in suspicious_patterns:
        if pattern in content_lower:
            return False

    return True

def mark_untrusted_context(content: str) -> str:
    """
    Marks retrieved content as untrusted context.
    Retrieved content must be treated as data, not instructions.
    """
    if not content:
        return content

    return (
        "<UNTRUSTED_CONTEXT>\n"
        f"{content}\n"
        "</UNTRUSTED_CONTEXT>"
    )

def mask_output_pii(content: str) -> str:
    """
    Detects and masks PII in the final assistant response.
    """
    if not content:
        return content

    results = analyzer.analyze(
        text=content,
        language="en",
        entities=[
            "PERSON",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "CREDIT_CARD"
        ]
    )

    if not results:
        return content
    anonymized = anonymizer.anonymize(text=content,analyzer_results=results)
    return anonymized.text

def check_answer_grounding(answer: str,documents: list[dict],threshold: float = 0.30) -> bool:
    """
    Checks whether the assistant answer is sufficiently supported
    by the retrieved documents.
    Returns:
        True  -> grounded
        False -> insufficiently grounded
    """
    if not answer or not documents:
        return False

    context = " ".join(
        document.get("content", "")
        for document in documents
    )

    if not context:
        return False

    answer_words = set(answer.lower().split())
    context_words = set(context.lower().split())

    if not answer_words:
        return False

    overlap = len(answer_words.intersection(context_words))
    score = overlap / len(answer_words)

    return score >= threshold