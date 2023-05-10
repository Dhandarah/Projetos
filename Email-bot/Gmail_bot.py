import base64
import os
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import schedule
import time

# Configurações
SENDER_EMAIL = 'seu_email@gmail.com'
RECEIVERS = ['email1@example.com', 'email2@example.com']
SUBJECT = 'Assunto do email'
BODY = 'Corpo da mensagem'
DIRECTORY_PATH = '/caminho/do/diretorio/'

# Autenticação
def authenticate_gmail():
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

# Função para criar e-mail
def create_message_with_attachments(sender, to, subject, message_text, file_paths):
    message = MIMEMultipart()
    message['to'] = COMMASPACE.join(to)
    message['subject'] = subject

    message.attach(MIMEText(message_text))

    for file_path in file_paths:
        content_type, encoding = mimetypes.guess_type(file_path)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'

        main_type, sub_type = content_type.split('/', 1)
        with open(file_path, 'rb') as fp:
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
        encoders.encode_base64(msg)

        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
        message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

# Função para enviar e-mail
def send_email(service, message):
    try:
        message = (service.users().messages().send(userId="me", body=message).execute())
        print(F'Email enviado para {message["to"]}, Message Id: {message["id"]}')
    except HttpError as error:
        print(F'Ocorreu um erro: {error}')
        message = None
    return message

# Função para listar todos os arquivos em um diretório
def list_files(directory):
    files = []
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            files.append(os.path.join(directory, file))
    return files

# Função para enviar e-mails agendados
def send_scheduled_email():
    print("Enviando e-mail agendado...")
    service = authenticate_gmail()
    attachments = list_files(DIRECTORY_PATH)
    message = create_message_with_attachments(SENDER_EMAIL, RECEIVERS, SUBJECT, BODY, attachments)
    send_email(service, message)

# Agendar envio de e-mail todo dia 28 às 10h
schedule.every().day.at("10:00").do(send_scheduled_email)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(60)  # Aguarda 60 segundos antes de verificar novamente
