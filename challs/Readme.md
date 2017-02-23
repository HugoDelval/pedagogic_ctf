# Add  challenges


## Create directory structure  :

Go to the git cloned repo :

    cd ~/ctf_pedagogique/challs
you can use environment variable to ease directory creation  that must end up with .dir:

    export NEW_CHALL_NAME=php_exec
    mkdir $NEW_CHALL_NAME.dir
Now you must create the json file that will describe your challenge,
"parameters" is used to pass arguments to you script in a ordered way :

```json
{
  "name": "name of your challenge",
  "points": 100,
  "description": " your challenge description ",
  "parameters": [
    {
      "name": "name of the input displayed to the user. As this is the first parameter, this will be passed as first argv to your challenge script",
      "placeholder": "simple example display to the user"
    }
  ],
  "languages": [
    {
      "name": "name the language (example: PYTHON)",
      "extension": "extension of the language (example: .py)"
    }
  ],
  "resolved_conclusion":"your challenge conclusion note."
}
```

add your challenge named after $NEW_CHALL_NAME.pl, this could be any script , don't be fooled by the extention.
Create a check() funtion in  check.py that will return 1 if you challenge is still usable
Create a exploit() function in exploit.py that will return 1 if you challenge is still hackable
then add your new challenge into init.sh :
  
  echo "userdel $NEW_CHALL_NAME" >> init.sh
  echo "(cd /srv/ctf_go/ && ./load_challenges.py $NEW_CHALL_NAME)" >> init.sh
  ./init.sh    
    
