import requests
import json

class Ticket:
    def __init__(self, number, amount, quantity=1):
        self.number = number
        self.amount = amount
        self.quantity = quantity

    def __str__(self):
        return f"{self.number} {self.amount}"

    def __repr__(self):
        return f"{self.number} {self.amount}"

# read file read lines
def loadLottery():
    file = open('decimos.txt','r')
    lines = [line.strip() for line in file.readlines()]
    file.close()

    tickets = []
    for line in lines:
        ticket = line.split(':')
        if len(ticket) == 2:
            tickets.append(Ticket(ticket[0], float(ticket[1])))
        if len(ticket) == 3:
            tickets.append(Ticket(ticket[0], float(ticket[1]), int(ticket[2])))
            # print(ticket)
    return tickets

def getTicketRevenue(ticket):
    urlElPais = 'https://api.elpais.com/ws/LoteriaNavidadPremiados?n=' + ticket.number
    response = requests.get(urlElPais)
    data = json.loads(response.text.split('=')[1])
    revenue = -1
    if data['error'] == 0:
        price = data['premio']
        revenue = ticket.quantity * ticket.amount * price/20 
    return revenue

if __name__ == '__main__':
    totalRevenue = 0
    totalSpentMoney = 0
    lotteryTickets = loadLottery()
    winTickets = set()
    print(f"Comprobando décimos:")
    for ticket in lotteryTickets:
        totalSpentMoney += ticket.amount * ticket.quantity
        revenue = getTicketRevenue(ticket)
        if revenue > 0:
            print(f"¡Premiado {ticket.number}! Cantidad: {ticket.quantity} - Premio total: {revenue}€")
            winTickets.add(ticket.number)
            totalRevenue += revenue
    if len(winTickets) > 0:
        print(f"¡Décimos premiados!: {winTickets}")
    else:
        print(f"\n\n¡No hay décimos premiados! :(\n")

    print(f"\nTotal ganado: {totalRevenue}€")
    print(f"Total gastado: {totalSpentMoney}€")
    print(f"Ganancia: {totalRevenue - totalSpentMoney}€")
