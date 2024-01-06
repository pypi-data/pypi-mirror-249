$def with (micropub_endpoint, access_token, file_root)
#!/bin/bash

micropub_endpoint=https://ragt.ag/posts
access_token=secret-token:H/_MnZxm795q9.9bNLI//zqK3ex1wl94_+SKTNCwFqP_~/_i9wUmDJSYM_OE+PCwSMxP..mCJj7YV+iE~CtcH.cfsitG_RkibB3IDDUz.74oPEuKU_lPy60NF+pdsE.N
file_root="/root/ragt.ag"
url=`cat $file_root/last-url.txt`

input_file=$1
video_filename=$2
output=$file_root/archive/$2;

curl -X POST -i $micropub_endpoint -H "Authorization: Bearer $access_token" \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"update\",\"url\":\"$url\",\"replace\":{\"content\":\"<p>The live stream has ended. The archived version will be available here shortly.</p>\"}}"

ffmpeg -y -i $input_file -acodec libmp3lame -ar 44100 -ac 1 -vcodec libx264 $output;
video_url="/live/archive/$video_filename"

ffmpeg -i $output -vf "thumbnail,scale=1920:1080" -frames:v 1 $output.jpg
photo_url="/archive/$video_filename.jpg"

curl -X POST -i $micropub_endpoint -H "Authorization: Bearer $access_token" \
  -H "Content-Type: application/json" \
  -d "{\"action\":\"update\",\"url\":\"$url\",\"replace\":{\"content\":\"<p>The live stream has ended.</p>\"},\"add\":{\"video\":\"$video_url\",\"photo\":\"$photo_url\"}}"
