# musicSubApp
A web application - Music Subscription App.
This app allows user to register with it and setup a profile.
Then the user can browse through different artist and their music to subscribe them and add them to their profile.
The three parameters for search are Artist name, Year of album, and Tittle of album.

The app is developed using HTML for front end and Flask for backend. 
It was deployed on AWS using its diffrent services.
DynamoDB was used for USER information database as well as music table containing Artist names, titles of tracks, and the years in which they were released.
S3 buckets for uploading the Json file containg the data for Album covers as images.
App uses querry for searching through the music lists.
It was deployed using EC2 instance of AWS.
