# Marvel Strike Force Player and Alliance Management Tools

The attempt is to automate data collection for player and alliance management to find a stop gap for a missing api or data scraping ability. 

Can convert an alliances player data from spreadsheet to json data. The initial spreadsheet data is manually entered.

First attempt at the automated data collection is by taking screenshots of the player profile page that would upload to a cloud directory that the program will download a zip, unzip package, and use pytesseract OCR to parse relevant player data to then populate the alliance data. 

Currently, the OCR has a long (very long) way to go... If I can get it to work, the rest of the data work will be relatively simple and straightforward. 
