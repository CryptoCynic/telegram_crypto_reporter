import pandas as pd
import asyncio
import time
from telethon import TelegramClient
import os
from dotenv import load_dotenv
import logging
from datetime import datetime, timedelta
import argparse
import subprocess
from pathlib import Path

# Python 3.10 recommended - python crypto_cynic_tg_scraper.py --ai gemini --keep_files.py
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

# Generate session filename
SESSION_FILE = "telegram_scraper.session"
session_path = Path(SESSION_FILE)
os.environ['SESSION_FILE'] = str(session_path)

async def get_client(api_id, api_hash, phone):
    """Initialize Telegram client with auto-generated session file"""
    client = TelegramClient(SESSION_FILE, api_id, api_hash)
    await client.start(phone=phone)
    return client

async def scrape_channel(client, channel_username, hours_back):
    """Scrape messages from a channel"""
    try:
        channel = await client.get_entity(channel_username)
        messages = []
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        async for message in client.iter_messages(channel, offset_date=cutoff_time):
            message_data = {
                'channel': channel_username,
                'message_id': message.id,
                'date': message.date,
                'text': message.text,
                'views': getattr(message, 'views', 0),
                'forwards': getattr(message, 'forwards', 0),
                'replies': getattr(message.replies, 'replies', 0) if message.replies else 0
            }
            messages.append(message_data)
        
        return messages
    except Exception as e:
        logging.error(f"Error scraping channel {channel_username}: {e}")
        return []

async def async_main(hours: int):
    load_dotenv()
    
    # Telegram credentials
    client = await get_client(
        os.getenv('API_ID'),
        os.getenv('API_HASH'),
        os.getenv('PHONE')
    )
    
    crypto_telegram_channels = [
        'PUMPNOW800',
        'JimmyLeshTrader',
        'Robertt_admin',
        'Cryptoprofitcoachadmin',
        'cryptohoyden',
        'attackerme',
        'Arpiner7',
        'Erick',
        'DmitriFRI',
        'philipv7',
        'wallstreetqueenadmin',
        'cicalex',
        'alexad07',
        'Olivia_Soul',
        'gqsoul',
        'arbitragetesting',
        'Lucky_Adams',
        'TheJenus',
        'Bianket_Men',
        'KerolosAdel',
        'TopGbrg',
        'ProCrypto_NY2',
        'MichelleGreen1',
        '4evercrypto',
        'JedasnK',
        'ElizG',
        'DimaF',
        'ivanpetrov',
        'CryptoKing',
        'alexcastro5',
        'steveadm',
        'justincrypto',
        'Marcsxb',
        'top9_rian',
        'forthelulz',
        'samirpower',
        'Pac43',
        'naatween',
        'smebm',
        'CryptoGirl_Mar',
        'RobertoK',
        'algaeblitz2',
        'rob_whale',
        'CryptoGrows',
        'mikevazovskyi',
        'miaMybtc',
        'elibraX',
        'jonnesnow',
        'Rocket_Pump_Channel',
        'iqcash_admin',
        'tomexpert',
        'davecf',
        'Rose_Javelin',
        'Cryptonews',
        'frankdefi',
        'monetizesupport',
        'Pentoska',
        'Cryptoadmin',
        'leoversa',
        'ralfvm',
        'PAULHEX',
        'MEGA_SHARK',
        'cryptosamurai_owner',
        'jamescpt',
        'ryder_reilly',
        'CryptoJohn',
        'Oliverbf',
        'vip_crypto_signals_company',
        'astroboiz',
        'robertus78',
        'GodBarni',
        'antoncrypt',
        'BCPCadmin',
        'Rachel_Ree',
        'Merc_hawk',
        'AaronWithCrypto',
        'CryptoNewsAdmin',
        'saloni_jn',
        'ProjectPromoters',
        'brianbollinger',
        'Altcoin_Admin',
        'TraderLucYY',
        'Bulls_Admintrader',
        'nakamotocat',
        'ELizabeth_WST',
        'jasonbuzz',
        'Cryptosupport',
        'Steve_Admin',
        'AllenWestern',
        'SwedenTrader',
        'raitlukass',
        'CryptoTrader2014',
        'infostoreeu',
        'Margin_Trader',
        'cryptorank',
        'Fesions',
        'BitcoinSmarts',
        'Lishats',
        'crypto_faux'
    ]
    
    crypto_news_channels = [
        'miaMybtc',
        'attackerme',
        'Arpiner7',
        'jonnesnow',
        'tomexpert',
        'Cryptonews',
        'frankdefi',
        'monetizesupport',
        'Pentoska',
        'leoversa',
        'ralfvm',
        'jamescpt',
        'ryder_reilly',
        'CryptoJohn',
        'philipv7',
        'alexad07',
        'Oliverbf',
        'iqcash_admin',
        'gqsoul',
        'astroboiz',
        'robertus78',
        'GodBarni',
        'Rachel_Ree',
        'Merc_hawk',
        'AaronWithCrypto',
        'CryptoNewsAdmin',
        'saloni_jn',
        'Olivia_Soul',
        'brianbollinger',
        'nakamotocat',
        'cryptorank',
        'BitcoinSmarts',
        'crypto_faux',
        'CryptoRetro',
        'CryptoFight',
        'CryptoGem',
        'CryptoIndustry',
        'CryptoHunter',
        'CryptoCall',
        'CryptoExpert',
        'TONCryptoNews',
        'CryptoShilling',
        'DeFiNews',
        'CryptoNewspaper',
        'CryptoMax',
        'CryptoBox',
        'CryptoLake',
        'CryptoPower',
        'CryptoUnited',
        'Crypto4News',
        'CryptoMagazine',
        'CryptoHub',
        'CryptoArena',
        'TokensStream',
        'CryptoLand',
        'CryptoLVL',
        'TokenMap',
        'CryptoPortal',
        'GimmeCoin',
        'GildCoin',
        'DroppersOfBTC',
        'BlockchainProgress',
        'CryptoPush',
        'CryptoBitca',
        'CryptoClubUSA',
        'CryptoCaliforniaClub',
        'CoinQuest',
        'NFTERA',
        'AltcoinHolder',
        'CryptoFlake',
        'CoinGapeNews',
        'CryptoUnfolded',
        'ProCryptoNews',
        'FirstCryptoNews',
        'CryptoRankNews',
        'Cointelegraph',
        'BitcoinNews',
        'CryptoDaily',
        'CoinDesk',
        'CryptoSlate',
        'TheBlock',
        'DecryptMedia',
        'CoinTelegraph',
        'BitcoinMagazine',
        'CryptoGlobe',
        'NewsBTC',
        'CryptoBriefing',
        'CryptoNinjas',
        'BitcoinExchangeGuide',
        'CryptoNewsZ',
        'BlockchainNews',
        'CryptoNewsPoint',
        'CoinSpeaker',
        'BitcoinWarrior',
        'CryptoNewsWorld',
        'CryptoReporter',
        'BlockchainReporter',
        'CryptoTicker',
        'CoinJournal',
        'CryptoVest',
        'CryptoNewsLine',
        'CoinPedia',
        'BitcoinistNews',
        'CryptoNewsNow',
        'BlockTribune',
        'CryptoGazette',
        'BitcoinNewsToday',
        'CryptoNewsWire',
        'BlockchainTimes',
        'CryptoNewsDaily',
        'BitcoinCentral',
        'CryptoNewsUpdate',
        'BlockchainReport',
        'CryptoNewsFlash',
        'BitcoinPulse',
        'CryptoNewsWatch',
        'BlockchainPress',
        'CryptoNewsNetwork',
        'BitcoinTrend',
        'CryptoNewsBeat',
        'BlockchainBuzz',
        'CryptoNewsToday',
        'BitcoinInsider',
        'CryptoNewsFeed',
        'BlockchainFocus',
        'CryptoNewsLive',
        'BitcoinReport',
        'CryptoNewsAlert',
        'BlockchainDaily',
        'CryptoNewsDigest',
        'BitcoinBulletin',
        'CryptoNewsCentral',
        'BlockchainWeekly',
        'CryptoNewsJournal',
        'BitcoinChronicle',
        'CryptoNewsMonitor',
        'BlockchainInsight',
        'CryptoNewsRadar',
        'BitcoinObserver',
        'CryptoNewsSource',
        'BlockchainUpdate',
        'CryptoNewsSummary',
        'BitcoinAnalyst',
        'CryptoNewsTracker',
        'BlockchainWatch',
        'CryptoNewsVision',
        'BitcoinMonitor',
        'BlockchainXpress',
        'CryptoNewsZone',
        'BitcoinDigest',
        'CryptoNewsBase',
        'BlockchainCentral',
        'CryptoNewsChannel',
        'BitcoinDispatch',
        'CryptoNewsDesk',
        'BlockchainEra',
        'CryptoNewsFocus',
        'BitcoinGlobal',
        'CryptoNewsHub',
        'BlockchainIntel',
        'CryptoNewsIndex',
        'BitcoinJournal',
        'CryptoNewsKing',
        'BlockchainLine',
        'CryptoNewsMaker',
        'BitcoinNetwork'
    ]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Scrape trading channels
    trading_messages = []
    for channel in crypto_telegram_channels:
        messages = await scrape_channel(client, channel, hours)
        trading_messages.extend(messages)
        await asyncio.sleep(2)  # Rate limiting
    
    # Scrape news channels
    news_messages = []
    for channel in crypto_news_channels:
        messages = await scrape_channel(client, channel, hours)
        news_messages.extend(messages)
        await asyncio.sleep(2)  # Rate limiting
    
    # Save to CSV files
    if trading_messages:
        pd.DataFrame(trading_messages).to_csv(f'crypto_trading_messages_{timestamp}.csv', index=False)
    if news_messages:
        pd.DataFrame(news_messages).to_csv(f'crypto_news_messages_{timestamp}.csv', index=False)
    
    await client.disconnect()
    return timestamp

def main():
    parser = argparse.ArgumentParser(description='Telegram Channel Scraper')
    parser.add_argument('--hours', type=int, default=1,
                       help='Number of hours of history to scrape (default: 1)')
    parser.add_argument('--ai', choices=['openai', 'gemini'], default='openai',
                       help='Choose AI service for analysis')
    parser.add_argument('--keep_files', action='store_true',
                       help='Keep CSV files after analysis')
    args = parser.parse_args()

    try:
        # Run async scraping
        timestamp = asyncio.run(async_main(args.hours))
        
        # Run the analyzer with arguments
        subprocess.run([
            'python', 'crypto_cynic_tg_reporter.py',
            '--ai', args.ai,
            '--timestamp', timestamp,
            *(['--keep_files'] if args.keep_files else [])
        ], check=True)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()