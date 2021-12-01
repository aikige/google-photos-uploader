# Implementation Note

## Permission

Since this script is focusing on uploading image, access for read permission is limited to `https://www.googleapis.com/auth/photoslibrary.readonly.appcreateddata`.
This option is selected since Google Photos dose not currently allow user to append new image to the album which is not created by under authentication of the application.

As result, this script claims following permissions:

* `https://www.googleapis.com/auth/photoslibrary.appendonly` -- used to add image, create new album.
* `https://www.googleapis.com/auth/photoslibrary.readonly.appcreateddata` -- used to retrieve list of album.

## How to specify album

To specify album to add an image, this script requests *albumId*.

But, this script is not implementing feature to search album by title, for simplicity.

If you want to identify the *albumId*, please use feature to list albums.
