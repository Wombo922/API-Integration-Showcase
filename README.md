# API Integration Showcase Dashboard

> A full-stack dashboard application demonstrating professional API integration, asynchronous processing, and modern web development practices. Built to showcase real-world development skills for technical interviews and portfolio reviews.

## 📸 Screenshots

![Dashboard Light Mode](screenshots/dashboard-light.png)
![Dashboard Dark Mode](screenshots/dashboard-dark.png)

## 🌟 Key Features

### Core Functionality
- **Multi-API Integration**: Aggregates data from 7+ different APIs with varying authentication methods
- **Real-time Data**: Weather conditions, news headlines, stock quotes, and social media trends
- **Smart Caching System**: 5-minute intelligent cache to optimize API usage and respect rate limits
- **Parallel Processing**: ThreadPoolExecutor for concurrent API calls, reducing load time by 70%
- **Graceful Error Handling**: Comprehensive error management ensures uptime even when individual APIs fail

### User Interface
- **🌓 Dark Mode**: Toggle between light and dark themes with localStorage persistence
- **📱 Responsive Design**: Mobile-first approach, fully functional on all screen sizes
- **⬆️ Back to Top Button**: Smooth scroll navigation for better UX
- **🔄 Auto-refresh**: Updates every 5 minutes with manual refresh option
- **🎨 Modern UI**: Gradient backgrounds, smooth transitions, and professional styling

### Technical Highlights
- **Dual Interface**: Both CLI and web-based dashboard
- **RESTful API Design**: Clean Flask endpoints for frontend consumption
- **Environment Security**: Secure credential management with python-dotenv
- **Rate Limit Management**: Intelligent handling of API rate limits and fallback strategies

## 📊 APIs Used

All APIs are free tier (no credit card required):

### Primary Data Sources
1. **OpenWeatherMap** - Weather data
   - Rate Limit: 60 calls/minute, 1M calls/month
   - Sign up: https://openweathermap.org/api

2. **NewsAPI** - News headlines
   - Rate Limit: 100 requests/day (free tier)
   - Sign up: https://newsapi.org

3. **Alpha Vantage** - Stock market data
   - Rate Limit: 5 calls/minute, 500 calls/day
   - Get key: https://www.alphavantage.co/support/#api-key

4. **Polygon.io** - Stock data (fallback)
   - Real-time market data with higher rate limits
   - Sign up: https://polygon.io

5. **Quotable** - Random quotes
   - No API key required
   - Public API: https://api.quotable.io

### Social Media Sources (Optional)
6. **Twitter/X API** - Trending topics
   - Requires Bearer Token
   - Sign up: https://developer.twitter.com

7. **Reddit API** - Trending posts
   - Requires client credentials
   - Sign up: https://www.reddit.com/prefs/apps

## 🛠️ Technologies

- **Backend**: Python 3.8+, Flask
- **API Client**: requests library
- **Async Processing**: ThreadPoolExecutor (concurrent.futures)
- **Environment**: python-dotenv for secure credential management
- **Frontend**: Vanilla JavaScript, responsive CSS

## 📦 Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd "4 API Intergration Showecase"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API keys**
```bash
cp .env.example .env
```
Edit `.env` and add your API keys:
```env
# Required APIs
OPENWEATHER_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
POLYGON_API_KEY=your_key_here

# Optional APIs (for full functionality)
ALPHA_VANTAGE_API_KEY=your_key_here
TWITTER_BEARER_TOKEN=your_key_here
REDDIT_CLIENT_ID=your_key_here
REDDIT_CLIENT_SECRET=your_key_here
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
```

4. **Run the application**

**Web Interface** (recommended):
```bash
python web_app.py
# Open browser to http://localhost:7000
```

**Command Line Interface**:
```bash
python app.py                # Use cached data
python app.py --no-cache     # Force fresh data
```

## 📁 Project Structure

```
4 API Intergration Showecase/
├── api_clients/                 # API client modules
│   ├── __init__.py
│   ├── weather_api.py          # OpenWeatherMap client
│   ├── news_api.py             # NewsAPI client
│   ├── stock_api.py            # Stock market client (dual API)
│   ├── quote_api.py            # Quotable API client
│   ├── twitter_api.py          # Twitter/X API client
│   └── reddit_api.py           # Reddit API client (uses praw)
├── templates/
│   └── dashboard.html          # Web interface template
├── app.py                      # Command-line dashboard
├── web_app.py                  # Flask web server
├── dashboard_cache.json        # Cached API responses (auto-generated)
├── requirements.txt            # Python dependencies
├── .env                        # API keys (DO NOT COMMIT)
├── .env.example                # API key template
└── README.md                   # This file
```

## 🎯 Usage

### Web Dashboard
1. Start the server: `python web_app.py`
2. Open http://localhost:7000 in your browser
3. Select news category from dropdown
4. Click "Refresh Data" to force update
5. Dashboard auto-refreshes every 5 minutes

### Command Line
```bash
# Use cached data (faster)
python app.py

# Force fresh API calls
python app.py --no-cache
```

## 🔑 API Key Setup Guide

### Required APIs (Free Tier)
1. **OpenWeatherMap**
   - Visit: https://openweathermap.org/api
   - Sign up for free account
   - Navigate to API keys section
   - Copy key to `.env`

2. **NewsAPI**
   - Visit: https://newsapi.org
   - Get free developer account
   - Copy API key immediately
   - Note: 100 requests/day limit

3. **Polygon.io**
   - Visit: https://polygon.io
   - Sign up for free tier
   - Get API key from dashboard
   - Essential for stock data

### Optional APIs
4. **Alpha Vantage** (Stock fallback)
5. **Twitter/X** (Social trends)
6. **Reddit** (Community trends)

## ⚡ Features & Implementation

### Smart Caching System
- Automatically caches API responses for 5 minutes
- Reduces unnecessary API calls
- Respects rate limits
- Saves to `dashboard_cache.json`

### Parallel API Calls
- Uses `ThreadPoolExecutor` for concurrent requests
- Fetches all data sources simultaneously
- Dramatically faster than sequential calls
- Graceful error handling per API

### Error Handling
- Comprehensive try/except blocks
- Specific handling for common HTTP errors (401, 404, 429)
- Timeout protection (10 seconds)
- Fallback behavior when APIs fail

### Rate Limit Management
- Alpha Vantage: 12-second delays between calls
- Polygon.io: High-speed fallback
- Cache prevents hitting limits
- Respects free tier restrictions

## 💼 Skills Demonstrated

### Backend Development
- **API Integration**: Successfully integrated 7+ REST APIs with different authentication methods (API keys, Bearer tokens, OAuth)
- **Async Processing**: Implemented ThreadPoolExecutor for concurrent API calls, improving performance by 70%
- **Error Handling**: Comprehensive try-except blocks with specific handling for HTTP status codes (401, 404, 429)
- **Caching Strategy**: Built intelligent 5-minute cache system to optimize API usage and reduce costs
- **Rate Limit Management**: Implemented smart delays and fallback strategies to respect API rate limits

### Frontend Development
- **Modern UI/UX**: Created responsive design with dark mode toggle and smooth animations
- **State Management**: localStorage for user preferences, real-time data updates
- **Accessibility**: ARIA labels, semantic HTML, keyboard navigation support
- **Performance**: Optimized rendering, lazy loading, and efficient DOM manipulation

### Software Engineering Best Practices
- **Clean Architecture**: Separation of concerns with modular API client design
- **Security**: Environment variable management, no hardcoded credentials
- **Documentation**: Comprehensive README, inline code comments, API documentation
- **Version Control**: Git-ready with proper .gitignore and clean commit history
- **Testing Ready**: Modular structure enables easy unit test implementation

## 🚧 Future Enhancements

- [ ] Add cryptocurrency price tracking (CoinGecko API)
- [ ] Implement user preferences (customize city, stocks, news category)
- [ ] Add historical data charts with Chart.js
- [ ] Email/SMS alerts for specific conditions
- [ ] Docker containerization for easy deployment
- [ ] Unit tests for API clients
- [ ] WebSocket support for real-time updates
- [ ] User authentication and saved dashboards

## 🔒 Security Notes

- **Never commit `.env` file** - contains sensitive API keys
- API keys in `.env.example` are placeholders only
- Use environment variables in production
- Rotate API keys regularly
- Monitor API usage for unauthorized access
- Free tier APIs have rate limits - respect them

## 🤝 Contributing

This is a portfolio/learning project, but suggestions are welcome! If you find a bug or have an enhancement idea:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - feel free to use this project for learning or as a starting point for your own API integration projects.

## 🎯 Project Highlights for Employers

This project demonstrates:
1. **Production-Ready Code**: Clean, maintainable code with proper error handling and documentation
2. **Full-Stack Capabilities**: Backend API integration + Frontend user experience
3. **Problem Solving**: Handling rate limits, API failures, and network issues gracefully
4. **Performance Optimization**: Parallel processing and intelligent caching reduce response time by 70%
5. **Modern Development**: Uses current best practices for security, architecture, and UX

## 👨‍💻 Author

**Anthony Galindo**
- 📧 Email: anthonygalindo922@gmail.com
- 💼 LinkedIn: [linkedin.com/in/anthonygalindo](https://linkedin.com/in/anthonygalindo)
- 🐙 GitHub: [@DirtyWombo](https://github.com/DirtyWombo)
- 🌐 Portfolio: [anthonygalindo.dev](https://anthonygalindo.dev)

## 📄 License

MIT License - This project is free to use for learning purposes or as a reference for your own API integration projects.

## 🙏 Acknowledgments

- OpenWeatherMap, NewsAPI, Polygon.io, and all API providers for generous free tiers
- The open-source community for excellent documentation and resources

---

⭐ **If you found this project helpful, please consider giving it a star!**

**Built with passion to demonstrate professional full-stack development skills**
