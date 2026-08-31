import sys
import re
import os

try:
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
    import phonenumbers
    from phonenumbers import geocoder, carrier
except ImportError:
    os.system("pip install PyQt5 phonenumbers")
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
    import phonenumbers
    from phonenumbers import geocoder, carrier

class PhoneTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Phone Number Tracker')
        self.resize(480, 500)
        self.setStyleSheet("background-color: #2b2b2b;")
        
        layout = QVBoxLayout()

        self.label = QLabel('Enter Number (e.g. 8801712... or +1234...):')
        self.label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        layout.addWidget(self.label)

        self.entry_box = QLineEdit()
        self.entry_box.setStyleSheet("background-color: white; color: black; font-size: 14px; padding: 6px;")
        layout.addWidget(self.entry_box)

        self.track_btn = QPushButton('Track Number')
        self.track_btn.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; font-weight: bold; padding: 10px;")
        self.track_btn.clicked.connect(self.check_number)
        layout.addWidget(self.track_btn)

        self.output_box = QTextEdit()
        self.output_box.setStyleSheet("background-color: #f4f4f4; color: black; font-family: Courier; font-size: 14px;")
        self.output_box.setReadOnly(True)
        layout.addWidget(self.output_box)

        self.setLayout(layout)

    def check_number(self):
        raw_input = self.entry_box.text().strip()
        self.output_box.clear()

        if not raw_input:
            QMessageBox.critical(self, "Error", "Please enter a phone number.")
            return

        cleaned_num = re.sub(r'[^\d+]', '', raw_input)

        if not cleaned_num.startswith('+'):
            cleaned_num = '+' + cleaned_num

        try:
            parsed_num = phonenumbers.parse(cleaned_num)
            
            is_valid = phonenumbers.is_valid_number(parsed_num)
            valid_str = "True" if is_valid else "False (Invalid/Incomplete)"

            country_code = parsed_num.country_code
            location_desc = geocoder.description_for_number(parsed_num, "en")
            network = carrier.name_for_number(parsed_num, "en")
            
            local_fmt = phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.NATIONAL)
            intl_fmt = phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            
            res = f"Validate Phone Number: {valid_str}\n"
            res += f"Find Location: {location_desc or 'Unknown'}\n"
            res += f"Country name: {location_desc or 'Unknown'}\n"
            res += f"Country code: {country_code}\n"
            res += f"Local format: {local_fmt}\n"
            res += f"International number: {intl_fmt}\n"
            res += f"Location: {location_desc or 'Unknown'}\n"
            res += f"Validity: {valid_str}\n"
            res += f"Carrier/Network: {network or 'Unknown'}\n"
            
            self.output_box.setText(res)
            
        except phonenumbers.NumberParseException:
            QMessageBox.critical(self, "Error", "Invalid format. Ensure country code is included.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PhoneTrackerApp()
    ex.show()
    sys.exit(app.exec_())
