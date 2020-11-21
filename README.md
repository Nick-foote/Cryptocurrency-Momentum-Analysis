# Cryptocurrency Momentum Trading Analysis

#### Introduction
This program pulls in  data of the price history of Bitcoin, Ethereum, XRP & Link cryptocurrencies.
Using the momentum in the change of price, calculated by user chosen Exponential Moving Average values,
a trading strategy is calculated whether to buy or sell the coin, accumulating the profit over each trade.

At the end the program will compare your chosen EMA crossover strategy against a simple buy and hold approach,
reporting your Return of Investment.



#### Start Up

First of all the program will ask the user to chose which coin to perform the analysis on:

```
Options currently are:

    Bitcoin (btc)
    ETHEREUM (eth)
    XRP (xrp)
    LINK (link)

Enter a asset you want to examine: 
```

After the user has selected an asset, they will then be select an action to perform:

```
Please pick an option:

    1) Review chart for Price History
    2) Enter EMA values Analysis results for an EMA crossover strategy 
    3) Review best 20 highest performing EMA combinations

    Or press ENTER to quit
  
Your selection:   
```

Charting the Price History over the years available

<img width="700" alt="crpyto_analysis_11" src="https://user-images.githubusercontent.com/68865367/99875739-c22c7580-2be9-11eb-8b7c-b46d2b7fca77.png">

#### Entering EMA values to create a crossover strategy

After the user enters the value for the fast and slow EMA lengths, the program will plot both EMA lines over the price history.
Where the fast EMA crosses over above the slow EMA, the trading strategy indicates to go long and but the asset, and to sell when the fast EMA dips below the slow line.



<img width="700" alt="crpyto_analysis_08" src="https://user-images.githubusercontent.com/68865367/99875736-ba6cd100-2be9-11eb-9f7c-a177c5458839.png">


#### Plotting the results of the EMA trading Indicator

Example result of a trading strategy using Bitcoin:
<img width="700" alt="crpyto_analysis_04" src="https://user-images.githubusercontent.com/68865367/99875753-df614400-2be9-11eb-92fe-ac90d215d680.png">
```
With an initial investment of $100 in Bitcoin, using the chosen strategy you would have return of $4,840 today
Overall return on investment is 4,740.27%
```

And with Ethereum:
<img width="700" alt="crpyto_analysis_06" src="https://user-images.githubusercontent.com/68865367/99875758-e4be8e80-2be9-11eb-8234-335a1964e747.png">

#### Comparing different results

The user is then able to retrieve the best performing EMA values for each asset, ranked by each ROI:

```
-- Top performing EMA values (fast/slow) for Bitcoin --

5/15 with a return of 5172%
10/30 with a return of 5076%
11/21 with a return of 5067%
5/13 with a return of 4994%
12/35 with a return of 4906%
5/20 with a return of 4834%
13/17 with a return of 4740%
```

