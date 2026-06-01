import concurrent.futures
import traceback
from typing import Dict, List, Callable

def run_collectors(collectors: Dict[str, Callable], query: str):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_name = {
            executor.submit(func, query): name 
            for name, func in collectors.items()
        }
        
        for future in concurrent.futures.as_completed(future_to_name):
            name = future_to_name[future]
            try:
                data = future.result()
                yield {
                    "collector": name,
                    "status": "success",
                    "data": data
                }
            except Exception as e:
                yield {
                    "collector": name,
                    "status": "failed",
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
