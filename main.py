from fastapi import FastAPI

from loadData import loadData
from database import LeakedEmailsDB

app = FastAPI()

data = loadData()
db = LeakedEmailsDB(data)

@app.get('/dataLeaks/')
def getDataLeaksByEmail(email):
  leakedEmails = db.get(email=email)
  response = list(map(lambda e: e.company, leakedEmails))
  return { 'dataLeaks': response }

@app.get('/emails/')
def getLeakedEmailsByDomain(domain):
  leakedEmails = db.get(domain=domain)
  response = list(map(lambda e: e.email, leakedEmails))
  return { 'emails': response }