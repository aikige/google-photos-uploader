# An example to upload image to google photos, for limited-input devices

This is minimal example of python script to upload an image to Google Photos.

There is several similar projects,
but this program can be run on embedded device which has limited-input methods, like headless Raspberry Pi.

This example is using OAuth scenario for [Limited-input devices](https://developers.google.com/identity/protocols/oauth2#device).

## Preparation - Create Project and Get Client Secret

Please follow instruction of [Create credentials](https://developers.google.com/workspace/guides/create-credentials) and retrieve JSON file for Client Secrets.

Here, important point is:

1. When you create new Client ID in [credentials](https://console.cloud.google.com/apis/credentials) setting, please select "TV and Limited input device" as "Application type".
1. Please download created Client ID information and store the downloaded JSON file into working folder. This script uses it as input for *Client Secret*.

## 1st Run -- Authentication

When you run first time, please follow this steps:

1. The script will show URL for authentication to standard output.
1. Please open your favorite browser to open URL and perform authentication.
    Here, browser will show security warnings, but please ignore these warnings.
1. At last step of authentication, the authorization code will be shown on your browser.
1. Please copy the code and enter it to standard input of this script, to complete authentication.

## Important Notice

Please refer [API limits and quotas](https://developers.google.com/photos/library/guides/api-limits-quotas) published by Google, and understand number of API calls available for a project.

## References

* ido-ran/[google-photos-api-python-quickstart](https://github.com/ido-ran/google-photos-api-python-quickstart) -- good reference for authentication process.
* Google Developers > Products > Google Photos APIs > Guides > [Library API overview](https://developers.google.com/photos/library/guides/overview)
* google-api-python-client > [OAuth 2.0](https://googleapis.github.io/google-api-python-client/docs/oauth.html)

