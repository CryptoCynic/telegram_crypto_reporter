# 🤖 TGCryptoReporter

A Python-based tool that scrapes cryptocurrency-related Telegram channels, analyzes content using AI (OpenAI or Google Gemini), and generates comprehensive market insights.

**Attention**: It might take time to run due to number of messages to be analyzed. Either alter the channel list to a shorter one or input just 1 or 2 in the argument --hours. Openai model method is not working for the moment but consider using Gemini by getting a [free API key from Google AI Studio](https://aistudio.google.com).

---
<p align="center">
  <img src="logo.png" alt="TGCryptoReporter" width="400" />
</p>

## Overview

**TGCryptoReporter** automatically collects messages from specified crypto Telegram channels, processes them for market insights, and generates AI-powered summaries focusing on key market trends and announcements.

## Features

### **Data Collection**  
- Automated Telegram channel scraping ([Get your API_ID and API_HASH](https://my.telegram.org/auth)) 
- Support for both trading and news channels  
- Configurable time window for message collection  

### **Analysis**  
- Dual AI models support through APIs ([OpenAI](https://platform.openai.com/api-keys) / [Google Gemini](https://aistudio.google.com))  
- Cryptocurrency mention tracking  
- Message engagement metrics (views, forwards)  

### **Output**  
- CSV file generation for raw data  
- Detailed analysis reports in TXT format  
- Optional file retention  

---

## Setup

1. **Create a `.env` file** with your credentials:

    ```
    API_ID=your_telegram_api_id  
    API_HASH=your_telegram_api_hash  
    PHONE=your_phone_number  
    OPENAI_API_KEY=your_openai_key  
    GOOGLE_API_KEY=your_gemini_key  
    ```

2. **Install dependencies**:

    ```
    pip install -r requirements.txt
    ```

3. **Run the scraper** with different options:

    ```
    # Use OpenAI and keep files
    python channel_scraper.py --ai openai --keep_files

    # Use Gemini and auto-delete files after analysis
    python channel_scraper.py --ai gemini

    # Default usage
    python channel_scraper.py
    ```

---

## Output Files

- **Timestamped CSV files** containing scraped messages  
- **Analysis report** with cryptocurrency mentions and market insights  
- **Logging file** for debugging  

> **Note**: The script automatically handles Telegram session management and authentication. CSV files are cleaned up after analysis unless the `--keep_files` flag is used.

---

## Support the Development of Crypto Toolkits

If you find this tool helpful, you can support the development and support of this and similar ones through crypto donations:

- **Solana (SOL)**  
  `BEDzMx27TPRh6d1tJokGuSLec4yut7KJaw1QoZRJw7bH`

- **Ethereum (ETH)**
  `0x530B73D02793b5bB12C7571A053c81883cE078FD`

- **Polygon**
  `0x530B73D02793b5bB12C7571A053c81883cE078FD`

- **Bitcoin (BTC)**
  `bc1qjq8rmvkvautk2t9urm739vuw3gn00zd5l9qmqd`
