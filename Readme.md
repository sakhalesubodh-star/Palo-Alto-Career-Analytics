# Career Progression and Promotion Gap Analysis

## Project Overview
This project explores employee career progression, promotion gaps, and attrition patterns using Python and an interactive Streamlit dashboard. The goal is to identify workforce trends and suggest areas where organizations may review career development and employee retention practices.

## Business Objectives
- Analyze employee attrition patterns.
- Examine years since the last promotion.
- Compare attrition rates across departments.
- Segment employees by promotion-gap duration.
- Present findings through an interactive dashboard.
- Recommend areas for further retention analysis.

## Tools and Technologies
- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Plotly
- Streamlit
- Jupyter Notebook

## Project Workflow
1. Data loading and quality checks.
2. Exploratory data analysis (EDA).
3. Promotion-gap categorization and feature engineering.
4. Career progression analysis.
5. Attrition analysis by department and promotion gap.
6. Interactive Streamlit dashboard development.
7. Retention recommendations and reporting.

## Dashboard Pages
- **Overview:** Employee KPIs and summary information.
- **Promotion Gap Analysis:** Promotion-gap distributions and departmental comparisons.
- **Attrition Analysis:** Overall attrition and departmental trends.
- **Career Clusters:** Exploratory segments based on promotion-gap duration.
- **Retention Insights:** Attrition comparisons and potential retention actions.

## How to Run the Project

### 1. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn plotly streamlit
```

### 2. Configure the dataset
Place the source CSV in the `Data` folder and update the dataset path in `app.py` if required.

### 3. Launch the dashboard
From the project directory, run:
```bash
streamlit run app/app.py
```

Update the command if your `app.py` is stored in a different folder.

## Key Considerations
- Attrition patterns are associations and do not establish causation.
- Promotion-gap segments are exploratory categories, not proof of promotion eligibility.
- The current dashboard's Career Clusters page uses rule-based segments unless the trained clustering results are connected.
- Validate findings and consider additional business context before making workforce decisions.

## Dataset Note
Document the dataset's original source and intended context here. Do not represent the dataset as actual Palo Alto Networks employee data unless its provenance confirms that it is.

## Author
Data Analytics Internship Project