import json
import csv

# Pfad zur JSON-Datei
json_file_path = "DarkNight_Dataset/Case_DarkNight.json"

# JSON-Datei öffnen und laden
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Open a CSV file to write to
with open('python_output.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Write the header with the new column order
    writer.writerow(["Sender DisplayName", "Sender AppID", "Recipient Name", "Recipient AppID", "Text", "Timestamp", "Direction", "Attachments"])
    
    # Iterate through the JSON structure to find the necessary data
    for image in data.get("Images", []):
        artifacts = image.get("Artifacts", {})
        
        for platform, conversations in artifacts.items():
            for conversation in conversations:
                for message_id, messages in conversation.items():
                    for message in messages:
                        timestamp = message.get("Time", "")
                        text = message.get("Text", "").replace('\n', ' ')
                        direction = message.get("Direction", "")
                        sender_display_name = message.get("Sender", {}).get("DisplayName", "")
                        sender_app_id = message.get("Sender", {}).get("AppId", "")
                        
                        # Since there can be multiple recipients, we'll handle them in a loop
                        for recipient in message.get("Recipients", []):
                            recipient_name = recipient.get("Name", "")
                            recipient_app_id = recipient.get("AppId", "")
                            
                            # Process Attachments
                            attachments = message.get("Attachments", [])
                            # Convert each attachment to string, handling dictionaries or other types
                            attachment_strings = []
                            for attachment in attachments:
                                if isinstance(attachment, dict):
                                    # Convert the dict to a string representation, or extract relevant info
                                    attachment_strings.append(json.dumps(attachment).replace('\n', ' '))
                                else:
                                    attachment_strings.append(str(attachment).replace('\n', ' '))
                            
                            # Join all attachments into a single string
                            attachments_str = ", ".join(attachment_strings)
                            
                            # Write a row to the CSV with the updated column order
                            writer.writerow([sender_display_name, sender_app_id, recipient_name, recipient_app_id, text, timestamp, direction, attachments_str])

print("Data has been written to python_output.csv")
