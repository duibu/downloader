from tqdm import tqdm
from datetime import datetime

def get_progress_bar(bar_total):
    return tqdm(desc=datetime.now().strftime("[%H:%M:%S") + ']',total=bar_total,bar_format='{desc} [{bar:85}]{percentage:3.0f}% ({n_fmt}/{total_fmt}) [{elapsed}<{remaining}, {rate_fmt}]', ascii=True)