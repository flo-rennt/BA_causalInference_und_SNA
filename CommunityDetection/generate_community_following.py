import pandas as pd
import random

#file einleisen
Final_User_Data = pd.read_csv('Final_User_Data.csv')

def generate_following_with_community(users, communities, user_community_map):
    followees = []
    user_community = user_community_map[users]
    
    # Innerhalb der Community mehr kanten, zwischen Communites weniger
    innerhalb_community_users = [user for user in unique_users if user_community_map[user] == user_community]
    zwischen_community_users = [user for user in unique_users if user_community_map[user] != user_community]
    
    # Zufallszahl für innerhalb der Community (Range in höherem Bereich)
    followees += random.sample(innerhalb_community_users, random.randint(3, 5))
    
    # Zufallszahl für zwischen Communities (Range niedriger)
    followees += random.sample(zwischen_community_users, random.randint(0, 2))
    
    return list(set(followees))

# Filtern, sodass doppelte user entfallen
unique_users = Final_User_Data['username'].unique()

# mapping zwischen Communities und Usern
user_community_map = dict(zip(Final_User_Data['username'], Final_User_Data['community']))

# Following mit Community Bedingung
Final_User_Data['following'] = Final_User_Data['username'].apply(
    lambda x: generate_following_with_community(x, Final_User_Data['community'], user_community_map)
)

# Save the data
Final_User_Data.to_csv('updated_final_user_data.csv', index=False)
