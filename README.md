# Trading in Bitso

In this project I look to explore the API of Bitso, implement some algorithms for automatic and semi-automatic trading, Use data sources to make the predictions, deploy in a web service as "Python Anywhere" and set notifications for every trading. The final desirable result would be an API for trading with Bitso, seting some parameters which can be load in the algorithm designed.

## Exploring API

The API of Bitso has a complete repository with all the information in the next link: [Bitso API Repository](https://github.com/bitsoex/bitso-py)

Here I will try to extract all the insights that I have about the use of this tool, with the most necesary instructions and report their behaivor.

The first thing to do is installing the bitso API.Is quite easy just using pip3 with the following instruction over the bash terminal: 

    pip3 install bitso-py
    
After thar just import the library with:

    import bitso
    
In the following link is the code of the exploratory simple work to find out in general matter what the API does and how can be done the placing y cancelling orders procedure. [Code of exploration](https://github.com/albertoid/bitso/blob/master/Bitso.ipynb)

## Data Sources
The main data source at the begining is from Bitso it self, by means of scraping, all the historical indormation has been downloaded, and with some aditional functions it will be updated automatically.

## Designing Algorithm for trading

## Deploying in web server
For a deploy in web server I'm using an Ubuntu's free instance in EC2 AWS. is needed to install a virtual display and configure the driver of selenium, I'll explain how to do this.:

### Virtual Display
There are several virtual displays, but which is working better at least in Ubuntu is [xvfbwrapper](https://github.com/cgoldberg/xvfbwrapper), here is how to install it and use it.

It is needed to install Xvfb, you can doit with `sudo apt-get install xvfb`, `yum install xorg-x11-server-Xvfb` , etc

### Configuration of Selenium Firefox's Web Driver

For this the guide that I could found and that works for me is [this](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu/871077#871077?newreg=c009dd10ec804e188de0f596d03cb1a0):

Go to the geckodriver [releases page](https://github.com/mozilla/geckodriver/releases). Find the latest version of the driver for your platform and download it. For example:

> wget https://github.com/mozilla/geckodriver/releases/download/v0.27.0/geckodriver-v0.27.0-linux64.tar.gz

Extract the file with:

>tar -xvzf geckodriver*

Make it executable:

>chmod +x geckodriver

Add the driver to your PATH so other tools can find it:

>export PATH=$PATH:/path-to-extracted-file/.

Without this is possible that selenium does not work properly.


## Notifications of Trading
