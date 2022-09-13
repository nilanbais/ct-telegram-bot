import re

import context

from framework.text_analysis import get_sentiment_score

regex_statement = '[$][^\s]+'  # matches $[A-Z]

text =  "This guide will teach you how to trade crypto altcoins such as "
temp = """✅ This guide will teach you how to trade crypto altcoins such as: 
                \n \n $MATIC +45,000%,\n$SOL +50,000%,\n$EGLD +12,000%,\n$LUNA +18,000% 
                before it went to 0\n\n❌ It won't teach you how to take coke and ass pi
                ctures https://t.co/Qz9qkDZXNO"""

result = re.findall(regex_statement, text)
print(result)