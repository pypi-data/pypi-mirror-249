# yt_pld - YouTubeUpload
### This app helps you automate uploading videos to your YouTube channel. Selenium is used for uploading.

# Installation
### To install, run the following command in your terminal:

    pip install yt-pld

# Example of use

    from yt_pld import upload_multiple_videos


    video_list = [
        {
            "video_path": 'your_video_path',
            "title_text": 'your_title_for_video',
            "description_text": 'your_description_for_video'
        },
        # Add more video entries as needed
    ]

    login_data = {
        "chrome_driver_path": 'your_chrome_driver_path',
        "email": 'your_email',
        "password": 'your_password',
        "channel_name": 'your_channel_name'
    }

    upload_multiple_videos(login_data, video_list)

## Description of parameters to be transferred
`video_list` - pass to this list as many dictionaries with video data as many videos you need to upload (currently you can upload a maximum of 10 videos per day)\
`video_path` - your path to the video you want to upload to your channel\
`title_text` - title for the video\
`description_text` - description for the video\

`login_data` - pass to this dictionary the login data for your YouTube creative studio\
`chrome_driver_path` - path to your chrome driver\
`email` - your email to log in to your google account, to which your YouTube channel is linked to\
`password` - password for the google account to which your YouTube channel is linked\
`channel_name` - name of the channel you want to upload video to\