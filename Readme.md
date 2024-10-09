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

EcoWheels is an innovative mobile application designed to transform the public transport landscape of Mumbai into a more sustainable and eco-friendly system. Our app empowers users to make greener travel choices while enhancing their commuting experience through the following key features:

Trip Planner: EcoWheels offers a comprehensive trip planning feature that identifies eco-friendly travel routes. Users can easily calculate distances and assess the carbon footprint of their journeys. The app also suggests nearby bus stops, metro stations, and other public transport options, helping users make informed decisions for a more sustainable commute.

Environmental Impact Chart: Stay informed about your travel habits with our detailed chart that displays average fuel consumption and carbon footprints. Users can track their progress towards greener travel and understand the positive impact of their choices on the environment.

Community Chatroom: Connect with like-minded individuals in our public chatroom where users can discuss and organize carpools. This feature fosters a sense of community, encouraging collaborative efforts to reduce the number of vehicles on the road and promote shared transportation options.

With EcoWheels, you’re not just traveling; you’re contributing to a cleaner, greener Mumbai. Join us on our mission to revolutionize public transport and make a positive impact on our environment!

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
