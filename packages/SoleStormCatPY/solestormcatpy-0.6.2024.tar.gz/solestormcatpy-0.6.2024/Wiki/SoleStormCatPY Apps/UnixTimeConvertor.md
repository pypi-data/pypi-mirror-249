# UnixTimeConvertor
`unixtimecon` is a module that allows for a person to see the current Unix time, and allows for the user to put in any Unix time to see what the time would be in their area. REQUIRES `tzlocal` MODULE.
 Commands `unixConvertor()` and `unixConvertorN()` used [this](https://stackoverflow.com/a/40769643) 
 resource for creation. `unixPrint()` used [this](https://stackoverflow.com/a/75417916) for creation.
## How to Use
There are 3 ways to use `unixtimecon`.
The first, being a time convertor, which translates a Unix time to your local time. To use, run `SoleStormCatPY.unixtimecon.unixConvertor()`. THe second is the same as the first, but the Unix time is specified in the command. To use, run `SoleStormCatPY.unixtimecon.unixConvertorN(number)`, where `number` is the Unix time that you want to use. The third shows the current Unix time. To use, run `SoleStormCatPY.unixtimecon.unixPrint()`.