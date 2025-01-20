!Chromedriver.exe required in project directory for the project to work
!Chromedriver version needs to be equal to chrome version for the project to work

  This repository contains a personal project that uses data from 2 sources, an API and webscraped data, to compare gas prices between 2 Romanian cities.

  For the implementation, the city inserted in the first textbox uses API calls to get the prices of all the gas stations in the specified city. The first API call gets the code for the searched city, the second API call returns all the gas stations
with their informations. Afterwards, the code processes the information and extracts only the gas station name and gas price, deletes entries if there are duplicate lines, and creates a .csv file named "produse_combustibili_{input_text1}_API.csv" .
  The API used is undocumented, from this website - https://monitorulpreturilor.info/ .
  
  For the city inserted in the second textbox, the code webscrapes all the listings of gas stations of a city after a search. For this task, I used Chromedriver version 131 with selenium to automate the process of searching the specified city. The automation
itself opens chrome on this website - https://www.peco-online.ro/index.php, inserts the city in the "Introduceti locatia" textbox, hits "Cauta", and then extracts the list with all the gas stations and their prices. After filtering the duplicate
data, the code saves all the gas stations names and prices, and creates a .csv file named "produse_combustibili_{input_text2}_webscraped.csv".

  As for the visualization of the data extracted, I have a function called "compare_fuel_prices(file1, file2, city1, city2)", that takes both .csv files crated and the city names and creates a bar graph that shows the gas price differences for all
the common and different gas stations found in the 2 cities specified in the text boxes of the UI.

  The UI itself is very easy to use, all you have to do is insert 2 Romanian cities in the first and second text boxes, and then hit "Caută prețuri". Afterwards, in the project directory 2 .csv files will be created, named corresponding to the
datasource they have (API/Webscraped data). The data in the .csv files is already processed, so it is readable.
