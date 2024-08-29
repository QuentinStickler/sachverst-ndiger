import json
import csv

# Pfad zur JSON-Datei
json_file_path = "Aufgabe 1\Case_DarkNight.json"

# JSON-Datei öffnen und laden
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# CSV-Datei öffnen, um darin zu schreiben
with open('python_mit_messenger_output.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Kopfzeile schreiben, inklusive der neuen Spalte "Platform"
    writer.writerow(["Platform", "Sender Name", "Sender AppID", "Recipient Name", "Recipient AppID", "Text", "Timestamp", "Direction", "Attachments"])
    
    # Durch die JSON-Struktur iterieren, um die notwendigen Daten zu finden
    for image in data.get("Images", []):
        artifacts = image.get("Artifacts", {})
        
        for platform, conversations in artifacts.items():  # Platform ist der Name des Dienstes
            for conversation in conversations:
                for message_id, messages in conversation.items():
                    for message in messages:
                        timestamp = message.get("Time", "")
                        text = message.get("Text", "").replace('\n', ' ')
                        direction = message.get("Direction", "")
                        sender_display_name = message.get("Sender", {}).get("DisplayName", "")
                        sender_app_id = message.get("Sender", {}).get("AppId", "")
                        
                        # Da es mehrere Empfänger geben kann, behandeln wir diese in einer Schleife
                        for recipient in message.get("Recipients", []):
                            recipient_name = recipient.get("Name", "")
                            recipient_app_id = recipient.get("AppId", "")
                            
                            # Anhänge verarbeiten
                            attachments = message.get("Attachments", [])
                            # Jedes Attachment in einen String konvertieren, um Diktate oder andere Typen zu behandeln
                            attachment_strings = []
                            for attachment in attachments:
                                if isinstance(attachment, dict):
                                    # Das Dict in eine String-Darstellung umwandeln oder relevante Infos extrahieren
                                    attachment_strings.append(json.dumps(attachment).replace('\n', ' '))
                                else:
                                    attachment_strings.append(str(attachment).replace('\n', ' '))
                            
                            # Alle Anhänge in einen einzigen String zusammenfassen
                            attachments_str = ", ".join(attachment_strings)
                            
                            # Eine Zeile in die CSV-Datei mit der aktualisierten Spaltenreihenfolge und dem Dienstnamen schreiben
                            writer.writerow([platform, sender_display_name, sender_app_id, recipient_name, recipient_app_id, text, timestamp, direction, attachments_str])

print("Data has been written to python_output.csv")
