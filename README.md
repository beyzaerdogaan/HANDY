# Handy Application

The Handy Application is a Python-based application with a graphical user interface (UI). It allows users to perform various tasks conveniently. This README file provides information on how to run the code and configure MySQL in localhost.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)

## Prerequisites

Before running the Handy Application, ensure you have the following prerequisites installed on your system:

- Python (version 3.8)
- MySQL (version 5.7 or above)

## Installation

To install the Handy Application, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/beyzaerdogaan/HANDY.git
   ```
2. Navigate to the project directory:

   ```bash
   cd HANDY
   ```
3. Install the required packages
   

## Configuration

To configure MySQL in localhost for the Handy Application, follow these steps:

1. Ensure you have MySQL installed and running on your machine. If not, download and install it from the official MySQL website.

2. Create a new MySQL database for the application.

3. Open the `databese_config.py` file in a text editor.

4. Update the following configuration variables with your MySQL credentials:

    ```python 
        DB_HOST = 'localhost'  # MySQL host (usually localhost)
        DB_USER = 'your-username'  # MySQL username
        DB_PASSWORD = 'your-password'  # MySQL password
        DB_DATABASE = 'your-database'  # MySQL database name
    ```

5. Replace `your-username`, `your-password`, and `your-database` with your actual MySQL credentials.

6. Save the `database_config.py` file.
   
# Running the Application
To run the Handy Application, follow these steps:

1. Open a terminal or command prompt.

2. Navigate to the project directory:

   ```bash 
       cd handy-application
   ```

3. Run the following command:
    ```bash 
        python ui-backend.py
    ```
   
The application's graphical user interface should now open. You can interact with it to perform various tasks.

That's it! You have successfully set up and run the Handy Application on your local machine. Enjoy using the application!

If you encounter any issues or have any questions, feel free to contact us at https://handy-project.netlify.app/#footer.