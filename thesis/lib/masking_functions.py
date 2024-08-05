import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import math
import pandasql as ps
import time
import string
from typing import Any, Callable
import copy
from datetime import datetime, timedelta, date
import random
import calendar
import sys
from decimal import Decimal

# Medical dataset

def bucketize_age(age, b_size):
    l = age // b_size
    h = l+1
    return '['+str(l*b_size)+' - '+str(h*b_size-1)+']'

def blur_zip(zip_code, nFields):
    assert(nFields <= 6 and nFields > 0)
    return zip_code[:-nFields]+("X"*nFields)


def blur_string(value, num_blur_fields):
    value = str(value)
    try:
        # Ensure num_blur_fields is an integer
        num_blur_fields = int(num_blur_fields)
    except ValueError:
        raise ValueError("The number of blur fields must be an integer.")
    
    # Check if the number of blur fields is greater than the length of the value
    if num_blur_fields > len(value):
        num_blur_fields = len(value)
    
    # Replace the last num_blur_fields characters with 'X'
    blurred_value = value[:-num_blur_fields] + 'X' * num_blur_fields
    return blurred_value

def generalize_diagnosis(diagnosis, level):
    if level == 1:
        return diagnosis[:-1]+("X")
    elif level == 2:
        return diagnosis[:-4]+("XX.X")
    else:
        raise Exception("For the MF generalize_diagnosis level should be either 1 or 2, and was "+str(level))
    
def add_relative_noise(value, relNoise, cast_to_int=True):
    assert(relNoise > 0.0 and relNoise < 1.0)
    if cast_to_int:
        return int(np.random.uniform(value-(value*relNoise),value+(value*relNoise)))
    else:
        return np.random.uniform(value-(value*relNoise),value+(value*relNoise))
    
def blur_phone(phone, nFields):
    phone_str = str(phone)
    if nFields >= len(phone_str):
        return "X"*len(phone_str)
    else:
        return phone_str[:-nFields]+("X"*nFields) 
    
def blur_phone2(phone):
    return f"{phone[:6]}-XXX-XXXX"
    
# TPCH

def noise_date(date_str, level, noise):
    date_format = "%Y-%m-%d"
    date = datetime.strptime(date_str, date_format)
    noise = abs(noise)
    if level == "DAYS":
        min_date = date - timedelta(days=noise)
        max_date = date + timedelta(days=noise)
    elif level == "WEEKS":
        min_date = date - timedelta(weeks=noise)
        max_date = date + timedelta(weeks=noise)
    elif level == "MONTHS":
        min_date = date - timedelta(days=noise * 30)  # Approximate months with 30 days
        max_date = date + timedelta(days=noise * 30)
    elif level == "YEARS":
        min_date = date - timedelta(days=noise * 365)  # Approximate years with 365 days
        max_date = date + timedelta(days=noise * 365)
    else:
        raise Exception(f"For the MF NOISE_DATE level should be either \"DAYS\", \"WEEKS\", \"MONTHS\" or \"YEARS\" and was {level}")

    start_timestamp = (min_date - datetime(1970, 1, 1)).total_seconds()
    end_timestamp = (max_date - datetime(1970, 1, 1)).total_seconds()

    random_timestamp = random.uniform(start_timestamp, end_timestamp)
    random_date = datetime.utcfromtimestamp(random_timestamp).date()

    return random_date.strftime(date_format)

def generalize_date(date_str, level):
    date_format = '%Y-%m-%d'
    try:
        # Ensure the input is a string
        if isinstance(date_str, date):
            date_str = date_str.strftime(date_format)
        parsed_date = datetime.strptime(date_str, date_format)
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return None

    if level == "MONTH":
        return datetime(parsed_date.year, parsed_date.month, 1).date().strftime(date_format)
    elif level == "YEAR":
        return datetime(parsed_date.year, 1, 1).date().strftime(date_format)
    else:
        raise Exception(f"For the MF GENERALIZE_DATE level should be either \"MONTH\" or \"YEAR\" and was {level}")

def generalize_number(value, divisor):
    factor = value / divisor
    return math.floor(factor) * divisor


def suppress(value):
    return "XXXXX"

def bucketize2(value, b_size, shift):
    l = (value - shift) // b_size
    h = l + 1.0
    return f"[{l * b_size + shift},{h * b_size + shift})"

def bucketize(value, b_size):
    value = float(value)
    l = value // b_size
    h = l + 1.0
    return f"[{l * b_size},{h * b_size})"

def suppress_phone(value):
    parts = value.split('-')
    
    # Mask each part with X's
    masked_parts = []
    for part in parts:
        masked_parts.append('X' * len(part))
    
    # Join the masked parts with hyphens
    masked_phone_number = '-'.join(masked_parts)
    
    return masked_phone_number


def mf_adapter(value, masking_function, mf_parameters):
    if value == "NaN":
        return np.nan
    
    if masking_function.__name__ == 'bucketize_age':
        if len(mf_parameters) != 1:
            raise Exception("For "+masking_function.__name__+" only the bucketsize is required.")
        b_size = float(mf_parameters[0])
        return bucketize_age(value, b_size)
    elif masking_function.__name__ == 'blur_zip':
        if len(mf_parameters) != 1:
            raise Exception("For "+masking_function.__name__+" only the number of blurred fields is required.")
        nFields = int(mf_parameters[0])
        return blur_zip(value, nFields)
    elif masking_function.__name__ == 'generalize_diagnosis':
        if len(mf_parameters) != 1:
            raise Exception("For "+masking_function.__name__+" only the generalization level is required.")
        level = int(mf_parameters[0])
        return generalize_diagnosis(value, level)
    elif masking_function.__name__ == 'add_relative_noise':
        if len(mf_parameters) == 1:
            relNoise = float(mf_parameters[0])
            return add_relative_noise(value, relNoise)
        elif len(mf_parameters) == 2:
            relNoise = float(mf_parameters[0])
            if type(mf_parameters[1]) == bool:
                cast_to_int = mf_parameters[1]
            else:
                cast_to_int = (mf_parameters[1] == 'True')
            return add_relative_noise(value, relNoise, cast_to_int)
        else:
            raise Exception("For "+masking_function.__name__+" only the relative noise is required and optionally a boolean if the result should be cast to int.")
    elif masking_function.__name__ == 'blur_phone':
        if len(mf_parameters) != 1:
            raise Exception("For "+masking_function.__name__+" only the number of blurred fields are required.")
        nFields = int(mf_parameters[0])
        return blur_phone(value, nFields)
    elif masking_function.__name__ == 'noise_date':
        if len(mf_parameters) != 2:
            raise Exception("For "+masking_function.__name__+" only the level and amount of noise are required.")
        noise = int(mf_parameters[1])
        return noise_date(value, mf_parameters[0], noise)
    elif masking_function.__name__ == 'generalize_date':
        if len(mf_parameters) != 1:
            raise Exception("For "+masking_function.__name__+" only the level is required.")
        return generalize_date(value, mf_parameters[0])
    elif masking_function.__name__ == 'suppress':
        if len(mf_parameters) != 0:
            raise Exception("For "+masking_function.__name__+" no extra parameters are required.")
        return suppress(value)
    elif masking_function.__name__ == 'bucketize2':
        if len(mf_parameters) != 2:
            raise Exception("For "+masking_function.__name__+" only the bucketsize and shift are required.")
        b_size = float(mf_parameters[0])
        shift = float(mf_parameters[1])
        return bucketize2(value, b_size, shift)
    elif masking_function.__name__ == 'bucketize':
        if len(mf_parameters) != 1:
            raise Exception("For "+masking_function.__name__+" only the bucketsize is required.")
        b_size = float(mf_parameters[0])
        return bucketize(value, b_size)
    elif masking_function.__name__ == 'generalize_number':
        if len(mf_parameters) != 1:
            raise Exception("For "+masking_function.__name__+" only the divisor is required.")
        divisor = float(mf_parameters[0])
        return generalize_number(value, divisor)
    elif masking_function.__name__ == 'blur_string':
        if len(mf_parameters) != 1:
            raise Exception("For "+masking_function.__name__+" only the divisor is required.")
        divisor = float(mf_parameters[0])
        return blur_string(value, divisor)
    elif masking_function.__name__ == 'suppress_phone':
        if len(mf_parameters) != 0:
            raise Exception("For "+masking_function.__name__+" no extra parameters are required.")
        return suppress_phone(value)
    else:
        raise Exception("Masking function "+masking_function.__name__+" does not exist.")
    

def mask(original, masking_function, masked_attr, *mf_parameters):
    masked = original.copy()
    masked[masked_attr] = masked[masked_attr].apply(lambda x: mf_adapter(x, masking_function, mf_parameters))
    return masked

# Inverse Masking Functions
def inverse_bucketize_age(bucketized_age: str) -> list:
    values = []
    low, high = [int(float(s)) for s in re.findall(r'\d+\.\d+|\d+', bucketized_age)]
    for j in range(low, high+1):
        values.append(str(j))
    return values

def inverse_blur_zip(blured_zip: str) -> list:
    assert(len(blured_zip) == 6)
    if blured_zip.isnumeric():
        return [blured_zip]
    
    cut = blured_zip.find("X")
    base_zip = blured_zip[:cut]
    assert(base_zip == "" or base_zip.isnumeric())  
    assert(blured_zip[cut:] == "X"*(6-cut))
    values = []
    for i in range(10**(6-cut)):
        tail = str(i)
        values.append(base_zip+((6-cut-len(tail))*"0")+tail)
    return values

def inverse_blur_string(blurred_value: str) -> list:
    # Ensure blurred_value is a string
    blurred_value = str(blurred_value)
    # Find the index of the first 'X'
    cut = blurred_value.find("X")
    if cut == -1:
        # If there are no 'X' characters, return the original string
        return [blurred_value]
    base_value = blurred_value[:cut]
    num_blur_fields = len(blurred_value) - cut
    # Verify the consistency of the input
    assert(blurred_value[cut:] == "X" * num_blur_fields)
    # Generate all possible combinations
    values = []
    for i in range(26**num_blur_fields):
        tail = ""
        temp = i
        for _ in range(num_blur_fields):
            tail = string.ascii_uppercase[temp % 26] + tail
            temp //= 26
        values.append(base_value + tail)
    return values

def inverse_generalize_diagnosis(generalized_diagnosis: str) -> list:
    head = generalized_diagnosis[0]
    possible_heads = string.ascii_uppercase.replace("U", "").replace("W", "").replace("X", "")
    assert head in possible_heads and len(generalized_diagnosis) == 5, f"Input with wrong formating. {generalized_diagnosis}"

    values = []
    if generalized_diagnosis[1:] == "XX.X":
        for i in np.arange(0.0, 100.0, 0.1):
            tail = str(i)
            if i < 10.0:
                values.append(head+"0"+tail[:3])
            else:
                values.append(head+tail[:4])
        return values
    elif generalized_diagnosis[3:] == ".X" and generalized_diagnosis[1:3].isnumeric():
        for i in range(10):
            values.append(generalized_diagnosis[:4]+str(i))
        return values
    else:
        raise Exception("Input with wrong formating.")

def inverse_blur_phone_OLD(blured_phone: str) -> list:
    if blured_phone.isnumeric():
        return [blured_phone]
    phone_len = len(blured_phone)
    cut = blured_phone.find("X")
    base_phone = blured_phone[:cut]
    assert(base_phone == "" or base_phone.isnumeric())  
    assert(blured_phone[cut:] == "X"*(phone_len-cut))
    values = []
    for i in range(10**(phone_len-cut)):
        tail = str(i)
        values.append(base_phone+((phone_len-cut-len(tail))*"0")+tail)
    return values

def inverse_blur_phone(blured_phone: str) -> list:
    phone_prefix = blured_phone[:3]
    values = []
    for i in range(0, 10000000, 1):
        rest = f"{i:07d}"
        values.append(f"{phone_prefix}{rest[:3]}-{rest[3:]}")
    return values

def inverse_generalize_date(date, level) -> list:
    str_input = False
    if isinstance(date, str):
        str_input = True
        date_format = "%Y-%m-%d"
        date = datetime.strptime(date, date_format)
    values = []
    if level == "MONTH":
        current_date = datetime(date.year, date.month, 1).date()
        _, last_day = calendar.monthrange(date.year, date.month)
        end_date = datetime(date.year, date.month, last_day).date()
    elif level == "YEAR":
        current_date = datetime(date.year, 1, 1).date()
        end_date = datetime(date.year, 12, 31).date()
    else:
        raise Exception(f"For the inverse MF INVERSE_GENERALIZE_DATE level should be either \"MONTH\" or \"YEAR\" and was {level}")

    while current_date <= end_date:
        if str_input:
            values.append(current_date.strftime(date_format))
        else:
            values.append(pd.Timestamp(current_date))
        current_date += timedelta(days=1)
    
    return values

def inverse_generalize_date_SO(level):
    def partially_applied(date_str):
        return inverse_generalize_date(date_str, level)
    return partially_applied
    

def inverse_bucketize(value: str, granularity: float, format: str = "{:.1f}") -> list:
    values = []
    low, high = [float(s) for s in re.findall(r'([-+]?\d+\.\d+|[-+]?\d+)', value)]
    if (value[-1] == ")"):
        arr = np.arange(low, high, granularity)
        arr = arr[~np.isclose(arr, high)]
        for j in arr:
            values.append(format.format(j))
    elif (value[-1] == "]"):
        arr = np.arange(low, high+granularity, granularity)
        arr = arr[~np.isclose(arr, high+granularity)]
        for j in arr:
            values.append(format.format(j))
    return values

def inverse_bucketize_SO(granularity, format: str = "{:.1f}"):
    def partially_applied(value):
        return inverse_bucketize(value, granularity, format)
    return partially_applied

def inverse_bucketize2(value: str, precision: int = 0) -> list:
    granularity = 10**(-precision)
    values = []
    low, high = [float(s) for s in re.findall(r'([-+]?\d+\.\d+|[-+]?\d+)', value)]
    if (value[-1] == ")"):
        arr = np.arange(low, high, granularity)
        arr = arr[~np.isclose(arr, high)]
        for j in arr:
            values.append(np.round(j, precision))
    elif (value[-1] == "]"):
        arr = np.arange(low, high+granularity, granularity)
        arr = arr[~np.isclose(arr, high+granularity)]
        for j in arr:
            values.append(np.round(j, precision))
    return values

def inverse_bucketize_SO2(precision: int = 0):
    def partially_applied(value):
        return inverse_bucketize2(value, precision)
    return partially_applied

def inverse_suppress_segment(value: str) -> list:
    return ["AUTOMOBILE", "BUILDING  ", "FURNITURE ", "HOUSEHOLD ", "MACHINERY "]

def inverse_suppress_shippriority(value: str) -> list:
    return [1, 2, 3, 4, 5]

def inverse_generalize_number(value, divisor, granularity: float, format: str = "{:.1f}"):
    value = float(value)
    values = []
    factor = value / divisor
    low = value
    high = divisor * (factor + 1)

    arr = np.arange(low, high, granularity)
    arr = arr[~np.isclose(arr, high)]
    for j in arr:
        values.append(format.format(j))
    return values

def inverse_generalize_number_SO(divisor, granularity: float = 0.1, format: str = "{:.1f}"):
    def partially_applied(value):
        return inverse_generalize_number(value, divisor, granularity, format)
    return partially_applied

def inverse_suppress_phone(masked_phone):
    assert len(masked_phone) == 15 and all(c in "X-0123456789" for c in masked_phone), f"Input with wrong formatting: {masked_phone}"
    
    possible_digits = string.digits
    values = []

    def generate_combinations(masked, index=0, current=''):
        if index == len(masked):
            values.append(current)
            return
        if masked[index] == 'X':
            for digit in possible_digits:
                generate_combinations(masked, index + 1, current + digit)
        else:
            generate_combinations(masked, index + 1, current + masked[index])

    generate_combinations(masked_phone)
    return values

def inverse_noise_date(input_date_str, level, noise):
    date_format = "%Y-%m-%d"
    input_date = datetime.strptime(input_date_str, date_format)
    noise = abs(noise)
    
    if level == "DAYS":  # DAYS
        min_date = input_date - timedelta(days=noise)
        max_date = input_date + timedelta(days=noise)
    elif level == "WEEKS":  # WEEKS
        min_date = input_date - timedelta(weeks=noise)
        max_date = input_date + timedelta(weeks=noise)
    elif level == "MONTHS":  # MONTHS
        min_date = input_date - timedelta(days=noise * 30)  # Approximate months with 30 days
        max_date = input_date + timedelta(days=noise * 30)
    elif level == "YEARS":  # YEARS
        min_date = input_date - timedelta(days=noise * 365)  # Approximate years with 365 days
        max_date = input_date + timedelta(days=noise * 365)
    else:
        raise Exception(f"For the MF NOISE_DATE, level should be either 'DAYS', 'WEEKS', 'MONTHS', or 'YEARS' and was {level}")

    possible_dates = []
    current_date = min_date
    while current_date <= max_date:
        possible_dates.append(current_date.strftime(date_format))
        current_date += timedelta(days=1)
    
    return possible_dates

def inverse_noise_date_SO(level, noise):
    def partially_applied(value):
        return inverse_noise_date(value, level, noise)
    return partially_applied

def plot_probabilities(dist):
    dist_copy = dist.copy().sort_index()
    # labels = dist.index.to_series().apply(lambda x: '{0}-{1}'.format(*x))
    # labels = dist.index

    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(range(len(dist_copy.values)),dist_copy.values)
    plt.show()


diagnosis_alphabet = []
letters = string.ascii_uppercase.replace("U", "").replace("W", "").replace("X", "")
for letter in letters:
    for number in np.arange(0.0, 100.0, 0.1):
        number = np.trunc(number*10)/(10)
        if number < 10.0:
            diagnosis_alphabet.append(letter+"0"+str(number)) 
        else:
            diagnosis_alphabet.append(letter+str(number))

c_acctbal_alphabet = []
for number in np.arange(0.00, 100.00, 0.01):
        # Format the number to two decimal places
        formatted_number = f"{number:.2f}"
        # Combine the letter with the formatted number
        c_acctbal_alphabet.append(f"{formatted_number}")

class Alphabet:
    def __init__(self):
        self.alphabet = {}

    def index_of(self, value):
        return self.alphabet.get(value, -1)

    def bin_n_distinct(self, lower_bound, upper_bound):
        low = self.index_of(lower_bound)
        up = self.index_of(upper_bound)
        if low >= 0 and up >= 0 and up > low:
            return up - low
        if up == low:
            return 1
        return -1

class DateAlphabet(Alphabet):
    def index_of(self, value):
        try:
            date = datetime.strptime(value, "%Y-%m-%d")
            return date.timestamp()
        except ValueError:
            return -1

    def bin_n_distinct(self, lower_bound, upper_bound):
        try:
            parsed_low = datetime.strptime(lower_bound, "%Y-%m-%d")
            parsed_upper = datetime.strptime(upper_bound, "%Y-%m-%d")
            return (parsed_upper - parsed_low).days
        except ValueError:
            return -1
    

class FloatAlphabet(Alphabet):
    def __init__(self, lower_bound=sys.float_info.min, upper_bound=sys.float_info.max, decimal_places = 1):
        super().__init__()
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.decimal_places = decimal_places

    def index_of(self, value):
        if isinstance(value, str):
            value = float(value)
        if not isinstance(value, (int, float)):
            return -1
        if value > self.upper_bound or value < self.lower_bound:
            return -1
        return round(value - self.lower_bound, self.decimal_places) // (1/(10*self.decimal_places))

    def bin_n_distinct(self, lower_bound, upper_bound):
        lower_bound = float(lower_bound)
        upper_bound = float(upper_bound)
        if lower_bound >= upper_bound:
            return 0
        return round(upper_bound - lower_bound, self.decimal_places) // (1/(10*self.decimal_places))

