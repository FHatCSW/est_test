# EST Client Wrapper

This Python script demonstrates the usage of the est.client library to interact with an EST (Enrollment over Secure Transport) server. The script provides a convenient wrapper class ESTClientWrapper that encapsulates common EST functionalities, such as configuring basic authentication, obtaining CA certificates, creating Certificate Signing Requests (CSRs), and enrolling for client certificates.

## Installation

Before running the script, make sure to install the required dependencies. You can install them using the following command:

```bash
pip install -r requirements.txt
```

## Configuration

Credentials and other configuration parameters are stored in a config.json file. Edit this file to include your specific EST server details, usernames, passwords, and aliases.

```json
{
    "host": "your_hostname",
    "username": "your_username",
    "password": "your_password",
    "client_alias": "/your_client_alias",
    "server_alias": "/your_server_alias"
}
```

## Usage

Run the script using the following command:

```bash
python main.py
```
