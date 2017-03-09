# pip install PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter


# Luhn's algo verification was stolen from
# https://github.com/garwoodpr/LuhnAlgorithmProof/blob/4253637/luhn/luhn.py#L11-L71
def do_luhn(cardNumber):
    cardLength = str(cardNumber)
    try:
        cardNumbers = int(cardNumber)
    except ValueError:
        return(False)
    cardLength = len(cardLength)
    everyOtherFromFarRightFor16 = [-2, -4, -6, -8, -10, -12, -14, -16]
    everyOtherFromFarRightFor15 = [-2, -4, -6, -8, -10, -12, -14]
    everyOddFromFarRightButOneFor15 = [-3, -5, -7, -9, -11, -13, -15]
    everyOddFromFarRightButOneFor14 = [-3, -5, -7, -9, -11, -13]
    doubleList = []
    doubleSet = []
    addUpDoubles = 0
    addUpOthers = 0
    # setup the counting variables for appropriate card lengths
    if (cardLength == 16):
        doubleList = everyOtherFromFarRightFor16
        addUpTheOddDigits = everyOddFromFarRightButOneFor15
    elif (cardLength == 15):
        doubleList = everyOtherFromFarRightFor15
        addUpTheOddDigits = everyOddFromFarRightButOneFor15
    elif (cardLength == 14):
        doubleList = everyOtherFromFarRightFor15
        addUpTheOddDigits = everyOddFromFarRightButOneFor14
    else:
        return(False)
    # select the items for doubling
    for each in doubleList:
        doubleThis = cardNumber[each]
        doubleThis = int(doubleThis) * 2
        nowDoubled = str(doubleThis)
        # add single digit items to the doubleSet
        if (len(nowDoubled) == 1):
            nowDoubled = nowDoubled
            doubleSet.append(nowDoubled)
        else:
            # add each digit of 2-digit items to each other
            # and then add each item to the the doubleSet
            db1, db2 = nowDoubled[0], nowDoubled[1]
            db1, db2 = int(db1), int(db2)
            dbladd = db1 + db2
            doubleSet.append(dbladd)
    # add all items in the doubleSet together
    for each in doubleSet:
        addUpDoubles += int(each)
    # add together all items not previously doubled
    for each in addUpTheOddDigits:
        addOther = cardNumber[each]
        otherToAdd = int(addOther)
        addUpOthers += otherToAdd
    # add all the summed up additions together
    totalSum = int(addUpDoubles) + int(addUpOthers)
    # multiply totalSum by 9, then Modulus '%' that number by 10
    totalSumTimesNine = (totalSum * 9)
    modTheTotalSum = (totalSumTimesNine % 10)
    # compare modTheTotalSum to the right-most digit of cardNumber
    if (str(modTheTotalSum) == cardNumber[-1]):
        return(True)
    else:
        return(False)



def decrypt_pdf(input_path, output_path, passwords):
    with open(input_path, 'rb') as input_file, open(output_path, 'wb') as output_file:
        reader = PdfFileReader(input_file)
        for password in passwords:
            try:
                reader.decrypt(password)
                reader.getNumPages()
            except Exception:
                continue
            break

        writer = PdfFileWriter()

        for i in range(reader.getNumPages()):
            writer.addPage(reader.getPage(i))

        writer.write(output_file)
        return password


def gen_card_numbers(first_8, last_4):
    base_format = '{}{}{}'.format(first_8, '{}', last_4)
    cards = []
    for i in xrange(0, 10000):
        tmp_c = base_format.format(str(i).zfill(4))
        if do_luhn(tmp_c):
            cards.append(tmp_c)
    return cards


if __name__ == '__main__':
    card_numbers = gen_card_numbers(first_8='56785678', last_4='5678')
    password = decrypt_pdf('encrypted.pdf', 'decrypted.pdf', card_numbers)

    print "The card number is '{}'".format(password)
