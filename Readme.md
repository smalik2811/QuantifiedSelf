# Quantified Self

Quantified Self is a web application that allows users to track various aspects of their daily lives. Users can create trackers for different types of data, log their entries, and visualize their progress over time.

## Problem Statement

In today's fast-paced world, keeping track of various aspects of our lives can be challenging. Whether it's monitoring our health, productivity, or habits, having a centralized system to log and visualize this data can be incredibly beneficial. Quantified Self aims to provide a user-friendly platform where individuals can create custom trackers, log their data, and gain insights through visualizations.

## Demo Video

https://github.com/user-attachments/assets/3e1d5c3c-bfc2-446d-a675-2ebdfad4d8cc

## Project Structure

```
.
├── api.yaml
├── app.py
├── Final Report.pdf
├── Readme.md
├── requirements.txt
├── instance\
| ├── database.sqlite3
├── static/
│ ├── bootstrap/
│ │ ├── css/
│ │ │ └── bootstrap.min.css
│ │ ├── img/
│ │ │ └── computer.png
│ │ ├── js/
│ │ │ └── bootstrap.min.js
├── templates/
│ ├── addlog.html
│ ├── addlog2.html
│ ├── addtracker.html
│ ├── editlog.html
│ ├── edittracker.html
│ ├── home.html
│ ├── index.html
│ ├── signup.html
│ └── summary.html
```

## Folders and Files

- **instance**: Contains the SQLite database file.
- **static/**: Contains CSS, PNG, and JavaScript files.
  - **bootstrap/**: Contains Bootstrap CSS and JS files.
- **templates/**: Contains HTML files for the web application.
- **app.py**: Contains all the backend code and can be directly executed to run the web app.
- **api.yaml**: Contains the API documentation and schema definitions. This file is included due to the project requirement and has not been used in the project.
- **requirements.txt**: Lists the dependencies required for running the application.

## Setup and Installation

Follow these steps to set up the project on your local machine:

### 1. Clone the repository:

```sh
git clone https://github.com/smalik2811/QuantifiedSelf/settings
cd QuantifiedSelf
```

### 2. Create and Activate Virtual Environment

- #### **For Windows:**
  ```sh
  python -m venv venv
  venv\Scripts\activate
  ```
- #### **For macOS/Linux:**
  ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install the required dependencies:

```sh
pip install -r requirements.txt
```

### 4. Run the application:

```sh
python app.py
```

### 5. Access the Application:

Open your browser and navigate to `http://localhost:5000`.

## Usage

### User Authentication

You can either create a new account or use the following dummy credentials:

**Username**: `smalik2811`
**Password**: `password`

_(Note: This is not recommended for a real application due to security concerns)_

## Features

- **Trackers:** Create and manage trackers for different types of data.

- **Logs:** Add, edit, and delete logs for each tracker.

- **Visualization:** View your progress over time using charts.

## License

This project was created as part of my coursework at the [Indian Institute of Technology, Madras](https://www.iitm.ac.in/) for my undergraduate degree.

## Copyright Notice

This code is copyrighted by Sonu (c) 2022.

While this code is publicly available on GitHub, it is intended for viewing and learning purposes only. Use of this code in any other form, including modification, distribution, or incorporation into other projects, is prohibited without explicit permission from the copyright holder.

## Acknowledgements

- [Bootstrap](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)
- UI design inspired by [Coding With Nick](https://github.com/codingwithnick)

## Contact

For any inquiries, please contact [Sonu](mailto:smalik2811@gmail.com).
