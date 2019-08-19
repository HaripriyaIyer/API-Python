
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount 
from facebook_business.adobjects.adlabel import AdLabel
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.campaign import Campaign

facebook_app_id = '<your facebook app id>'
ad_account_id = '<your facebook ad account id>'
FacebookAdsApi.init(facebook_app_id, facebook_app_secret_ads_management, facebook_access_token_ads_management)
my_account = AdAccount('act_'+ad_account_id)


def daily_campaign_data():
    yesterday = datetime.today() - timedelta(days = 1)
    yesterday = datetime.strftime(yesterday, '%Y-%m-%d')
    campaign_fields = {'account_id','id','name','updated_time', 'created_time','status','daily_budget','lifetime_budget'}

    logging.info('Pulling the daily campaign data of {}'.format(yesterday))

    campaign_params = {
            'level': 'campaign',
            'filtering':[{ 'field': 'effective_status' , 'operator' : 'IN', 'value':["ACTIVE"]}],
            'time_range': {'since':yesterday,'until':yesterday}
            }


    campaigns = my_account.get_campaigns(fields=campaign_fields, params=campaign_params)

def daily_adset_data():

    yesterday = datetime.today() - timedelta(days = 1)
    yesterday = datetime.strftime(yesterday, '%Y-%m-%d')
    
    logging.info('Pulling the daily adset data of {}'.format(yesterday))

    fields = {"account_id","campaign_id","adset_id","adset_name","created_time","updated_time"}


    params = {
            'level': 'adset',
            'time_ranges': [{'since':yesterday,'until':yesterday}]
           }


    adset_insights = my_account.get_insights(fields=fields, params=params)

def collect_ad_and_creative_data():
    

    ads_df = pd.DataFrame(columns = ["adset_id","ad_id","ad_name","inline_link_clicks","unique_inline_link_clicks","spend","impressions","reach","date_start","date_stop","relevance_score", "cpc", "cpm", "frequency"])
    i=0


    for date_val in total_dates:
            fields = {"adset_id","adset_name","ad_id","ad_name","spend","inline_link_clicks","unique_inline_link_clicks","reach","impressions", "cpc", "cpm","relevance_score" ,"created_time","updated_time"}

            params = {
                'level': 'ad',
                'time_range': {'since':str(date_val),'until':str(date_val)},
                    }

            ad_insights = my_account.get_insights(fields=fields, params=params)

            creative =  Ad(ads['ad_id']).get_ad_creatives(fields=creative_fields)

