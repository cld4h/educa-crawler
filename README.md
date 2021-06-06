# This project is to get program information from educanada.ca

Searching Page URL: https://w05.educanada.ca/index.aspx?action=programsearch-rechercheprogramme&lang=eng

## Dependency

* [requests](https://docs.python-requests.org/en/master/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
## Output Format

```csv
programId,provinceName,cityName,programName,programURL,schoolName,programCategory,EducationLevel
```

## Education Level

EducationLevel, value
Training, 3,1,4
College, 18,5,6,8,31,32
University, 25,10,33,34,30,35
University - Master, 36,11,27
University - Doctorate, 37,12,38,39,40,41

## Program Category

programCategory,description
01,Agriculture, Agricultural Occupations and related sciences
04,Architecture and related services
05,Area, Ethnic, Cultural and Gender Studies
32,Basic Skills
26,Biological and Biomedical sciences
52,Business, Management, Marketing and related support services
09,Communication, Journalism and related programs
10,Communications Technologies and Support Services
11,Computer and Information Sciences and Support Services
46,Construction Trades
13,Education
14,Engineering
15,Engineering Technology
23,English Language and Litterature/Letters
19,Family and Consumer Sciences/Human Sciences
16,Foreign Languages, Literatures and Linguistics
55,French (Canadian) Language and Literatures/Letters
51,Health Professions and related Clinical Sciences
34,Health-Related Knowledge and Skills
53,High School/Secondary Diplomas and Certificate Programs
54,History
35,Interpersonal and Social Skills
22,Law, Legal Services and Legal Studies
36,Leisure and Recreational Activities
24,Liberal Arts and Sciences, General Studies and Humanities
25,Library Science
27,Mathematics and Statistics
47,Mechanic and Repair Technology
29,Military Technologies
30,Multi/Interdisciplinary Studies
03,Natural Resources and Conservation
NC,Not Codeable
31,Parks, Recreation, Leisure and Fitness Studies
12,Personal and Culinary Services
38,Philosophy and Religion
40,Physical Sciences
48,Precision Production Trades
43,Protective Services
42,Psychology
44,Public Administration and Services
41,Sciences Technology/Technicians
45,Social Sciences
21,Technology Education/Industrial Arts
39,Theological Studies and Religious Vocations
49,Transportation and Materials Moving
50,Visual and Performing Arts
