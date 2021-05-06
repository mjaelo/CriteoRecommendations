import json
import pickle
import matplotlib.pyplot as plt

import pandas as pd

from optimizer import optimizer

"""
core najlepiej ajk dac jakas agreacje produktow. Produkty sie powtarzaja
per day profit factor to zliczyc profity dla jednego produktu
również npm zakladamy (nie wyliczmay) 10% i cligratio wyliczmy, by potimizer rozroznił balans drogich zadkich produktów i tanich czestych.
optimizer zwraca liste nie sprzedawanych produktow do symulatora na jutro
w per data mozna odfiltrowanie produktow zwrocone od optimizera
sprawdzenie listy od optimizera, jak działa? jest w fimlmiku niby.
"""

"""
Etap 1
1. Dzielimy dane z csv po id partnera i zapisujemy w osobnych plikach
2. Wyliczmy sredni koszt klikniecia dla całego zbioru, ze wszystkich dni (w profilu partnera).
zakładamy, że kazde klikniecie kosztuje nas tyle samo. avg_click_cost = profit ze wszytskich dni / liczba klikniec ze wszystkich dni
4. wyznaczamy NPM, CTR niekoniecznie (to w prezentacji opisane)
5. wysyłamy dane do Optimizera,
3. wyliczamy rentowność na dany dzień
Etap 2
6. Optymizer zwraca nam listę produktów, których nie ma być w ofercie dla następnego dnia (w etap 1 random)
i zwracamy do symulatora liste bez tych produktów do polecenia klientowi
7. Jakoś sprawdzamy tą listę? Optymalizujemy na podstawie poprzednich dni, tak aby rentowność była większa. wykres rentowności zrobić?
"""

# w S2 chodzi o obliczenie całkowitych zysków, czyli trzeba policzyć koszt kliknięcia,  zysk - koszta utrzymania reklam
# w s2 trzeba obliczyc
# NPM-zyski końcowe,  CTR - czestoltliwosc klikania,  rentownosc- oplacalnosc, avg_click_cost, NPG - net profit gain
# sredni koszt klikniecia= tworze df ze wszystkich par
# caly przychod z urzytkownika,

# liczy sie raz:
# click_cost = partner income/num_of_events //koszt klikniecia
# partern profit= partner income- avg_click_cost*numOfEvrents

# partner profit = codziennie sie liczy
# npm = 10% zawssze?
# sprzedaz z dnia- avg_clickcost
# profit gain to sustain profit bez optim - sustain profitz optim. w najlepszym przypadku ujemnym
# partner per day= income+10%income

# podzielic na dni i dla kazdego odpalic optim. pierwszego dnia nic, bo nie usuwa prod
# obliczamy profit
# przychod z dnia - (suma klikniec?)
# kazdy wiersz to klikniecie


# C0F515F0A2D0A5D9F854008BA76EB5372= 235
# 04A66CE7327C6E21493DA6F3B9AACC75 = 6
exluded_yesterday = 0
yesterday_json = [[], [], []]  # [excluded,seen,actually_ex]


class simulation_executor:
    def execute_simulation(self):
        # wywolanie kilku wybranych partnerow
        ids = [235, 6]
        partner_list = []
        print('executing...')
        for id in ids:
            partner = partner_profile(id)
            print("avg click cost for partner", str(id), "=", partner.avg_click)
            partner_list.append(partner)
        sim_core = simulation_core()
        sim_core.next_day(partner_list)


# do pobrania csv partnerow i obliczenia ich avg_click_cost
class partner_profile:
    def __init__(self, id_):
        self.partnerId = id_
        self.read_partners_profiles()

    partnerId = 0
    avg_click = 0
    df = 0

    def read_partners_profiles(self):
        self.df = pd.read_csv('partners/partner' + str(self.partnerId) + '.csv')
        profit = self.df['SalesAmountInEuro'].sum()
        click_times = len(self.df)
        self.avg_click = profit * 0.12 / click_times


class simulation_core:
    product_list = []
    data_set = {}
    labelEncoders = pickle.load(open("dane/lablencoder.pickle", "rb"))

    def __init__(self):
        self.data_set["days"] = []

    def make_json(self, pid, day, excluded, seen):
        pid = self.labelEncoders['partner_id'].inverse_transform(pid)
        if excluded != []:
            excluded = self.labelEncoders['product_id'].inverse_transform(excluded)
        seen = self.labelEncoders['product_id'].inverse_transform(seen)
        actually = list(set(excluded).intersection(seen))
        # opuznienie 1 dnia
        global yesterday_json
        self.data_set["days"].append(
            {
                "day": str(day),
                "productsToExclude": list(map(str, yesterday_json[0])),
                "productsSeenSoFar": list(map(str, yesterday_json[1])),
                "productsActuallyExcluded": list(map(str, yesterday_json[2]))
            }
        ),
        with open('logs/exclusion_' + str(pid) + '.json', 'w') as outfile:
            json.dump(self.data_set, outfile)
        yesterday_json = [excluded, seen, actually]

    def next_day(self, partner_array):
        for partner in partner_array:
            global X_days, Y_profit
            global yesterday_json
            X_days = []
            Y_profit = []
            yesterday_json = [[], [],[]]
            self.product_list = []
            print("\n\n")
            days_all = (partner.df['click_timestamp'].astype('datetime64[ns]')).dt.date
            days = days_all.unique()
            first_day = days[0]
            for day in days:
                # dla kazdego partnera, tworze pierwszy last day (partner.yesterday) ze wszystkich produktów
                # potem dla kazdego dnia w perpartnersim tworze dane do optimizera
                day_data = partner.df.loc[days_all == day]  # dane z danego dnia
                # lista produktów jest aktualizowana kazdego dnia
                prods_today = list(day_data['product_id'].unique())
                self.product_list = list(set(self.product_list + prods_today))
                if day == first_day:
                    global exluded_yesterday  # wykluczone dane z zeszlego dnia
                    exluded_yesterday = []
                    # empty file
                    self.data_set["days"].clear(),
                    with open('logs/exclusion_' + str(partner.partnerId) + '.json', 'w') as outfile:
                        json.dump(self.data_set, outfile)
                per_partner_simulation.next_day(self, day_data, day, partner,prods_today)
            pid = self.labelEncoders['partner_id'].inverse_transform(partner.partnerId)
            profit_graph(pid)


Y_profit = []
X_days = []


def profit_graph(pid):
    global X_days, Y_profit
    days = range(len(X_days))
    plt.plot(days, Y_profit)
    plt.ylabel("Net Profit Gain")
    plt.xlabel("Days")
    plt.title("pid = " + str(pid))
    plt.show()


class per_partner_simulation:
    def next_day(self, today, day, partner,prods_today):
        # Obliczanie Net Profit Gain
        profit = today['SalesAmountInEuro'].sum()
        click_times = len(today)
        NPG = click_times * partner.avg_click - profit * 0.22
        
        global X_days, Y_profit
        X_days.append(day)
        Y_profit.append(NPG)

        #wyznaczanie listy polecanych produktow
        #excluded = optimizer._get_excluded_products_pseudorandomly(self)
        excluded=optimizer.next_day(self,NPG,prods_today)
        print("on "+str(day)+" excluded "+str(len(excluded))+" products")
        global exluded_yesterday
        exluded_yesterday = excluded
        pid = today['partner_id'].array[0]
        self.make_json(pid, day, excluded, self.product_list)


if __name__ == '__main__':
    simulation_executor().execute_simulation()
