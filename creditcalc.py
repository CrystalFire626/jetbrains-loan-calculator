import math
import argparse
import sys
parser = argparse.ArgumentParser()

parser.add_argument("--type", type=str)
parser.add_argument("--payment", type=int)
parser.add_argument("--principal", type=int)
parser.add_argument("--periods", type=int)
parser.add_argument("--interest", type=float)

args = parser.parse_args()

parameters = [args.type, args.payment, args.principal, args.periods, args.interest]
negative_numbers = []

for i in parameters:
    if isinstance(i, (int, float)):
        if i < 0:
            negative_numbers.append(i)

if args.type not in ["annuity", "diff"]:
    print("Incorrect parameters")
    sys.exit()
if args.type == "diff" and args.payment is not None:
    print("Incorrect parameters")
    sys.exit()
if sum(x is not None for x in parameters) < 4:
    print("Incorrect parameters")
    sys.exit()
if args.interest is None:
    print("Incorrect parameters")
    sys.exit()
if negative_numbers:
    print("Incorrect parameters")
    sys.exit()

monthly_interest = args.interest / 1200

if args.type == "annuity" and args.periods is None:
    num_of_months = math.ceil(math.log(args.payment / (args.payment - monthly_interest * args.principal), 1 + monthly_interest))
    overpayment = (num_of_months * args.payment) - args.principal
    years = num_of_months // 12
    years_ending = "year" if years == 1 else "years"
    months = num_of_months % 12
    months_ending = "month" if months == 1 else "months"
    if years == 0:
        print(f"It will take {months} {months_ending} to repay this loan!")
    else:
        print(f"It will take {years} {years_ending} and {months} {months_ending} to repay this loan!" if months != 0 else f"It will take {years} {years_ending} to repay this loan!")
    print(f"Overpayment = {math.ceil(overpayment)}")

if args.type == "annuity" and args.principal is None:
    loan_principal = math.ceil(args.payment / ((monthly_interest * math.pow(1 + monthly_interest, args.periods)) / (math.pow(1 + monthly_interest, args.periods) - 1)))
    overpayment = args.payment * args.periods - loan_principal
    print(f"Your loan principal = {loan_principal}!")
    print(f"Overpayment = {math.ceil(overpayment)}")

if args.type == "annuity" and args.payment is None:
    annuity_payment = math.ceil(args.principal * (monthly_interest * math.pow(1 + monthly_interest, args.periods)) / (math.pow(1 + monthly_interest, args.periods) - 1))
    overpayment = annuity_payment * args.periods - args.principal
    print(f"Your annuity payment = {annuity_payment}!")
    print(f"Overpayment = {math.ceil(overpayment)}")

if args.type == "diff":
    month = 1
    sum_of_payments = 0
    while month <= args.periods:
        payment = math.ceil(args.principal / args.periods + monthly_interest * (args.principal - (args.principal * (month - 1)) / args.periods))
        print(f"Month {month}: payment is {payment}")
        month += 1
        sum_of_payments += payment
    overpayment = sum_of_payments - args.principal
    print()
    print(f"Overpayment = {math.ceil(overpayment)}")
