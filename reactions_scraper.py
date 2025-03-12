import requests
import pandas as pd
import csv
from auth import auth
headers = auth()[0]
cookies = auth()[1]
filename = "reactions_output.csv"
# writing to csv file
with open(filename, 'a') as csvfile:
    
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Name","Title","Profile_URL","Type_Of_Reaction"])
for start in range(0,10000,10):
    query_id = "voyagerSocialDashReactions.78a64a3508374043e1d8c20396164408"
    post_urnli = "7237685950187786240"
   
    url = f"https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(count:10,start:{start},threadUrn:urn%3Ali%3Aactivity%3A{post_urnli})&queryId={query_id}"
    data = requests.get(url, headers=headers, cookies=cookies).json()
    reaction_data = data['included']
    # Extract relevant information
    profiles = []
    output_data_list = []
    for item in data.get("included", []):
        if item.get("$type") == "com.linkedin.voyager.dash.social.Reaction":
            try:
                name = item.get("reactorLockup", {}).get("title", {}).get("text", "N/A")
                
                title = item.get("reactorLockup", {}).get("subtitle", {}).get("text", "N/A")
                profile_url = item.get("reactorLockup", {}).get("navigationUrl", "N/A")
                reaction_type = item.get("reactionType", "N/A")
        
                output_data_list.append(name)
                output_data_list.append(title)
                
                output_data_list.append(profile_url)
                output_data_list.append(reaction_type)
                
                # existing_csv_df = pd.read_csv(filename)
                # existing_profile_url = existing_csv_df['Profile_URL'].tolist()
               
                # if profile_url not in existing_profile_url:
                df = pd.DataFrame([output_data_list])
                df.to_csv(filename,index=False,header=False,mode="a")
                output_data_list.clear()
                # else:
                #     output_data_list.clear()
            except:
                pass
