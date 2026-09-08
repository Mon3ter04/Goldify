from dotenv import load_dotenv
from os import getenv
from datetime import datetime,date
from typing import Literal
from dateutil.relativedelta import relativedelta
import requests
from pathlib import Path
from json import dump,load
DATA_DIR = Path("data/GOLD_18_RLS")

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
    def find_covering_file(start_date: date, end_date: date):
        if not DATA_DIR.exists():
            return None

        for folder in DATA_DIR.iterdir():
            if not folder.is_dir():
                continue

            range_name = folder.name

            saved_start, saved_end = range_name.split("TO")

            saved_start = date.fromisoformat(saved_start)
            saved_end = date.fromisoformat(saved_end)

            if saved_start <= start_date and end_date <= saved_end:
                return folder / f"{folder.name}.json"

        return None
        
    def get_history(self, start_date: date,end_date: date):
        return self.find_covering_file(start_date,end_date)

    @staticmethod
    def save_history(start_date,end_date,response_data):
        folder = DATA_DIR / f"{start_date}TO{end_date}"
        folder.mkdir(parents=True, exist_ok=True)
        filepath = folder / f"{start_date}TO{end_date}.json"
        
        with open(filepath, "w", encoding="utf-8") as file:
            dump(response_data, file, indent=4)

    @staticmethod
    def file_load(filepath):
        with open(f"{filepath}", "r", encoding="utf-8") as file :
            return load(file)


    def get_day_price(self): 
        data= self.base_request(self.api_config["header"],
            self.api_config["url"])

        return self.response_cleaner(data, "day")

    def get_week_price(self):
        start_date, end_date = self.get_date("week")
        url = self.api_config["url"]+f"/history?from={start_date}&to={end_date}"

        hist = self.get_history(start_date, end_date)
        if hist == None :
            data = self.base_request(self.api_config["header"],url)
            cleared_data = self.response_cleaner(data, "week")
            saved_data = self.save_history(start_date, end_date, cleared_data)
            return cleared_data
        else :
            return self.file_load(hist)

       
    def get_month_price(self):
        start_date, end_date = self.get_date("month")
        url = self.api_config["url"]+f"/history?from={start_date}&to={end_date}"

        hist = self.get_history(start_date, end_date)
        if hist == None :
            data = self.base_request(self.api_config["header"],url)
            cleared_data = self.response_cleaner(data, "month")
            saved_data = self.save_history(start_date, end_date, cleared_data)
            return cleared_data
        else :
            return self.file_load(hist)
        
    
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

    
