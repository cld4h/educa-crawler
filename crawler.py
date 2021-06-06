import requests
from bs4 import BeautifulSoup

SearchPageURL = "https://w05.educanada.ca/index.aspx?action=programsearch-rechercheprogramme&lang=eng"
ResultPageURL = 'https://w05.educanada.ca/index.aspx?action=programresult-resultatprogramme&lang=eng'

headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

EduLevdict = {
        'Tra': '3,1,4',
        'Col': '18,5,6,8,31,32',
        'Uni': '25,10,33,34,30,35',
        'Mas': '36,11,27',
        'Doc': '37,12,38,39,40,41'
}

EduLevdescription= {
        'Tra': 'Training',
        'Col': 'College',
        'Uni': 'University',
        'Mas': 'University - Master',
        'Doc': 'University - Doctorate'
}

ProgCatedict = {
        '01':'01-Agriculture, Agricultural Occupations and related sciences',
        '04':'04-Architecture and related services',
        '05':'05-Area, Ethnic, Cultural and Gender Studies',
        '32':'32-Basic Skills',
        '26':'26-Biological and Biomedical sciences',
        '52':'52-Business, Management, Marketing and related support services',
        '09':'09-Communication, Journalism and related programs',
        '10':'10-Communications Technologies and Support Services',
        '11':'11-Computer and Information Sciences and Support Services',
        '46':'46-Construction Trades',
        '13':'13-Education',
        '14':'14-Engineering',
        '15':'15-Engineering Technology',
        '23':'23-English Language and Litterature/Letters',
        '19':'19-Family and Consumer Sciences/Human Sciences',
        '16':'16-Foreign Languages, Literatures and Linguistics',
        '55':'55-French (Canadian) Language and Literatures/Letters',
        '51':'51-Health Professions and related Clinical Sciences',
        '34':'34-Health-Related Knowledge and Skills',
        '53':'53-High School/Secondary Diplomas and Certificate Programs',
        '54':'54-History',
        '35':'35-Interpersonal and Social Skills',
        '22':'22-Law, Legal Services and Legal Studies',
        '36':'36-Leisure and Recreational Activities',
        '24':'24-Liberal Arts and Sciences, General Studies and Humanities',
        '25':'25-Library Science',
        '27':'27-Mathematics and Statistics',
        '47':'47-Mechanic and Repair Technology',
        '29':'29-Military Technologies',
        '30':'30-Multi/Interdisciplinary Studies',
        '03':'03-Natural Resources and Conservation',
        'NC':'NC-Not Codeable',
        '31':'31-Parks, Recreation, Leisure and Fitness Studies',
        '12':'12-Personal and Culinary Services',
        '38':'38-Philosophy and Religion',
        '40':'40-Physical Sciences',
        '48':'48-Precision Production Trades',
        '43':'43-Protective Services',
        '42':'42-Psychology',
        '44':'44-Public Administration and Services',
        '41':'41-Sciences Technology/Technicians',
        '45':'45-Social Sciences',
        '21':'21-Technology Education/Industrial Arts',
        '39':'39-Theological Studies and Religious Vocations',
        '49':'49-Transportation and Materials Moving',
        '50':'50-Visual and Performing Arts'
}

class crawler:

#   proxies = {
#           "http": "http://127.0.0.1:8080",
#           "https": "http://127.0.0.1:8080",
#   }


    def __init__(self, EducationLevel, programCategory, continuefrom=0):
        self.EducationLevel = EducationLevel
        self.programCategory = programCategory
        self.CSV = open(ProgCatedict[programCategory]+"-"+EducationLevel+".csv","a")
        self.continuefrom = continuefrom

    def __del__(self):
        self.CSV.close()

    def getdata(self,fieldset):
        proglist = fieldset.find_all("li","span-8")
        for prog in proglist:
            programName = prog.label.string.lstrip()
            programId = prog.find_all(attrs={"name": "programId"})[0]['value']
            programURL = prog.a['href']
            programtl = prog.a['title'].split(',')
            schoolName = programtl[0]
            cityName = programtl[1].lstrip()
            provinceName = programtl[2].lstrip()
            self.CSV.write(programId+','+provinceName+','+cityName+','+programName+','+programURL+','+schoolName+','+ProgCatedict[self.programCategory]+','+EduLevdescription[self.EducationLevel]+'\n')

    def crawling(self):
        try:
            self.SR_result = requests.get(SearchPageURL,headers=headers)
            # Raise exception if got 4xx or 5xx
            self.SR_result.raise_for_status()
            self.SR_cookies = self.SR_result.cookies
            self.SR_soup = BeautifulSoup(self.SR_result.content,"html.parser")

            self.VIEWSTATE = self.SR_soup.find_all("input",id="__VIEWSTATE")[0]['value']
            self.VIEWSTATEGENERATOR= self.SR_soup.find_all("input",id="__VIEWSTATEGENERATOR")[0]['value']
            self.EVENTVALIDATION= self.SR_soup.find_all("input",id="__EVENTVALIDATION")[0]['value']

            self.queryData = {
                    '__VIEWSTATE': self.VIEWSTATE,
                    '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR,
                    '__EVENTVALIDATION': self.EVENTVALIDATION,
                    'HomeTab$Home$TextBoxKeyword': '',
                    'HomeTab$Home$ddlKeyWordSearchType': '1',
                    'HomeTab$Home$ddlCategories': self.programCategory,
                    'HomeTab$Home$ddlStudyLanguage': '2',
                    'EducationLevel': EduLevdict[self.EducationLevel],
                    'Provinces': '14',
                    'HomeTab$Home$Submit': 'Display a List of Programs'
            }

            PP_results = requests.post(SearchPageURL, headers=headers, cookies=self.SR_cookies, data=self.queryData)
            PP_soup = BeautifulSoup(PP_results.content,"html.parser")
#           fieldset tag contains Ten programs info
            fieldset = PP_soup.fieldset
            buttons = fieldset.nextSibling.nextSibling
            button_num = 2
            print(fieldset.legend.string)
            pages = len(buttons.find_all(attrs={"type": "submit"})) - 1
            jump = 0
            if self.continuefrom:
                button_num = self.continuefrom
                jump = self.continuefrom - 2
                print("Continue From Page"+str(self.continuefrom))
            else:
                self.getdata(fieldset)
            while button_num <= pages:
                self.PP_VIEWSTATE = PP_soup.find_all("input",id="__VIEWSTATE")[0]['value']
                self.PP_VIEWSTATEGENERATOR = PP_soup.find_all("input",id="__VIEWSTATEGENERATOR")[0]['value']
                self.PP_EVENTVALIDATION = PP_soup.find_all("input",id="__EVENTVALIDATION")[0]['value']
                self.PP_queryData = {
                        '__VIEWSTATE': self.PP_VIEWSTATE,
                        '__VIEWSTATEGENERATOR': self.PP_VIEWSTATEGENERATOR,
                        '__EVENTVALIDATION': self.PP_EVENTVALIDATION,
                        "HomeTab$Home$ProgramListTableSearch$RepeaterNextPageing$ctl%02d$Button1"%jump: str(button_num)
                        # You can also try to jump backward "HomeTab$Home$ProgramListTableSearch$RepeaterPerviousPageing$ctl%02d$LinkButtonPage"%(button_num-1)
                }
                #print(self.PP_queryData)
                retry_times=4
                while True:
                    PP_results = requests.post(ResultPageURL, headers=headers, cookies=self.SR_cookies, data=self.PP_queryData)
                    retry_times=retry_times-1
                    if PP_results.status_code == 200:
                        break
                    if retry_times < 0:
                        break
                PP_results.raise_for_status()
                PP_soup = BeautifulSoup(PP_results.content,"html.parser")
                fieldset = PP_soup.fieldset
                print(ProgCatedict[self.programCategory]+":"+self.EducationLevel+":Page"+str(button_num))
                self.getdata(fieldset)
                button_num = button_num + 1
                if jump:
                    jump = 0
        except Exception as e:
            print(e)

if __name__ == "__main__":
    Edu = [
            "Uni"
            ]
    Cat = [
            "14"
            ]
    for cat in Cat:
        for edu in Edu:
            c = crawler(edu,cat,23)
            c.crawling()
