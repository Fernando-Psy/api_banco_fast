from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
app = FastAPI()

# Modelo conta bancária
class Account(BaseModel):
    account_id: int
    balance: float

# Armazemnamento das contas em memória
accounts: Dict[int, Account] = {}

# Endpoint para nova conta
@app.post("/accounts/", response_model=Account)
async def create_account(account: Account):
    if account.account_id in accounts:
        raise HTTPException(status_code=400, detail="Essa conta já existe!")
    accounts[account.account_id] = account
    return account

# Endpoint dos detalhes da conta
@app.get("/accouns/{account_id}", response_model=Account)
async def get_account(account_id: int):
    account = accounts.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada!")
    return account

# Endpoint de dep´sito
@app.post("/accounts/{acount_id}/deposit")
async def deposit(account_id: int, amount: float):
    account = accounts.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada!")
    if amount <= 0:
        raise HTTPException(status_code=404, detail="O valor do depósito deve ser maior que zero")

    account.balance += amount
    return {"message": "Deposit successful", "new_balance": account.balance}

# Endpoint para sacar dinheiro da conta
@app.post("/accounts/{account_id}/withdraw")
async def withdraw(account_id: int, amount: float):
    account = accounts.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada!")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="O valor de retirada deve ser maior que zero")
    if amount > account.balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    account.balance -= amount
    return {"message": "Retirada bem sucedida!", "new_balance": account.balance}

# Endpoint para listar todas as contas
@app.get("/accounts/", response_model=List[Account])
async def list_accounts():
    return list(accounts.values())