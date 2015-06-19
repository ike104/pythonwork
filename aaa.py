
import csv

csvFile = open('csvtst.txt', 'wb')
csvField = ['data-eventid','date','time','currency','event']
csvWriter = csv.DictWriter(csvFile,csvField,extrasaction='ignore',delimiter=',',quoting=csv.QUOTE_MINIMAL)
dat = {'impact': '', 'actual': '', 'graph': '', 'detail': '', 'forecast': '0.0%', 'currency': 'EUR', 'data-eventid': '57605', 'time': 'All Day', 'date': 'Mon', 'event': 'German Prelim CPI m/m', 'previous': '0.0%'}
csvWriter.writerow(dat)
csvFile.close()
