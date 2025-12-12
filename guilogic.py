import csv
import os

from PyQt6.QtWidgets import *
from accounts import Account, SavingAccount
from main_window import *

class BankGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        if hasattr(self, "pinEnter"):
            self.pinEnter.setEchoMode(QLineEdit.EchoMode.Password)

        self.accounts = {}

        self.load_accounts()
        self.refresh_account_combo()

        self.createBtn.clicked.connect(self.create_account)
        self.depositBtn.clicked.connect(self.deposit)
        self.withdrawBtn.clicked.connect(self.withdraw)
        self.showBalanceBtn.clicked.connect(self.show_balance)
        self.accountCombo.currentIndexChanged.connect(
            self.display_selected_account
        )

    def _validate_pin_text(self, text):
        #check pin
        text = text.strip()
        if len(text) != 4 or not text.isdigit():
            raise ValueError("PIN must be exactly 4 digits.")
        return text

    def load_accounts(self):
        #load accounts from CSV file
        if not os.path.exists("../accounts.csv"):
            return

        try:
            with open("../accounts.csv", "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row.get("name", "").strip()
                    acc_type = row.get("type", "").strip()
                    balance_text = row.get("balance", "0").strip()
                    pin = row.get("pin", "").strip()

                    if name == "":
                        continue

                    try:
                        balance = float(balance_text)
                    except ValueError:
                        balance = 0.0

                    if acc_type == "Saving":
                        acc = SavingAccount(name, pin if pin else None)
                        if balance != acc.get_balance():
                            acc.set_balance(balance)
                    else:
                        acc = Account(name, balance, pin if pin else None)

                    self.accounts[name] = acc
        except Exception as e:
            self.outputBox.clear()
            self.outputBox.append(
                f"Error: Failed to load accounts: {e}"
            )


    def autosave(self):
    #saves to a CSV file if something updates, learned this from internship
        try:
            with open("../accounts.csv", "w", newline="") as file:
                file.write("name,type,balance,pin\n")
                for acc in self.accounts.values():
                    name = acc.get_name()
                    balance = acc.get_balance()
                    acc_type = (
                        "Saving"
                        if isinstance(acc, SavingAccount)
                        else "Checking"
                    )
                    # access the private __pin attribute from Account
                    pin = getattr(acc, "_Account__pin", "")
                    file.write(
                        f"{name},{acc_type},{balance:.2f},{pin}\n"
                    )
        except Exception as e:
            self.outputBox.clear()
            self.outputBox.append(
                f"Error: Autosave failed: {e}"
            )

    def refresh_account_combo(self):
        #refreshes the combo box when accounts update, learned this from the internet
        self.accountCombo.clear()
        for name in self.accounts:
            self.accountCombo.addItem(name)

    def display_selected_account(self):
        # displays the information
        if hasattr(self, "balanceViewer"):
            self.balanceViewer.clear()

    def create_account(self):
        # creats the account with name, pin, account type, and amount
        try:
            self.outputBox.clear()

            name = self.nameInput.text().strip()
            acc_type = self.typeCombo.currentText().strip()

            if name == "":
                raise ValueError("Name cannot be blank.")

            if not hasattr(self, "pinCreate"):
                raise ValueError("PIN input widget not found.")

            pin_text = self.pinCreate.text()
            pin = self._validate_pin_text(pin_text)

            if hasattr(self, "NamountInput"):
                start_text = self.NamountInput.text().strip()
            else:
                start_text = ""

            if start_text != "":
                start_balance = float(start_text)
            else:
                start_balance = 0.0

            if start_balance < 0:
                raise ValueError("Starting balance cannot be negative.")

            if acc_type == "Account":
                self.accounts[name] = Account(name, start_balance, pin)
            elif acc_type == "Saving Account":
                if start_balance < 100:
                    self.outputBox.append(
                        "Error: Savings accounts require a minimum "
                        "starting balance of 100.00."
                    )
                    return

                self.accounts[name] = SavingAccount(name, pin)
                extra = (
                    start_balance - self.accounts[name].get_balance()
                )
                if extra > 0:
                    self.accounts[name].deposit(extra)
            else:
                raise ValueError("Invalid account type selected.")

            self.refresh_account_combo()
            self.autosave()

            self.nameInput.clear()
            if hasattr(self, "NamountInput"):
                self.NamountInput.clear()
            self.pinCreate.clear()
            self.typeCombo.setCurrentIndex(0)

            balance = self.accounts[name].get_balance()
            self.outputBox.append(
                f"Created account '{acc_type}' for '{name}' "
                f"of '{balance:.2f}'."
            )
        except Exception as e:
            self.outputBox.clear()
            self.outputBox.append(f"Error: {e}")

    def deposit(self):
        #handles all the deposite logic
        try:
            self.outputBox.clear()

            name = self.accountCombo.currentText().strip()
            if name == "":
                raise ValueError("Select an account first.")
            if name not in self.accounts:
                raise ValueError("Account does not exist.")

            if not hasattr(self, "pinEnter"):
                raise ValueError("PIN entry widget not found.")

            entered_pin = self._validate_pin_text(self.pinEnter.text())
            if not self.accounts[name].check_pin(entered_pin):
                raise ValueError("Incorrect PIN.")

            if (
                not hasattr(self, "EamountInput")
                or self.EamountInput.text().strip() == ""
            ):
                raise ValueError("Enter an amount to deposit.")

            amount = float(self.EamountInput.text())
            if amount <= 0:
                raise ValueError("Deposit amount must be positive.")

            if self.accounts[name].deposit(amount):
                self.outputBox.append("Deposit successful.")
            else:
                self.outputBox.append("Deposit failed.")

            self.autosave()

            if hasattr(self, "balanceViewer"):
                self.balanceViewer.clear()
                self.balanceViewer.append(str(self.accounts[name]))
        except Exception as e:
            self.outputBox.clear()
            self.outputBox.append(f"Error: {e}")

    def withdraw(self):
        #handles all the withdrawl logic
        try:
            self.outputBox.clear()

            name = self.accountCombo.currentText().strip()
            if name == "":
                raise ValueError("Select an account first.")
            if name not in self.accounts:
                raise ValueError("Account does not exist.")

            if not hasattr(self, "pinEnter"):
                raise ValueError("PIN entry widget not found.")

            entered_pin = self._validate_pin_text(self.pinEnter.text())
            if not self.accounts[name].check_pin(entered_pin):
                raise ValueError("Incorrect PIN.")

            if (
                not hasattr(self, "EamountInput")
                or self.EamountInput.text().strip() == ""
            ):
                raise ValueError("Enter an amount to withdraw.")

            amount = float(self.EamountInput.text())
            if amount <= 0:
                raise ValueError("Withdraw amount must be positive.")

            if self.accounts[name].withdraw(amount):
                self.outputBox.append("Withdraw successful.")
            else:
                self.outputBox.append(
                    "Withdraw failed (insufficient funds "
                    "or below minimum)."
                )

            self.autosave()

            if hasattr(self, "balanceViewer"):
                self.balanceViewer.clear()
                self.balanceViewer.append(str(self.accounts[name]))
        except Exception as e:
            self.outputBox.clear()
            self.outputBox.append(f"Error: {e}")

    def show_balance(self):
        #handles all the logic to show balances
        try:
            self.outputBox.clear()

            name = self.accountCombo.currentText().strip()
            if name == "" or name not in self.accounts:
                raise ValueError("Account does not exist.")

            if not hasattr(self, "pinEnter"): #found in PQ documentation
                raise ValueError("PIN entry widget not found.")

            entered_pin = self._validate_pin_text(self.pinEnter.text())
            if not self.accounts[name].check_pin(entered_pin):
                raise ValueError("Incorrect PIN.")

            if hasattr(self, "balanceViewer"):
                self.balanceViewer.clear()
                self.balanceViewer.append(str(self.accounts[name]))
            else:
                self.outputBox.append(str(self.accounts[name]))
        except Exception as e:
            self.outputBox.clear()
            self.outputBox.append(f"Error: {e}")
