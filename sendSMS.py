import subprocess

def sendSMS():
    peringatan = "Telah terjadi pelanggaran protokol Physical Distancing di Ruangan"
    ruangan = "L203"
    Link = 'https://tecorp.me/dede/'
    noTlp = "08953215888"
    kirim = (peringatan + " " + ruangan + " " + "Silahkan Klik link berikut untuk melihat foto" + " " + Link)
    subprocess.call(['curl', '-X', 'POST', "https://api.thebigbox.id/sms-notification/1.0.0/messages", 
                    '-H', "accept: application/x-www-form-urlencoded", '-H', "x-api-key: 2y2XT6ELcv16nD92H4mTpktqdF2sEChk", 
                    '-H', "Content-Type: application/x-www-form-urlencoded", '-d', "msisdn="+ noTlp + '&content=' + kirim])
sendSMS()
print("SMS has been sent")