# AI-Trading-Bot

## An AI-driven trading bot leveraging sentiment analysis with deep learning to automate stock trading decisions, integrating Alpaca's API for real-time market data, backtesting using Yahoo Finance data, and SQL for storing earnings and performance metrics.

This project embodies an AI-driven trading bot that utilizes machine learning and natural language processing (NLP) to automate stock trading decisions based on sentiment analysis of financial news headlines. Built using Python, the bot integrates several key libraries and tools. For sentiment analysis, it utilizes Transformers from the Hugging Face library, specifically the FinBERT model, fine-tuned for financial sentiment classification. The PyTorch framework is employed to run the deep learning models efficiently, leveraging GPU acceleration when available. The bot interacts with Alpaca's API to fetch real-time market data and execute trades in a paper trading environment, configured using API keys for authentication. Backtesting functionality is implemented using Yahoo Finance data, facilitated by the YahooDataBacktesting module. Additionally, the bot incorporates SQL database to store earnings and performance metrics, enhancing data management and analysis capabilities. Overall, the project combines natural language processing techniques with financial data handling to create an advanced trading system capable of making informed trading decisions autonomously. 


<img width="1422" alt="Screenshot 2024-07-16 at 3 59 45 PM" src="https://github.com/user-attachments/assets/0cd49663-c8a9-46cc-be77-6e5e0080e504">


<img width="1004" alt="Screenshot 2024-07-16 at 4 05 06 PM" src="https://github.com/user-attachments/assets/179ee0d5-07ca-4018-ab27-7d5f711f7a56">

## How to Run the Bot
1. Create a virtual environment `conda create -n trader python=3.10` 
2. Initialize it `conda init zsh`
3. Activate it `conda activate trader`
4. Install initial dependencies `pip install lumibot timedelta alpaca-trade-api==3.1.1`
5. Install libraries `pip install torch torchvision torchaudio transformers` 
6. Update the `API_KEY` and `API_SECRET` with values from your Alpaca account 
7. Run the bot `python3 tradingbot.py`

