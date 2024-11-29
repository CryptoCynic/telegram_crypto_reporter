import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI
import argparse
import logging
import time

# Add logging configuration at the top of the script
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CryptoAnalyzer:
    def __init__(self, ai_service: str, keep_files: bool, timestamp: str):
        self.ai_service = ai_service.lower()
        self.keep_files = keep_files
        self.timestamp = timestamp
        self.ai_client = self._setup_ai_client()
        self.max_retries = 3
        self.retry_delay = 60  # seconds
        
        self.crypto_dict = {
            'bitcoin': 'BTC',
            'ethereum': 'ETH',
            'tether': 'USDT',
            'solana': 'SOL',
            'bnb': 'BNB',
            'xrp': 'XRP',
            'dogecoin': 'DOGE',
            'usd coin': 'USDC',
            'cardano': 'ADA',
            'avalanche': 'AVAX',
            'tron': 'TRX',
            'toncoin': 'TON',
            'polkadot': 'DOT',
            'chainlink': 'LINK',
            'bitcoin cash': 'BCH',
            'litecoin': 'LTC',
            'stellar': 'XLM',
            'aptos': 'APT',
            'hedera': 'HBAR',
            'internet computer': 'ICP',
            'dai': 'DAI',
            'cronos': 'CRO',
            'pol': 'POL',
            'ethereum classic': 'ETC',
            'bittensor': 'TAO',
            'render': 'RNDR',
            'kaspa': 'KAS',
            'arbitrum': 'ARB',
            'celestia': 'TIA',
            'vechain': 'VET',
            'mantra': 'OM',
            'filecoin': 'FIL',
            'bonk': 'BONK',
            'okb': 'OKB',
            'stacks': 'STX',
            'cosmos': 'ATOM',
            'dogwifhat': 'WIF',
            'fantom': 'FTM',
            'injective': 'INJ',
            'monero': 'XMR',
            'sei': 'SEI',
            'immutable': 'IMX',
            'optimism': 'OP',
            'mantle': 'MNT',
            'aave': 'AAVE',
            'algorand': 'ALGO',
            'the graph': 'GRT',
            'bitget token': 'BGB',
            'first digital usd': 'FDUSD',
            'floki': 'FLOKI',
            'theta network': 'THETA',
            'thorchain': 'RUNE',
            'ethena': 'ENA',
            'worldcoin': 'WLD',
            'raydium': 'RAY',
            'maker': 'MKR',
            'pyth network': 'PYTH',
            'the sandbox': 'SAND',
            'lido dao': 'LDO',
            'jupiter': 'JUP',
            'kucoin token': 'KCS',
            'flow': 'FLOW',
            'bitcoin sv': 'BSV',
            'arweave': 'AR',
            'gala': 'GALA',
            'polygon': 'MATIC',
            'eos': 'EOS',
            'bittorrent': 'BTT',
            'tezos': 'XTZ',
            'starknet': 'STRK',
            'flare': 'FLR',
            'jasmy': 'JASMY',
            'quant': 'QNT',
            'decentraland': 'MANA',
            'axie infinity': 'AXS',
            'helium': 'HNT',
            'multiversx': 'EGLD',
            'neo': 'NEO',
            'gatetoken': 'GT',
            'apecoin': 'APE',
            'akash network': 'AKT',
            'dydx': 'DYDX',
            'ecash': 'XEC',
            'mina': 'MINA',
            'nexo': 'NEXO',
            'xdc network': 'XDC',
            'chiliz': 'CHZ',
            'pendle': 'PENDLE',
            'ordi': 'ORDI',
            'conflux': 'CFX',
            'ethereum name service': 'ENS',
            'iota': 'MIOTA',
            'zcash': 'ZEC',
            'usdd': 'USDD',
            'ftx token': 'FTT',
            'pancakeswap': 'CAKE',
            'aelf': 'ELF',
            '0x protocol': 'ZRX',
            'arkham': 'ARKM',
            'woo': 'WOO',
            'trust wallet token': 'TWT',
            'reserve rights': 'RSR',
            'siacoin': 'SC',
            'basic attention token': 'BAT',
            'amp': 'AMP',
            'iotex': 'IOTX',
            'ankr': 'ANKR',
            'space id': 'ID',
            'osmosis': 'OSMO',
            'dash': 'DASH',
            'manta network': 'MANTA',
            'origintrail': 'TRAC',
            'ethereumpow': 'ETHW',
            'qtum': 'QTUM',
            'zetachain': 'ZETA',
            'just': 'JST',
            'gas': 'GAS',
            'baby doge coin': 'BABYDOGE',
            'creditcoin': 'CTC',
            'safepal': 'SFP',
            'ravencoin': 'RVN',
            'polymesh': 'POLYX',
            'harmony': 'ONE',
            'terra': 'LUNA',
            'mask network': 'MASK',
            'chia': 'XCH',
            'threshold': 'T',
            'peercoin': 'PPC',
            'gridcoin': 'GRC',
            'primecoin': 'XPM',
            'nxt': 'NXT',
            'auroracoin': 'AUR',
            'mazacoin': 'MZC',
            'nervos network': 'CKB',
            'shiba inu': 'SHIB',
            'deso': 'DESO',
            'sui': 'SUI',
            'pepe': 'PEPE',
            'near protocol': 'NEAR',
            'unus sed leo': 'LEO',
            'uniswap': 'UNI',
            'wrapped bitcoin': 'WBTC',
            'wrapped ethereum': 'WETH',
            'wrapped tron': 'WTRX',
            'verge': 'XVG',
            'stellar lumens': 'XLM',
            'vertcoin': 'VTC',
            'nano': 'XNO',
            'firo': 'FIRO',
            'safemoon': 'SAFEMOON',
            'ambacoin': 'AMBA',
            'namecoin': 'NMC'
        }

    def _setup_ai_client(self):
        """Initialize AI client"""
        load_dotenv()
        
        if self.ai_service == 'openai':
            return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        elif self.ai_service == 'gemini':
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            return genai.GenerativeModel('gemini-1.5-flash')
        else:
            raise ValueError("Invalid AI service")

    def analyze_messages(self, messages: list) -> str:
        """Generate AI analysis of messages with retry logic"""
        prompt = """Analyze these cryptocurrency messages focusing on:
        1. Key commercial and technical agreements
        2. Government decisions and regulations
        3. Geopolitical events affecting cryptocurrency
        4. Major market movements
        
        Format the analysis with clear sections."""
        
        for attempt in range(self.max_retries):
            try:
                if self.ai_service == 'openai':
                    response = self.ai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a crypto market analyst."},
                            {"role": "user", "content": f"{prompt}\n\nMessages:\n{messages}"}
                        ],
                        max_tokens=1500
                    )
                    return response.choices[0].message.content
                else:
                    response = self.ai_client.generate_content(
                        f"{prompt}\n\nMessages:\n{messages}"
                    )
                    return response.text
                    
            except Exception as e:
                logging.error(f"AI analysis attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    logging.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logging.error("All retry attempts failed")
                    return "Analysis failed due to API limitations. Please try again later."

    def count_mentions(self, messages: list) -> dict:
        """Count cryptocurrency mentions"""
        mentions = {name: 0 for name in self.crypto_dict.keys()}
        
        for message in messages:
            if not isinstance(message, str):
                continue
            
            message = message.lower()
            for name, symbol in self.crypto_dict.items():
                mentions[name] += message.count(name)
                mentions[name] += message.count(symbol.lower())
        
        return mentions

    def generate_report(self, summary: str, mentions: dict) -> str:
        """Generate analysis report"""
        report_file = f"crypto_analysis_{self.timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"Cryptocurrency Analysis Report - {datetime.now()}\n")
            f.write("=" * 50 + "\n\n")
            
            if summary:
                f.write("ANALYSIS SUMMARY\n")
                f.write("-" * 20 + "\n")
                f.write(summary + "\n\n")
            
            f.write("CRYPTOCURRENCY MENTIONS\n")
            f.write("-" * 20 + "\n")
            for crypto, count in sorted(mentions.items(), key=lambda x: x[1], reverse=True):
                f.write(f"{crypto.upper()} ({self.crypto_dict[crypto]}): {count} mentions\n")
        
        return report_file

    def cleanup_files(self):
        """Clean up CSV files if not keeping them"""
        if not self.keep_files:
            for prefix in ['crypto_trading_messages_', 'crypto_news_messages_']:
                filename = f"{prefix}{self.timestamp}.csv"
                if os.path.exists(filename):
                    os.remove(filename)
                    logging.info(f"Removed {filename}")

def main():
    parser = argparse.ArgumentParser(description='Crypto News Analysis Tool')
    parser.add_argument('--ai', choices=['openai', 'gemini'], default='openai',
                       help='Choose AI service')
    parser.add_argument('--keep_files', action='store_true',
                       help='Keep CSV files after analysis')
    parser.add_argument('--timestamp', required=True,
                       help='Timestamp for CSV files')
    args = parser.parse_args()

    try:
        analyzer = CryptoAnalyzer(args.ai, args.keep_files, args.timestamp)
        
        # Read CSV files
        trading_file = f"crypto_trading_messages_{args.timestamp}.csv"
        news_file = f"crypto_news_messages_{args.timestamp}.csv"
        
        all_messages = []
        for file in [trading_file, news_file]:
            if os.path.exists(file):
                df = pd.read_csv(file)
                all_messages.extend(df['text'].tolist())
        
        if not all_messages:
            logging.error("No messages found")
            return

        summary = analyzer.analyze_messages(all_messages)
        mentions = analyzer.count_mentions(all_messages)
        report_file = analyzer.generate_report(summary, mentions)
        
        logging.info(f"Analysis saved to {report_file}")
        analyzer.cleanup_files()
        
    except Exception as e:
        logging.error(f"Analysis failed: {e}")

if __name__ == "__main__":
    main()