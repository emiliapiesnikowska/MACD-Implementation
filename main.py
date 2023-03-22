from matplotlib import pyplot
from datetime import datetime

import pandas


def OdczytDanych():
    df = pandas.read_csv(
        "./dane/frank_szwajcarski.csv")
    dane = [tuple(x) for x in df.values]
    dane.reverse()

    time1 = [(i[1]) for i in dane]
    daty = [datetime.strptime(x, '%Y-%m-%d') for x in time1]

    wartosci_waluty = [float(it[2]) for it in dane]

    return daty,wartosci_waluty

def wykresMACD(macd, daty,signal):


    pyplot.plot(daty[35::], macd[35::], label="macd", color='red')
    pyplot.plot(daty[35::], signal, label="signal", color='blue')
    pyplot.legend()
    pyplot.ylabel('Wartość składowych')
    pyplot.xlabel('Data')
    pyplot.title('Wskaźnik MACD')
    pyplot.show()






def EMA(n, dane, day):

    #wzor (1) z instrukcji
    #           (p[0]+ (1 - alpha)p[1] + (1 - alpha)^(2)p[2]+...+(1 - alpha)^(n)p[n])
    #  EMA(n) = --------------------------------------------------------------------
    #                 (1 + (1 - alpha) + (1 - alpha)^(2) +...+(1-alpha)^(n)
        alpha = 2 / (n + 1)
        p = dane[day - n: day+1:]
        p.reverse()
        dzielna = float(0.0)
        dzielnik = float(0.0)
        a = 1
        for i in range(n+1):

            dzielna += a * p[i]
            dzielnik += a
            a *= (1-alpha)
        wynik = dzielna/dzielnik
        return wynik


def MACD(wartosci_waluty, macd):
    #MACD = EMA[12] - EMA[26]
    for i in range(len(wartosci_waluty)):
        if i >= 26:
            macd[i] = EMA(12, wartosci_waluty, i) - EMA(26, wartosci_waluty, i)


def SIGNAL(macd):
    #wykładnicza średnia krocząca o okresie 9, policzona z MACD
    signal = []
    for i in range(35, len(macd)):
        signal.append(EMA(9, macd, i))
    return signal







def WykresSymulacja( time, macd, exchange_rate, poczatek, koniec, name,signal):

        pyplot.plot(time[poczatek:koniec], macd[poczatek:koniec], color="blue", label="macd")
        pyplot.plot(time[poczatek:koniec], signal[poczatek:koniec], color="red", label="signal")
        pyplot.legend()
        pyplot.title("Składowe wskaźnika MACD")
        pyplot.ylabel("Wartość składowej ")
        pyplot.xlabel("Data")
        pyplot.show()


def Symulacja(wartosci_waluty, KupLubSprzedaj, Kapital, poczatek, koniec, macd):
        #tworze zmienną Kapital2, która jest potrzebna do określenia czy można ponownie
        Kapital2 = 0.0
        #podjecie decyzji o sprzedazy/kupnie
        for i in range(poczatek, koniec):
            # MACD przecina SIGNAL od góry - sprzedaj
            if macd[i - 1] > signal[i - 1] and macd[i] < signal[i]:
                KupLubSprzedaj[i] = -1

                if Kapital2 != 0:
                    Kapital = Kapital2 * wartosci_waluty[i]
                    Kapital2 = 0
                print("Sprzedano " + daty[i].strftime("%m/%d/%Y"))

            # MACD przecina SIGNAL od dołu - kup
            elif macd[i - 1] < signal[i - 1] and macd[i] > signal[i]:
                KupLubSprzedaj[i] = 1
                if Kapital != 0:
                    Kapital2 = Kapital / wartosci_waluty[i]
                    Kapital = 0
                print("Kupiono " + daty[i].strftime("%m/%d/%Y"))


        #jesli ostatnią decyzja było kupno to sprzedaje akcje w ostatnim dniu przedzialu
        #w przeciwnym wypadku wartość końcowa to nasze zarobki, na koniec nie wykonujemy żadnej akcji
        if Kapital == 0:
            print(Kapital2 * wartosci_waluty[koniec])
        else:
            print(Kapital)



if __name__ == '__main__':

    #wartosci_waluty to zmienna oznaczająca wartość waluty w aktualnym dniu
    daty, wartosci_waluty = OdczytDanych()
    macd = []

    for i in range(0, len(daty)):
        macd.append(0.0)

    MACD(wartosci_waluty, macd)
    signal = SIGNAL(macd)
    wykresMACD(macd, daty,signal)



    KupLubSprzedaj=[]
    for i in range(0, len(macd)):
        KupLubSprzedaj.append(0)

    Kapital = 1000.0

    poczatek = 1
    koniec = 200
    Symulacja(wartosci_waluty[35::], KupLubSprzedaj , Kapital,poczatek, koniec,macd)

    WykresSymulacja(daty[35::], macd, wartosci_waluty[35::],poczatek , koniec, "dolar", signal)

