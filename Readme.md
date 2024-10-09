# EcoWheels

EcoWheels is a web application project focused on sustainable transportation solutions, built primarily using Python and HTML. This repository contains the source code, project structure, and requirements for building and running the application.

## Table of Contents

- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## About the Project

EcoWheels is designed to provide eco-friendly transport options through an interactive web platform. Users can explore sustainable transportation choices, such as electric bikes or car-sharing services, and manage various functionalities through the provided admin interface.

## Getting Started

To get started with EcoWheels, you will need to clone the repository and install the necessary dependencies.

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Clone the Repository

```bash
git clone https://github.com/Didfu/EcoWheels.git
cd EcoWheels
```

## Features

- **User Authentication**: Sign up, log in, and manage user accounts.
- **Admin Panel**: Admin can manage transport listings, user information, and other settings.
- **Transport Listings**: Users can view and select various transportation options.
- **Interactive Dashboard**: Provides key insights into transportation usage and environmental impact.

## Technologies

EcoWheels uses the following technologies:

- **Frontend**: HTML, CSS
- **Backend**: Python (Django)
- **Database**: SQLite

## Installation

1. Navigate to the project directory and install the required packages:

```bash
pip install -r requirements.txt
```

2. Apply database migrations:

```bash
python manage.py migrate
```

3. Run the development server:

```bash
python manage.py runserver
```

## Usage

Once the server is running, open your browser and navigate to `http://127.0.0.1:8000/` to access the EcoWheels application. Use the provided admin panel to manage the platform.

## Contributing

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request for review.

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a pull request.

## License

This project is licensed under the MIT License.
