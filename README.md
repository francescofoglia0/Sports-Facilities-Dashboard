# Sports Facility Management Dashboard

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

A multi-page interactive web application built with **Python** and **Streamlit**, designed to manage the scheduling, analytics, and daily operations of a sports facility.

## Core Features

*   **Interactive Multi-Page UI:** Developed a fluid and responsive user interface using Streamlit, allowing staff to navigate between course overviews, instructor management, and scheduling boards.
*   **Relational Database Integration:** The frontend is fully integrated with a **MySQL** database backend. All data interactions (reading schedules, updating courses, adding instructors) are handled via complex, secure SQL queries.
*   **Real-Time Analytics:** Utilizes **Pandas** to fetch, process, and display real-time operational data, transforming raw database tables into readable schedules and performance metrics.
*   **Application-Level Constraint Checking:** Implemented robust logic to prevent double-booking, scheduling conflicts, and data inconsistencies (e.g., ensuring an instructor cannot be assigned to two overlapping classes).

## Repository Structure

*   `_Home.py`: The main entry point of the Streamlit application and landing page.
*   `pages/`: Contains the individual sub-pages of the dashboard (e.g., Courses, Instructors, New Lessons).
*   `utils/`: Python utility scripts for database connection handling, SQL query execution, and data formatting.
*   `images/`: Contains static assets and UI resources used within the dashboard.

## How to Run

Ensure you have a local or remote MySQL database running, and update the database credentials in the `utils/` connection files.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/francescofoglia0/Sports-Facility-Dashboard.git](https://github.com/francescofoglia0/Sports-Facility-Dashboard.git)
   cd Sports-Facility-Dashboard
   ```

2. **Install the dependencies:**
   ```bash
   pip install streamlit pandas mysql-connector-python
   ```

3. **Run the application:**
   ```bash
   streamlit run _Home.py
   ```
   The dashboard will automatically open in your default web browser at `http://localhost:8501`.
