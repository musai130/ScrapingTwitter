import requests
import re

headers = {
    'authority': 'api.twitter.com',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'content-type': 'application/json',
    'origin': 'https://twitter.com',
    'referer': 'https://twitter.com/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'x-client-transaction-id': 'ozr1/19RNKGAUwBgUZ3H0R1GGNM4Orpl0jiNk23TVVG5gkM0CIMvD7GraRl0YpB4J4PjCaKHATKnEwD6DuOZS3aCVuTmog',
    'x-guest-token': '1770084064198000754',
    'x-twitter-active-user': 'yes',
    'x-twitter-client-language': 'ru',
}

headersTwitter = {
    'authority': 'twitter.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'referer': 'https://twitter.com/elonmusk',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}


params = {
    'variables': '{"userId":"44196397","count":20,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true}',
    'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}',
}

with open("proxy.txt") as file:
    ProxyList = file.readlines()
ProxyList = list(ProxyList[i].replace("\n", "") for i in range(len(ProxyList)))
for proxy in ProxyList:
    proxies = {
    'http' : f'http://{proxy}',
    'https' : f'http://{proxy}'
    }
    link = 'https://twitter.com'
    try:
        resp = requests.get(link, proxies=proxies, timeout=2, headers=headersTwitter)
        text = resp.text
        guest_token= "".join(re.findall(r'(?<=\"gt\=)[^;]+', text))
        headers['x-guest-token'] = guest_token
        response = requests.get('https://api.twitter.com/graphql/eS7LO5Jy3xgmd3dbL044EA/UserTweets',params=params,proxies=proxies,headers=headers, timeout=2)
        print('Proxy valid')
        json_response = response.json()
        result = json_response.get("data", {}).get("user", {}).get("result", {})
        timeline = result.get("timeline_v2", {}).get("timeline", {}).get("instructions", {})
        entries = [x.get("entries") for x in timeline if x.get("type") == "TimelineAddEntries"]
        entries = entries[0] if entries else []
        count = 0
        for entry in entries:
            content = entry.get("content")
            entry_type = content.get("entryType")
            tweet_id = entry.get("sortIndex")
            if entry_type == "TimelineTimelineItem":
                item_result = content.get("itemContent", {}).get("tweet_results", {}).get("result", {})
                legacy = item_result.get("legacy")
                tweet_data =  legacy.get("full_text")
                
                if  'https://' in re.findall(r"https://", tweet_data):
                    pass
                else:
                    print(f"{count+1}. {tweet_data}")
                    count+=1
                    print('------')
                if count == 10: break
        break
    except Exception as e:
        print(e)
        print("Proxy not valid")
        print('------')



