import Spreadsheet
sheet = App.ActiveDocument.addObject("Spreadsheet::Sheet")
sheet.Label = "Dimensions"


App.getDocument("ciambella").saveAs(u"/home/giacomo/prova.FCStd")

mysql -h 172.17.0.2 -u freecad -p DBTubi