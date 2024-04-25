'''
The Visual Studio Code Exchange 
A paper trading application in the terminal.

Users can access real time stock market data using Yahoo API
Users can analyze company data and even access news sources thorugh URL
User will be able to access thier portoflio and make trades via command line interface
User will be able to buy and sell securities of a desired stock in a simulated enviorment
Cryptocurrencies are unsupported 

/// DISCLAIMER ///
ALL OPENSOURCE LIBRARIES AND APIS HAVE BEEN CITED PER THE ACADEMIC CODE
'''

#Module imports
import yfinance as yf # yfinance 0.2.37 - Opensource library for extracting live and historical stock market data using publicy available Yahoo API's; GitRepo https://github.com/ranaroussi/yfinance
import plotext as plt # plotext 5.3.0 - Opensource library for plotting data directily in terminal; GitRepo https://github.com/piccolomo/plotext
import pprint # - Library for organized lengthy outputs; https://github.com/python/cpython/blob/3.12/Lib/pprint.py
from datetime import date
import locale

# Set locale to English
locale.setlocale(locale.LC_ALL, 'en_US')

fStringNextLine = "\n"

# Users start out with $250,000 in buying power 
userPortfolio = {
    "name": "",
    "buyingPower": 250000,
    "totalAssets": 0,
    "securities": [],
}

# Initialize User portoflio object/dictionary 
transactionHistory = {
    "buys": [],
    "sells": [],
    'transactionCount': 0
}

# Main Program
def main():

    # Object class for creating a candle stick chart for a stock
    class candleStickChart:
        def __init__(self, symbol, start):
            self.symbol = symbol
            self.start = start

        def showData(self):
            # plotext functions to display candlestick charts
            stock = yf.Ticker(self.symbol)
            stockData = stock.info
            companyName = stockData["shortName"]
            plt.date_form("d/m/Y")
            start = plt.string_to_datetime(self.start)
            end = plt.today_datetime()
            data = yf.download(self.symbol, start, end)
            dates = plt.datetimes_to_string(data.index)

            plt.clf()
            plt.theme("dark")
            plt.candlestick(dates, data)
            plt.title(f"{companyName} Stock Price CandleSticks")

            plt.show()

    # Function for formatting the giant dictionary of comapny data            
    def formatCompanyData(companyData):
        output = "\n"
        for key in companyData:
            value = str(companyData[key])
            output += f"{key : <50}"
            output += f"{value : >0}"
            output += "\n"
        return output        

    # Object class for fetching company data 
    class companyOverview:
        def __init__(self, symbol):
            self.symbol = symbol

        def showData(self):
            data = yf.Ticker(self.symbol)
            data = formatCompanyData(data.info)
            return data


    def answerWithData(answer) -> tuple:
        if answer.lower() == "yes":
            quantData = companyOverview(security)
            return False, quantData.showData()
        if answer.lower() == "no":
            return False, "Very Well"
        else:
            print("Invalid Input")


    # Ask user for name and give them an introduction
    print("\nWelcome, trader! This is the VSXT, or Visual Studio Exchange Terminal! You've finally acquired enough investment capital, $250,000, to buy some serious stocks. The goal is make maximum returns. You'll start by analyzing some company data!\n")
    userPortfolio["name"] = input("What shall I call you? - ")
    print(f"\nHello, {userPortfolio['name']}!\n")
    print("Let's start analyzing some real-time market data. Our Terminal is powered by the publicly available Yahoo API's. We'll be using the data to analyze a companies financial data as well as any relevant news. Most commands are expecting a 'yes' or 'no' input unless specified. And 'exit' is for extiting the command loop and movign on to the next one.\n")

    # Create function for users lookup stocks of their choice and see data
    security = input("Start by entering a SEC valid Ticker - ")
    start = input("Enter starting range for data in d/m/Y - ")
    data = candleStickChart(security, start)
    data.showData()

    userWantsData = True
    while userWantsData:
        answer = input("Would you like to see more data?\n")
        fetchedData = answerWithData(answer)
        fatData = fetchedData[1]
        userWantsData = fetchedData[0]

    print(fatData)


    # WITH SYS.STDIN AS FILE MODULES ARENT GLOBAL! Or you'll get a I/O error!
    # Just use while True loops to get user input.
    symbol = yf.Ticker(security)
    while True:
        userInput = input("Would you like to see news? - ")
        try:
            if userInput == 'yes':
                pprint.pprint(symbol.news)
            elif userInput == 'no':
                print("Alrighty, hustler!\n")
            else:
                raise Exception("yes or no?")
        except Exception as e:
            print(e)
        else:
            break
    
    # Returns True if the user enters a valid command, false otherwise
    def checkCommand(inputs) -> bool:
        if len(inputs) > 1: #Checks if input is more than one word
            if inputs[0] not in commands: #Checks if first word is not a command
                return False
            
            symbol = yf.Ticker(inputs[1]) #Checks if second word is a valid ticker
            data = symbol.info
            if len(data) < 2:
                return False
            return True
        else:
            if inputs not in commands:
                return False
            symbol = yf.Ticker(inputs)
            data = symbol.info
            if len(data) < 2:
                return False
            return True

    class executeTrade:
        def __init__(self, executable, symbol) -> None:
            self.executable = executable
            self.symbol = symbol

        # TODO - User will buy shares at ask price 
        def buy(self):
            print("Your Portfolio\n")
            for asset in userPortfolio['securities']:
                symbol = yf.Ticker(asset['asset'])
                companyData = symbol.info
                try:
                    currentStockValue = companyData['currentPrice']
                except:
                    currentStockValue = companyData['ask'] 

                asset['marketValue'] = asset['sharesBought']*currentStockValue
                asset['totalReturn'] = round(asset['marketValue'] - asset['boughtFor'], 2) 
            pprint.pprint(userPortfolio)


            today = date.today()
            currentDate = today.strftime("%B %d, %Y")

            transactionData = {
                'symbol': self.symbol,
                'transactionType': 'buy',
                'executed': currentDate,
                'pricePerShare': float,
                'sharesBought': float,
            }

            symbol = yf.Ticker(self.symbol)
            companyData = symbol.info
            try:
                price = companyData['ask']
            except:
                price = companyData['currentPrice'] 
            liquidCash = userPortfolio['buyingPower']

            while True:
                try:
                    sharesAmount = float(input('How many shares do you want to buy? - '))
                    if sharesAmount <= 0.000001:
                        raise ValueError("Input a decimal or integer value greater that 0.000001")
                    if userPortfolio['buyingPower'] - sharesAmount*price <= 0:
                        raise ValueError(f"Insuffecient Buying Power. You have {liquidCash}")
                except ValueError as e:
                    print(e)

                else: 
                    cost = round(sharesAmount*price, 2)
                    userPortfolio['buyingPower'] -= cost

                    liquidCash = userPortfolio['buyingPower']
                    transactionData['pricePerShare'] = price
                    transactionData['sharesBought'] = sharesAmount
                    transactionHistory['buys'].append(transactionData)
                    transactionHistory['transactionCount'] += 1
                    cDate = transactionData['executed']

                    # Try and Except handler to fetch data price data when markets are closed, ultimately enabling a 24/7 trading platform
                    try:
                        currentPrice = companyData['bid'] 
                    except:
                        currentPrice = companyData['currentPrice']

                    asset = {
                        "asset": self.symbol,
                        "marketValue": round(currentPrice*transactionData['sharesBought'], 2),
                        "boughtFor": round(transactionData['pricePerShare']*transactionData['sharesBought'], 2),
                        "sharesBought": sharesAmount,
                        "totalReturn": 0,
                    }

                    userPortfolio['securities'].append(asset)
                    userPortfolio['totalAssets'] += asset['marketValue']

                    return f"\nYour buy of {sharesAmount} shares at {locale.currency(cost, grouping=True)} for {self.symbol} has been executed.\nPrice - {locale.currency(price, grouping=True)}\nBuying power - {locale.currency(liquidCash, grouping=True)}\nExecuted - {cDate}\n"
        
        # TODO - User will sell shares at bid price
        def sell(self):
            print("Your Portfolio")
            for asset in userPortfolio['securities']:
                symbol = yf.Ticker(asset['asset'])
                companyData = symbol.info
                try:
                    currentStockValue = companyData['currentPrice']
                except:
                    currentStockValue = companyData['bid'] 

                asset['marketValue'] = asset['sharesBought']*currentStockValue
                asset['totalReturn'] = asset['marketValue'] - asset['boughtFor'] 
            pprint.pprint(userPortfolio)

            today = date.today()
            currentDate = today.strftime("%B %d, %Y")

            transactionData = {
                'symbol': self.symbol,
                'transactionType': 'sell',
                'executed': currentDate,
                'pricePerShare': float,
                'sharesSold': float,
            }

            symbol = yf.Ticker(self.symbol)
            companyData = symbol.info
            
            # Try and Except handler to fetch data price data when markets are closed, ultimately enabling a 24/7 trading platform
            try: 
                price = companyData['bid']
            except:
                price = companyData['currentPrice']

            cDate = transactionData['executed']
            liquidCash = userPortfolio['buyingPower']
            
            while True:
                try:
                    sharesAmount = float(input('How many shares do you want to sell? - '))

                    for security in userPortfolio['securities']:
                        if security['asset'] == self.symbol:
                            amountOfShares = security['sharesBought']

                    if sharesAmount <= 0.000001 or sharesAmount > amountOfShares:
                        raise ValueError("Input a decimal or integer value greater that 0.000001")
                except Exception as e:
                    print(e)
                else:
                    transactionData['pricePerShare'] = price
                    transactionData['sharesSold'] = sharesAmount

                    transactionHistory['sells'].append(transactionData)
                    transactionHistory['transactionCount'] += 1
                    liquidCash += price * sharesAmount
                    userPortfolio['totalAssets'] = liquidCash

                    # TODO - Calculate the average price per share if a user decidesd to buy a stock more than one time 
                        



                    for security in userPortfolio['securities']:
                        if security['asset'] == self.symbol:
                            security['sharesBought'] -= sharesAmount
                            security['boughtFor'] = security['sharesBought'] * price
                            security['marketValue'] = security['sharesBought']*currentStockValue
                            security['totalReturn'] = round(security['marketValue'] - security['boughtFor'], 2)

                    pprint.pprint(userPortfolio)                        
                    return f"\nYour sell of {sharesAmount} shares at {locale.currency(price*sharesAmount, grouping=True)} for {self.symbol} has been executed.\nPrice - {locale.currency(price, grouping=True)}\nBuying power - {locale.currency(liquidCash, grouping=True)}\nExecuted - {cDate}\n"

    # Try except block for executed user input
    class buyOrSell:
        def __init__(self, symbol) -> None:
            self.symbol = symbol

        def buyOrSell(self):
            while True:
                executable = input("Buy or sell? ").lower()
                
                try:
                    if executable.lower() == 'exit':
                        return 1
                    if executable.lower() not in ("buy", "sell"):
                        raise Exception("Invalid Command")
                except Exception as e:
                    print(e)
                else:
                    executed = executeTrade(executable, self.symbol)

                    if executable == 'buy':
                        return executed.buy()
                    else:
                        return executed.sell()

    commands = [
        'getNews',
        'getInfo',
        'getChart',
        'getPortfolio',
        'getActions',
        'getDividends',
        'getSplits',
        'getShareCount',
        'getFinancials',
        'getHolders',
        'getRecs',
        'getEarningDates',
        'getOptions',
        'trade'
    ]

    class runCommand:
        def __init__(self, command, symbol) -> None:
            self.command = command
            self.symbol = symbol
        
        def run(self):
            symbol = self.symbol
            symbol = yf.Ticker(symbol)
        
            if self.command == 'getNews':
                return symbol.news
            
            elif self.command == 'getInfo': 
                return symbol.info
            
            elif self.command == 'getChart':
                start = input("Enter starting range for data in d/m/Y - ")
                data = candleStickChart(self.symbol, start)
                data.showData() 
                return "Chart"
            
            elif self.command == 'getActions':
                return symbol.actions
        
            elif self.command == 'getDividends':
                return symbol.dividends
        
            elif self.command == 'getSplits':
                return symbol.splits
        
            elif self.command == 'getShareCount':
                start = input("Enter starting range for data in y-m-d - ")
                return symbol.get_shares_full(start=start, end=None)
            
            elif self.command == 'getFinancials':
                while True:
                    companyFinancials = input("Choose from incomeStatement, balanceSheet, cashFlow, qrtlyIncomeStatement, qrtlyBalanceSheet, or qrtlyCashFlow - ")
                    try:
                        if companyFinancials == 'incomeStatement':
                            return symbol.income_stmt
                        elif companyFinancials == 'balanceSheet':
                            return symbol.balance_sheet
                        elif companyFinancials == 'cashFlow':
                            return symbol.cash_flow
                        elif companyFinancials == 'qrtlyIncomeStatement':
                            return symbol.quarterly_income_stmt
                        elif companyFinancials == 'qrtlyBalanceSheet':
                            return symbol.quarterly_balance_sheet
                        elif companyFinancials == 'qrtlyCashFlow':
                            return symbol.quarterly_cash_flow
                        elif companyFinancials == 'back':
                            return 
                        else:
                            raise Exception("Query Company Financial Data - ")
                    except Exception as e:
                        print(e)

            elif self.command == 'getHolders':
                return symbol.major_holders
        
            elif self.command == 'getRecs':
                return symbol.recommendations, symbol.recommendations_summary, symbol.upgrades_downgrades
        
            elif self.command == 'getEarningDates':
                return symbol.earnings_dates, symbol.earnings_forecasts, symbol. earnings_trend
        
            elif self.command == 'getOptions':
                # TODO - print option expirations for a security
                while True:
                    # TODO - fetch user input if they would like to see option chains for a specific date
                    yesOrNo = input(f"Here is a list of options expirations for {self.symbol} - {symbol.options} - fetch option chain data? Input 'yes' or 'no' - ") 
                    try:
                        if yesOrNo == 'yes':
                            date = input("Input date in YYYY-MM-DD for an expiration date - ") # This is prone to user input error
                            opt = symbol.option_chain(date.strip())
                            break
                        elif yesOrNo == 'no':
                            return ""
                        else:
                            raise Exception("Invalid input")
                    except Exception as e:
                        print(e)


                while True:        
                    callsOrPuts = input("Fetch calls, puts, or both? - ").lower()
                    try:
                        if callsOrPuts not in ('calls'):

                            return opt.calls
                        elif callsOrPuts not in ('puts'):
                            return opt.puts
                        elif callsOrPuts not in ('both'):
                            return opt
                        else:
                            raise Exception("Invalid input")
                    except Exception as e:
                        print(e)
            
            elif self.command == 'trade':
                executed = buyOrSell(self.symbol).buyOrSell()
                if executed == 1:
                    return "Exited Transaction Interface"
                return executed
            
            else:
                commandError = checkCommand([self.command, self.symbol]) 
                if not commandError:
                    return 500
                else: 
                    return 69

    def readUserCommand(userCommand):
        inputs = userCommand.split(" ")
        if inputs == 'getPortfolio':
            return inputs, 'foo'
        if checkCommand(inputs):
            return inputs[0], inputs[1]
        else:
            return "Invalid Inputs"

    print(f"To access more company data, use the command line interface and input the following <command> <tickerSymbol>. The list of commands are as follows {commands}")

    class commandLoop:
        def runLoop():
            while True:
                userCommand = input("Enter space seperated command and symbol, or 'getPortfolio' to view your portfolio or 'exit' to quit the terminal. - ")
                if userCommand == 'exit':
                    break
                elif userCommand == 'getPortfolio':
                    pprint.pprint(userPortfolio)
                    continue
                else: 
                    out = readUserCommand(userCommand)
                try: 
                    companyData = runCommand(out[0], out[1])
                    executed = companyData.run()
                    if executed == 500:
                        raise Exception(f"{fStringNextLine}Invalid Command, Commands are {commands}")
                    if executed == 69:
                        raise Exception("FTX took all you're money!")
                except Exception as e:
                    print(e)
                else: 
                    if out[0] == 'trade' or out== 'getPortfolio':
                        print(executed)
                    else:
                        pprint.pprint(executed)

    commandLoop.runLoop()

main()