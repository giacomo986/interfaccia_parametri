import Spreadsheet
sheet = App.ActiveDocument.addObject("Spreadsheet::Sheet")
sheet.Label = "Dimensions"


App.getDocument("ciambella").saveAs(u"/home/giacomo/prova.FCStd")