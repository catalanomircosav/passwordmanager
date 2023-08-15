from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)
    
    def load_key(self, path): 
        with open(path, 'rb') as f:
            self.key = f.read()
    
    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        
        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    def load_password_file(self, path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode()).decode()

                f.write(site + ":" + encrypted + "\n")

    def get_password(self, site):
        return self.password_dict[site]
    
def main():
    password = {
        "email":"12334567",
        "facebook":"7654321",
        "youtube":"pornhub",
    }

    pm = PasswordManager()

    print("""Cosa vuoi fare?
    (1) Crea un nuovo file chiave
    (2) Carica un file chiave esistente
    (3) Crea un nuovo file password
    (4) Carica un file password esistente
    (5) Aggiungi una nuova password
    (6) Ottieni una password
    (7) Esci
    """)

    done = False

    while not done:
        choice = input("Inserisci la tua scelta: ")

        if choice == "1":
            path = input("Inserisci il percorso del file chiave: ")
            pm.create_key(path)

        elif choice == "2":
            path = input("Inserisci il percorso del file chiave: ")
            pm.load_key(path)

        elif choice == "3":
            path = input("Inserisci il percorso del file password: ")
            pm.create_password_file(path, password)
        
        elif choice == "4":
            path = input("Inserisci il percorso del file password: ")
            pm.load_password_file(path)

        elif choice == "5":
            site = input("Inserisci il sito: ")
            password = input("Inserisci la password")
            pm.add_password(site, password)
        
        elif choice == "6":
            site = input("Inserisci il sito: ")
            print(pm.get_password(site))

        elif choice == "7":
            exit() 

        else: 
            print("Scelta non valida")

if __name__ == "__main__":
    main()