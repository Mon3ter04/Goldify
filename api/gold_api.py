from dotenv import load_dotenv
from os import getenv
from datetime import datetime
from typing import Literal
from dateutil.relativedelta import relativedelta
import requests

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
            return {"header" : headers, "url" : api_url}

    @staticmethod
    def base_request(header,url):
        response = requests.get(
            url=url,
            headers=header
        )

        return response.json()

    @staticmethod
    def get_date(time_frame : Literal["week","month"]) :

        today = datetime.now().date()
        match time_frame :
            case "week" :
                return [today - relativedelta(weeks=1),today]
            case "month" :
                return [today - relativedelta(months=1),today]
            case _ :
                raise ValueError("wrong value")
    
    @staticmethod
    def get_history(start_date,end_data):
        print()

    def get_day_price(self): 
        data= self.base_request(self.api_config["header"],
        self.api_config["url"])

        return response_cleaner(data, "day")

    def get_week_price(self):
        start_date, end_date = get_date("week")
        url = self.api_config["url"]+f"/history?from={start_date}&to={end_date}"
        data = self.base_request(self.api_info["header"],url)

        return self.response_cleaner(data,"week")
       
    def get_month_price(self):
        start_date, end_date = get_date("month")
        url = self.api_config["url"]+f"/history?from={start_date}&to={end_date}"
        data = self.base_request(self.api_info["header"],url)
        return self.response_cleaner(data,"month")
    
    def response_cleaner(self,data,data_type : Literal["day","week","month"]) :
        match data_type :
            case "day" :
                clean_day_data = {data["businessTime"][:10] : data["value"]}
                return clean_day_data

            case "week" :
                self.clean_week_data = {}
                for item in data :
                    self.clean_week_data.update({f"{item["businessTime"][:10]}":item["value"]})
                return self.clean_week_data
            case "month" :
                self.clean_month_data = {}
                for item in data :
                    self.clean_month_data.update({f"{item["businessTime"][:10]}":item["value"]})
                return self.clean_month_data

    
