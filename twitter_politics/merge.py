import sys
import csv
import os
import pandas as pd

phi_dict = {}
phi_data = pd.read_csv("data/phi-2018.csv")
for index, line in phi_data.iterrows():
	phi_dict[line["merge"]] = line["phi"]

merge_data = pd.read_csv("merged_list.csv")
for index, line in merge_data.iterrows():
	user = line["account_handle"].lower() 
	if user in phi_dict:
		line["phi"] = phi_dict[user]
		merge_data.loc[index] = line

influ = pd.read_csv("twitter_influencers_first.csv")
for index, line in influ.iterrows():
	user = line["account_handle"].lower() 
	if user in phi_dict:
		line["account_handle"] = ""
		influ.loc[index] = line

influ.to_csv("new_influencers.csv", index = False, header = True)
merge_data.to_csv("new_merged_list.csv", index = False, header = True)





