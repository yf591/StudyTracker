# StudyTracker

A study time management application that gamifies learning by turning study sessions into experience points and levels.

## Features

- 📊 Track study time and progress for different subjects
- 🎮 Gamification system with EXP points and levels
- 📈 Detailed analytics and visualization
- 🎯 Progress tracking with daily/weekly/monthly views
- 🎫 Reward ticket system for motivation
- 📝 Study record management

## Repository Structure
```bash
StudyTracker/
├── main.py              # Application entry point
├── models/              # Directory for data models
│   ├── __init__.py     # Python package initialization file
│   └── study_tracker.py # Model class for managing and storing study data
├── views/               # Directory for GUI components
│   ├── __init__.py     # Python package initialization file
│   ├── app.py          # Main application GUI class
│   ├── dialogs.py      # Dialog window classes
│   └── stats/          # Directory for statistical view components
│       ├── __init__.py # Python package initialization file
│       ├── analysis_view.py  # View class for analysis data
│       ├── daily_view.py     # View class for daily statistics
│       ├── management_view.py # View class for record management
│       └── status_view.py    # View class for current status
└── utils/              # Directory for utility functions
    ├── __init__.py    # Python package initialization file
    ├── analytics.py   # Utility functions for data analysis
    └── config.py      # Application configuration definitions
```

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/StudyTracker.git
cd StudyTracker
```

2. Create and activate a virtual environment:
**Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install required packages
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python main.py
```

## Disclaimer
This application is provided "as is" without warranty of any kind. Use at your own risk.

## License
This project is licensed under the MIT License - see the LICENSE file for details.