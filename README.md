# How to install (on CNCZ Apache with uWSGI)

## Deploying
0. Clone this repo in `/www/pucadmin/live/repo` (on the science filesystem)
1. `poetry install` to create the venv.
2. Create `/www/pucadmin/live/repo/website/PUCadmin/settings/production.py` and `/www/pucadmin/live/repo/website/PUCadmin/settings/management.py` based on the `.example` files (set secret key and passwords).
3. Run the `deploy.sh` script. This script can be run to update, too.

Important notices:
- The science filesystem (accessed via lilo) is mounted in a different way then on lilo. Make sure to use relative paths.
- The database credentials for differ for lilo or the webserver. Therefore, management commands from lilo must be run with `PUCadmin.settings.management` (which is done automatically by `manage.py`).
- To run management commands on production, first activate the python env with `poetry shell`.
- Note that the webserver does not have write permissions, except for the `writable/` folder. `manage.py collectstatic` must therefore be run explicitly and the media folder is located in there.
- Via `/admin-login`, it is possible to bypass SAML login (for example for first installation when SAML has not yet been set up).


## SAML configuration
To login, we use SAML. This needs to be configured. The SAML metadata for the CNCZ SAML IdP right now:

```xml
<?xml version="1.0"?>
<md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" entityID="signon.science.ru.nl/saml-ru">
    <md:IDPSSODescriptor protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
        <md:KeyDescriptor use="signing">
            <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
                <ds:X509Data>
                    <ds:X509Certificate>MIIETzCCAzegAwIBAgIJAKwffKBlFTjcMA0GCSqGSIb3DQEBBQUAMIG9MQswCQYDVQQGEwJOTDETMBEGA1UECAwKR2VsZGVybGFuZDERMA8GA1UEBwwITmlqbWVnZW4xLzAtBgNVBAoMJlJhZGJvdWQgVW5pdmVyc2l0eSwgRmFjdWx0eSBvZiBTY2llbmNlMQ0wCwYDVQQLDARDTkNaMR0wGwYDVQQDDBRzaWdub24uc2NpZW5jZS5ydS5ubDEnMCUGCSqGSIb3DQEJARYYcG9zdG1hc3RlckBzY2llbmNlLnJ1Lm5sMB4XDTEzMTAxNzE4MzYxMVoXDTMzMTAxMjE4MzYxMVowgb0xCzAJBgNVBAYTAk5MMRMwEQYDVQQIDApHZWxkZXJsYW5kMREwDwYDVQQHDAhOaWptZWdlbjEvMC0GA1UECgwmUmFkYm91ZCBVbml2ZXJzaXR5LCBGYWN1bHR5IG9mIFNjaWVuY2UxDTALBgNVBAsMBENOQ1oxHTAbBgNVBAMMFHNpZ25vbi5zY2llbmNlLnJ1Lm5sMScwJQYJKoZIhvcNAQkBFhhwb3N0bWFzdGVyQHNjaWVuY2UucnUubmwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDPOH0c2f3n4XluMoPfje/MiaoXhCri+amfOtnafdmYGbyGuwF72F0uq6MvNX3OdtBbDGmnFpfQYspfS7jNjFUvkLsnIMGPY4p+5lDD675cKn9CnwfsA1cppZl2Zc09Zf3BLKelKNzYWtAvY7sNX9e4NntlcObgW1yqZCg9JC8X8CY1xKMwkbGEl4Ltxc636+mOiZsKduD7kcL9Hf1akT4wX3WGhXsQbifbVrBIoBCV4Rom8n4YDrxdqi7+bRx1wNhi6Y0tALYqxdAJ/J3wLm6tzFcNketIKUTN4r0gq+mAQSo0Lcwt/GpdlFqD6EoEFSlcqAqxfeWK4PWLeDyOQD4FAgMBAAGjUDBOMB0GA1UdDgQWBBT/3wfM9BDMslqpaNXoJlmv4vn9rTAfBgNVHSMEGDAWgBT/3wfM9BDMslqpaNXoJlmv4vn9rTAMBgNVHRMEBTADAQH/MA0GCSqGSIb3DQEBBQUAA4IBAQBlcARvzuYwIKmnF4fXbl7yAmAfbELoFzbrdZYL+ZWePjPAgw/gDrjpWC8JcVdprt3BPHLj1tu+oWexOVGxVUGxAZyRm/7IvADz5N7BCSwG4zeqDcjkVOdKhlEjJVXquENpU1VnrwqFahh1Hdtryyjp27nNQtkgUKxbV47nO+cWYIVruia9SFwkOczWr+c8IE4lYjgycD6nKRQJzCeUpVfa/ROtHZJ4XxQUMPNE2OmT3gGygbu2QKOm8jiC1w9TDOlAZcDx8zF3hwFYh/gWd/x4CC0VZEEwCb1meWezr5X6jXvVjVduH32yfkld2ZvpFzjD5DPicZTRT/jLCXi++0+s</ds:X509Certificate>
                </ds:X509Data>
            </ds:KeyInfo>
        </md:KeyDescriptor>
        <md:SingleLogoutService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://pr.signon.science.ru.nl/saml-ru-kv94235b-puc/saml2/idp/SingleLogoutService.php"/>
        <md:NameIDFormat>urn:oasis:names:tc:SAML:2.0:nameid-format:transient</md:NameIDFormat>
        <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://pr.signon.science.ru.nl/saml-ru-kv94235b-puc/saml2/idp/SSOService.php"/>
    </md:IDPSSODescriptor>
</md:EntityDescriptor>
```

For our `url_params` we use: `{"idp_slug": "science_puc"}`, base url `https://puc-admin.science.ru.nl` and entity id `puc-admin.science.ru.nl` (!).

The attributes returned are: `uid`, which is the `NameID` and should be mapped to the `username` field. Other attributes are currently not present. 
Moreover, we use the following settings:

- User default values: `is_staff` is `True` so every user can actually see the (empty) admin page.
- `NameID is case sensitive` is `False`
- `Create users that do not already exist` is `True`
- `Associate existing users with this IdP by username` is `True` (this is a vulnerability for username spoofing but with only 1 IdP this is no problem)
- `Respect IdP session expiration` is `True` (!)
- `Logout triggers SLO` is `True` as well


# Data minimisation
Data can be minimised by running `manage.py minimisedata`. This will use the following policy:

##### Users
Users that have not logged in for 2 years, or are not connected to an organisation will be removed.

##### Competitions
Personal information from students and supervisors for competition submissions, is minimised 31 days after the competition has ended. Address, email and phone number are deleted. Name, school and the submitted document, together with the reports are kept indefinitely.

##### Questions
All personal information from students that submitted a question is deleted after 1 year  if the question has been marked completed. The content of the question itself and the school are stored indefinitely, but name and email are deleted. 

