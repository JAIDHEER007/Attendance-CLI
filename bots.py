import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import quote_plus
import copy

class Bot1:
    __headers = {
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "Connection": "keep-alive"
    }

    # URLs
    urlDefault = "http://info.aec.edu.in/aec/default.aspx"
    urlAttnd = "http://info.aec.edu.in/AEC/ajax/StudentAttendance,App_Web_z03ar5c-.ashx"
    
    # Payloads
    loginPayload = "__VIEWSTATE={viewstate}&__VIEWSTATEGENERATOR={viewstategenerator}&__EVENTVALIDATION={eventvalidation}&txtId1=&txtPwd1=&txtId2={uid}&txtPwd2={pwd}&imgBtn2.x=41&imgBtn2.y=18&txtId3=&txtPwd3="
    attndPayload = "rollNo={rid}\nfromDate={fDate}\ntoDate={tDate}\nexcludeothersubjects=false"

    # Query Params
    querystring = {"_method":"ShowAttendance","_session":"r"}

    def __init__(self, userData):
        self.__userData = userData
        self.cookieJar = {}
        self.formData = {}

    def checkInternet(self) -> None:
        try:
            response = requests.request("GET", "http://google.com")
            if response.status_code != 200:
                raise Exception()
        except Exception as exp:
            raise Exception("Check Internet Connection") from None


    def getVitalData(self) -> None:
        """
            Extracts ASP.NET Session ID\n
            Extracts Hidden Form Data that is used for form Validation
        """

        payload = ""

        response = requests.request("GET", Bot1.urlDefault, data=payload, headers = Bot1.__headers)

        if response.status_code != 200:
            raise Exception("Failed to get ASP Session ID Cookie")
        
        try: 
            aspCookie = dict(response.history[1].cookies)
            aspCookie['ASP.NET_SessionId']
        except Exception as exp:
            raise Exception("Failed to get ASP Session ID Cookie") from None
        
        self.cookieJar.update(aspCookie)

        soup = BS(response.text, 'html.parser')
        self.formData['viewstate'] = soup.find("input", {"type":"hidden", "id":"__VIEWSTATE"})['value']
        self.formData['viewstategenerator'] = soup.find("input", {"type":"hidden", "id":"__VIEWSTATEGENERATOR"})['value']
        self.formData['eventvalidation'] = soup.find("input", {"type":"hidden", "id":"__EVENTVALIDATION"})['value']

    def makeLogin(self) -> None:
        payload = Bot1.loginPayload.format(
            viewstate = quote_plus(self.formData['viewstate']), 
            viewstategenerator = quote_plus(self.formData['viewstategenerator']),
            eventvalidation = quote_plus(self.formData['eventvalidation']),
            uid = quote_plus(self.__userData['uid']),
            pwd = quote_plus(self.__userData['pwd'])
        )
        
        headers = copy.deepcopy(Bot1.__headers)
        headers["cookie"] = "ASP.NET_SessionId={}".format(self.cookieJar['ASP.NET_SessionId'])
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        response = requests.request("POST", Bot1.urlDefault, data=payload, headers=headers)

        if response.status_code != 200:
            raise Exception("Failed to get Form Authentication Cookie")
        

        try: 
            frmAuthCookie = dict(response.history[0].cookies)
            frmAuthCookie['frmAuth']
        except Exception as exp:
            raise Exception("Failed to get Form Authentication Cookie. Check User ID and Password") from None
        
        self.cookieJar.update(frmAuthCookie)

    def getAttendanceRD(self, fDate = "", tDate = "") -> str:
        
        payload = Bot1.attndPayload.format(
            rid = quote_plus(self.__userData['uid']),
            fDate = fDate,
            tDate = tDate
        )

        headers = copy.deepcopy(Bot1.__headers)
        headers['cookie'] = "ASP.NET_SessionId={aspCookie}; frmAuth={frmAuthCookie}".format(
            aspCookie = self.cookieJar['ASP.NET_SessionId'], 
            frmAuthCookie = self.cookieJar['frmAuth']
        )

        response = requests.request("POST", Bot1.urlAttnd, data=payload, headers=headers, params=Bot1.querystring)

        return response.text
