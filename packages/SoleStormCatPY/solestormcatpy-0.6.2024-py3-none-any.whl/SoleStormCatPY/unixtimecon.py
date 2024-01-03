#This utilizes Python's datetime.datetime module and tztime to show Unix Timestamp in current time

from datetime import datetime as dt
import tzlocal as lt

#To use this, just run SoleStormCatPY.unixtimecon.unixConvertor()
def unixConvertor():
    #Found at https://stackoverflow.com/a/40769643
    unixInput = input('What is the Unix time that you want to convert?     ')
    unixTime = float(unixInput)
    myTime = lt.get_localzone()
    localTime = dt.fromtimestamp(unixTime, myTime)

    print('Unix time converted to your local time: ')
    print(localTime.strftime("%Y-%m-%d %H:%M:%S.%f%z (%Z)"))

#To use this, run SoleStormCatPY.unixtimecon.unixConvertorN(number), where number is the Unix time
def unixConvertorN(number):
    #Uses stuff from the unixConvertor() command
    unixInput = float(number)
    myTime = lt.get_localzone()
    localTime = dt.fromtimestamp(unixInput, myTime)

    print('Local time for Unix time ',number)
    print(localTime.strftime("%Y-%m-%d %H:%M:%S.%f%z (%Z)"))

#To use this, just run SoleStormCatPY.unixtimecon.unixPrint()
def unixPrint():
    #Found at https://stackoverflow.com/a/75417916
    unixTime = (dt.now() - dt(1970,1,1)).total_seconds()

    print('The Current Unix Time is:')
    print(unixTime)