# AQOJ
 An abbreviation for Aqours Online Judge. An online judge system made with Django framework whose judge system is based on judger for ACDream.

## HOW TO DEPLOY?
1. Run the shell script `deploy.sh` in your bash shell to copy files to the server.
2. Connect to the server via SSH and cd to the directory of folder "JUDGE".
3. Uncomment the last line inside `JUDGE/urls.py`.
4. Run `python3 manage.py collectstatic` and restart Apache server using `apachectl restart`.
5. If changes are made to the judgement program, kill the process and rerun `nohup sh run.sh 2>/dev/null`.
6. Done!