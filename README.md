# Card number cracker

A friend got an email with their credit card's first 8 digits written in 1 place and the last 4 digits at another.

Attached to the email, there was a password protected pdf. The password being the card number itself.
I am trying to time how long it takes to crack someone's credit card number if I got my hands on one of these emails and attached pdf.


I've created a PDF which is encrypted with a valid card number `5678567856785678` and uploaded it with the associated code for testing.

## Requirements

```
pip install PyPDF2
```

## Usage
```
time python crack.py
```

## Results

On a 2.7 GHz Intel Core i5 (on the 13 inch MBP), it takes roughly 15 seconds :-/
