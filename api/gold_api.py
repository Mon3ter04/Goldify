from dotenv import load_dotenv
from os import getenv
from datetime import datetime
from typing import Literal
from dateutil.relativedelta import relativedelta

class GoldAPI :
    def __init__(self):
        self.api_config = self.load_config()

    @staticmethod
    def load_config():
        load_dotenv()
        api_key = getenv("API_KEY")
        api_url = getenv("API_URL")
        headers = {
            "Accept": "application/json",
            "X-API-Key":api_key
        }
        if not api_key :
            raise ValueError("api key not found")
        elif not api_url :
            raise ValueError("api url not found")
        else :
            return {"header" : api_key, "url" : api_url}

    @staticmethod
    def base_request(header,url):
        response = requests.get(
            url=url,
            header=header
        )

        return response.json()

    @staticmethod
    def get_date(time_frame : Literal["week","month","year"]) :

        today = datetime.datetime.now().date()
        match time_frame :
            case "week" :
                return [today,today - relativedelta(weeks=1)]
            case "month" :
                return [roday,today - relativedelta(months=1)]
            case "year" :
                return [today,today - relativedelta(years=1)]
            case _ :
                raise ValueError("wrong value")
 

    def get_day_price(self):
        self.api_info = self.api_config
        day_date = base_request()


        response = ""

        return response

    def get_week_price(self):
        start_date = get_date("week")[0]
        des_date = get_date("week")[1]
        self.api_info = self.api_config
        self.week_url = self.api_info[url+f"history?from={start_date}&to={des_date}"]
        week_data = base_request(self.api_info["header"],self.week_url)
        return week_data
        

    def get_month_price(self):
        start_date = get_date("month")[0]
        des_date = get_date("month")[1]
        self.api_info = self.api_config
        self.month_url = self.api_info[url+f"history?from={start_date}&to={des_date}"]
        month_data = base_request(self.api_info["header"],self.week_url)

        return month_data



        response = ""

        return response
    
    def response_cleaner(self,response) :

        self.clean_response = ""

        return clean_response


    
    
