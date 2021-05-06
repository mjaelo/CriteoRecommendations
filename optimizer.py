import json
import random

product_rating = []


class optimizer:
    def __init__(self):
        print('\noptimizer init')

    def next_day(self, NPG, prods_today):
        rating_limit = 100
        global product_rating
        # oproznienie listy ocen, jesli pierwszy dzien, czyli zmiana klienta
        if len(self.data_set['days']) == 0:
            product_rating = []
        else:
            avg = sum(product_rating) / len(product_rating)
            if avg < -rating_limit / 2 or avg > rating_limit / 2:
                # jesli wiekszosc wynikow jest za bardzo dodatnia/ujemna, wyrównuję wynik
                for i in range(len(product_rating)):
                    product_rating[i] -= avg / 2
        all_products_so_far = self.product_list
        excluded = []
        # tworze ocene skutecznosci produktu, bazujac, czy npg w dniu kiedy byl reklamowany byl generalnie pozytywny
        # oznacza to, ze zacznie zwracac dobre wyniki dopiero po jakims czasie
        rating = NPG
        for i in range(len(all_products_so_far)):
            if i + 1 > len(product_rating):
                product_rating.append(rating)
            else:
                this_rating = product_rating[i]
                cond = any(ele == all_products_so_far[i] for ele in prods_today)
                # sprawdzanie, czy dzis pojawil sie ten produkt
                if cond:
                    this_rating += rating
                if this_rating < 0:
                    excluded.append(all_products_so_far[i])
                    if this_rating < -rating_limit:
                        this_rating = this_rating + this_rating * -0.50
                    this_rating = this_rating + this_rating * -0.10
                    # zwiekszam ocene a kazdym razem, gdy zostaly niewybrane, by dac im druga szanse w przyszlosci
                else:
                    if this_rating > rating_limit:
                        this_rating = this_rating + this_rating * -0.50
                product_rating[i] = this_rating
        return excluded

    def _get_excluded_products_pseudorandomly(self):
        dummy_list_of_potentially_excluded_products = self.product_list
        dummy_list_of_potentially_excluded_products.sort()
        how_many_ratios = 20
        dummy_how_many_products = round(len(dummy_list_of_potentially_excluded_products) / how_many_ratios)
        random.seed(12)
        excluded_products = random.sample(dummy_list_of_potentially_excluded_products, dummy_how_many_products)
        return excluded_products
