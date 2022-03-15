import csv


with open("exemplo_2.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["nome", "email", "telefone"])
    writer.writerow(["Gabriel", "gabriel@email.com", "2121212"])
    writer.writerow(["Gabriel", "gabriel@email.com", "2121212"])
    writer.writerow(["Gabriel", "gabriel@email.com", "2121212"])
    writer.writerow(["Gabriel", "gabriel@email.com", "2121212"])