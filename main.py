from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
from bs4 import BeautifulSoup
from googlesearch import search
import requests

def welcome():
    hai = 'Selamat Datang'
    return hai

def brainly(chat):
    print('process')
    cari = f"{chat} brainly"

    links = []

    for j in search(cari, tld="co.id", num=20, stop=20, pause=2): 
        if 'https://brainly.co.id/tugas/' in j:
            links.append(j)

    
    data = []

    try:
        for a in range(0,3):
            html = requests.get(links[a])
            soup = BeautifulSoup(html.content,'html.parser')
            jawaban_terverifikasi = soup.find('div',attrs={'data-testid':"answer_box_text"}).get_text()
            clear_data = jawaban_terverifikasi.replace('\n','')
            data.append(clear_data)

        jawaban = f'''
        Jawaban 1
        {data[0]}

        Jawaban 2
        {data[1]}

        Jawaban 3
        {data[2]}
        '''
        return jawaban

    except:
        print('gagal')
        jawaban = 'Mohon maaf kami tidak dapat menyelesaikan pertanyaan tersebut'
        return jawaban
 
app = Flask(__name__)
 
@app.route("/")
def wa_hello():
    return "Hello, World!"
 
@app.route("/core", methods=['POST'])
def wa_sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    
    pesan = request.form.get('Body').lower() # Reading the message from the whatsapp
 
    print("pesan-->",pesan)
    resp = MessagingResponse()
    reply=resp.message()
    # Create reply
    if pesan == "hi":
       reply.body(welcome())
    elif pesan == "video":
       reply.media('https://www.appsloveworld.com/wp-content/uploads/2018/10/640.mp4')
    else:
        reply.body(brainly(pesan))
 
 
    return str(resp)
if __name__ == "__main__":
    app.run(debug=True)