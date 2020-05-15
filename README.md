# Trading in Bitso

In this project I look to explore the API of Bitso, implement some algorithms for automatic and semi-automatic trading, Use data sources to make the predictions, deploy in a web service as "Python Anywhere" and set notifications for every trading. The final desirable result would be an API for trading with Bitso, seting some parameters which can be load in the algorithm designed.

## Exploring API

The API of Bitso has a complete repository with all the information in the next link: [Bitso API Repository](https://github.com/bitsoex/bitso-py)

Here I will try to extract all the insights that I have about the use of this tool, with the most necesary instructions and report their behaivor.

The first thing to do is installing the bitso API, I am having some problems trying to install it with conda over a virtual envioroment, I couldnt make pip3 work, and with pip never find the bitso api to be installed. So I had to install python3 alone over other location to be able to installed with pip3 just in the terminal with: 

    pip3 install bitso-py
    
After thar just import the library with:

    import bitso
    
In the following link is the code of the exploratory simple work to find out in general matter what the API does and how can be done the placing y cancelling orders procedure. [Code of exploration](https://github.com/albertoid/bitso/blob/master/Bitso.ipynb)

## Data Sources


## Designing Algorithm for trading

## Deploying in web server



## Notifications of Trading
