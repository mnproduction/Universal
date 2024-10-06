# Universal Web Scraper 🦀


## 🚧 Under Construction 🚧

**Note**: This project is currently under active development. Some features may be incomplete or subject to change. We appreciate your patience and welcome any feedback or contributions to help improve the Universal Web Scraper.


## Table of Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Set Up Virtual Environment](#set-up-virtual-environment)
  - [Install Dependencies](#install-dependencies)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Description

**Universal Web Scraper** is a versatile web scraping tool built with Python and Streamlit. It allows users to scrape data from any website by specifying custom fields to extract. The application processes the scraped data, saves it in multiple formats (JSON, CSV, Excel), and provides insights into token usage and associated costs based on selected models.

## Features

- **Dynamic Field Extraction**: Specify custom fields to extract using tag inputs.
- **Multiple Output Formats**: Save scraped data as JSON, CSV, Excel, and Markdown files.
- **Token Usage Calculation**: Automatically calculate input and output tokens and estimate associated costs.
- **User-Friendly Interface**: Intuitive UI built with Streamlit for seamless interaction.
- **Error Handling**: Robust error management to ensure smooth scraping operations.
- **Modular Codebase**: Clean and maintainable code structure for easy scalability.

## Installation

### Prerequisites

- **Python 3.8+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
- **Git**: To clone the repository. Download from [git-scm.com](https://git-scm.com/downloads).

### Clone the Repository

```bash
git clone https://github.com/yourusername/universal-web-scraper.git
cd universal-web-scraper
```

### Set Up Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### Install Dependencies

Ensure you have the latest version of `pip`:

```bash
pip install --upgrade pip
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the Streamlit app using the following command:

```bash
streamlit run streamlit_app.py
```

This will open the application in your default web browser. If it doesn't open automatically, navigate to [http://localhost:8501](http://localhost:8501) in your browser.

### Configuration

1. **Select Model**: Choose the desired model from the sidebar (e.g., `gpt-4o-mini`, `gpt-4o-2024-08-06`).
2. **Enter URL**: Input the URL of the website you wish to scrape.
3. **Specify Fields**: Use the tag input to specify the fields you want to extract from the webpage.
4. **Run Scraper**: Initiate the scraping process. Once completed, the data will be displayed and available for download in various formats.

## Project Structure

```plaintext
universal-web-scraper/
├── .gitignore
├── requirements.txt
├── scraper.py
├── streamlit_app.py
├── README.md
└── output/
    └── raw_data/
        └── raw_data_YYYYMMDD_HHMMSS.txt
```

- **.gitignore**: Specifies files and directories to be ignored by Git.
- **requirements.txt**: Lists all Python dependencies required for the project.
- **scraper.py**: Contains the core scraping logic and data processing functions.
- **streamlit_app.py**: The Streamlit application script that provides the user interface.
- **README.md**: This documentation file.
- **output/raw_data/**: Directory where raw scraped data is stored.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeature
   ```
5. Open a Pull Request.

Please ensure your code adheres to the project's coding standards and include relevant tests.

## Credits and Thanks

Special thanks to:

- **Reda Marzouk**
  - 💼 LinkedIn: [reda-marzouk-rpa](https://www.linkedin.com/in/reda-marzouk-rpa/)
  - 🤖 YouTube: [@redamarzouk](https://www.youtube.com/@redamarzouk)

We extend our heartfelt gratitude to Reda Marzouk for his invaluable contributions and inspiration to this project. His expertise in RPA and web scraping has been instrumental in shaping the direction and capabilities of this Universal Web Scraper.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or suggestions, feel free to reach out:

- **Email**: [your.email@example.com](mailto:my.novosolov@gmail.com)
- **GitHub**: [@yourusername](https://github.com/mnproduction)

---

Happy Scraping! 🦀
