from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF
from requests import *
from yahoo_finance import Share
import pandas as pd
from pandas import DataFrame


# As the data from swpc is not avaliable as in the book, so in this demo program,
# I will use the data from Yahoo finance to test the reportlab.

apple = Share('AAPL')
historical_data = apple.get_historical('2015-01-01', '2015-12-31')
data = DataFrame(historical_data)[['Close', 'Date', 'Volume']].reindex(columns=['Date', 'Close', 'Volume'])

price = data['Close'].tolist()
price = list(map(float, price))
volume = data['Volume'].tolist()
tmp = data['Date'].tolist()
date = list(range(0, len(tmp)))
drawing = Drawing(400, 200)
lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
dis_data = list(zip(date, price))
lp.data = [dis_data]
lp.lines[0].strokeColor = colors.blue
drawing.add(lp)
renderPDF.drawToFile(drawing, 'sample.pdf', 'Apple')
print('end')
