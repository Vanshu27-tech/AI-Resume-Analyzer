from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the Sentence Transformer model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_match(resume_text, jd_text):
    """
    Calculate semantic similarity between Resume and Job Description.

    Parameters:
        resume_text (str): Extracted text from the Resume
        jd_text (str): Extracted text from the Job Description

    Returns:
        float: Match percentage (0-100)
    """

    # Handle empty input
    if not resume_text.strip() or not jd_text.strip():
        return 0

    # Generate embeddings
    resume_embedding = model.encode([resume_text])
    jd_embedding = model.encode([jd_text])

    # Calculate cosine similarity
    similarity = cosine_similarity(
        resume_embedding,
        jd_embedding
    )[0][0]

    # Convert similarity score to percentage
    match_percentage = round(similarity * 100, 2)

    # Ensure the value stays between 0 and 100
    match_percentage = max(0, min(match_percentage, 100))

    return match_percentage


def get_match_level(match_score):
    """
    Return a human-readable interpretation of the match score.
    """

    if match_score >= 90:
        return "Excellent Match"

    elif match_score >= 75:
        return "Very Good Match"

    elif match_score >= 60:
        return "Good Match"

    elif match_score >= 40:
        return "Average Match"

    else:
        return "Poor Match"