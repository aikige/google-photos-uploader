# An sample python script for uploading image to Google Photos, for limited-input devices

This is minimal example of python script to upload an image to Google Photos.

There is several similar projects,
but this program can be run on embedded device which has limited-input methods, like headless Raspberry Pi.

This example is using OAuth scenario for [Limited-input devices](https://developers.google.com/identity/protocols/oauth2#device).

## Preparation

### Create Project and Get Client Secret

Please follow google's instruction ([Create credentials](https://developers.google.com/workspace/guides/create-credentials)) and retrieve JSON file for the *Client Secrets*.

Here, please keep following in mind when you create the *Client Secret*:

1. When you create new Client ID in [credentials](https://console.cloud.google.com/apis/credentials) setting, please select "TV and Limited input device" as "Application type".
1. Please download created Client ID information and store the downloaded JSON file into working folder. This script uses it as input for *Client Secret*.
    Default name for *Client Secret* is `client_secret.json`.

### Install dependent library

Please install required libraries:

```
pip install -r requirements.txt
```

Note that, this script is tested with Python v3.x.

### 1st Run -- Authentication and Authorization

When you run first time (recommended to run `python google_photos_uploader -l`), please follow this steps:

1. The script will show URL for authentication in standard output.
1. Please open the URL with your favorite browser and perform authentication and authorization.
    Here, browser will show security warnings, but please ignore these warnings.
1. At last step of authorization, an *Authorization Code* will be shown on your browser.
1. Please copy the code and enter it to the standard input of this script, to complete authorization.
1. The script stores authorization information (*Credential*) to file,
    by default name of the *Credential* store is `credentials.pickle`.
    This script uses stored *Credential* for succeeding calls.

## Usage

To upload an image (`YOUR_IMAGE`), please simply execute following:

```
python google_photos_uploader.py YOUR_IMAGE
```

If you want to add the image to specific album, please specify album ID like:

```
python google_photos_uploader.py YOUR_IMAGE -a ALBUM_ID
```

The script can list up available album as follows, and these album list includes information about `ALBUM_ID`.

```
python google_photos_uploader.py -l
```

If you want to create album, please execute following.

```
python google_photos_uploader.py -n "Album Title"
```

## Important Notice

Please refer [API limits and quotas](https://developers.google.com/photos/library/guides/api-limits-quotas) published by Google, and understand number of API calls available for a project.

## References

* ido-ran/[google-photos-api-python-quickstart](https://github.com/ido-ran/google-photos-api-python-quickstart) -- good reference for authentication process.
* Google Developers > Products > Google Photos APIs > Guides > [Library API overview](https://developers.google.com/photos/library/guides/overview)
* google-api-python-client > [OAuth 2.0](https://googleapis.github.io/google-api-python-client/docs/oauth.html)

