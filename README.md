# HSBCGroup
This is a python application to add mulitple people to a whatsapp group from a CSV.


This is based off the code seen here: https://github.com/CodeChefVIT/whatsapp-groupadd/tree/master

Rather than the CSV format described in the above project, the phone numbers can be selected with any format CSV by specifying the name/path of the CSV, and then the name of the column that contains the phone numbers.

No need to save the contacts, but does require the CSV with the phone numbers, selenium, and the desktop version of Whatsapp.

To run:
Update path and CSV Column name.

Download necessary libraries and selenium from: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH
Make sure to download the right version based off your Edge version which you can find by clicking the three ... -> Help and feedback -> About Microsoft Edge

if you're on Windows:
Run pip install -r requirements.txt
