# *************** HOMEWORK 6 ***************
# TODO: GOOD LUCK!

# ****************************************************** Start **********************************************
import yfinance as yf
import datetime
from matplotlib import pyplot as plt

today = datetime.date.today()


def get_object_single_stock(name_stock, start='1980-01-01', end=str(today), interval='5d'):
    """
    the function makes dataframe with the historical details about the stock by the function arguments
    :param name_stock:(str) name of the stock
    :param start:(str) start date
    :param end: (str) ending date
    :param interval:(str) time interval
    :return:(dataframe) the function makes dataframe
     with the historical details about the stock by the function arguments
    """
    ticker_name = yf.Ticker(name_stock)
    data_frame = ticker_name.history(interval=interval, start=start, end=end)
    return data_frame


def get_object_multiple_stock(list_stocks, start='1980-01-01', end=str(today), interval='5d'):
    """
    the function returns historical data about list of stocks
    :param list_stocks: (list(str)) list with stocks names
    :param start:(str) start date
    :param end: (str) ending date
    :param interval:(str) time interval
    :return: (dict) dictinary with stock name as key and dataframe as value
    """
    multiple_stock = {}
    for i in list_stocks:
        multiple_stock[i] = get_object_single_stock(i, start, end, interval)
    return multiple_stock


def get_object_multiple_stock_v2(list_stocks, start='1980-01-01', end=str(today), interval='5d'):
    """
    the function returns historical data about stocks
    :param list_stocks: (list(str)) list of the stocks names
    :param start:(str) start date
    :param end: (str) ending date
    :param interval:(str) time interval
    :return: (dataframe) the function returns dataframe with the columns grouped by the stock name
    """
    data_frame = yf.download(list_stocks, start=start, end=end, interval=interval, group_by="Ticker")
    return data_frame


# ******************************************************PART 1 - info**********************************************
def daily_return(stock):
    """
    the function gets dataframe and calculates the % of the daily revenue of the stock.
    :param stock:(dataframe) data frame of the stock
    :return:(float) the percentage of the revenue
            (float) the std of the revenue
    """
    index = stock.index
    number_of_rows = len(index)
    i = number_of_rows
    average_list = []
    while i > 1:
        day_zero = stock['Close'].iloc[i - 2]
        day_one = stock['Close'].iloc[i - 1]
        average = ((float(day_one) - float(day_zero)) / float(day_zero)) * 100
        average_list.append(average)
        i -= 1
    average_b = sum(average_list) / len(average_list)
    var = sum((l - average_b) ** 2 for l in average_list) / len(average_list)
    std = var ** (1 / 2)
    return average_b, std


def information_of_stock(name_stock):
    """
    the function returns the dividend and the stock web
    :param name_stock: (str) stock name
    :return: (float) stock's dividend , (str) the website of the stock
    """
    stock = yf.Ticker(name_stock)
    try:
        div_rate = stock.info['dividendRate']
        url = stock.info["website"]
        return div_rate, url
    except:
        return None


# ******************************************************PART 2 - plot**********************************************

def plot_price(stock):
    """
    the function returns graph of the the close value of the stock for years
    :param stock:(DataFrame) dataframe of the stock
    :return:(AxesSubplot) object that represents the graph
    """
    fig, axe = plt.subplots()
    axe.plot(stock['Close'], color='deeppink')
    axe.set_title('Stock prices')
    axe.set_xlabel('Date')
    axe.set_ylabel('Close')
    return axe


# ******************************************************PART 3 - file**********************************************
def save_dividends(name_stock):
    """
    the function gets str with stock name and writes in file the dividends value that big or equal to the median.
    the dividends values will be writen line by line from to lowest value to the biggest by time stamp.
    :param name_stock:(str) the name of the stock
    :return: (csv file) dividends file
    """
    stock = yf.Ticker(name_stock)
    dib = stock.dividends
    med_b = dib.median()
    bigger_than_med = dib >= med_b
    clean = dib[bigger_than_med]
    clean.index = clean.index.strftime('%Y-%m-%d %H:%M:%S')
    clean.to_csv("Dividends.csv")
