## THIS IS OUR PROGRAM WHICH WILL BE USED TO TAKE JSON DATA 

import json
import csv
from decimal import *
import datetime
import pandas as pd
from sklearn.cluster import KMeans 


def main(args):
    file = 'activities.txt'
    opened = open(file,encoding='utf-8')
    var = opened.read()
    vars_js = json.loads(var)
    vars_js_n = []
    for each in vars_js:
        if each['start_latitude'] is not None:
            vars_js_n.append(each)
    vars_js_k = []
    for each in vars_js:
        if each['start_latitude'] is not None:
            vars_js_k.append({'distance':pow(each['distance']/150,.35),
                          'elevtime':pow((each['total_elevation_gain']/each['moving_time'])*150,.8)})
    df = pd.DataFrame(vars_js_k)
    kmeans = KMeans(n_clusters=6,random_state=3425)
    kmeans.fit(df)
    labels = kmeans.predict(df)
    labels2 = []
    for each in labels:
        if each==0:
            labels2.append(2)
        if each==1:
            labels2.append(1)
        if each==2:
            labels2.append(0)
        if each==3:
            labels2.append(2)
        if each==4:
            labels2.append(0)
        if each==5:
            labels2.append(1)

    for x in range(len(labels)):
        vars_js_n[x]['difficulty'] = labels2[x]

    with open('acts_rows.csv', 'w', newline='') as csvfile:
        actwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        actwriter.writerow(["Run ID","Distance","Time","Time Changed","Moving Time","Elevation Gain","Elevation Over Time",
                    "Start Latitude","Start Longitude","Polyline","Difficulty"])
        for each in vars_js_n:
            lat_s = each['start_latitude']
            lon_s = each['start_longitude']
            #print(lat_s)
            if lat_s is not None:
                if (Decimal(lat_s) <= 34 and Decimal(lat_s) >= 33):
                    time1 = str(datetime.timedelta(seconds=each['moving_time']))
                    actwriter.writerow([each['id'],each['distance']/1609.344,each['moving_time'],time1,
                        each['elapsed_time']-each['moving_time'],each['total_elevation_gain'],
                        each['total_elevation_gain']/each['moving_time'],
                        lat_s,lon_s,each['map']['summary_polyline'],each['difficulty']])

if __name__=="__main__":
    import sys
    main(sys.argv)