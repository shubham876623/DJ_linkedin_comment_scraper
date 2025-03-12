import requests
import pandas as pd
import csv
from auth import auth
headers = auth()[0]
cookies = auth()[1]
filename = "comment_output.csv"
# writing to csv file
with open(filename, 'a') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["Name","title","Comment","Profile_URL","Likes","Replies"])

for start in range(0,1000000,100):
    query_id = "voyagerSocialDashComments.95ed44bc87596acce7c460c70934d0ff"
    post_urnli = "7237685950187786240"
    url = f"https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(count:100,numReplies:1,socialDetailUrn:urn%3Ali%3Afsd_socialDetail%3A%28urn%3Ali%3Aactivity%3A{post_urnli}%2Curn%3Ali%3Aactivity%3A{post_urnli}%2Curn%3Ali%3AhighlightedReply%3A-%29,sortOrder:RELEVANCE,start:{start})&queryId={query_id}"
    data = requests.get(url, headers=headers, cookies=cookies).json()
   
    # Store parsed results
    parsed_comments = []
    comments_data = data['included']
    # Extract social activity counts
    social_activity_counts = {}
    for item in comments_data:
        if item.get("$type") == "com.linkedin.voyager.dash.feed.SocialActivityCounts":
            entity_urn = item.get("entityUrn")
            social_activity_counts[entity_urn] = {
                "likes": sum(reaction.get("count", 0) for reaction in item.get("reactionTypeCounts", [])),
                "comments": item.get("numComments", 0)
            }
    output_data_list = []
    # Extract comments and related details
    for item in comments_data:
        if item.get("$type") == "com.linkedin.voyager.dash.social.Comment":
            commenter = item.get("commenter", {})
            title = commenter.get("subtitle")
            name = commenter.get("title", {}).get("text", "Unknown")
            profile_url = commenter.get("navigationUrl", "N/A")
            comment_text = item.get("commentary", {}).get("text", "No comment")
            
            # Get related social activity counts
            entity_urn = item.get("urn")
            social_data = social_activity_counts.get(f"urn:li:fsd_socialActivityCounts:{entity_urn}", {"likes": 0, "comments": 0})
            
            parsed_comments.append({
                "Name": name,
                "title":title,
                "Comment": comment_text,
                "Profile_URL": profile_url,
                "Likes": social_data["likes"],
                "Replies": social_data["comments"]
            })
            output_data_list.append(name)
            output_data_list.append(title)
            
            output_data_list.append(comment_text)
            output_data_list.append(profile_url)
            output_data_list.append(social_data["likes"])
            output_data_list.append(social_data["comments"])
            existing_csv_df = pd.read_csv(filename)
            existing_profile_url = existing_csv_df['Profile_URL'].tolist()
           
            if profile_url not in existing_profile_url:
                df = pd.DataFrame([output_data_list])
                df.to_csv(filename,index=False,header=False,mode="a")
                output_data_list.clear()
            else:
                output_data_list.clear()
                
            
            
   