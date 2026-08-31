import tkinter as tk
from tkinter import messagebox
import requests
import base64
import re
import os
import sys

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except ImportError:
    os.system(f"{sys.executable} -m pip install phonenumbers requests -q")
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone

def check_number():
    mobile = entry.get().strip()
    output_text.delete('1.0', tk.END)
    
    cleaned_num = re.sub(r'[^\d+]', '', mobile)
    if not cleaned_num.startswith('+'):
        cleaned_num = '+' + cleaned_num

    try:
        parsed = phonenumbers.parse(cleaned_num)
        is_valid = phonenumbers.is_valid_number(parsed)
        
        url_base = base64.b64decode('aHR0cHM6Ly9hcGkuYXBpbGF5ZXIuY29tL251bWJlcl92ZXJpZmljYXRpb24vdmFsaWRhdGU/bnVtYmVyPQ=='.encode('ascii')).decode('ascii')
        api_key = base64.b64decode('dGdDckRFOVF0QVF4Q1lvNnk4dHprMUdtQTJKbzBYZmI='.encode('ascii')).decode('ascii')
        
        api_data = {}
        if is_valid:
            try:
                resp = requests.get(f"{url_base}{cleaned_num}", headers={"apikey": api_key}, timeout=5)
                if resp.status_code == 200:
                    api_data = resp.json()
            except:
                pass
        
        c_name = api_data.get('country_name', 'Unknown')
        c_code = api_data.get('country_code', str(parsed.country_code))
        l_format = api_data.get('local_format', phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL))
        i_format = api_data.get('international_format', phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL))
        location_api = api_data.get('location', '')
        
        loc_geo = geocoder.description_for_number(parsed, "en")
        carrier_name = carrier.name_for_number(parsed, "en")
        tz_list = timezone.time_zones_for_number(parsed)
        
        final_loc = location_api if location_api else loc_geo
        state_city = loc_geo if loc_geo else "Unknown"
        village_town = final_loc if final_loc else "Unknown"
        
        res = f"Validate Phone Number : {'Valid' if is_valid else 'Invalid/Incomplete'}\n"
        res += f"Find Location       : {final_loc}\n"
        res += f"Country name        : {c_name}\n"
        res += f"Country code        : {c_code}\n"
        res += f"Local format        : {l_format}\n"
        res += f"International number: {i_format}\n"
        res += f"Location            : {final_loc}\n"
        res += f"Validity            : {is_valid}\n"
        res += f"State/City/Region   : {state_city}\n"
        res += f"Town/Village/Place  : {village_town}\n"
        res += f"Carrier/Network     : {carrier_name if carrier_name else 'Unknown'}\n"
        res += f"Timezone            : {', '.join(tz_list) if tz_list else 'Unknown'}\n"
        res += f"Postcode            : N/A (Not trackable via phone)\n"
        
        output_text.insert(tk.END, res)
        
    except phonenumbers.NumberParseException:
        messagebox.showerror("Error", "Invalid Number Format. Include the country code.")
    except Exception:
        messagebox.showerror("Error", "An unexpected error occurred.")

def show_about():
    messagebox.showinfo("About", "Mobile Number Validation OSINT Tool\nCoded based on requested UI.")

root = tk.Tk()
root.title("Mobile Number Validation")
root.geometry("700x550")
root.configure(bg="#f0f0f0")

top_frame = tk.Frame(root, bg="black")
top_frame.pack(fill=tk.X)

banner = r"""
   ___  _  _  __  __       ___  _  _  ____  ___  _  _  ____  ____  
  /  \ | || ||  \/  |     / __|| || ||  __|| __|| |/ /|  __||  _ \ 
 | || \| || || |\/| | ___| |   |    || |__ | |  | ' / | |__ | | \ |
<< | \ \ || || |  | | ___| |   | || ||  __|| |  |  <  |  __|| |> >
 | |  \_ ||_|| |  | |    | |__ | || || |__ | |__| . \ | |__ | | /  
  \_\   \_|__|_|  |_|     \___||_||_||____||___||_|\_\|____||__/   
"""
lbl_banner = tk.Label(top_frame, text=banner, bg="black", fg="#00ff00", font=("Courier", 11, "bold"), justify=tk.CENTER)
lbl_banner.pack(pady=5)

mid_frame = tk.Frame(root, bg="#f0f0f0")
mid_frame.pack(pady=10)

lbl_prompt = tk.Label(mid_frame, text="Enter your mobile number:", font=("Arial", 12), bg="#f0f0f0")
lbl_prompt.pack()

entry = tk.Entry(mid_frame, font=("Arial", 12), width=40, justify=tk.CENTER)
entry.pack(pady=8)

btn_frame = tk.Frame(mid_frame, bg="#f0f0f0")
btn_frame.pack(pady=5)

btn_check = tk.Button(btn_frame, text="Check", width=15, font=("Arial", 11), relief=tk.RAISED, bd=2, command=check_number)
btn_check.grid(row=0, column=0, padx=15)

btn_about = tk.Button(btn_frame, text="About", width=15, font=("Arial", 11), relief=tk.RAISED, bd=2, command=show_about)
btn_about.grid(row=0, column=1, padx=15)

output_frame = tk.Frame(root, bg="#f0f0f0")
output_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

output_text = tk.Text(output_frame, font=("Courier", 11), bg="white", fg="black", bd=2, relief=tk.SUNKEN)
output_text.pack(fill=tk.BOTH, expand=True)

root.mainloop()
