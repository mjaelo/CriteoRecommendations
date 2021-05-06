import pickle
import random
import pandas as pd


def verify(criteo_df):
    # do weryfikacji 1 kroku:
    labelEncoders = pickle.load(open("dane/lablencoder.pickle", "rb"))
    hashed_partners = labelEncoders['partner_id'].inverse_transform(criteo_df['partner_id'])
    hashed_id = ["C0F515F0A2D0A5D9F854008BA76EB537", "E3DDEB04F8AFF944B11943BB57D2F620",
                 "E68029E9BCE099A60571AF757CBB6A08"]
    unhashed_id = labelEncoders['partner_id'].transform(hashed_id)
    for i in range(3):
        partner = pd.read_csv('partners/partner' + str(unhashed_id[i]) + '.csv', index_col=0)
        print("test_params for partner_id " + hashed_id[i] + " : ", partner.shape[0])

def who_am_i(hashed_id):
    labelEncoders = pickle.load(open("dane/lablencoder.pickle", "rb"))
    unhashed_id = labelEncoders['partner_id'].transform(hashed_id)
    print(unhashed_id)

def divideForPartners(criteo_df):
    partnersid = pd.unique(criteo_df["partner_id"])
    for id in partnersid:
        sorted = criteo_df.loc[criteo_df['partner_id'] == id].sort_values(by=['click_timestamp'])
        sorted.to_csv("partners/partner" + str(id) + ".csv", index=False)

def createData(criteo_df):
    product_list=criteo_df['product_id'].unique()
    pd.DataFrame(product_list).to_csv("product_list.csv", index=False)

# C0F515F0A2D0A5D9F854008BA76EB5372= 235
# 04A66CE7327C6E21493DA6F3B9AACC75 = 6
if __name__ == '__main__':
    who_am_i('04A66CE7327C6E21493DA6F3B9AACC75')
    """
    criteo_df = pd.read_csv('dane/criteoCategorized.csv', index_col=0,nrows=100000)
    column_names = criteo_df.columns
    # product title- product category- zashashowane nazwy przez google
    #print(column_names)
    #divideForPartners(criteo_df)
    createData(criteo_df)
    #verify(criteo_df)"""
