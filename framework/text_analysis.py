import textblob


CRYPTO_SYMBOL_REGEX_PATTERN = "(\$[A-Z]+)"


def get_sentiment_score(input_text: str) -> dict:
    """
    Function returns a sentiment object with the following scores.
    - polarity score -> how possitive or negative a text is.
    - subjectivity score -> how factual a text is. (or how much of an opinion)
    """
    # Creating a text object
    text_object = textblob.TextBlob(text=input_text)
    # Assigning the sentiment attribute to it's own variable + returning variable
    senitment_object = text_object.sentiment
    return senitment_object

