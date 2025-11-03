# Friday Project 6: Apple Vision Pro Sentiment Analysis

A comprehensive GUI application for performing advanced sentiment analysis and aspect extraction on Apple Vision Pro customer feedback using OpenAI's GPT models.

## 📋 Project Overview

This project analyzes 80-100 customer reviews from a SQLite database (`feedback.db`) to:
- **Categorize sentiment** (Positive, Negative, Neutral) for each review
- **Extract specific product aspects** mentioned in reviews
- **Identify customer likes and dislikes** about the Apple Vision Pro
- **Generate actionable recommendations** for product improvement based on data-driven insights

The application provides an intuitive GUI with visualizations to help the product development team make targeted improvements in future versions.

---

## 🚀 Quick Start Guide

### Prerequisites

Make sure you have Python 3.7+ installed, then install required packages:

```bash
pip install openai matplotlib
```

**Note**: `tkinter` comes pre-installed with Python. `sqlite3` is also included in standard Python.

### Installation Steps

1. **Clone or Download** this repository

2. **Set up your OpenAI API Key**:
   - Get your API key from https://platform.openai.com/api-keys
   - Open `MasonsAPI_KEY.py`
   - Add your key:
     ```python
     OPENAI_API_KEY = 'sk-proj-your-actual-key-here'
     ```
   - Save the file

3. **Ensure Database is Available**:
   - Make sure `feedback.db` is in the project directory
   - Or be ready to browse to its location in the GUI

4. **Run the Application**:
   ```bash
   python sentiment_analysis_gui.py
   ```

---

## 📖 How to Use the Application

### Tab 1: Setup & Load Data

1. **Check API Status**: Look for the green checkmark ✓ indicating your API key loaded successfully
2. **Database Connection**: 
   - The default path is `feedback.db`
   - Click **Browse** if your database is in a different location
3. **Load Reviews**: Click the **Load Reviews** button
4. **Verify**: Check the Status window to confirm reviews were loaded successfully

### Tab 2: Run Analysis

You have three analysis options:

#### Option 1: Run Full Analysis (Recommended)
- Click **Run Full Analysis** to perform both sentiment analysis and aspect extraction
- This is the most comprehensive option and meets all project requirements
- Progress bar shows real-time updates
- Analysis output displays results as they're processed

#### Option 2: Sentiment Analysis Only
- Click **Start Sentiment Analysis** to categorize each review as positive, negative, or neutral
- Provides confidence scores for each prediction
- Use this if you only want overall sentiment without detailed aspects

#### Option 3: Aspect Extraction Only
- Click **Start Aspect Extraction** (requires sentiment analysis to be completed first)
- Extracts specific features mentioned (display, comfort, price, battery, etc.)
- Tags each aspect as positive, negative, or neutral

**Progress Tracking**:
- Watch the progress bar for completion status
- Real-time logging shows each review being processed
- Notifications appear when analysis completes

### Tab 3: Results

**Summary Statistics**:
- Total reviews analyzed
- Sentiment distribution (percentages)
- Total and unique aspects extracted
- Top 5 most mentioned aspects

**Detailed Results Table**:
- Review ID
- Overall sentiment
- Confidence score
- Key aspects mentioned

**Export Functionality**:
- Click **Export Results to JSON** to save complete analysis
- Useful for archiving, sharing, or further processing

### Tab 4: Visualizations

Generate professional charts to understand your data:

#### 1. Sentiment Distribution
- Bar chart showing positive, negative, and neutral review counts
- Color-coded for easy interpretation (Green = Positive, Red = Negative, Yellow = Neutral)
- Shows exact counts above each bar

#### 2. Aspect Frequency
- Horizontal bar chart of top 10 most mentioned aspects
- Identifies which features customers talk about most
- Helps prioritize areas for analysis

#### 3. Aspect Sentiment
- Grouped bar chart showing positive, negative, and neutral mentions for each aspect
- **Critical for identifying pain points**: Features with high negative mentions need attention
- **Identifies strengths**: Features with high positive mentions are marketing opportunities

#### 4. Generate Recommendations
- Opens a detailed report window with:
  - Overall sentiment summary
  - Top 5 strengths (most appreciated features)
  - Top 5 areas for improvement (common complaints)
  - Prioritized actionable recommendations
  - Strategic insights for product development
- **Export** the recommendations as a text file

---

## 📊 Understanding Your Results

### Sentiment Categories

- **POSITIVE**: Customer expresses satisfaction, praise, or positive experience
- **NEGATIVE**: Customer expresses dissatisfaction, criticism, or problems
- **NEUTRAL**: Balanced review or factual information without strong sentiment

### Common Aspects Extracted

The system identifies mentions of:
- **Display**: Screen quality, resolution, clarity
- **Comfort**: Fit, weight distribution, wearing experience
- **Price**: Cost, value for money
- **Battery**: Battery life, charging
- **Software**: Apps, interface, operating system
- **Design**: Aesthetics, build quality
- **Weight**: How heavy the device feels
- **Apps**: Available applications and ecosystem
- **Performance**: Speed, responsiveness, processing power
- **Field of View**: Visual coverage and immersion

### Interpreting Confidence Scores

- **0.8-1.0**: High confidence - sentiment is very clear
- **0.6-0.8**: Moderate confidence - sentiment is fairly clear
- **0.0-0.6**: Lower confidence - review may be ambiguous

---

## 🎯 Project Objectives (All Met ✅)

### 1. Sentiment Categorization ✅
- ✓ Performs sentiment analysis using Python
- ✓ Uses OpenAI's API for individual review analysis
- ✓ Categorizes as POSITIVE, NEGATIVE, or NEUTRAL

### 2. Aspect Extraction ✅
- ✓ Identifies specific aspects/features mentioned
- ✓ Determines what customers like or dislike
- ✓ Tags aspects with sentiment

### 3. Data Presentation ✅
- ✓ Clear, concise summary of findings
- ✓ Bar charts for sentiment distribution
- ✓ Aspect frequency visualization
- ✓ Aspect sentiment comparison charts

### 4. Insights and Recommendations ✅
- ✓ Identifies key areas of satisfaction
- ✓ Identifies areas of dissatisfaction
- ✓ Provides actionable recommendations based on specific aspects

---

## 📁 Project Structure

```
FridayProj6/
│
├── sentiment_analysis_gui.py    # Main GUI application
├── MasonsAPI_KEY.py             # Your OpenAI API key (KEEP PRIVATE!)
├── feedback.db                   # Customer reviews SQLite database
├── README.md                     # This documentation file
│
├── .gitignore                    # Protects API key from version control
│   MasonsAPI_KEY.py
│   *.db
│   __pycache__/
│   *.pyc
│
└── exports/                      # (Created when you export)
    ├── results.json              # Analysis results
    └── recommendations.txt       # Recommendation report
```

---

## 🔒 Security & Best Practices

### Protecting Your API Key

**CRITICAL**: Your API key is linked to your OpenAI account and billing!

1. **Never commit `MasonsAPI_KEY.py` to version control**
2. **Create a `.gitignore` file** with:
   ```
   MasonsAPI_KEY.py
   *.db
   __pycache__/
   *.pyc
   .DS_Store
   ```
3. **Never share your API key** in screenshots, code shares, or demos
4. **Keep the file private** - it should only exist on your local machine

### If Your Key is Compromised

1. Go to https://platform.openai.com/api-keys
2. Delete the compromised key immediately
3. Generate a new key
4. Update `MasonsAPI_KEY.py` with the new key

---

## 💡 Tips for Best Results

### For Analysis
1. **Run full analysis** for the most comprehensive insights
2. **Wait for completion** - don't interrupt the process (1-2 minutes for ~80 reviews)
3. **Check the output log** to ensure all reviews are processed
4. **Export immediately** after analysis to preserve results

### For Visualizations
1. **Start with Sentiment Distribution** to understand overall customer satisfaction
2. **Use Aspect Frequency** to identify what matters most to customers
3. **Focus on Aspect Sentiment** to find specific pain points and strengths
4. **Generate Recommendations** last - it synthesizes all the data

### For Recommendations
- The recommendations are prioritized by frequency
- Higher frequency = more customers affected = higher priority
- Use negative aspects to guide product improvements
- Use positive aspects in marketing and feature highlights

---

## 🐛 Troubleshooting

### "API Key not found" Error
**Problem**: Red message saying API key not loaded

**Solution**:
1. Open `MasonsAPI_KEY.py`
2. Verify it contains: `OPENAI_API_KEY = 'sk-proj-...'`
3. Make sure the key is in quotes
4. Save the file
5. Restart the application

### "No tables found in database" Error
**Problem**: Database file doesn't contain expected data

**Solution**:
1. Verify `feedback.db` exists in the project folder
2. Try using the Browse button to manually select it
3. Check that the database isn't corrupted (try opening with SQLite browser)
4. Ensure the database has a table with reviews

### Analysis Fails During Processing
**Problem**: Errors appear in the Analysis Output window

**Solution**:
1. **Check internet connection** - API calls require internet
2. **Verify API key is valid** - test at https://platform.openai.com
3. **Check API credits** - ensure you have sufficient OpenAI credits
4. **Review error messages** - they usually indicate the specific problem
5. **Try again** - occasional network issues can cause temporary failures

### Charts Not Displaying
**Problem**: Visualization tab shows nothing or errors

**Solution**:
1. Ensure you've completed the analysis first
2. Check that matplotlib is installed: `pip install matplotlib`
3. Try closing and regenerating the visualization
4. Check for errors in the status log

### Application Freezes
**Problem**: GUI becomes unresponsive

**Solution**:
- This is normal during analysis - processing happens in background thread
- Wait for the progress bar to complete
- Do NOT close the application during analysis
- If truly frozen (more than 5 minutes), restart and try again with fewer reviews

---

## 📈 Sample Output

After running full analysis on ~80 reviews, you can expect:

```
Total Reviews Analyzed: 79

Sentiment Distribution:
  Positive: 45 (57.0%)
  Negative: 25 (31.6%)
  Neutral: 9 (11.4%)

Total Aspects Extracted: 234
Unique Aspects: 15

Top 5 Most Mentioned Aspects:
  display: 45 times
  price: 38 times
  comfort: 32 times
  battery: 28 times
  apps: 24 times
```

---

## 🎓 Learning Outcomes

This project demonstrates practical skills in:

- **API Integration**: Working with OpenAI's GPT models
- **GUI Development**: Building user-friendly interfaces with Tkinter
- **Database Operations**: Reading from SQLite databases
- **Data Analysis**: Processing and aggregating customer feedback
- **Data Visualization**: Creating informative charts with Matplotlib
- **Natural Language Processing**: Sentiment analysis and aspect extraction
- **Multi-threading**: Keeping GUIs responsive during long operations
- **Software Engineering**: Modular code, error handling, user experience design

---

## 🔧 Technical Details

### Technologies Used
- **Python 3.7+**: Core programming language
- **Tkinter**: GUI framework
- **OpenAI API**: GPT-3.5-turbo for NLP tasks
- **SQLite3**: Database connection
- **Matplotlib**: Data visualization
- **Threading**: Asynchronous processing

### API Usage
- **Model**: gpt-3.5-turbo
- **Temperature**: 0.3 (for consistent, focused responses)
- **Max Tokens**: 50 for sentiment, 300 for aspects
- **Cost**: Approximately $0.01-0.02 per 100 reviews (varies by token usage)

### Performance
- **Analysis Speed**: ~1-2 minutes for 80-100 reviews
- **Memory Usage**: Minimal (< 100MB)
- **Database**: Supports SQLite databases of any size

---

## 📝 Assignment Submission Checklist

Before submitting your project, ensure:

- [ ] All reviews have been analyzed
- [ ] All four visualization types are generated
- [ ] Results exported to JSON
- [ ] Recommendations generated and reviewed
- [ ] Screenshots of key visualizations taken
- [ ] **`MasonsAPI_KEY.py` is NOT included in submission**
- [ ] README.md explains your findings
- [ ] Code is well-commented and follows project structure

---

## 🤝 Support

If you encounter issues:

1. **Check this README** - most common issues are covered
2. **Review error messages** - they usually indicate the problem
3. **Verify setup** - API key and database must be properly configured
4. **Check OpenAI status** - visit https://status.openai.com
5. **Test with fewer reviews** - try analyzing just 10-20 reviews first

---

## 📄 License

This project is for educational purposes as part of Friday Project 6.

---

**Project Created By**: Mason  
**Course**: Advanced Sentiment Analysis  
**Date**: 2024  
**Purpose**: Analyze Apple Vision Pro customer feedback to drive product improvements

---

## 🎉 Ready to Get Started?

1. Set up your API key in `MasonsAPI_KEY.py`
2. Run `python sentiment_analysis_gui.py`
3. Load your reviews
<<<<<<< HEAD
4. Click "Run Full Analysis"     
5. Explore your results!
    
**Good luck with your analysis!** 🚀   
=======
4. Click "Run Full Analysis"
5. Explore your results!

**Good luck with your analysis!** 🚀# FridayProj6
>>>>>>> 3a34f2765ccbb88ff22b633d575ecfd24702d5c5
