# Tidio_Chat_Task
A program that facilitates communication with a Tidio web chat widget
## How to Run the Code

### Prerequisites
Install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```
### How To Run
1. Run the program from the command line with the following arguments:   
   ```bash
   python tidio_cli.py --key <TIDIO_PROJECT_PUBLIC_KEY> --visitor_id <VISITOR_ID> --url <TIDIO_CHAT_URL>
   ```
2. Start chatting freely

### Arguments
1. --key: The public key of your Tidio project (required).
2. --visitor_id: The unique ID of the visitor (required)
3. --url: The URL of the Tidio chat widget (default=http://localhost:8000).

### Usage
1. Type messages in the terminal and press Enter to send.
2. Messages from the operator will appear in the terminal.
3. Press Ctrl+C to disconnect and exit the program.