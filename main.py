from api.gold_api import GoldAPI 
import os
ga = GoldAPI()
clear = lambda: os.system("cls")

if __name__ == "__main__":

    time  = int(input("day: 1, week: 2, month: 3 : \n\n\n"))

    match time :
        case 1 :
            print(ga.get_day_price())
        case 2 :
            print(ga.get_week_price())
        case 3 :
            print(ga.get_month_price())