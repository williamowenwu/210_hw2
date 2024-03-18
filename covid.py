import csv
from collections import defaultdict

# averages the age in a list of dicts in format (age-age)
def avg_age(covid_dict: list[dict]):
    for person in covid_dict:
        if not person['age'].isdigit():
            low, hi = person['age'].split('-')
            person['age'] = round((float(hi) + float(low))/2)
            print(f"ID: {person['ID']} new age: {person['age']}")
            
def alter_date(covid_dict: list[dict]):
    for person in covid_dict:
        for date in ['date_onset_symptoms', 'date_admission_hospital', 'date_confirmation']:
            day, month, year = person[date].split('.')
            person[date] = f"{month}.{day}.{year}"
            # print(f"ID: {person['ID']} new dates: {person[date]}")

def fill_long_lat(covid_dict: list[dict]):
    total_long = defaultdict(float)
    long_count = defaultdict(int)
    total_lat = defaultdict(float)
    lat_count = defaultdict(int)
    
    for person in covid_dict:
        if person["latitude"] != "NaN":
            total_long[person['province']] += float(person['latitude'])
            long_count[person['province']] += 1
        if person["longitude"] != "NaN":
            total_lat[person['province']] += float(person['longitude'])
            lat_count[person['province']] += 1
    
    for person in covid_dict:
        if person["latitude"] == "NaN":
            person['latitude'] = round(total_lat[person['province']]/lat_count[person['province']],2)
        if person["longitude"] == "NaN":
            person['longitude'] = round(total_long[person['province']]/long_count[person['province']], 2)

# fills in missing city
def fill_in_city(covid_dict: list[dict]):
    all_cities = defaultdict(list)
    num_of_cities = defaultdict(lambda: defaultdict(int))
    for person in covid_dict:
        if person['city'] != 'NaN':
            if person['city'] not in all_cities[person['province']]:
                all_cities[person['province']].append(person['city'])
            num_of_cities[person['city']] += 1
    
    most_common_city_by_province = {}
    
    most_common_city_by_province = {}
    for province, cities in all_cities.items():
    # Find the city with the highest count, sorting alphabetically in case of a tie
        max_city = sorted(num_of_cities[province].items(), key=lambda x: (-x[1], x[0]))[0][0]
        most_common_city_by_province[province] = max_city

    # for person in covid_dict:
    #     if person['city'] == 'NaN':
    #         person['city'] = max_keys[person['province']]

if __name__ == "__main__":
    with open('covidTrain.csv', 'r') as f:
        covid_dict = list(csv.DictReader(f))

        avg_age(covid_dict)
        
        alter_date(covid_dict)
        
        fill_long_lat(covid_dict)
        
        fill_in_city(covid_dict)
        
        with open("covidResult.csv", 'w') as result:
            fields = covid_dict[0].keys()
            writer = csv.DictWriter(result, fieldnames=fields)
            writer.writeheader()
            for person in covid_dict:
                writer.writerow(person)