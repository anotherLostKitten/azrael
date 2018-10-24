# azrael -- Sarar Aseer, Jason Tung, Zane Wang and Johnny Wong

# Da Art of Storytellin'

Team azrael (note the lowercase a!) brings to you, the valued user, a website which allows its registered members to contribute to stories anonymously created and contributed to by others.

Non registered members do not fret!! We implemented a REGISTER feature in addition to logining in. All login information is stored in 'users' table of data/azrael_stories.db. 

After logging in, users have the option of viewing (full) stories they have previously contributed to, create a new story and write its very first line, or add to existing stories created to by other users. When adding to a story created by another user, the user only has the ability to view the last line contributed.
All stories are stored in their own table in data/azrael_stories.db where the table name is the name of the story.


### How 2 Launch
1. Clone the repo! You can clone with ssh or https by copying the link, then
```
git clone \<link\>
```
2. Open a virtual environment!
3. Use the virtual environment to run 
```
python main.py
```
4. Interact with our project at http://127.0.0.1:5000/ on any browser!

### Dependencies
- <b>Python 3</b>:
We are using python 3 for this assignment, because pip is built into it!
A major stdlib we use is sqlite3. 
- <b>Wheel</b>:
Once you have python 3, you can run the command: 
```
pip install wheel
```
- <b>Flask</b>:
Once you have python 3 and wheel installed, you just run the command:
```
pip install flask
```
### Problems?
#### If you get an error not listed below, please open an issue!
<b>Address already in use:</b>
The address 127.0.0.1 at port 5000 is already in use! Please close that server.

<b>Flask/Wheel/Python on init run: </b>
Either your virtual environment is not on OR the version of py/flask/wheel is not compliant with what we have listened in our dependencies! Follow the instructions; read twice cut once!

