# NutriPlan AI - AI-Powered Diet Planner

NutriPlan AI is an intelligent diet planning application that leverages Langchain with Groq LLM to deliver personalized nutrition guidance. The application helps users create customized meal plans based on their health goals, dietary preferences, and nutritional requirements.

## Features

- **User Profile Management**
  - Demographic information collection
  - Activity level assessment
  - Dietary preferences and restrictions
  - Health goals tracking

- **Automated Nutrition Calculations**
  - BMR (Basal Metabolic Rate) calculation
  - TDEE (Total Daily Energy Expenditure) estimation
  - Optimal macronutrient distribution

- **AI-Powered Meal Planning**
  - Personalized daily and weekly meal plans
  - Customizable meal frequency
  - Detailed nutrient analysis
  - Recipe suggestions with nutritional information

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**: Langchain with Groq LLM
- **Data Processing**: Pandas, NumPy
- **Database**: SQLite
- **Visualization**: Plotly

## Prerequisites

- Python 3.12
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/diet-planner.git
cd diet-planner
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Unix/MacOS
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run src/app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Follow the on-screen instructions to:
   - Create your user profile
   - Set your health goals
   - Generate personalized meal plans

## Project Structure

```
diet-planner/
├── src/
│   ├── app.py                 # Main Streamlit application
│   ├── utils/                 # Utility functions
│   ├── models/                # Data models
│   ├── database/             # Database operations
│   └── pages/                # Streamlit pages
├── requirements.txt          # Project dependencies
└── README.md                # Project documentation
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- USDA FoodData Central for nutritional data
- Langchain and Groq for AI capabilities
- Streamlit for the web interface framework
