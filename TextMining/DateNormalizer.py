import pandas as pd
import re

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
# df.str.lower().head(10)


# 04/20/2009; 04/20/09; 4/20/09; 4/3/09
# df.str.extract(r'(?P<month>[\d]{2,4})/(?P<day>[\d]{1,2})/(?P<year>[\d]{2,4})')


# Mar-20-2009; Mar 20, 2009; March 20, 2009; Mar. 20, 2009; Mar 20 2009;
df.str.lower().str.extractall(r'\b(?P<month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may'
                              r'|june?|july?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?'
                              r'|nov(?:ember)|dec(?:ember)?)([\.\-\s]\s*)'
                              r'(?P<day>[\d]{1,2})(?:[st|nd|rd|th]?[\-,\.\s]\s*)'
                              r'(?P<year>[\d]{2,4})\b')

# 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
# Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
df.str.lower().str.extractall(r'(\b(?P<day>[\d]{1,2})([st|nd|rd|th]?[,\.\s]\s*))'
                              r'(?P<month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may'
                              r'|june?|july?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?'
                              r'|nov(?:ember)|dec(?:ember)?)([\.\-\s]\s*)'
                              r'(?P<year>[\d]{2,4})\b')

# Feb 2009; Sep 2009; Oct 2010
# df.str.lower().str.extractall(r'(?P<month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may'
#                              r'|june?|july?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?'
#                              r'|nov(?:ember)|dec(?:ember)?)([\.\-\s]\s*)'
#                              r'(?P<year>[\d]{2,4})\b')
