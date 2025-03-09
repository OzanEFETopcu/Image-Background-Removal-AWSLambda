# Image Background Remover Function
**This is a lambda function written in python, specifically using rembg and pillow libraries, that takes a base64 encoded image and removes its background and returns it the same format**

## Update Version 2.0:
After a long and trial process of trying to implement rembg wihtout scraping the library into bare skeleton and reaching to no measurable decrease on the cold start duration of the lambda function I found out that the only thing that was keeping the initial 
response time at 100+ seconds was the import of rembg library, so I decided to lower the version of Python to 3.9 and installed the rembg-aws-lambda package that is the fork of the original rembg file (more information about this project further in the README).

## Technical Specifications:
- Deployed using AWS Cloudformation IaC
- The project gets hosted on ECR as a Docker container (Due to size constraints of the rembg libraries other methods of function deployment is not possible)


## Why A Project Like This?
The need for such a project comes from trying to use AWS Lambda functions and a somewhat bloated library called "rembg". This library uses the Pillow (Python Imaging Library) in order to seperate background and the object of an image, however; if you want to use any library other than core python libraries you need to provide them to lambda in the project.

In that situation you have 2 options: either zip each external library you want to use and host it on S3, or create a Docker image of your whole project including the libraries being used and host it on ECR for it to be polled by AWS Lambda on invocation and later on. Well, it turns out that "rembg" library is so huge that only way to store such a library is by the second method.

Of course there is also another option, getting rid of all the unnecessary files that take up space which was done in the past by a dev called Ritvik Nag ([the repository](https://github.com/rnag/rembg-aws-lambda)). Unfortunately last update to it was on 2023 (2 years ago as of me writing this) and it wasn't compatible with the version of Python I was using; and I wasn't going to get my hands dirty and go through the same process for a project of this scale so instead I decided that using Docker would be the easiest option.

## How To Deploy?
### Requirements:
- Docker CLI
- AWS CLI
- AWS CDK
### Steps:
1. Make sure that the right AWS account is configured onto your AWS CLI
2. For first time CloudFront deployments in an account and region initially call `cdk bootstrap --region <region_of_your_choice>` 
3. Using `cdk deploy` deploy this project into the AWS ECR
4. The function will return a link that will be used for sending requests
   
*It is important that the Dockerfile has*

`ENV NUMBA_CACHE_DIR="/tmp/"`

`ENV U2NET_HOME="/tmp"` 

*lines in them as internal libraries in "rembg" tries to cache and load ML libraries into a directory however AWS Lambda places the project folder into a read-only directory and only writable directory is /tmp*

## Possible Future Updates:
- [x] Fix the "rembg" download issue on read-only directory of Lambda
- [ ] Use AWS API Gateway and implement security practices to prevent the abuse of requests
- [x] Optimize the cold-start time of the function as the initial request can take upto 100 seconds with downloading of the libraries