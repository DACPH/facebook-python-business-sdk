# Copyright 2014 Facebook, Inc.

# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.

# As with any software that integrates with the Facebook platform, your use
# of this software is subject to the Facebook Developer Principles and
# Policies [http://developers.facebook.com/policy/]. This copyright notice
# shall be included in all copies or substantial portions of the software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Creates an ad through a utility function.
"""

from facebookads import FacebookSession
from facebookads import FacebookAdsApi
from facebookads.objects import (
    AdAccount,
    AdPreview,
    AdSet,
)

import ad_creation_utils
import configparser
import os

config = configparser.RawConfigParser()
this_dir = os.path.dirname(__file__)
config_filename = os.path.join(this_dir, 'my_app_session.cfg')

with open(config_filename) as config_file:
    config.readfp(config_file)

### Setup session and api objects
session = FacebookSession(
    config.get('Authentication', 'app_id'),
    config.get('Authentication', 'app_secret'),
    config.get('Authentication', 'access_token'),
)
api = FacebookAdsApi(session)

if __name__ == '__main__':
    FacebookAdsApi.set_default_api(api)

    # Get my account (first account associated with the user associated with the
    #                 session of the default api)
    my_account = AdAccount.get_my_account()

    print('**** Creating ad...')

    # Create my ad
    my_ad = ad_creation_utils.create_website_clicks_ad(
        account=my_account,

        name="Visit Seattle",
        country='US',

        title="Visit Seattle",                             # How it looks
        body="Beautiful Puget Sound.",
        url="http://www.seattle.gov/visiting/",
        image_path=os.path.join(this_dir, 'test.png'),

        bid_type=AdSet.BidType.cpm,
        bid_info={AdSet.Field.BidInfo.impressions: 53},  # $0.53 / thousand
        daily_budget=1000,  # $10.00 per day

        age_min=13,
        age_max=65,

        paused=True,  # Default is False but let's keep this test ad paused
    )
    print('**** Done!')

    # Get the preview and write an html file
    preview = my_ad.get_ad_preview(params={
        AdPreview.Field.ad_format: AdPreview.AdFormat.right_column_standard
    })
    preview_filename = os.path.join(this_dir, 'preview_ad.html')
    preview_file = open(preview_filename, 'w')
    preview_file.write(
        "<html><head><title>Facebook Ad Preview</title><body>%s</body></html>"
        % preview.get_html()
    )
    preview_file.close()
    print('**** %s has been created!' % preview_filename)
