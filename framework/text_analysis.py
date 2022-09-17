"""
Collection of all the functionality focussed on text analysis.
"""
import textblob

from framework.framework_utils.env_reader import EnvVarReader


CRYPTO_SYMBOL_REGEX_PATTERN = EnvVarReader().get_value('BOT_CRYPTO_SYMBOL_REGEX_PATTERN')


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

