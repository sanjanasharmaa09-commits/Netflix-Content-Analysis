# Netflix-Content-Analysis
End-to-end data analytics project using MySQL, Python, and Power BI
### Step 1 — Get the Dataset
1. Go to: https://www.kaggle.com/datasets/shivamb/netflix-shows
2. Download `netflix_titles.csv`
3. Place it in the `data/` folder

### Step 2 — MySQL Database
```sql
-- Open MySQL Workbench and run in order:
1. sql/01_create_database.sql   -- Creates database & imports CSV
2. sql/02_analysis_queries.sql  -- Runs 10 analytical queries
```

### Step 3 — Install Python Libraries
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Step 4 — Run Python Scripts
```bash
# From project root:
python python/01_data_cleaning.py
python python/02_eda_visualizations.py
python python/03_machine_learning.py
```

### Step 5 — Power BI Dashboard
- Follow: `powerbi_guide/POWERBI_SETUP_GUIDE.md`
- Import `data/netflix_cleaned.csv`
- Build 2-page interactive dashboard

---

## 📊 Deliverables

| # | Deliverable | Tool | Status |
|---|-------------|------|--------|
| 1 | MySQL database with 10 analytical queries | MySQL Workbench | ✅ |
| 2 | Cleaned, analysis-ready dataset (8,800+ records) | Python/Pandas | ✅ |
| 3 | 8 professional visualizations | Matplotlib/Seaborn | ✅ |
| 4 | Random Forest ML model (~95% accuracy) | Scikit-learn | ✅ |
| 5 | Interactive 2-page Power BI dashboard | Power BI | ✅ |
| 6 | 5 business recommendations | Analysis | ✅ |

---

## 📈 Key Findings

1. **Content Mix**: ~70% Movies vs ~30% TV Shows — Netflix is primarily movie-focused
2. **Growth Peak**: Content additions peaked in 2019-2020 before slowing
3. **US Dominance**: 35%+ of all content originates from the United States
4. **Audience Target**: TV-MA and TV-14 make up 75%+ of all content
5. **Movie Length**: Average movie duration is ~99 minutes

---

## 🤖 ML Model Results

| Metric | Score |
|--------|-------|
| Accuracy | ~95% |
| AUC-ROC | ~0.98 |
| Algorithm | Random Forest (200 trees) |
| Target | Movie vs TV Show |
| Features | Duration, Rating, Genre, Country, Year, etc. |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| MySQL Workbench | Data storage, SQL analytics |
| Python (Pandas, NumPy) | Data cleaning & processing |
| Matplotlib, Seaborn | Statistical visualizations |
| Scikit-learn | Machine learning model |
| Power BI | Interactive business dashboard |

---

## 📋 Resume Entry

```
NETFLIX CONTENT ANALYSIS PROJECT                          GitHub: [link]
Data Analytics | SQL, Python, Power BI                    Jan 2026

• Analyzed 8,800+ Netflix titles using MySQL to extract content 
  distribution, geographic, and temporal trends
• Built ETL pipeline with Python (Pandas, NumPy) to clean and 
  transform raw data, handling missing values across all columns
• Created 8 statistical visualizations (Matplotlib, Seaborn) 
  revealing content strategy patterns and growth trends
• Developed Random Forest classifier (~95% accuracy) to predict 
  content type using Scikit-learn
• Designed interactive 2-page Power BI dashboard with DAX measures 
  and cross-filtering for stakeholder analysis
• Generated 5 data-driven business recommendations for content 
  investment strategy

Skills: MySQL, Python, Pandas, NumPy, Scikit-learn, Matplotlib, 
Seaborn, Power BI, DAX, Data Cleaning, Machine Learning
```

---

*Dataset: Netflix Movies and TV Shows — Kaggle (Shivam Bansal)*
