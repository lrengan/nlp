import pandas as pd
import re

doc = []
with open('dates.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
# df.str.lower().head(10)


# 04/20/2009; 04/20/09; 4/20/09; 4/3/09
r1 = df.str.extract(r'\b(?P<month>[\d]{2,4})\s?/\s?(?P<day>[\d]{1,2})\s?/\s?(?P<year>[\d]{2,4})\b')

# 6/2008; 12/2009
r2 = df.str.extract(r'\b(?P<month>[\d]{2,4})\s?/\s?(?P<year>[\d]{2,4})\b')

# 2009; 2010
r3 = df.str.extract(r'\b(?P<year>[\d]{2,4})\b')

res = r1.copy()

for x in res.index:
    if pd.isnull(res['day'][x]) and not pd.isnull(r2['month'][x]):
        res['day'][x] = 1
        res['month'][x] = r2['month'][x]
        res['year'][x] = r2['year'][x]

for x in res.index:
    if pd.isnull(res['day'][x]) and not pd.isnull(r3['year'][x]):
        res['day'][x] = 1
        res['month'][x] = 1
        res['year'][x] = r3['year'][x]

# Mar-20-2009; Mar 20, 2009; March 20, 2009; Mar. 20, 2009; Mar 20 2009;
# Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
r4 = df.str.lower().str.extract(r'\b(?P<month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may'
                                r'|june?|july?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?'
                                r'|nov(?:ember)|dec(?:ember)?)(?:[\.\-\s]\s*)'
                                r'(?P<day>[\d]{1,2})(?:[st|nd|rd|th]?[\-,\.\s]\s*)'
                                r'(?P<year>[\d]{2,4})\b')
r4d = r4[not pd.isnull(r4['month'])]

# 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
r5 = df.str.lower().str.extract(r'(\b(?P<day>[\d]{1,2})([st|nd|rd|th]?[,\.\s]\s*))'
                                r'(?P<month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may'
                                r'|june?|july?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?'
                                r'|nov(?:ember)|dec(?:ember)?)([\.\-\s]\s*)'
                                r'(?P<year>[\d]{2,4})\b')
r5d = r5[not pd.isnull(r5['month'])]
r5d['key'] = r5d.index

r5d.merge(r4d, how='outer')

# Feb 2009; Sep 2009; Oct 2010
r6 = df.str.lower().str.extract(r'(?P<month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may'
                                r'|june?|july?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?'
                                r'|nov(?:ember)|dec(?:ember)?)([\.\-\s]\s*)'
                                r'(?P<year>[\d]{2,4})\b')
