# Working with MS Appcenter API using Python.
 
The Dockerfile in this repo builds image with `build.py` script inside using which one can run 
process of starting builds for last commits in all branches in some MS Appcenter application.
Custom Python module for Appcenter is placed into `appcenter` directory (I used this project as base: https://github.com/microsoft/appcenter-rest-python. 
But note that it implements only connection to the Appcenter API and some not very usefull classes. It lacks
any methods for working with branches and builds and I had to implement such classes and methods on my own - you can find them in `appcenter/branches.py`).

### To build image:

docker build -t <image name> <repo root directory>

### To initiate builds:

```
docker run -e APPCENTER_TOKEN=$APPCENTER_TOKEN \
           -e APPCENTER_OWNER=<owner name> \
           -e APPCENTER_APP=<app name> --rm -it <image name>
```

Container will automatically start build.py script which:
1. Receives names of all branches
2. Sets build configuration for each (if not set before)
3. Starts build for last commit in each branch.
4. Waits in loop while all builds finish.
5. Prints out to the standard output simple table with fields: branch name, build status, duration of build process, link to ZIP with build logs.

# Environment variables:
To run build.py you have to set:

| Variable | Value |
| ------ | ------ |
| APPCENTER_OWNER | name of the Appcenter user |
| APPCENTER_APP | Appcenter application name |
| APPCENTER_TOKEN | user's security token to communicate with API |
