import requests

import pandas as pd

for start in range(0,1000000,100):
    url = f"https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(count:100,numReplies:1,socialDetailUrn:urn%3Ali%3Afsd_socialDetail%3A%28urn%3Ali%3Aactivity%3A7237685950187786240%2Curn%3Ali%3Aactivity%3A7237685950187786240%2Curn%3Ali%3AhighlightedReply%3A-%29,sortOrder:RELEVANCE,start:{start})&queryId=voyagerSocialDashComments.95ed44bc87596acce7c460c70934d0ff"
    
    headers = {
        "accept": "application/vnd.linkedin.normalized+json+2.1",
        "accept-language": "en-US,en;q=0.9",
        "csrf-token": "ajax:4170353178585126843",
        "priority": "u=1, i",
        "referer": "https://www.linkedin.com/feed/update/urn:li:activity:7237685950187786240/",
        "sec-ch-prefers-color-scheme": "light",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "x-li-lang": "en_US",
        "x-li-page-instance": "urn:li:page:d_flagship3_detail_base;V+BWJ03GQvew98o/YgWYjg==",
        "x-li-pem-metadata": "Voyager - Feed - Comments=load-comments",
        "x-li-track": '{"clientVersion":"1.13.31976","mpVersion":"1.13.31976","osName":"web","timezoneOffset":5.5,"timezone":"Asia/Calcutta","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1.25,"displayWidth":1920,"displayHeight":1080}',
        "x-restli-protocol-version": "2.0.0"
    }
    
    cookies = {
        "bcookie": "v=2&8f69d89c-5c40-417b-837e-8f7fc6a79937",
        "li_sugr": "b6f156bb-6515-499a-9e89-0ee8763c116b",
        "bscookie": "v=1&20241229052853f13cf300-bdbc-4cf3-885b-213550030ddcAQG5Uoy3xCzc1M5vJrQKUDEBT1Ad80jK",
        "g_state": '{"i_l":0}',
        "liap": "true",
        "JSESSIONID": "ajax:4170353178585126843",
        "li_theme": "light",
        "li_theme_set": "app",
        "_guid": "16f1e496-7317-48fc-9210-8cdb9573bbe3",
        "dfpfpt": "36715cb96d7144bb9240658e8dc0f9a1",
        "timezone": "Asia/Calcutta",
        "AnalyticsSyncHistory": "AQIiFjDs9JwjPAAAAZVqKbBKc5snu6WL8bHSEN7ymo_OwfhZqARihhNntRA3DNZwhv-ZmLym7E1rV8oH9c7t7w",
        "lms_ads": "AQHemd_VmyWh2wAAAZVqKbMdC-ExVo4m9SC9nTwb8Wzk6mmZG-pruCvFcEbOmAM2pB1YVFZgfvY3GynBdUh_TS91-oqADK5R",
        "lms_analytics": "AQHemd_VmyWh2wAAAZVqKbMdC-ExVo4m9SC9nTwb8Wzk6mmZG-pruCvFcEbOmAM2pB1YVFZgfvY3GynBdUh_TS91-oqADK5R",
        "lang": "v=2&lang=en-us",
        "li_at": "AQEDAS7MJPwAe5IxAAABlBDl-5gAAAGVl6klGE0AZ7e_V59cefJF1nN4tAjpwOQkKNhWdjkupudszbCVj_Pn-8mrxMV9Yq5pCAt137kpbgasegwBXGQbzz3kXuzFxDHfibG8ixInkPdR7H5MvSXtLmnJ",
        "lidc": "b=OB48:s=O:r=O:a=O:p=O:g=5060:u=1235:x=1:i=1741404235:t=1741407875:v=2:sig=AQFgDeYtOjP2iUT1F-Bd_KNgpjJzaCtu"
    }
    
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
            name = commenter.get("title", {}).get("text", "Unknown")
            profile_url = commenter.get("navigationUrl", "N/A")
            comment_text = item.get("commentary", {}).get("text", "No comment")
            
            # Get related social activity counts
            entity_urn = item.get("urn")
            social_data = social_activity_counts.get(f"urn:li:fsd_socialActivityCounts:{entity_urn}", {"likes": 0, "comments": 0})
            
            parsed_comments.append({
                "Name": name,
                "Comment": comment_text,
                "Profile_URL": profile_url,
                "Likes": social_data["likes"],
                "Replies": social_data["comments"]
            })
            output_data_list.append(name)
            output_data_list.append(comment_text)
            output_data_list.append(profile_url)
            output_data_list.append(social_data["likes"])
            output_data_list.append(social_data["comments"])
            existing_csv_df = pd.read_csv("sampledata.csv")
            existing_profile_url = existing_csv_df['Profile_URL'].tolist()
            if profile_url not in existing_profile_url:
                print(output_data_list)
                df = pd.DataFrame([output_data_list])
                df.to_csv("sampledata.csv",index=False,header=False,mode="a")
                output_data_list.clear()
            else:
                output_data_list.clear()
                
            
            
   