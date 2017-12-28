import pandas as pd
import re

doc = []
with open('dates_cleaned.txt') as file:
    for line in file:
        doc.append(line)

df = pd.Series(doc)
# df.str.lower().head(10)

# 04/20/2009; 04/20/09; 4/20/09; 4/3/09
r_mdy_slash = re.compile(r'\b(?P<month>[\d]{1,2})\s?[/\-]\s?(?P<day>[\d]{1,2})\s?[/\-]\s?(?P<year>[\d]{2,4})\b')

# 6/2008; 12/2009
# r_my_slash = re.compile(r'\b(?P<month>[\d]{1,2})\s?[/\-]\s?(?P<year>[\d]{2,4})[:\s,\.\-\)$]\b')
r_my_slash = re.compile(r'\b(?P<month>[\d]{1,2})\s?[/\-]\s?(?P<year>[\d]{2,4})\b')

# 2009; 2010
r_y_slash = re.compile(r'(?:\s|^|~|r|s|y|\(|\.)(?P<year>\d\d\d\d)[:\s,\.\-\)$]')

# Mar-20-2009; Mar 20, 2009; March 20, 2009; Mar. 20, 2009; Mar 20 2009;
# Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
r_mdy_space = re.compile(r'\b(?P<month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may'
                         r'|june?|july?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?'
                         r'|nov(?:ember)|dec(?:ember)?)(?:[\.\-\s]\s*)'
                         r'(?P<day>[\d]{1,2})(?:(st|nd|rd|th)?[\-,.\s]\s*)'
                         r'(?P<year>[\d]{2,4})\b')

# 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
r_dmy_space = re.compile(r'\b(?P<day>[\d]{1,2})(?:(?:st|nd|rd|th)?[,\.\s]\s*)'
                         r'(?P<month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may'
                         r'|june?|july?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?'
                         r'|nov(?:ember)|dec(?:ember)?)([\.\-\s]\s*)'
                         r'(?P<year>[\d]{2,4})\b')

# Feb 2009; Sep 2009; Oct 2010
r_my_space = re.compile(r'(?P<month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may'
                        r'|june?|july?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?'
                        r'|nov(?:ember)|dec(?:ember)?)(?:[\.\-\s]\s*)'
                        r'(?P<year>[\d]{2,4})\b')


# Month as locale’s abbreviated name or locale full name
# Format string for strftime()
def make_month_format_str(ms):
    if len(ms) == 3:
        return "%b"
    else:
        return "%B"


# Assume all dates where year is encoded in only two digits are
# years from the 1900's (e.g. 1/5/89 is January 5th, 1989)
def make_year_str(ys):
    if len(ys) == 2:
        year_str = "19{}".format(ys)
    else:
        year_str = "{}".format(ys)
    return year_str


# assume there is only one date in line
# if line contains multiple date occurrences, return the first one
# Assume all dates in xx/xx/xx format are mm/dd/yy
# Assume all dates where year is encoded in only two digits are years from the 1900's (e.g. 1/5/89 is January 5th, 1989)
# If the day is missing (e.g. 9/2009), assume it is the first day of the month (e.g. September 1, 2009).
# If the month is missing (e.g. 2010), assume it is the first of January of that year (e.g. January 1, 2010).

# returns a pandas._libs.tslib.Timestamp object
def extract_date(line1):
    line_lc = line1.lower()
    m = r_mdy_slash.findall(line_lc)
    if len(m) > 0:
        year_str = make_year_str(m[0][2])
        time_str = "{0}/{1}/{2}".format(m[0][0], m[0][1], year_str)
        return pd.to_datetime(time_str, format='%m/%d/%Y')

    m = r_my_slash.findall(line_lc)
    if len(m) > 0 and int(m[0][0]) <= 12:
        year_str = make_year_str(m[0][1])
        time_str = "{0}/{1}/{2}".format(m[0][0], 1, year_str)
        return pd.to_datetime(time_str, format='%m/%d/%Y')

    m = r_y_slash.findall(line_lc)
    if len(m) > 0:
        # the regex matches only four digit years, so can use it directly with %Y
        time_str = "{0}/{1}/{2}".format(1, 1, m[0])
        return pd.to_datetime(time_str, format='%m/%d/%Y')

    m = r_mdy_space.findall(line_lc)
    if len(m) > 0:
        # Mar 20th, 2009 -> [('mar', '20', 'th', '2009')]
        # Mar-20-2009 -> [('mar', '20', '', '2009')]
        assert (len(m[0]) == 4)
        year_str = make_year_str(m[0][3])
        time_str = "{0} {1} {2}".format(m[0][0], m[0][1], year_str)
        format_str = make_month_format_str(m[0][0]) + " %d %Y"
        return pd.to_datetime(time_str, format=format_str)

    m = r_dmy_space.findall(line_lc)
    if len(m) > 0:
        # 20 Mar. 2009 -> [('20', 'mar', '. ', '2009')]
        # 20 March 2009 -> [('20', 'march', ' ', '2009')]
        assert (len(m[0]) == 4)
        year_str = make_year_str(m[0][3])
        time_str = "{0} {1} {2}".format(m[0][1], m[0][0], year_str)
        format_str = make_month_format_str(m[0][1]) + " %d %Y"
        return pd.to_datetime(time_str, format=format_str)
        # return m[0][1], m[0][0], m[0][2]

    m = r_my_space.findall(line_lc)
    if len(m) > 0:
        # Feb 2009 -> [('feb', '2009')]
        year_str = make_year_str(m[0][1])
        time_str = "{0} {1} {2}".format(m[0][0], 1, year_str)
        format_str = make_month_format_str(m[0][0]) + " %d %Y"
        return pd.to_datetime(time_str, format=format_str)

    # no matches
    return None


# end extract_date()


# Quick test of extract_date()
i = 0
for line in doc:
    d = extract_date(line)
    if d is None:
        print("{} : {}".format(i, line))
    else:
        print("{} : {}".format(i, d))
    i += 1

#
# # 04/20/2009; 04/20/09; 4/20/09; 4/3/09
# r1 = df.str.extract(r'\b(?P<month>[\d]{2,4})\s?/\s?(?P<day>[\d]{1,2})\s?/\s?(?P<year>[\d]{2,4})\b')
#
# # 6/2008; 12/2009
# r2 = df.str.extract(r'\b(?P<month>[\d]{2,4})\s?/\s?(?P<year>[\d]{2,4})\b')
#
# # 2009; 2010
# r3 = df.str.extract(r'\b(?P<year>[\d]{2,4})\b')
#
# res = r1.copy()
#
# for x in res.index:
#     if pd.isnull(res['day'][x]) and not pd.isnull(r2['month'][x]):
#         res['day'][x] = 1
#         res['month'][x] = r2['month'][x]
#         res['year'][x] = r2['year'][x]
#
# for x in res.index:
#     if pd.isnull(res['day'][x]) and not pd.isnull(r3['year'][x]):
#         res['day'][x] = 1
#         res['month'][x] = 1
#         res['year'][x] = r3['year'][x]
#
# # Mar-20-2009; Mar 20, 2009; March 20, 2009; Mar. 20, 2009; Mar 20 2009;
# # Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
# r4 = df.str.lower().str.extract(r'\b(?P<month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may'
#                                 r'|june?|july?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?'
#                                 r'|nov(?:ember)|dec(?:ember)?)(?:[\.\-\s]\s*)'
#                                 r'(?P<day>[\d]{1,2})(?:[st|nd|rd|th]?[\-,\.\s]\s*)'
#                                 r'(?P<year>[\d]{2,4})\b')
# r4d = r4[not pd.isnull(r4['month'])]
#
# # 20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
# r5 = df.str.lower().str.extract(r'(\b(?P<day>[\d]{1,2})([st|nd|rd|th]?[,\.\s]\s*))'
#                                 r'(?P<month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may'
#                                 r'|june?|july?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?'
#                                 r'|nov(?:ember)|dec(?:ember)?)([\.\-\s]\s*)'
#                                 r'(?P<year>[\d]{2,4})\b')
# r5d = r5[not pd.isnull(r5['month'])]
# r5d['key'] = r5d.index
#
# r5d.merge(r4d, how='outer')
#
# # Feb 2009; Sep 2009; Oct 2010
# r6 = df.str.lower().str.extract(r'(?P<month>jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may'
#                                 r'|june?|july?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?'
#                                 r'|nov(?:ember)|dec(?:ember)?)([\.\-\s]\s*)'
#                                 r'(?P<year>[\d]{2,4})\b')
