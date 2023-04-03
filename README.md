## CodeforcesProgressTracker
### "Visualize and track your Codeforces journey with a user-friendly and customizable interface."Codeforces problem extractor 

Written in Python, Fetch Data using Codeforces API calls, and Deploy with Flask

Caching [from functools import lru_cache]
- Good. It helps. Tested with and without this caching method. It saves us from having to do repetitive tasks like fetching again.
- For other ways of caching, I want to try Redis as a server-side cache
-- Also downloading all of contests data into a local storage / database

Parallel Processing [from concurrent.futures import ThreadPoolExecutor, as_completed]
- Significantly improves the speed of fetching data using API calls. 
- However, data displayed on the localhost webpage are not static...
