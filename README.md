# TweeterSraper
scrap data of like and retweet for each url from a select excel file

# 🌟 Project TweeterSraper 🌟  
*scrap like and retweet from tweeter link for you ✨*  

![Version](https://img.shields.io/badge/version-1.1.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)  

🚀 **Welcome to the automation future.** This project is just a fun side project to help my friends works on their task.  

---

## 🔥 Features  
- **Browse Excel file to load data**: Automatically get all data from excel and process load each of the twitter page and get the number of like and retweet.  
- **Display table of data**: Once all link processed and receive all the data, it will display the table that allow you to copy by click the first row and hold shift then select the last.  
- **Export excel**: export to replace excel.  

---

## ⚡ Quick Start  

1. **Install**  
   ```bash
   pip install -r requirements.txt
   ```

2. **Create excutable file for window**
   ```bash
   pyinstaller --onefile --add-data "drivers/chromedriver.exe;drivers" main.py
   ```
   
