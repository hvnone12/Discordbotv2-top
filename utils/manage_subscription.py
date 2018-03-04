import json
from datetime import datetime, timedelta
import config
#variation_id: 
# 3928 14 days
# 3929 1 month
# 3930 3 months
# 3931 6 months
# 3932 1 year
# product_id: 3914


class Subscriptions():
    def __init__(self, response):
        self.response=response
        self.subscriptions=[]
        self.products=[3928, 3929, 3930, 3931, 3932]
        self.product_names=['14 days', '1 month', '3 months', '6 months', '1 year']
        self.role_names=config.role_ids

    def sort_entries(self):
        for subs in self.response:
            subscription={}

            subscription['discord_id']=subs['billing']['last_name']
            subscription['status']=subs['status']
            subscription['variation_id']=subs['line_items'][0]['variation_id']
            index = [i for i,x in enumerate(self.products) if x == subscription['variation_id']]
            subscription['variation_type']=self.product_names[index[0]]
            subscription['role_id']=self.role_names[index[0]]

            end_date = subs['end_date']
            end_date=datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
            today_date=datetime.utcnow()
            days_left=end_date-today_date
            subscription['days_before_expire']=days_left.days

            # Checking earlier subscriptions appended
            append=True
            for i, sub in enumerate(self.subscriptions):

                # If another subscription shares the same discord id
                if sub['discord_id']==subs['billing']['last_name']:
                    
                    # if the latest subscription has been expired or cancelled it does nothing
                    if sub['status']=='active' and (subs['status']=='expired' or subs['status']=='cancelled'):
                        append=False
                    # if the earlier subscription is expired or cancelled the newer subscription overrides it
                    elif (sub['status']=='expired' or sub['status']=='cancelled') and subs['status']=='active':
                        self.subscriptions.pop(i)

                    # If both of the subscriptions are active
                    elif sub['status']=="active" and subs['status']=="active":
                        sub_index = [i for i,x in enumerate(self.products) if x == sub['variation_id']]
                        subs_index = [i for i,x in enumerate(self.products) if x == subs['line_items'][0]['variation_id']]

                        # Check which of the subscriptions type is the highest and removes the lowest one
                        if sub_index>subs_index:
                            append=False
                        elif subs_index>sub_index:
                            self.subscriptions.pop(i)

                        # If it's the same subscription type it checks how many days there are left before the subscription expires and removes the lowest one
                        else:
                            if sub['days_before_expire']>subscription['days_before_expire']:
                                append=False
                            else:
                                self.subscriptions.pop(i)

            #Send in new subscription
            if append:
                self.subscriptions.append(subscription)
        return self.subscriptions
