# LinkedIn Automation Project

This Python project automates the process of adding or following people on LinkedIn based on a provided CSV file.

## Prerequisites

- Python 3.x
- Selenium
- pandas

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/samuelsilvadev/linkedin-automation.git
    cd linkedin-automation
    ```

2. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Prepare your CSV file with the following columns:
    - `URL`

2. Create a `.env` file with your LinkedIn credentials, you can copy the .env.example:

    ```python
    LINKEDIN_USERNAME = 'your_email@example.com'
    LINKEDIN_PASSWORD = 'your_password'
    ```

3. Run the script:

    ```sh
    python connect_with_people.py --file path/to/your/csvfile.csv
    ```

## Disclaimer

Use this script responsibly and ensure compliance with LinkedIn's terms of service.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
