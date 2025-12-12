class Account:

    def __init__(self, name, balance=0, pin=None):
        self.__account_name = name
        self.__account_balance = balance
        self.__pin = pin  # store PIN
        self.set_balance(self.__account_balance)

    def set_pin(self, pin):
        #pin info
        self.__pin = pin

    def check_pin(self, pin):
        #checks if the pin is correct
        return self.__pin is not None and self.__pin == pin

    def has_pin(self):
        #checks pin
        return self.__pin is not None

    def deposit(self, amount):
        # deposites money into account
        if amount > 0:
            self.__account_balance += amount
            return True
        return False

    def withdraw(self, amount):
        # withdrawls from account
        if amount > 0 and amount <= self.__account_balance:
            self.__account_balance -= amount
            return True
        return False

    def get_balance(self):
        #gets balance around private varibles
        return self.__account_balance

    def get_name(self):
        #gets name around private varibles
        return self.__account_name

    def set_balance(self, value):
        #sets balance of accounts
        if value < 0:
            self.__account_balance = 0
        else:
            self.__account_balance = value

    def set_name(self, value):
        #name account
        self.__account_name = value

    def __str__(self):
        return (
            f"CHECKING ACCOUNT: name = {self.get_name()}, "
            f"balance = {self.get_balance():.2f}"
        )


class SavingAccount(Account):

    MINIMUM = 100
    RATE = 0.02

    def __init__(self, name, pin=None):
        # start at MINIMUM, with PIN
        super().__init__(name, self.MINIMUM, pin)
        self.__deposit_count = 0

    def apply_interest(self):
        #intrest function
        balance = self.get_balance()
        balance += balance * self.RATE
        self.set_balance(balance)

    def deposit(self, amount):
        # same function but with intrest
        success = super().deposit(amount)
        if success:
            self.__deposit_count += 1
            if self.__deposit_count % 5 == 0:
                self.apply_interest()
        return success

    def withdraw(self, amount):
        # same function but has the minmum requirements
        if amount > 0 and (self.get_balance() - amount) >= self.MINIMUM:
            return super().withdraw(amount)
        return False

    def set_balance(self, value):
        #same function but has the minmum requirements
        if value < self.MINIMUM:
            super().set_balance(self.MINIMUM)
        else:
            super().set_balance(value)

    def __str__(self):
        return (
            f"SAVING ACCOUNT: name = {self.get_name()}, "
            f"balance = {self.get_balance():.2f}"
        )
