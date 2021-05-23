import requests
from datetime import datetime
cowin_url= "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
telegram_api_url= "https://api.telegram.org/bot1841619990:AAHVHp1shdmcSjbVnF_9zUOPciS_r0uT7No/sendMessage?chat_id=@__groupid__&text="
now=datetime.now()
today_date= now.strftime("%d-%m-%Y")
groupid= "kannur_vaccine"

district_id=297

def get_data_from_cowin(district_id):
	query= "?district_id={}&date={}".format(district_id, today_date)
	final_url= cowin_url+query
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	response=requests.get(final_url,headers=headers)
	get_availability(response)

        

def get_availability(response):
     response_json= response.json()
     for center in response_json["centers"]:
         for session in center["sessions"]:
             if(session["available_capacity_dose1"]> 0 and session["min_age_limit"]<45 ):
                 message= "Name: {} , Slots: {}, MinimumAge: {}".format(
                     center["name"],session["available_capacity_dose1"],
                     session["min_age_limit"]
                     )
                 send_to_telegram(message)


def send_to_telegram(message):
    final_telegram_url=telegram_api_url.replace("__groupid__", groupid)
    final_telegram_url=final_telegram_url+message
    response=requests.get(final_telegram_url)
    print(response)
    
 


if __name__== "__main__":
	get_data_from_cowin(district_id)
