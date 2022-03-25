import faker 
import pandas as pd
import numpy as np
from random import randrange
import datetime as datetime
from datetime import timedelta


Faker = faker.Factory().create
fake = Faker()
# nr of users should be 100k 
n = 100000

# Create a fake dataset for 100k users with name, state, birth date and device_id
faker_data = pd.DataFrame([[fake.name(), 
                           fake.state(),
                           fake.date_of_birth(minimum_age =18, maximum_age = 65),
                           fake.msisdn()
                           ] 
            for _ in range(n)],
            columns=['user_name', 'user_state' , 'user_birth_date', 'deviceID' ])
# create a column user_id with ascending values
faker_data['user_id'] = range(1, 1+len(faker_data))


print(faker_data.head(30))
print(faker_data.dtypes)

# convert the data types to the right types
faker_data = faker_data.convert_dtypes()
# fix the user_id type
faker_data = faker_data.astype(
    {'user_id': 'int64'
     }
)

# change the birth date to datetime
faker_data['user_birth_date'] = pd.to_datetime(
    faker_data['user_birth_date'])
print(faker_data.dtypes)

# read the businesses dataset (10k rows)
businesses = pd.read_json("./data/sf_businesses.json", lines=True)
print(businesses)
print(businesses.dtypes)

# create (10.000 * 100) businesses --> 1M rows by concatinating the same dataset multiple times
df_repeated = pd.concat([businesses]*100, ignore_index=True)
print(df_repeated.shape)

# randint needs to be the same as the amount of users --> 100k
df_repeated['user_id'] = np.random.randint(1,100000, df_repeated.shape[0])
print(df_repeated.dtypes)
print(df_repeated)

# Join the two dataframes of the faked users to the one of the businesses
df_repeated2 = df_repeated.merge(faker_data, on = "user_id", how='left')
print(df_repeated2)
print(df_repeated2.dtypes)

# function to create a random date between three days using datetime module 
def random_date():
    """
    This function will return a random datetime between two datetime 
    objects.
    """

    start = datetime.datetime.strptime('2022-01-01 12:00 AM', '%Y-%m-%d %I:%M %p')
    end = datetime.datetime.strptime('2022-01-03 11:55 PM', '%Y-%m-%d %I:%M %p')
 
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

# create a new column using a lambda
df_repeated2['scan_timestamp'] = df_repeated2['business_name'].apply(lambda s: random_date())
print(df_repeated2)

# drop the user_id. We don't need it anymore
df_repeated2 = df_repeated2.drop('user_id', axis=1)

print(df_repeated2.dtypes)

# print a line of the dataframe
print(df_repeated2.head(1).to_json())

# write the result into a zipped parquet file
df_repeated2.to_parquet('./data/sf_appscans.parquet.gzip', compression='gzip')

# JSON export if we need it
#df_repeated2.to_json('./data/sf_fakedataset.json', lines=True, orient='records')

