"""
Created by: @CJeiPeer
Created at: 03/02/2024
Brief:
    This script generate strongest password, using the principles of security passwords
    explained in the README file.
Note: 
    Replace placeholder values ('Reeplace for your site' and 'Reeplace for your login') with your actual site name and login information before using it.

If you like followme on Linkedin: https://www.linkedin.com/in/alejocjaimes31/
"""
import pandas as pd
import string
import random
import time
from faker import Faker
from datetime import datetime

def bank_fake_keyword(limit:int)->list:
  # Create an instance of the 'Faker' class
  fake = Faker()
  Faker.seed(int(time.time()))
  """
    Generate a list of fake keywords related to cryptocurrencies and SWIFT-8.

    Parameters:
    - limit (int): The number of fake keywords to generate for each category.

    Returns:
    - list: A list containing fake keywords, including cryptocurrency names,
            cryptocurrency codes, and SWIFT-8 codes.
  """
  # Generate lists with randomly generated cryptocurrency names, codes, and SWIFT-8 codes
  cryptocurrency_name = [fake.cryptocurrency_name() for _ in range(limit)]
  cryptocurrency_code = [fake.cryptocurrency_code() for _ in range(limit)]
  swift8 = [fake.swift8() for _ in range(limit)]
  # Combine the three lists to get a single list of fake keywords
  return cryptocurrency_name + cryptocurrency_code + swift8

def password_generate(limit:int)->str:
  """
    Generate a random password with specific complexity requirements.

    Parameters:
    - limit (int): The length of the generated password.

    Returns:
    - str: A randomly generated password that meets complexity requirements.
  """
  # 1. Define the character sets to use for password generation.
  upper_letters= string.ascii_uppercase
  lower_letters = string.ascii_lowercase
  digits = string.digits
  special_characters = "!@#$%^&*()_+"
  current_year = datetime.now().year
  # Generate a list of fake bank-related keywords
  bank_keyword = bank_fake_keyword(limit)
  # 2. Select a keyword from the list and append the current year
  p_keyword_selected = random.choice(bank_keyword) + str(current_year)
  # 3. Determine the length of each character set based on the limit
  limit_split = limit // 4
  p_upper_letters = ''.join(random.sample(upper_letters,limit_split))
  p_lower_letters = ''.join(random.sample(lower_letters,limit_split))
  p_digits = ''.join(random.sample(digits,limit_split))
  p_special_characters = ''.join(random.sample(special_characters,limit_split))

  # 4. Generate a random password using the specified length limit.
  all_characters = p_upper_letters + p_lower_letters + p_keyword_selected \
            + p_special_characters + p_digits
  
  password = ''.join(random.sample(all_characters, limit))
  # Ensure the password meets the complexity requirements:
  # - At least one uppercase letter
  # - At least one lowercase letter
  # - At least one digit
  # - At least one special character
  while not any(c.isupper() for c in password) or \
        not any(c.islower() for c in password) or \
        not any(c.isdigit() for c in password) or \
        not any(c in special_characters for c in password):
    password = ''.join(random.sample(all_characters, limit))
  return password

def password_manager(limit_password:int, limit_rows)->pd.DataFrame:
  """
    Generate a password manager DataFrame with randomly generated passwords.

    Parameters:
    - limit_password (int): The length of each generated password.
    - limit_rows (int): The number of rows (passwords) to generate in the DataFrame.

    Returns:
    - pd.DataFrame: A DataFrame containing site names, date of generation, and randomly generated passwords.
  """
  # 1. Define the columns for the DataFrame
  columns = ['Site','Date Generated','Login','Password']
  # 2. Create an empty DataFrame with the specified columns
  df = pd.DataFrame(columns=columns)
   # 3. Generate passwords and populate the DataFrame
  df['Password'] = [password_generate(limit_password) for _ in range(limit_rows)]
  # 4. Set a placeholder site name for the 'Site' column (replace with your site name)
  df['Site'] = 'Reeplace for your site'
  # 5. Set a placeholder site name for the 'Login' column (replace with your site name)
  df['Login'] = 'Reeplace for your login'
  # 6. Set the 'Date Generated' column with the current date and time
  current_date = datetime.now().strftime("%Y%m%d")
  df['Date Generated'] = datetime.now().strftime("%Y/%m/%d %H:%M")
  return df,current_date

if __name__ == '__main__':
  # Generate df.
  limit_password = int(input("Type limit password (limit min recommended 12): "))
  limit_rows = int(input("How many passwords do you need generate?: "))
  df,current_date = password_manager(limit_password,limit_rows)
  # export df
  file_export = 'Passwords'+current_date+'.xlsx'
  df.to_excel(file_export,index=False)